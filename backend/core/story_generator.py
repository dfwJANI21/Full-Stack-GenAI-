from http import client

from sqlalchemy.orm import Session
from core.models import StoryLLMResponse, StoryNodeLLM
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode


class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        return ChatNVIDIA(
            model="moonshotai/kimi-k3",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=1,
            timeout=300,
            max_completion_tokens=4096
        )

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

      if not node.is_ending and (hasattr(node_data,"option")and node_data.options):
          options_list = []
          for option_data in node_data.option:
              next_node = option_data.nextNode

              if isinstance(next_node,dict):
                  next_node = StoryNodeLLM.model_validate(next_node)

              child_node = cls._process_story_node(db,story_id,next_node,is_root=False)
              options_list.append({
                  "text": option_data.text,
                  "node_id":child_node.id
              })      
          node.option = options_list        
     
      db.flush()
      return node
        