# test_agent.py

from agents.pantry_agent import run_pantry_agent
import json

if __name__ == "__main__":
    ingredients = "potato, spinach"
    result = run_pantry_agent(ingredients)

    print("\n✅ Agent Output:")
    print(json.dumps(result, indent=2))
