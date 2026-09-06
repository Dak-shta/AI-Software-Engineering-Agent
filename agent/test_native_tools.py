from dotenv import load_dotenv
from groq import Groq

from agent.tools import TOOL_SCHEMAS

load_dotenv()

client = Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
    {
        "role": "user",
        "content": (
            "List the files in the repository at sample_repo. "
            "Use repo_path exactly as 'sample_repo'."
        )
    }
],
    tools=TOOL_SCHEMAS,
    tool_choice="auto",
    temperature=0,
    max_tokens=200,
)

message = response.choices[0].message

print("Content:")
print(message.content)

print("\nTool calls:")

if message.tool_calls:
    for call in message.tool_calls:
        print("Tool:", call.function.name)
        print("Arguments:", call.function.arguments)
else:
    print("No tool call generated.")