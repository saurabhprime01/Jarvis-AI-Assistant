from tools.base import BaseTool, registry
import numexpr

@registry.register
class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Useful for performing mathematical calculations. Input should be a mathematical expression string."

    async def run(self, expression: str, **kwargs) -> str:
        try:
            result = numexpr.evaluate(expression).item()
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
