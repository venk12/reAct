import typer
from agent import Agent
from system import system_prompt
import json
import re
from tools import get_planet_mass, calculate, get_planet_distance

def parse_comma_separated_values(input_string):
    # Split the string by commas and remove any leading/trailing spaces
    values = [value.strip() for value in input_string.split(',')]
    return values

def clean_values_string(values_str):
    """
    Clean up the VALUES string to make it JSON-compatible:
    - Replace single quotes with double quotes.
    - Replace Python-specific None with JSON-compatible null.
    - Remove trailing commas (e.g., ",}").
    """
    # Replace single quotes with double quotes
    values_str = values_str.replace("'", '"')
    # Replace None with null
    values_str = values_str.replace("None", "null")
    # Replace \n to ""
    values_str = values_str.replace("\n","")
    # Remove trailing commas
    values_str = re.sub(r",\s*}", "}", values_str)
    # Parse the cleaned string as JSON
    return json.loads(values_str)

def main(name: str = "NEWTON"):
    typer.echo(f"Hello. Let me morph into: {name}")
    agent = Agent(
                  name = name,
                  client='groq',
                  model="llama3-70b-8192", 
                  temperature=0
                 )
    
    while True:
        user_query = input("Ask something (or type 'END' to exit): ")
        if user_query.lower() in ["end","exit","quit"]:
            break

        thought_response = agent.think(user_query)
        print(thought_response)
        print("----------------------------------------------------------------------")

        if 'PAUSE' in thought_response and 'RESULT: None' in thought_response:

            print("Calculating using available tools and planned actions...")
            values_match = re.search(r"VALUES:\s*(\{.*\})", thought_response, re.DOTALL)
            json_str = values_match.group(1)
            action_blueprint = clean_values_string(json_str)

            sorted_blueprint = sorted(action_blueprint.values(), key=lambda x: x['NAME'])

            # Variables to store intermediate results
            results = {}

            # Execution loop
            for step in sorted_blueprint:
                action = step['ACTION']
                name = step['NAME']  # Variable name from 'NAME' field
                if action == 'get_planet_mass':
                    results[name] = get_planet_mass(step['INPUT'])
                elif action is None:
                    results[name] = step['RESULT']
                elif action == 'calculate':
                    expression = step['INPUT']
                    for var, value in results.items():
                        expression = expression.replace(var, str(value))
                    results[name] = calculate(expression)
                elif action == 'get_planet_distance':
                    args = parse_comma_separated_values(step['INPUT'])
                    results[name] = get_planet_distance(args[0], args[1])

            # Final result for var_3
            final_result = results.get("var_3", None)
            output = {"RESULT": final_result}
            print(output)            


if __name__ == "__main__":
    typer.run(main)