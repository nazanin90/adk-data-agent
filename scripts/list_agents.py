"""
This script lists all Data Analytics Agents in a project using the Conversational Analytics API.
"""

import os
import sys

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.ca_api_helper import list_data_agents

if __name__ == "__main__":
    print("Listing Data Analytics Agents...")
    agents = list_data_agents()
    if not agents:
        print("No Data Analytics Agents found.")
    else:
        print("Found Data Analytics Agents:")
        for agent in agents:
            print(f"- {agent.name}")
