from tools import tools

# Generate the formatted text
available_actions = "\n\n".join([
    f"{tool}:\n{details['example_usage']}\n{details['description']}"
    for tool, details in tools.items()
])

think_prompt = f"""
You are a reasoning agent that analyzes the user's QUESTION and determines the appropriate ACTIONS (tools) to fulfill the query. 

**Guidelines:**
1. If the query requires tools, specify the tools and their inputs.
2. If the query does not require tools, provide the direct RESPONSE.
3. If multiple tools are needed, outline their sequence and inputs clearly.

**Available Tools:**
{available_actions}

**Response Format:**
- THOUGHTS: Your reasoning about the user's question.
- VALUES: Intermediate or final values. Use "Waiting" for values to be retrieved via tools.
  Example: {{'variable_name': {{'ID': 'step_number', 'ACTION': 'tool_name', 'INPUT': 'tool_input', 'RESPONSE': 'Waiting'}}}}
- ACTION: Tool to execute and their inputs. If no tool is needed, state `None`.
- RESULT: (Optional) Direct response if tools are not needed.
- PAUSE: Always include this to signal the agent is ready for execution (when tools are used).

**Example 1: Query with Tool Use**
QUESTION: What is the mass of Earth times 2?
THOUGHTS: I need to find the mass of Earth and multiply it by 2.
VALUES: {{
    'earth_mass': {{'NAME':'var_1', 'ACTION': 'get_planet_mass', 'INPUT': 'Earth', 'RESULT': None}},
    'multiplier': {{'NAME':'var_2', 'ACTION': None, 'INPUT': None, 'RESULT': 2}}
    'result': {{'NAME':'var_3', 'ACTION': 'calculate', 'INPUT': 'var_1 * var_2', 'RESULT': 'Waiting'}}
}}
PAUSE

**Example 2: Query Without Tool Use**
QUESTION: What is the closest star to Earth?
THOUGHTS: I need to find the closest star to Earth, but no tools are needed.
TOOLS: None
RESPONSE: 'The Sun'

Now, respond to the following QUESTION in the specified format:
"""

system_prompt = f"""
    You are an AI that is created to help the user. Wait for user queries, instructions and behave accordingly.
""".strip()

# system_prompt = f"""
# You run in a loop of Thought, Action, PAUSE, Observation.
# At the end of the loop you output an Answer
# Use Thought to describe your thoughts about the question you have been asked.
# Use Action to run one of the actions available to you - then return PAUSE.
# Observation will be the result of running those actions.

# Your available actions are: 

# Example session:

# Question: What is the mass of Earth times 2?
# Thought: I need to find the mass of Earth
# Action: get_planet_mass: Earth
# PAUSE 

# You will be called again with this:

# Observation: 5.972e24

# Thought: I need to multiply this by 2
# Action: calculate: 5.972e24 * 2
# PAUSE

# You will be called again with this: 

# Observation: 1,1944×10e25

# If you have the answer, output it as the Answer.

# Answer: The mass of Earth times 2 is 1,1944×10e25.

# Now it's your turn, give me appropriate THOUGHTS and ACTION for
# """.strip()