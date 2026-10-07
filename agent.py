import json

from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

WORKSPACE = Path("workspace").resolve()

def calculate(a, b, operation):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Unknown operation"

def read_note(filename):
    file_path = (WORKSPACE / filename).resolve()

    if WORKSPACE not in file_path.parents:
        return "Access denied: file is outside the workspace."

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def write_note(filename, content):
    file_path = (WORKSPACE / filename).resolve()

    if WORKSPACE not in file_path.parents:
        return "Access denied: file is outside the workspace."

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Successfully wrote to {filename}"

load_dotenv()

client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "calculate",
        "description": "Perform basic arithmetic using two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number."
                },
                "b": {
                    "type": "number",
                    "description": "The second number."
                },
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform."
                }
            },
            "required": ["a", "b", "operation"],
            "additionalProperties": False
        },
                "strict": True
    },
    {
        "type": "function",
        "name": "read_note",
        "description": "Read the contents of a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the text file to read."
                }
            },
            "required": ["filename"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "write_note",
        "description": "Write content to a text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the text file to write to."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                }
            },
            "required": ["filename", "content"],
            "additionalProperties": False
        },
        "strict": True
    }
]

user_goal = input("You: ")

response = client.responses.create(
    model="gpt-5.5",
    input=user_goal,
    tools=tools
)

max_steps = 10
step = 0

while step < max_steps:
    step += 1

    print(f"\n--- Step {step} ---")

    tool_calls = [
        item for item in response.output
        if item.type == "function_call"
    ]

    if not tool_calls:
        print("Agent 001:", response.output_text)
        break

    tool_outputs = []

    for tool_call in tool_calls:

        print(f"\nAgent wants to use: {tool_call.name}")

        arguments = json.loads(tool_call.arguments)

        print("Arguments:", arguments)

        try:
            if tool_call.name == "calculate":
                result = calculate(
                    arguments["a"],
                    arguments["b"],
                    arguments["operation"]
                )
            elif tool_call.name == "read_note":
                result = read_note(arguments["filename"])
            elif tool_call.name == "write_note":
                result = write_note(
                    arguments["filename"],
                    arguments["content"]
                )
            else:
                result = "Unknown tool"

        except Exception as error:
            result = f"Tool error: {type(error).__name__}: {error}"

        print("Tool result:", result)

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result)
            }
        )

    response = client.responses.create(
        model="gpt-5.5",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools
    )

else:
    print(f"\nAgent 001 stopped after reaching the {max_steps}-step limit.")
    