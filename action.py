from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import logging
import sys
import os
import asyncio
import models
import perception

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def call_tools(function_name: str, arguments: dict):
    server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            logging.info("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                logging.info("Session created, initializing...")
                await session.initialize()
                result = await session.call_tool(function_name, arguments=arguments)
                print(f"Tool {function_name} called with arguments {arguments} and returned {result.content}")
        return result
    except TimeoutError:
        print("LLM generation timed out!")
        logging.error("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        logging.error(f"Error in LLM generation: {e}")
        raise

    '''
                    logging.info(f"DEBUG: Converting parameter {param_name} with value {value} to type {param_type}")
                    cval = cast_value(value, param_type)
                    arguments[param_name] = cval
                
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
            
                return result
    except Exception as e:
        logging.error(f"DEBUG: Error details: {str(e)}")
        logging.error(f"DEBUG: Error type: {type(e)}")
        raise e
        
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
                        break
                    else:
                        result_str = f"[{', '.join(iteration_result)}]"
                else:
                    result_str = str(iteration_result)
                
                iteration_response.append(
                    f"In the {iteration + 1} iteration you called {func_name} with {arguments} parameters, "
                    f"and the function returned {result_str}."
                )
                last_response = iteration_result

            except Exception as e:
                print(f"DEBUG: Error details: {str(e)}")
                print(f"DEBUG: Error type: {type(e)}")
                import traceback
                traceback.print_exc()
                iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                break
            
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