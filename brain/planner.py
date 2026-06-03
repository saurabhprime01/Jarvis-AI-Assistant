from brain.agent import jarvis_brain
from tools.base import registry
from loguru import logger
import json

class Planner:
    def __init__(self):
        self.system_prompt = """
        You are the Planning module of JARVIS. Your job is to break down a user request into a sequence of tool calls.
        
        AVAILABLE TOOLS:
        {tools_list}
        
        RESPONSE FORMAT:
        Return a JSON list of steps. Each step should be:
        {{"tool": "tool_name", "input": {{"param1": "value1"}}, "reason": "why this step?"}}
        
        If no tools are needed, return an empty list [].
        Only return the JSON.
        """

    async def create_plan(self, user_request: str) -> list:
        tools_list = registry.list_tools()
        prompt = self.system_prompt.format(tools_list=json.dumps(tools_list, indent=2))
        
        # Use LLM to generate plan
        # Note: In a real implementation, we'd use a specific prompt or function calling
        full_message = f"{prompt}\n\nUser Request: {user_request}"
        
        try:
            # For now, we reuse the brain's session or a new one
            response = await jarvis_brain.get_response("planner_internal", full_message)
            # Try to parse JSON from the response
            # Note: This is a simplified version
            if "[" in response and "]" in response:
                json_str = response[response.find("["):response.rfind("]")+1]
                return json.loads(json_str)
            return []
        except Exception as e:
            logger.error(f"Error creating plan: {e}")
            return []

planner = Planner()
