from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from dotenv import load_dotenv
from google import genai
import logging
import sys
import os
import asyncio
import models
import action

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def generate_with_timeout(client, prompt, model, timeout=30):
    logging.info("Starting LLM generation...")
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
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        logging.error("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        logging.error(f"Error in LLM generation: {e}")
        raise



async def decide_next_step(up_to_date_prompt: str, client: genai.Client, model: str, tools: list, iteration_count: int):
    try:
        response = await generate_with_timeout(client, up_to_date_prompt, model)
        response_text = await get_response(tools, response.text, iteration_count)        
        return response_text
    except Exception as e:
        logging.error(f"DEBUG: Error details: {str(e)}")
        logging.error(f"DEBUG: Error type: {type(e)}")
        raise e

async def get_response(tools: list, llm_response: str, iteration_count: int):
    try:
        if llm_response.startswith("FINAL_ANSWER:"):
            return llm_response
        else:
            _, function_info = llm_response.split(":", 1)
            parts = [p.strip() for p in function_info.split("|")]
            func_name, params = parts[0], parts[1:]
            
            logging.info(f"\nDEBUG: Raw function info: {function_info}")
            logging.info(f"DEBUG: Split parts: {parts}")
            logging.info(f"DEBUG: Function name: {func_name}")
            logging.info(f"DEBUG: Raw parameters: {params}")

            # Find the matching tool to get its input schema
            tool = next((t for t in tools if t.name == func_name), None)
            if not tool:
                print(f"DEBUG: Available tools: {[t.name for t in tools]}")
                raise ValueError(f"Unknown tool: {func_name}")

            logging.info(f"DEBUG: Found tool: {tool.name}")
            logging.info(f"DEBUG: Tool schema: {tool.inputSchema}")

            # Prepare arguments according to the tool's input schema
            arguments = {}
            schema_properties = tool.inputSchema.get('properties', {})
            logging.info(f"DEBUG: Schema properties: {schema_properties}")

            argumentCount = 0
            for param_name, param_info in schema_properties.items():
                param_type = param_info.get('type', 'string')

                value = params[argumentCount]
                argumentCount += 1
                
                logging.info(f"DEBUG: Converting parameter {param_name} with value {value} to type {param_type}")
                cval = cast_value(value, param_type)
                arguments[param_name] = cval
            
            print(f"DEBUG: Final arguments: {arguments}")
            print(f"DEBUG: Calling tool {func_name}")
            
            result = await action.call_tools(func_name, arguments=arguments)
            print(f"DEBUG: Raw result: {result}")
            
            # Get the full result content
            if hasattr(result, 'content'):
                print(f"DEBUG: Result has content attribute")
                # Handle multiple content items
                if isinstance(result.content, list):
                    iteration_result = [
                        item.text if hasattr(item, 'text') else str(item)
                        for item in result.content
                    ]
                else:
                    iteration_result = str(result.content)
            else:
                print(f"DEBUG: Result has no content attribute")
                iteration_result = str(result)
                
            print(f"DEBUG: Final iteration result: {iteration_result}")
        
            return_value = f"In the {iteration_count} iteration you called {func_name} with {arguments} parameters, and the function returned {iteration_result}."
            return return_value

    except Exception as e:
        print(f"DEBUG: Error details: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
             
            
def cast_value(value, value_type):
    try:
        if value_type == 'integer':
            return int(value)
        elif value_type == 'number':
            return float(value)
        elif value_type == 'array':
            # Handle array input
            if isinstance(value, str):
                value = value.strip('[]').split(',')
            return [int(x.strip()) for x in value]
        else:
            return str(value)
    except Exception as e:
        logging.error(f"Error casting value {value} to type {value_type}: {e}")
        return str(value)




'''

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import logging
import sys
import os



import asyncio
import models
import perception

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

max_iterations = 10
iteration = 0
iteration_response = None

async def decide(system_prompt: str, query: str, llm_response: str):

    if llm_response.startswith("FUNCTION_CALL:"):
        _, function_info = llm_response.split(":", 1)
        parts = [p.strip() for p in function_info.split("|")]
        func_name, params = parts[0], parts[1:]
        
        print(f"\nDEBUG: Raw function info: {function_info}")
        print(f"DEBUG: Split parts: {parts}")
        print(f"DEBUG: Function name: {func_name}")
        print(f"DEBUG: Raw parameters: {params}")
        
        try:
            # Find the matching tool to get its input schema
            tool = next((t for t in tools if t.name == func_name), None)
            if not tool:
                print(f"DEBUG: Available tools: {[t.name for t in tools]}")
                raise ValueError(f"Unknown tool: {func_name}")

            print(f"DEBUG: Found tool: {tool.name}")
            print(f"DEBUG: Tool schema: {tool.inputSchema}")

            # Prepare arguments according to the tool's input schema
            arguments = {}
            schema_properties = tool.inputSchema.get('properties', {})
            print(f"DEBUG: Schema properties: {schema_properties}")

            for param_name, param_info in schema_properties.items():
                if not params:  # Check if we have enough parameters
                    raise ValueError(f"Not enough parameters provided for {func_name}")
                    
                value = params.pop(0)  # Get and remove the first parameter
                param_type = param_info.get('type', 'string')
                
                print(f"DEBUG: Converting parameter {param_name} with value {value} to type {param_type}")
                
                # Convert the value to the correct type based on the schema
                if param_type == 'integer':
                    arguments[param_name] = int(value)
                elif param_type == 'number':
                    arguments[param_name] = float(value)
                elif param_type == 'array':
                    # Handle array input
                    if isinstance(value, str):
                        value = value.strip('[]').split(',')
                    arguments[param_name] = [int(x.strip()) for x in value]
                else:
                    arguments[param_name] = str(value)

            print(f"DEBUG: Final arguments: {arguments}")
            print(f"DEBUG: Calling tool {func_name}")
            
            result = await session.call_tool(func_name, arguments=arguments)
            print(f"DEBUG: Raw result: {result}")
            
            # Get the full result content
            if hasattr(result, 'content'):
                print(f"DEBUG: Result has content attribute")
                # Handle multiple content items
                if isinstance(result.content, list):
                    iteration_result = [
                        item.text if hasattr(item, 'text') else str(item)
                        for item in result.content
                    ]
                else:
                    iteration_result = str(result.content)
            else:
                print(f"DEBUG: Result has no content attribute")
                iteration_result = str(result)
                
            print(f"DEBUG: Final iteration result: {iteration_result}")
            
            # Format the response based on result type
            if isinstance(iteration_result, list):
                if "Paint opened successfully" in iteration_result[0]:
                    result_str = "that paint has opened successfully"
                elif "Rectangle drawn Successfully" in iteration_result[0]:
                    result_str = "that rectangle has drawn successfully"
                elif "added successfully" in iteration_result[0]:
                    result_str = "that text has added successfully"
                    print(f"-"*50)
                    print(f"All the tasks are done successfully")
                    print(f"-"*50)
                elif "rror" in iteration_result[0]:
                    print(f"Error in iteration {iteration}: {iteration_result[0]}")
                    
                else:
                    result_str = f"[{', '.join(iteration_result)}]"
            else:
                result_str = str(iteration_result)
            
            return f"In the {iteration + 1} iteration you called {func_name} with {arguments} parameters, and the function returned {result_str}."
            

        except Exception as e:
            print(f"DEBUG: Error details: {str(e)}")
            print(f"DEBUG: Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
'''