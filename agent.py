import os
import re
from groq import Groq
import random

from system import system_prompt, think_prompt

class Agent:
    def __init__(self, name, client, model="llama3-70b-8192", temperature=0):
        
        # State Management
        self.name = name
        self.state = "IDLE"
        
        # 
        if client == 'groq':
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature
        self.messages = []
        
        # Append the system message as the first prompt
        self.messages.append({"role": "system", "content": self.system_prompt})

    def think(self, user_query: str = ""):
        """
        Triggers the agent to think about the user query.
        - input: user_query
        - processing: 
            - create a user_prompt based on query
            - append to the message list
            - run llm on the message list
        - output: thought with a keyword 'PAUSE' and/or 'Action'
        """

        # Append the think prompt and user query
        self.messages.append({"role": "system", "content": think_prompt})
        self.messages.append({"role": "user", "content": user_query})
        
        # Execute the thought process (e.g., using an LLM)
        thought_result = self.execute()
        
        return thought_result


    def append_user_message(self, message: str):
        if message:
            self.messages.append({"role": "user", "content": message})

    def append_system_message(self, message: str):
        if message:
            self.messages.append({"role": "system", "content": message})
        
    def execute(self):
        """
        Executes chat completion based on the current message list.
        - input: None
        - processing: 
            - runs chat completion based on preset agent parameters
        - output: response [str]
        """
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=self.temperature
        )
        
        response = chat_completion.choices[0].message.content
        return response

    # def handle_pause(self, response: str):
    #     print("Handling pause...")
    #     # Regex to extract the function call and argument
    #     match = re.search(r"Action:\s*(\w+):\s*(.+)", response)
    #     if match:
    #         function_call = match.group(1)
    #         argument = match.group(2)
    #         print(f"Function Call: {function_call}, Argument: {argument}")

    #         # Call the appropriate function based on the function_call
    #         if function_call == "tool_1":
    #             self.tool_1(argument)
    #         else:
    #             print(f"Unknown function call: {function_call}")

    #     else:
    #         print("No match found for Action pattern.")
