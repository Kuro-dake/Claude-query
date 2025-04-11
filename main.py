import anthropic
import json

import sys
import os

client = anthropic.Anthropic(
    # default api key in the env var ANTHROPIC_API_KEY
    # or
    # api_key='...xyz...'
)

def get_query_params():

    if sys.argv[1] == "query":
        query = " ".join(sys.argv[2])
        full_query = (  "Return up to three (but less if they're not needed) variants of a linux command "
                        f"that would carry out the following request: {query}."
                        "Return it as a json object following the format: "
                        '{"commands": [{"command": ${the command itself}, "description": ${a one sentence description for the command itself, and each parameter of the command} }],'
                        ' "explanation": ${empty string}}')
    elif sys.argv[1] == "assist":
        command = " ".join(sys.argv[2:])
        query = "\n".join(sys.stdin.readlines())

        if not query:
            query = sys.stderr.errors

        full_query = (  f"The command \"{command}\" returns an error. Return up to three (but less if they're not needed) variants of a modified linux command "
                        f"that would fix the following error: {query}."
                        "Return it as a json object following the format: "
                        '{"commands": ["command": ${the command itself}, "description": ${a one sentence description for the command itself, and each parameter of the command}],'
                        ' "explanation" : ${explain the error and how the command fixes it}}')
    else:
        print("Invalid argument. Please use either 'query' or 'assist'.")
        exit(1)

    return dict(
        model="claude-3-7-sonnet-20250219",
        max_tokens=5000,
        temperature=1,
        system="You are a linux system administrator.",

        messages=[{"role": "user",
                   f"content": full_query}]
    )

get_query_params()

message = client.messages.create(
    **get_query_params()
)

try:
    result = json.loads(message.content[0].text.replace("```json\n", "").replace("```", ""))
except json.JSONDecodeError:
    print("Could not decode the response from the API. Try increasing the max_tokens parameter.")
    exit(1)

user = os.getenv("USER")

if result.get("explanation"):
    print(result["explanation"], end="\n\n")

commands = result["commands"]

with open(f"/home/{user}/.bash_history", "a") as f:
    for command in commands:
        print(f"- {command['command']}\n \t {command['description']}\n")
        f.write(f"{command['command']}\n")

exit()
