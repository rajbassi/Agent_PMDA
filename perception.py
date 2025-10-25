from dotenv import load_dotenv
from google import genai
from pdb import set_trace as st
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import logging
import os
import asyncio
import models

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def get_query_perception(client, model, tools_description, timeout=30):
    """Generate content with a timeout"""
    prompt = """You are a math agent. Your task is to solve a math equation having operators like +, -, *, /, and parentheses. 
            
            - List all the steps to solve an equation from the prosepective that equation will be solved by a someone else. 
            - You must use the available tools to solve the equation.
            - Just give the general strategy and examples of how to solve the equation.
            - Do not include your thought process or what you are doing to determine the steps.
"""

    logging.info(f"Tools description: {tools_description}")

    logging.info("Starting LLM generation...")
    prompt = prompt + "\n\nAvailable tools: \n" + tools_description + "\n\n"
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model=model,
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        logging.info(f"Response text: {response.text}")
        return response.text
    except TimeoutError:
        print("LLM generation timed out!")
        logging.error("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        logging.error(f"Error in LLM generation: {e}")
        raise


