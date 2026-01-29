import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_KEY")

if api_key is None:
    raise Exception("api_key not found")


def main():
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Agentic loop - continue until we get a text response
    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt, 
                temperature=0
            )
        )

        if args.verbose and response.usage_metadata is not None:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print()

        # Check if the model wants to call functions
        if response.function_calls:
            # Add the model's response to messages
            messages.append(types.Content(
                role="model",
                parts=[types.Part(function_call=fc) for fc in response.function_calls]
            ))
            
            # Execute each function call
            function_results = []
            for function_call in response.function_calls:
                # Call the function and get the result
                function_call_result = call_function(function_call, verbose=args.verbose)
                
                # Validate the result
                if not function_call_result.parts:
                    raise RuntimeError("Function call returned empty parts list")
                
                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError("Function call returned None function_response")
                
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError("Function call returned None response")
                
                # Add to results list
                function_results.append(function_call_result.parts[0])
                
                # Print result if verbose
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                    print()
            
            # Add function results to messages
            messages.append(types.Content(role="tool", parts=function_results))
            
            # Continue the loop to get the next response
        else:
            # No function calls - we have a text response
            print(response.text)
            break


if __name__ == "__main__":
    main()
