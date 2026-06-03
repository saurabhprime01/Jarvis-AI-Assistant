from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the tool does."""
        pass

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """Execute the tool's logic."""
        pass

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self.tools[tool.name] = tool
        return tool

    def get_tool(self, name: str) -> BaseTool:
        return self.tools.get(name)

    def list_tools(self) -> list:
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]

registry = ToolRegistry()
