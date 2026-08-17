import os 
from dotenv import load_dotenv
from groq import Groq 
import json
load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

#function 
def get_weather(city):
    weather_data = {
        "Chennai": "32°C, sunny",
        "London": "18°C, cloudy",
        "New York": "24°C, partly cloudy",
    }
    
    return weather_data.get(city,"Weather  data not avaiable.")

#tools
tools = [
    {
        "type":"function",
        "function": {
            "name":"get_weather",
            "description":"Get the current weather for a city.",
            "parameters": {
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"The name of the city"
                    }
                },
                "required":["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model = "openai/gpt-oss-20b",
    messages = [
        {
            "role":"user",
            "content":"What is the weather in Chennai?"
        }
    ],
    tools = tools
)

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(tool_name)
        print(arguments)
        
        if tool_name == "get_weather":
            result = get_weather(arguments["city"])
            print("Tool result:",result)
            
            