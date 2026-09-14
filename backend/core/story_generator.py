import os
from sqlalchemy.orm import Session
from core.models import StoryLLMResponse, StoryNodeLLM
from core.config import settings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode


class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        api_key = (os.getenv("OPENAI_API_KEY") or getattr(settings, "OPENAI_API_KEY", "")).strip()
        base_url = (os.getenv("LLM_BASE_URL") or getattr(settings, "LLM_BASE_URL", "")).strip()
        model = (os.getenv("LLM_MODEL") or getattr(settings, "LLM_MODEL", "")).strip()

        if not base_url:
            if api_key.startswith("gsk_"):
                base_url = "https://api.groq.com/openai/v1"
                if not model:
                    model = "openai/gpt-oss-120b"
            elif api_key.startswith("sk-or-"):
                base_url = "https://openrouter.ai/api/v1"
                if not model:
                    model = "meta-llama/llama-3.3-70b-instruct"
            elif api_key.startswith("nvapi-"):
                base_url = "https://integrate.api.nvidia.com/v1"
                if not model:
                    model = "meta/llama-3.1-8b-instruct"

        if not model:
            model = "openai/gpt-oss-120b" if "groq" in base_url else "gpt-4o-mini"

        kwargs = {
            "model": model,
            "api_key": api_key,
            "temperature": 0.7,
            "timeout": 120,
        }
        if base_url:
            kwargs["base_url"] = base_url

        return ChatOpenAI(**kwargs)

    @classmethod
    def generate_story(cls, db: Session, theme: str, session_id: str = "Fantasy") -> Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)
        
        # Format the system and human content strings cleanly
        system_content = STORY_PROMPT
        human_content = f"Create story with this Theme: {theme}\n\n{story_parser.get_format_instructions()}"
        
        # Invoke the model with pure dictionary values OpenRouter understands
        raw_response = llm.invoke([
            {"role": "system", "content": system_content},
            {"role": "user", "content": human_content}
        ])
        
        # Safely read content from the LangChain response object
        response_text = raw_response.content
        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title,session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data,dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db,story_db.id,root_node_data,is_root=True)

        db.commit()
        return story_db
    @classmethod
    def _process_story_node(cls,db: Session,story_id:int,node_data: StoryNodeLLM,is_root: bool = False) -> StoryNode:
      node = StoryNode(
        story_id=story_id,
        content=node_data.content if hasattr(node_data,"content") else node_data["content"],
        is_root=is_root,
        is_ending = node_data.isEnding if hasattr(node_data,"isEnding") else node_data["isEnding"],
        is_winning_ending = node_data.isWinningEnding if hasattr(node_data,"isWinningEnding") else node_data["isWinningEnding"],
        options=[]
      )
      db.add(node)
      db.flush()

      options = getattr(node_data, "options", None)
      if isinstance(node_data, dict):
          options = node_data.get("options")

      if not node.is_ending and options:
          options_list = []
          for option_data in options:
              next_node = getattr(option_data, "nextNode", None) or (option_data.get("nextNode") if isinstance(option_data, dict) else None)
              text = getattr(option_data, "text", "") or (option_data.get("text", "") if isinstance(option_data, dict) else "")

              if isinstance(next_node, dict):
                  next_node = StoryNodeLLM.model_validate(next_node)

              child_node = cls._process_story_node(db, story_id, next_node, is_root=False)
              options_list.append({
                  "text": text,
                  "node_id": child_node.id
              })      
          node.options = options_list        
     
      db.flush()
      return node
        