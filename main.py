import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -------------------------
# Function
# -------------------------
def get_weather(city):
    weather_data = {
        "Chennai": "32°C, sunny",
        "London": "18°C, cloudy",
        "New York": "24°C, partly cloudy",
    }

    return weather_data.get(city, "Weather data not available.")

def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid mathematical Expression"
    
def get_time(city):
    time_data = {
        "Chennai": "21:30",
        "London": "17:00",
        "New York": "12:00",
    }

    return time_data.get(city, "Time data not available")

tool_registry = {
    "get_weather": get_weather,
    "calculator": calculator,
    "get_time": get_time,
}


# -------------------------
# Tool definition
# -------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression such as 25 * 48"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current time for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# -------------------------
# User input
# -------------------------
ask = input("What do you want to ask the AI? : ")

messages = [
    {
        "role": "user",
        "content": ask
    }
]


# -------------------------
# First AI call
# -------------------------
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools
)

message = response.choices[0].message


# -------------------------
# Handle tool calls
# -------------------------
if message.tool_calls:

    # IMPORTANT:
    # Add the assistant's tool-call message first
    messages.append(message)

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name
        arguments = json.loads(
            tool_call.function.arguments
        )

        print("Tool requested:", tool_name)
        print("Arguments:", arguments)

        # Find the Python function
        tool = tool_registry[tool_name]

        # Execute it
        result = tool(**arguments)

        print("Tool result:", result)

        # Give result back to LLM
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )


    # -------------------------
    # Second AI call
    # -------------------------
    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools
    )

    final_answer = final_response.choices[0].message.content

    print("\nFinal answer:")
    print(final_answer)


else:
    print("\nFinal answer:")
    print(message.content)