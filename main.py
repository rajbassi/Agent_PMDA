import perception
import decide
import action
import memory
import logging
import os
import asyncio
import models

from dotenv import load_dotenv
from google import genai
from pdb import set_trace as st
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import logging
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv(verbose=True, override=True)
api_key = os.getenv("GEMINI_API_KEY")
logging.info(f"API Key: {api_key}")
client = genai.Client(api_key=api_key)
model = os.getenv("MODEL")

memory = memory.Memory()

system_prompt = """You are a math agent. Your task is to solve a math equation having operators like +, -, *, /, and parentheses. 
                You must use the available tools to solve the equation.
            
You must respond with EXACTLY ONE line for each operation in one of these formats (no additional text):
1. For function calls:
   FUNCTION_CALL: function_name|param1|param2|...
   
2. For final answers:
   FINAL_ANSWER: [number]

Important:
- When a function returns multiple values, you need to process all of them
- Only give FINAL_ANSWER when you have completed all necessary calculations
- Do not repeat function calls with the same parameters
- Your entire response should be a single line starting with either 'FUNCTION_CALL:' or 'FINAL_ANSWER:'.
- Your response should not include both 'FUNCTION_CALL:' and 'FINAL_ANSWER:' in the same line

Examples:
- FUNCTION_CALL: add|5|3
- FUNCTION_CALL: subtract|5|3
- FINAL_ANSWER: [42]

DO NOT include any explanations or additional text.
."""

async def get_tools():
    """Get the tools from the MCP server"""
    try:
        # Create a single MCP server connection
        logging.info("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )

        async with stdio_client(server_params) as (read, write):
            logging.info("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                logging.info("Session created, initializing...")
                await session.initialize()
                
                # Get available tools
                logging.info("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                logging.info(tools)
                logging.info(f"Successfully retrieved {len(tools)} tools")

                # Create system prompt with available tools
                print(f"Number of tools: {len(tools)}")
                
                try:
                    # First, let's inspect what a tool object looks like
                    # if tools:
                    #     print(f"First tool properties: {dir(tools[0])}")
                    #     print(f"First tool example: {tools[0]}")
                    
                    tools_description = []
                    for i, tool in enumerate(tools):
                        try:
                            # Get tool properties
                            params = tool.inputSchema["properties"]
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            # Format the input schema in a more readable way                            
                            param_details = []
                            for param_name, param_info in params.items():
                                param_type = param_info.get('type', 'unknown')
                                param_details.append(f"{param_name}: {param_type}")
                            params_str = ', '.join(param_details)

                            if not params_str:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            tools_description.append(tool_desc)
                            logging.debug(f"Added description for tool: {tool_desc}")
                        except Exception as e:
                            print(f"Error processing tool {i}: {e}")
                            tools_description.append(f"{i+1}. Error processing tool")
                    
                    tools_description = "\n".join(tools_description)
                    logging.info("Successfully created tools description")
                except Exception as e:
                    logging.error(f"Error creating tools description: {e}")
                    tools_description = "Error loading tools"
            
    except Exception as e:
        logging.error(f"Error getting tools: {e}")
        raise
    return tools_description, tools


async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

async def main():
    global memory
    tools_description, tools = await get_tools()
    perception_output = await perception.get_query_perception(client, model, tools_description)
    percepted_prompt = f"{system_prompt}\n\n Reasoning to solve equation:\n {perception_output} \n\n"

    percepted_prompt = f"""{percepted_prompt} Before returning the FINAL_ANSWER, {memory.get('Output Format')}. \n\n"""
    print(percepted_prompt)
    query = f"Solve the equation: {memory.get('Input Equation')}" 
    iteration_response = None
    iteration = 0
    max_iterations = 10
    while iteration < max_iterations:
            print(f"\n--- Iteration {iteration + 1} ---")
            if iteration_response is None:
                current_query = query + " What should I do first?"
            else:
                current_query = current_query + "\n\n" + iteration_response
                current_query = current_query + "  What should I do next?"

            print(current_query)
            # Get model's response with timeout
            print("Preparing to generate LLM response...")
            iteration = iteration + 1
            prompt = f"{percepted_prompt} Query: {current_query}"
            try:
                    iteration_response = await decide.decide_next_step(prompt, client, model, tools, iteration)
                    print(f"LLM Response: {iteration_response}")

                    if iteration_response.startswith("FINAL_ANSWER:"):
                        print(f"Final Answer: {iteration_response}")
                        break
                    
            except Exception as e:
                print(f"Failed to get LLM response: {e}")
                break

if __name__ == "__main__":

    input_equation = input("Enter a math equation: ")
    memory.store("Input Equation", input_equation)

    output_format = input("Enter the output format: ")
    memory.store("Output Format", output_format)
    
    asyncio.run(main())
