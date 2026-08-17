import json 
import groq 
class Agent:
    def __init__(self,client,model,tools,tool_registry):
        self.client = client
        self.model = model
        self.tools = tools
        self.tool_registry = tool_registry
        
    def run(self,user_input):
        messages = [
            {
                "role":"user",
                "content":user_input
            }
        ]
        while True:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                tools = self.tools,
            )
            
            message = response.choices[0].message
            
            if not message.tool_calls:
                return message.content
            
            messages.append(message)
            print(messages)
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"Tool : {tool_name}\n")
                print(f"Arguments:{arguments}\n")
                
                tool = self.tool_registry[tool_name]
                
                result = tool(**arguments)
                
                print(f"Result : {result}\n")
                
                messages.append(
                    {
                        "role":"tool",
                        "tool_call_id":tool_call.id,
                        "content":result
                    }
                )