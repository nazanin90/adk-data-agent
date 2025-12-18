"""
This script creates a BigQuery Data Agent using the Conversational Analytics API.
"""

import argparse
import os
import sys

# Add the project root to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.ca_api_helper import create_bigquery_ca_data_agent
from src.agents import config_project

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a BigQuery Data Agent.")
    parser.add_argument("--agent_id", type=str, help="The ID or config variable name of the agent to create.")
    args = parser.parse_args()

    agent_id_str = args.agent_id if args.agent_id else "PATIENT_ANALYTICS_AGENT_ID"

    # Check if the provided agent_id is a variable name in config_project
    agent_id = getattr(config_project, agent_id_str) if hasattr(config_project, agent_id_str) else agent_id_str

    print(f"Creating BigQuery Data Agent with ID: {agent_id}")
    agent = create_bigquery_ca_data_agent(agent_id)
    print(f"Successfully created BigQuery Data Agent: {agent.name}")
