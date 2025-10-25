from typing import List
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
from pywinauto.application import Application
from win32api import GetSystemMetrics
import models
import sys

# instantiate an MCP server client
mcp = FastMCP("Calculator")
#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return a + b

@mcp.tool()
def add_list(numbers: List[int]) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(numbers)

#subtraction tool       
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return a - b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> int:")
    return a / b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return a * b


'''
#addition tool
@mcp.tool()
def add(input: models.AddInput) -> models.Output:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    result = models.Output(result=input.a + input.b, type="add")
    return result

@mcp.tool()
def add_list(input: models.AddListInput) -> models.Output:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    result = models.Output(result=sum(input.numbers), type="add")
    return result

#subtraction tool       
@mcp.tool()
def subtract(input: models.SubtractInput) -> models.Output:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    result = models.Output(result=input.a - input.b, type="subtract")
    return result

@mcp.tool()
def divide(input: models.DivideInput) -> models.Output:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> int:")
    result = models.Output(result=input.a / input.b, type="divide")
    return result

@mcp.tool()
def multiply(input: models.MultiplyInput) -> models.Output:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    result = models.Output(result=input.a * input.b, type="multiply")
    return result
'''
if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution

