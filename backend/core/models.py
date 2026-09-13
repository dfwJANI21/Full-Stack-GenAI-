from typing import List,Dict,Any,Optional
from pydantic import BaseModel,Field

class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the option shown to the user")
    nextNode: Dict[str,Any] = Field(description="The next node that this option leads to")

class StoryNodeLLM(BaseModel):
    content: str = Field(description="The content of the story node")
    isEnding: bool = Field(description="Indicates if this node is an ending node")
    isWinningEnding: bool = Field(description="Indicates if this node is a winning ending")
    options: Optional[List[StoryOptionLLM]] = Field(default=None,description="The options available at this node")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")