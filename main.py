import os

from dotenv import load_dotenv
from groq import Groq

from agent import Agent


load_dotenv()


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# TOOLS
# ==========================================

def get_weather(city):

    weather_data = {
        "Chennai": "32°C, sunny",
        "London": "18°C, cloudy",
        "New York": "24°C, partly cloudy",
    }

    return weather_data.get(
        city,
        "Weather data not available"
    )


def calculator(expression):

    return str(eval(expression))


def get_time(city):

    time_data = {
        "Chennai": "21:30",
        "London": "17:00",
        "New York": "12:00",
    }

    return time_data.get(
        city,
        "Time data not available"
    )


# ==========================================
# TOOL REGISTRY
# ==========================================

tool_registry = {

    "get_weather": get_weather,

    "calculator": calculator,

    "get_time": get_time,

}


# ==========================================
# TOOL DEFINITIONS
# ==========================================

tools = [

    {
        "type": "function",

        "function": {

            "name": "get_weather",

            "description":
                "Get the current weather for a city.",

            "parameters": {

                "type": "object",

                "properties": {

                    "city": {
                        "type": "string"
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

            "description":
                "Calculate a mathematical expression.",

            "parameters": {

                "type": "object",

                "properties": {

                    "expression": {
                        "type": "string"
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

            "description":
                "Get the current time for a city.",

            "parameters": {

                "type": "object",

                "properties": {

                    "city": {
                        "type": "string"
                    }

                },

                "required": ["city"]

            }
        }
    }

]


# ==========================================
# CREATE AGENT
# ==========================================

agent = Agent(

    client=client,

    model="openai/gpt-oss-20b",

    tools=tools,

    tool_registry=tool_registry,

)


# ==========================================
# RUN AGENT
# ==========================================

answer = agent.chat(
    "What is the weather in Chennai?"
)

print("\n🤖 Agent:")
print(answer)


answer = agent.chat(
    "What about London?"
)

print("\n🤖 Agent:")
print(answer)


answer = agent.chat(
    "And what about New York?"
)

print("\n🤖 Agent:")
print(answer)

agent.show_memory()