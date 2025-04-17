import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI()

def run_command(command):
    result = os.system(command)
    return f"Command executed with result: {result}"

def write_file(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"File '{filename}' written successfully."
    except Exception as e:
        return f"Error writing file: {e}"

avaiable_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output."
    },
    "write_file": {
        "fn": write_file,
        "description": "Writes content to a file. Takes filename and content as input."
    }
}

system_prompt = """
    You are a helpful AI Assistant who is specialized in executing user queries on a system and returning output.
    You work in start, plan, action, observe, and output modes.
    For the given user query and available tools, plan the step-by-step execution. Based on the planning,
    select the relevant tool from the available tools. Based on the tool selection, you perform an action to call the tool.
    Wait for the observation and, based on the observation from the tool call, resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for the next input.
    - Carefully analyze the user query.
    - Dont entertain any query which is not an operation or a command.

    Output JSON Format:
    {
        "step": "string",
        "content": "string",
        "function": "The name of the function if the step is action",
        "input": "The input parameter for the function (JSON format)",
    }

    Available Tools:
    - run_command: Takes a command as input to execute on system and returns output.
    - write_file: Writes content to a file. Takes filename and content as input.
  
    Example:
    User Query: Create a file named 'sum.py' that calculates the sum of two numbers and print the result.
      Output: { "step": "plan", "content": "The user wants to create a Python file to calculate the sum of two numbers." }
      Output: { "step": "plan", "content": "I should use the 'write_file' tool to create the file." }
      Output: { "step": "action", "function": "write_file", "input": { "filename": "sum.py", "content": "a = 5\\nb = 10\\nprint(a + b)" } }
      Output: { "step": "output", "content": "File 'sum.py' written successfully." }
      
"""

messages = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_query = input('>')
    messages.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
 
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name, False) != False:
                output = avaiable_tools[tool_name].get("fn")(**tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "content": output})})
                continue

        # if parsed_output.get("step") == "observe":
        #     print(f"👀: {parsed_output.get('content')}")
        #     continue

        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get('content')}")
            break
