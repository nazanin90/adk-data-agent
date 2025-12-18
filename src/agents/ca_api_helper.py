'''
File: ca_api_helper.py
Project: adk-data-analytics
File Created: Thursday, 18th September 2025 5:02:12 pm
Author: Dinesh Selvaraj (dineshselva@google.com)
-------------------------------------------------------------
Last Modified: Friday, 7th November 2025 6:20:26 am
Modified By: Dinesh Selvaraj (dineshselva@google.com>)
-------------------------------------------------------------
Copyright 2025 Google LLC. This software is provided as-is, without
warranty or representation for any use or purpose. Your use of it is
subject to your agreement with Google.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import json
from pathlib import Path

import yaml
from google.cloud import geminidataanalytics
from google.protobuf import field_mask_pb2

from . import config_project
from .utils_google_logging import get_logger

logger = get_logger(__name__)

conversation_messages = []

def create_bigquery_ca_data_agent(data_agent_id: str) -> geminidataanalytics.DataAgent:
    """Creates a BigQuery Data Analytics Agent.

    Args:
        data_agent_id: The Data Agent ID.

    Returns:
        A DataAgent object.
    """
    project_id = config_project.PROJECT_ID
    logger.info("Creating Data Analytics Agent...")
    data_agent_client = geminidataanalytics.DataAgentServiceClient()
    logger.info("DataAgentServiceClient created.")

    script_dir = Path(__file__).parent

    config_dir_name = config_project.AGENT_ID_TO_CONFIG_DIR.get(data_agent_id)
    if not config_dir_name:
        raise ValueError(f"No config directory found for agent ID: {data_agent_id}")

    # Load system instruction from data_agent_metadata.yaml
    metadata_file_path = script_dir.parent / 'data' / config_dir_name / 'system_instructions.yaml'
    with open(metadata_file_path) as file:
        metadata_config = yaml.safe_load(file)
    system_instruction = yaml.dump(metadata_config)
    logger.info("Loaded system instruction from metadata.")

    # Load BigQuery table context from bigquery_data_context.json
    bq_context_file_path = script_dir.parent / 'data' / config_dir_name / 'bigquery_data_context.json'
    with open(bq_context_file_path) as file:
        bq_context_config = json.load(file)
    logger.info("Loaded BigQuery table context.")

    table_references = []
    for table_item in bq_context_config["tables"]:
        fields = []
        if "fields" in table_item:
            for field_item in table_item["fields"]:
                fields.append(geminidataanalytics.Field(
                    name=field_item["name"],
                    description=field_item["description"]
                ))

        schema = geminidataanalytics.Schema(
            description=table_item.get("description", ""),
            synonyms=table_item.get("synonyms", []),
            tags=table_item.get("tags", []),
            fields=fields
        )

        bqr = geminidataanalytics.BigQueryTableReference(
            project_id=table_item["project_id"],
            dataset_id=table_item["dataset_id"],
            table_id=table_item["table_id"],
            schema=schema
        )
        table_references.append(bqr)
    logger.info("Created BigQuery table references with schema.")

    datasource_references = geminidataanalytics.DatasourceReferences(
        bq=geminidataanalytics.BigQueryTableReferences(
            table_references=table_references
        )
    )
    logger.info("Created datasource references.")

    example_queries = []
    if "example_queries" in bq_context_config:
        for query_item in bq_context_config["example_queries"]:
            example_queries.append(geminidataanalytics.ExampleQuery(
                natural_language_question=query_item["natural_language_question"],
                sql_query=query_item["sql_query"]
            ))
    logger.info("Created example queries.")

    published_context = geminidataanalytics.Context(
        system_instruction=system_instruction,
        datasource_references=datasource_references,
        example_queries=example_queries,
        options=geminidataanalytics.ConversationOptions(
            analysis=geminidataanalytics.AnalysisOptions(
                python=geminidataanalytics.AnalysisOptions.Python(
                    enabled=True
                )
            )
        )
    )
    logger.info("Created published context.")

    data_agent = geminidataanalytics.DataAgent(
        data_analytics_agent=geminidataanalytics.DataAnalyticsAgent(
            published_context=published_context
        )
    )
    data_agent.name = f"projects/{project_id}/locations/global/dataAgents/{data_agent_id}"
    logger.info("Created data agent.")

    request = geminidataanalytics.CreateDataAgentRequest(
        parent=f"projects/{project_id}/locations/global",
        data_agent_id=data_agent_id,
        data_agent=data_agent,
    )
    logger.info("Creating data agent request.")

    operation = data_agent_client.create_data_agent(request=request)
    logger.info("Waiting for Data Analytics Agent creation to complete...")
    response = operation.result()
    logger.info(f"Data Analytics Agent created with name: {response.name}")
    return response


def get_data_agent(data_agent_id: str) -> geminidataanalytics.DataAgent:
    """Gets a Data Analytics Agent.

    Args:
        data_agent_id: The Data Agent ID.

    Returns:
        A DataAgent object.
    """
    project_id = config_project.PROJECT_ID
    logger.info(f"Getting Data Analytics Agent: {data_agent_id}")
    data_agent_client = geminidataanalytics.DataAgentServiceClient()
    request = geminidataanalytics.GetDataAgentRequest(
        name=f"projects/{project_id}/locations/global/dataAgents/{data_agent_id}",
    )
    response = data_agent_client.get_data_agent(request=request)
    logger.info(f"Successfully retrieved Data Analytics Agent: {response}")
    return response

def list_data_agents():
    """Lists all Data Analytics Agents in a project."""
    project_id = config_project.PROJECT_ID
    logger.info(f"Listing all Data Analytics Agents for project: {project_id}")
    data_agent_client = geminidataanalytics.DataAgentServiceClient()
    request = geminidataanalytics.ListDataAgentsRequest(
        parent=f"projects/{project_id}/locations/global",
    )
    page_result = data_agent_client.list_data_agents(request=request)
    for response in page_result:
        logger.info(f"Found Data Agent: {response.name}")
    return page_result

def delete_data_agent(data_agent_id: str):
    """Deletes a Data Analytics Agent.

    Args:
        data_agent_id: The Data Agent ID.
    """
    project_id = config_project.PROJECT_ID
    logger.info(f"Deleting Data Analytics Agent: {data_agent_id}")
    data_agent_client = geminidataanalytics.DataAgentServiceClient()
    request = geminidataanalytics.DeleteDataAgentRequest(
        name=f"projects/{project_id}/locations/global/dataAgents/{data_agent_id}",
    )
    try:
        data_agent_client.delete_data_agent(request=request)
        logger.info("Data Agent Deleted")
    except Exception as e:
        logger.error(f"Error deleting Data Agent: {e}")


def update_data_agent(
    data_agent_id: str,
    display_name: str | None = None,
    description: str | None = None,
    system_instruction: str | None = None,
) -> None:
    """Updates a Data Analytics Agent.

    Args:
        data_agent_id: The Data Agent ID.
        display_name: The new display name for the agent.
        description: The new description for the agent.
        system_instruction: The new system instruction for the agent.
    """
    project_id = config_project.PROJECT_ID
    logger.info(f"Updating Data Analytics Agent: {data_agent_id}")
    data_agent_client = geminidataanalytics.DataAgentServiceClient()

    data_agent = geminidataanalytics.DataAgent()
    data_agent.name = (
        f"projects/{project_id}/locations/global/dataAgents/{data_agent_id}"
    )

    update_mask_paths = []

    if display_name:
        data_agent.display_name = display_name
        update_mask_paths.append("display_name")

    if description:
        data_agent.description = description
        update_mask_paths.append("description")

    if system_instruction:
        current_agent = get_data_agent(data_agent_id)
        current_published_context = current_agent.data_analytics_agent.published_context

        # Create a new context with the updated system instruction
        new_published_context = geminidataanalytics.Context(
            system_instruction=system_instruction,
            datasource_references=current_published_context.datasource_references,
            example_queries=current_published_context.example_queries,
            options=current_published_context.options,
        )

        data_agent.data_analytics_agent.published_context = new_published_context
        update_mask_paths.append("data_analytics_agent.published_context")

    if not update_mask_paths:
        logger.warning("No fields provided to update.")
        return

    update_mask = field_mask_pb2.FieldMask(paths=update_mask_paths)

    request = geminidataanalytics.UpdateDataAgentRequest(
        data_agent=data_agent,
        update_mask=update_mask,
    )

    try:
        data_agent_client.update_data_agent(request=request)
        logger.info(f"Data Agent {data_agent_id} updated successfully.")
    except Exception as e:
        logger.error(f"Error updating Data Agent {data_agent_id}: {e}")
        raise


if __name__ == "__main__":
    
    bigquery_data_agent_id = config_project.PATIENT_ANALYTICS_AGENT_ID

    agent = create_bigquery_ca_data_agent(bigquery_data_agent_id)
    logger.info(f"Created BigQuery Data Agent: {agent.name}")

    bigquery_data_agent_id = config_project.MEDICATION_INVENTORY_AGENT_ID

    agent = create_bigquery_ca_data_agent(bigquery_data_agent_id)
    logger.info(f"Created BigQuery Data Agent: {agent.name}")

    bigquery_data_agent_id = config_project.PBM_CLAIMS_AGENT_ID

    agent = create_bigquery_ca_data_agent(bigquery_data_agent_id)
    logger.info(f"Created BigQuery Data Agent: {agent.name}")


    #agent = get_data_agent(bigquery_data_agent_id)
    #print(f"Retrieved Data Agent: {agent.name}")

    list_data_agents()

    #get_data_agent(looker_data_agent_id)

    #delete_data_agent("patient_encounters-agent-6")

    # script_dir = Path(__file__).parent
    # metadata_file_path = script_dir.parent / 'data' / 'patient_records' / 'system_instructions.yaml'
    # with open(metadata_file_path) as file:
    #     metadata_config = yaml.safe_load(file)
    # system_instruction = yaml.dump(metadata_config)
    # logger.info("Loaded system instruction from metadata.")

    # update_data_agent(
    #     data_agent_id=bigquery_data_agent_id,
    #     system_instruction=system_instruction
    # )
