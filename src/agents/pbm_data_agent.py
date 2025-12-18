'''
File: pbm_data_agent.py
Project: adk-data-analytics
File Created: Sunday, 9th November 2025 3:07:43 am
Author: Dinesh Selvaraj (dineshselva@google.com)
-------------------------------------------------------------
Last Modified: Sunday, 9th November 2025 3:12:46 am
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

import uuid

from google.adk.tools import FunctionTool, ToolContext
from google.cloud import geminidataanalytics

from . import config_project
from .data_agent_helper import show_message
from .utils_google_logging import get_logger

logger = get_logger(__name__)

def stateful_chat_pbm_bq_data_agent(user_input: str, tool_context: ToolContext):
    """Gets results from a BigQuery Data Analytics Agent in a stateful manner.

    Args:
        user_input: The query for the agent.
        tool_context: The context of the tool.

    Returns:
        A dictionary with the agent's response.
    """
    project_id = config_project.PROJECT_ID
    agent_id = config_project.PBM_CLAIMS_AGENT_ID
    conversation_id = tool_context.state.get('pbm_data_agent_conversation_id')
    conversation_created = tool_context.state.get('pbm_data_agent_conversation_created', False)
    data_chat_client = geminidataanalytics.DataChatServiceClient()
    logger.info("DataChatServiceClient created.")

    # Create conversation if it doesn't exist or hasn't been created in backend yet
    if not conversation_id or not conversation_created:
        # Generate new ID if needed (may have been generated in callback but not created in backend)
        if not conversation_id:
            conversation_id = f"conv-{uuid.uuid4()}"
            logger.info(f"No conversation ID found, creating a new one: {conversation_id}")
        else:
            logger.info(f"Conversation ID exists ({conversation_id}) but not created in backend yet. Creating now...")

        conversation = geminidataanalytics.Conversation()
        conversation.agents = [f'projects/{project_id}/locations/global/dataAgents/{agent_id}']
        conversation.name = f"projects/{project_id}/locations/global/conversations/{conversation_id}"

        request = geminidataanalytics.CreateConversationRequest(
            parent=f"projects/{project_id}/locations/global",
            conversation_id=conversation_id,
            conversation=conversation,
        )
        data_chat_client.create_conversation(request=request)
        logger.info(f"Created new conversation in backend: {conversation_id}")
        if tool_context:
            tool_context.state['pbm_data_agent_conversation_id'] = conversation_id
            tool_context.state['pbm_data_agent_conversation_created'] = True
            logger.info("Updated tool context state with new conversation ID and created flag.")
    else:
        logger.info(f"Continuing existing conversation {conversation_id} for query: {user_input}")


    # Create a request that contains a single user message (the new question)
    messages = [geminidataanalytics.Message(
        user_message=geminidataanalytics.UserMessage(text=user_input)
    )]

    # Create a conversation_reference
    conversation_reference = geminidataanalytics.ConversationReference()
    conversation_reference.conversation = f"projects/{project_id}/locations/global/conversations/{conversation_id}"
    conversation_reference.data_agent_context.data_agent = f"projects/{project_id}/locations/global/dataAgents/{agent_id}"
    logger.info("Created conversation reference.")

    # Form the request
    request = geminidataanalytics.ChatRequest(
        parent=f"projects/{project_id}/locations/global",
        messages=messages,
        conversation_reference=conversation_reference
    )
    logger.info("Creating stateful chat request.")


    try:
        stream = data_chat_client.chat(request=request)
        logger.info("Request sent to chat API.")

        responses = []
        for response in stream:
            # In stateful chat, we don't need to manage the conversation history client-side.
            # logger.info(f"Received message: {response}")
            message = show_message(response)
            if message:
                responses.append(message)
        logger.info("Received response from chat API")

        if tool_context:
            tool_context.state['pbm_data_agent_tool_response'] = responses
            logger.info("Updated tool context state with agent response.")
        return responses
    except Exception as e:
        logger.error(f"Error getting response from Data Analytics Agent: {e}")
        return [{"status": "error", "error_message": str(e)}]


pbm_data_agent_tool = FunctionTool(func=stateful_chat_pbm_bq_data_agent)
