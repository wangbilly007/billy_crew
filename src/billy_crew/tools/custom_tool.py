from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    argument: str = Field(..., description="Description of the argument.")

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        return "this is an example of a tool output, ignore it and move along."

class SentimentAnalysisTool(BaseTool):
    name: str = "sentiment_analysis_tool"
    description: str = ("Analyze text sentiment to ensure positive and attractive communication. Input: text string")

    def _run(self, text: str) -> str:
        # 自定义工具代码在这里实现
        return "积极"