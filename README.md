# ADK Data Analytics Agent

## Overview

This project is a **multi-agent healthcare data analytics system** built with the Google Agent Development Kit (ADK). The system demonstrates a sophisticated architecture to answer natural language questions about healthcare data stored in BigQuery.

### Key Technologies

* **Google Agent Development Kit (ADK):** For agent orchestration and tool integration.
* **Gemini Data Analytics API:** For natural language to SQL conversion.
* **BigQuery:** For healthcare and medication data storage.

## Features

* **Multi-Agent Architecture:** A `healthcare_orchestrator` agent coordinates specialized agents for patient data, medication inventory, PBM claims, and web search.
* **Conversational Analytics:** Converts natural language questions into SQL queries to be executed on BigQuery.
* **Deployable to Agent Engine:** Includes a notebook for deploying the agent to Google Cloud's Agent Engine.

## Project Structure

```
adk-data-analytics-ge/
├───.env.example
├───.gitignore
├───deploy.ipynb
├───expose_to_agentspace.sh
├───pyproject.toml
├───README.md
├───setup.sh
├───scripts/
│   ├───create_bq_agent.py
│   ├───enable_services.sh
│   └───list_agents.py
└───src/
    ├───agents/
    │   ├───agent.py
    │   ├───medication_data_agent.py
    │   ├───patient_data_agent.py
    │   └───pbm_data_agent.py
    └───data/
        ├───medication_inventory/
        ├───patient_records/
        └───pbm_claims/
```

## Prerequisites

*   Python 3.12+
*   `uv` package manager (`pip install uv`)
*   Google Cloud SDK (`gcloud`) authenticated:
    ```bash
    gcloud auth application-default login
    ```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd adk-data-analytics-ge
    ```

2.  **Set up the environment and install dependencies:**
    ```bash
    ./setup.sh
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Configure the project:**
   * Edit `src/agents/config_project.py`:
     * Set `PROJECT_ID` to your GCP project
     * Configure CA agent IDs
     * Set BigQuery dataset references

   * Update CA agent configurations:
     * `src/data/patient_records/system_instructions.yaml`
     * `src/data/patient_records/bigquery_data_context.json`
     * Similar for medication inventory and pbm_claims

5. **Create CA DataAgents (One-time Setup):**

   ```bash
   python -m src.ca_api_helper
   ```

   This creates the CA agents in Google Cloud.

## Running the Agent Locally

After activating the virtual environment, you can run the agent locally using the ADK web server:

```bash
cd src/
adk web
```

This will start a local web server where you can interact with your agent.

## Deploying to Agent Engine

The `deploy.ipynb` notebook contains the code and instructions to deploy this agent to Google Cloud's Agent Engine. Open and run the notebook to deploy your agent.

Then, follow [this code](https://github.com/sokart/adk-agentengine-agentspace/blob/main/expose_to_agentspace.sh) to register the deployed agent in your Gemini Enterprise app.

## Agent Architecture

This project uses a multi-agent architecture orchestrated by a root agent.

*   **`healthcare_orchestrator` (Root Agent):** This is the main agent that receives user queries. It uses a planner to decide which specialized agent is best suited to handle the query.

*   **Specialized Agents (Tools):** The orchestrator uses the following agents as tools:
    *   **`patient_encounters_agent`**: Handles queries related to patient data.
    *   **`medication_inventory_agent`**: Handles queries about medication inventory.
    *   **`pbm_agent`**: Handles queries related to Pharmacy Benefit Manager (PBM) claims.
    *   **`google_search_agent`**: Handles general queries by searching the web.

Each specialized agent is responsible for a specific domain, making the system modular and extensible.

## Interacting with the Agent

1. Open the web UI in your browser (if you're running via adk web) - or through the Gemini Enterprise app
2. Type natural language questions about your healthcare data:
   * "How many patients have diabetes?"
   * "What is the total medication inventory across all locations?"
   * "Show me the most common diagnoses in the last month"
   * "Which pharmacies have aspirin in stock?"
   * "What is the number of approved versus rejected claims for each insurance plan?"
3. The agent will:
   * Route your query to the appropriate specialized agent
   * Convert your question to SQL
   * Query BigQuery
   * Return results in natural language with metadata
