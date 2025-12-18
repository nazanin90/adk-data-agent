'''
File: callback.py
Project: adk-data-analytics
File Created: Monday, 10th November 2025 8:37:31 am
Author: Dinesh Selvaraj (dineshselva@google.com)
-------------------------------------------------------------
Last Modified: Monday, 15th December 2025 4:10:00 pm
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
from typing import Any

import google.genai.types as types
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from .utils_google_logging import get_logger

logger = get_logger(__name__)


# ============================================================================
# PATIENT AGENT CALLBACKS
# ============================================================================

def check_before_agent(callback_context: CallbackContext) -> types.Content | None:
    """
    Logs entry and checks 'skip_llm_agent' in session state.
    If True, returns Content to skip the agent's execution.
    If False or not present, returns None to allow execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id

    logger.info(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    logger.info("[Callback] Current State")

    return None


def after_patient_agent_callback(callback_context: CallbackContext) -> types.Content | None:
    """
    This callback restructures the agent's output to include both the summary
    and the detailed tool response.

    For A2A transmission, embeds structured data as JSON in the text output.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logger.info(f"[Callback] Exiting agent: {agent_name} (Invocation: {invocation_id})")

    state = callback_context.state

    # Get the agent's text output
    agent_text_output = state.get('patient_agent_output', '')

    # Get the detailed tool response as a list of dicts
    tool_response_list = state.get('patient_data_agent_tool_response', [])

    # Merge the list of dicts into a single dict for better frontend display
    # Each dict has a single key (query, schema_resolved, sql_generated, etc.)
    # Merge them into one object: {query: "...", schema_resolved: {...}, ...}
    merged_tool_response = {}
    for item in tool_response_list:
        if isinstance(item, dict):
            merged_tool_response.update(item)

    # Wrap in a list to match JsonResponseFormatter expected format
    tool_response = [merged_tool_response] if merged_tool_response else []

    # Restructure agent_output to include both
    state['patient_agent_output'] = {
        'summary': agent_text_output,
        'tool_response': tool_response
    }

    # For A2A: Return structured data as plain JSON (no delimiters)
    # The orchestrator will parse this JSON directly
    structured_data = {
        'summary': agent_text_output,
        'tool_response': tool_response
    }

    # Return plain JSON as Content for A2A transmission
    return types.Content(parts=[types.Part(text=json.dumps(structured_data))])


def check_before_tool_patient(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> dict | None:
    """Inspects/modifies tool args or skips the tool call."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    logger.info(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    logger.info(f"[Callback] Original args: {args}")

    # Generate or retrieve a conversation ID if needed
    patient_data_agent_conversation_id = tool_context.state.get('patient_data_agent_conversation_id')
    if patient_data_agent_conversation_id:
        logger.info(f"[Callback] Using existing conversation ID: {patient_data_agent_conversation_id}")
    else:
        import uuid
        unique_conversation_id = str(uuid.uuid4())
        logger.info(f"[Callback] Generating new conversation ID : {unique_conversation_id}")
        tool_context.state['patient_data_agent_conversation_id'] = unique_conversation_id

    logger.info("[Callback] Proceeding with original or previously modified args.")
    return None


# ============================================================================
# MEDICATION AGENT CALLBACKS
# ============================================================================

def after_medication_agent_callback(callback_context: CallbackContext) -> types.Content | None:
    """
    This callback restructures the agent's output to include both the summary
    and the detailed tool response.

    For A2A transmission, embeds structured data as JSON in the text output.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logger.info(f"[Callback] Exiting agent: {agent_name} (Invocation: {invocation_id})")

    state = callback_context.state

    # Get the agent's text output (using the correct output_key)
    agent_text_output = state.get('medication_agent_output', '')

    # Get the detailed tool response as a list of dicts
    tool_response_list = state.get('medication_data_agent_tool_response', [])

    # Merge the list of dicts into a single dict for better frontend display
    # Each dict has a single key (query, schema_resolved, sql_generated, etc.)
    # Merge them into one object: {query: "...", schema_resolved: {...}, ...}
    merged_tool_response = {}
    for item in tool_response_list:
        if isinstance(item, dict):
            merged_tool_response.update(item)

    # Wrap in a list to match JsonResponseFormatter expected format
    tool_response = [merged_tool_response] if merged_tool_response else []

    # Restructure medication_agent_output to include both
    state['medication_agent_output'] = {
        'summary': agent_text_output,
        'tool_response': tool_response
    }

    # For A2A: Return structured data as plain JSON (no delimiters)
    # The orchestrator will parse this JSON directly
    structured_data = {
        'summary': agent_text_output,
        'tool_response': tool_response
    }

    # Return plain JSON as Content for A2A transmission
    return types.Content(parts=[types.Part(text=json.dumps(structured_data))])


def check_before_tool_medication(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> dict | None:
    """Inspects/modifies tool args or skips the tool call."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    logger.info(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    logger.info(f"[Callback] Original args: {args}")

    # Generate or retrieve a conversation ID if needed
    medication_data_agent_conversation_id = tool_context.state.get('medication_data_agent_conversation_id')
    if medication_data_agent_conversation_id:
        logger.info(f"[Callback] Using existing conversation ID: {medication_data_agent_conversation_id}")
    else:
        import uuid
        unique_conversation_id = str(uuid.uuid4())
        logger.info(f"[Callback] Generating new conversation ID : {unique_conversation_id}")
        tool_context.state['medication_data_agent_conversation_id'] = unique_conversation_id

    logger.info("[Callback] Proceeding with original or previously modified args.")
    return None


# ============================================================================
# PBM AGENT CALLBACKS (NEW)
# ============================================================================

def after_pbm_agent_callback(callback_context: CallbackContext) -> types.Content | None:
    """
    This callback restructures the PBM agent's output to include both the summary
    and the detailed tool response.

    For A2A transmission, embeds structured data as JSON in the text output.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    logger.info(f"[Callback] Exiting agent: {agent_name} (Invocation: {invocation_id})")

    state = callback_context.state

    # Get the agent's text output (using the correct output_key)
    agent_text_output = state.get('pbm_agent_output', '')

    # Get the detailed tool response as a list of dicts
    tool_response_list = state.get('pbm_data_agent_tool_response', [])

    # Merge the list of dicts into a single dict for better frontend display
    merged_tool_response = {}
    for item in tool_response_list:
        if isinstance(item, dict):
            merged_tool_response.update(item)

    # Wrap in a list to match JsonResponseFormatter expected format
    tool_response = [merged_tool_response] if merged_tool_response else []

    # Restructure pbm_agent_output to include both
    state['pbm_agent_output'] = {
        'summary': agent_text_output,
        'tool_response': tool_response
    }

    # For A2A: Return structured data as plain JSON (no delimiters)
    structured_data = {
        'summary': agent_text_output,
        'tool_response': tool_response
    }

    # Return plain JSON as Content for A2A transmission
    return types.Content(parts=[types.Part(text=json.dumps(structured_data))])


def check_before_tool_pbm(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> dict | None:
    """Inspects/modifies tool args or skips the tool call for the PBM agent."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    logger.info(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    logger.info(f"[Callback] Original args: {args}")

    # Generate or retrieve a conversation ID if needed
    pbm_data_agent_conversation_id = tool_context.state.get('pbm_data_agent_conversation_id')
    if pbm_data_agent_conversation_id:
        logger.info(f"[Callback] Using existing conversation ID: {pbm_data_agent_conversation_id}")
    else:
        import uuid
        unique_conversation_id = str(uuid.uuid4())
        logger.info(f"[Callback] Generating new conversation ID : {unique_conversation_id}")
        tool_context.state['pbm_data_agent_conversation_id'] = unique_conversation_id

    logger.info("[Callback] Proceeding with original or previously modified args.")
    return None


# ============================================================================
# COMMON AGENT CALLBACKS
# ============================================================================

def check_after_tool(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict) -> types.Content | None:
    """Common after tool callback for logging tool execution."""
    agent_name = tool_context.agent_name
    logger.info(f'[Callback] after_tool_callback for agent: {agent_name}')
    logger.info(f"[Callback] ✅ Tool {tool.name} finished.")
    logger.info(f"[Callback] Tool args: {args}")
    logger.info(f"[Callback] Tool response - {tool_response}")

    # Return None to use the tool's response as is.
    return None


# ============================================================================
# ORCHESTRATOR CALLBACKS
# ============================================================================

def before_agent_callback(callback_context: CallbackContext) -> types.Content | None:
    """
    Callback executed before the agent processes a new user message.

    Clears the tool_calls and tool_responses lists to ensure each turn starts fresh.
    """
    state = callback_context.state

    # Clear tool_calls and tool_responses from previous turn
    if 'tool_calls' in state:
        logger.info("[A2A Orchestrator] Clearing tool_calls from previous turn")
        state['tool_calls'] = []

    if 'tool_responses' in state:
        logger.info("[A2A Orchestrator] Clearing tool_responses from previous turn")
        state['tool_responses'] = []

    return None


def before_tool_callback(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> dict | None:
    """
    Callback executed before each tool call.

    Logs which A2A agent is about to be invoked with what input.
    """
    tool_name = tool.name
    agent_name = tool_context.agent_name

    logger.info(f"[A2A Orchestrator] Agent '{agent_name}' calling tool: {tool_name}")
    logger.info(f"[A2A Orchestrator] Tool input: {args}")

    # Store tool call info in state for later reference
    state = tool_context.state
    if 'tool_calls' not in state:
        state['tool_calls'] = []

    state['tool_calls'].append({
        'tool_name': tool_name,
        'input': str(args)
    })

    # Return None to proceed with tool execution
    return None


def after_tool_callback(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict
) -> dict | None:
    """
    Callback executed after each tool call.

    Logs the response from the A2A agent and captures detailed tool responses.
    Parses JSON directly from A2A string responses (no delimiters).
    """
    tool_name = tool.name
    agent_name = tool_context.agent_name

    logger.info(f"[A2A Orchestrator] Tool '{tool_name}' in agent '{agent_name}' completed")
    logger.info(f"[A2A Orchestrator] Tool response type: {type(tool_response)}")
    logger.info(f"[A2A Orchestrator] Tool response: {tool_response}")


    # Parse structured data from A2A responses
    structured_response = None

    if isinstance(tool_response, str):
        # Try parsing as direct JSON (no delimiters)
        try:
            structured_response = json.loads(tool_response)
            logger.info(f"[A2A Orchestrator] Parsed JSON string from {tool_name}")
            logger.info(f"[A2A Orchestrator] Structured data has tool_response with {len(structured_response.get('tool_response', []))} items")
        except json.JSONDecodeError as e:
            logger.warning(f"[A2A Orchestrator] tool_response is not valid JSON from {tool_name}: {e}")
            # Fallback: treat as plain text (for google_search_agent or other text-only tools)
            structured_response = {'text': tool_response}
            logger.info("[A2A Orchestrator] Treating response as plain text")
    elif isinstance(tool_response, dict):
        logger.info(f"[A2A Orchestrator] Tool response is already a dict (keys: {list(tool_response.keys())})")
        structured_response = tool_response

    # Store the extracted structured data
    state = tool_context.state
    if 'tool_responses' not in state:
        state['tool_responses'] = []

    # Store the structured response (or the original if extraction failed)
    state['tool_responses'].append({
        'tool_name': tool_name,
        'response': structured_response if structured_response else tool_response
    })

    # Return None to use original tool response
    return None


def after_orchestrator_callback(callback_context: CallbackContext) -> types.Content | None:
    """
    Callback to structure the orchestrator's output for the frontend.

    When the orchestrator calls A2A agent tools, this captures their response
    and structures it in a format compatible with the frontend.
    """
    state = callback_context.state
    agent_text_output = state.get('agent_output', '')

    # Get tool calls and responses
    tool_calls = state.get('tool_calls', [])
    tool_responses = state.get('tool_responses', [])

    logger.info(f"[A2A Orchestrator] Processing {len(tool_calls)} tool calls and {len(tool_responses)} responses")

    # Agent metadata for better frontend display (generic, extensible)
    agent_metadata = {
        'patient_data_agent': {
            'display_name': 'Patient Clinical Data',
            'icon': 'medical_services',
            'color': 'blue',
            'description': 'Patient encounters, diagnoses, medications, and vitals',
            'type': 'agent'  # A2A agent
        },
        'medication_inventory_agent': {
            'display_name': 'Medication Inventory',
            'icon': 'medication',
            'color': 'green',
            'description': 'Pharmacy stock levels and availability',
            'type': 'agent'  # A2A agent
        },
        # ADDED PBM METADATA HERE
        'pbm_data_agent': {
            'display_name': 'PBM Claims',
            'icon': 'payments',
            'color': 'purple',
            'description': 'Insurance claims, copays, and coverage',
            'type': 'agent'  # A2A agent
        },
        'google_search_agent': {
            'display_name': 'Google Search',
            'icon': 'search',
            'color': 'grey',
            'description': 'Web search for healthcare information',
            'type': 'tool'  # Built-in tool
        }
    }

    # Pair each tool call with its response for grouped display
    grouped_tool_results = []

    for tool_call in tool_calls:
        tool_name = tool_call['tool_name']
        tool_input = tool_call['input']

        # Find corresponding response by matching tool_name (not by index)
        tool_response = None
        for resp in tool_responses:
            if resp.get('tool_name') == tool_name:
                tool_response = resp
                break

        if not tool_response:
            logger.warning(f"[A2A Orchestrator] No matching tool response found for {tool_name}")
            continue

        response_data = tool_response.get('response', {})

        # Special handling for google_search_agent - it returns a string response, not structured data
        if tool_name == 'google_search_agent' and isinstance(response_data, str):
            logger.info(f"[A2A Orchestrator] google_search_agent string response detected (length: {len(response_data)})")
            merged_data = {'text': response_data}  # Store the structured markdown text
        # Extract tool_response list from structured response
        elif isinstance(response_data, dict) and 'tool_response' in response_data:
            tool_data_list = response_data.get('tool_response', [])
            logger.info(f"[A2A Orchestrator] tool_data_list has {len(tool_data_list)} items")
            # Merge list items into single dict
            merged_data = {}
            for item in tool_data_list:
                if isinstance(item, dict):
                    merged_data.update(item)
            logger.info(f"[A2A Orchestrator] merged_data keys: {list(merged_data.keys())}")
        elif isinstance(response_data, list):
            # Merge list items
            merged_data = {}
            for item in response_data:
                if isinstance(item, dict):
                    merged_data.update(item)
            logger.info(f"[A2A Orchestrator] merged_data keys (from list): {list(merged_data.keys())}")
        elif isinstance(response_data, dict):
            merged_data = response_data
            logger.info(f"[A2A Orchestrator] merged_data keys (direct dict): {list(merged_data.keys())}")
        else:
            merged_data = {}
            logger.warning(f"[A2A Orchestrator] response_data is not a recognized type: {type(response_data)}")

        # Add tool metadata (generic fallback for unknown tools)
        metadata = agent_metadata.get(tool_name, {
            'display_name': tool_name.replace('_', ' ').title(),
            'icon': 'query_stats',
            'color': 'grey',
            'description': f'Results from {tool_name}',
            'type': 'tool'  # Default to tool for unknown agents/tools
        })

        # Create grouped result structure
        grouped_result = {
            'tool_name': tool_name,
            'tool_input': tool_input,
            'tool_metadata': metadata,
            **merged_data  # Spread all response data (query, schema, sql, data, text, etc.)
        }

        grouped_tool_results.append(grouped_result)
        logger.info(f"[A2A Orchestrator] Grouped result for {tool_name} with {len(merged_data)} data fields")

    # Extract grounding metadata if google_search_agent was called
    grounding_metadata = state.get('grounding_metadata')

    # Structure the output with the orchestrator's summary and grouped tool results
    state['agent_output'] = {
        'summary': agent_text_output,
        'tool_response': grouped_tool_results,
        'grounding_metadata': grounding_metadata  # Pass through grounding sources for citations
    }

    logger.info(
        f"[A2A Orchestrator] Structured orchestrator output - summary length: {len(str(agent_text_output))}, "
        f"grouped tools: {len(grouped_tool_results)}, has grounding: {grounding_metadata is not None}"
    )
    return None


def collect_search_sources_callback(callback_context: CallbackContext) -> types.Content | None:
    """Extracts grounding metadata from google_search results."""
    session = callback_context._invocation_context.session
    state = callback_context.state

    # DEBUG: Print the agent's output before processing
    logger.info("=" * 80)
    logger.info("[DEBUG] Google Search Agent Output (RAW)")
    logger.info("=" * 80)
    agent_output = state.get('agent_output', '')
    logger.info(f"[DEBUG] Agent output type: {type(agent_output)}")
    logger.info(f"[DEBUG] Agent output length: {len(str(agent_output)) if agent_output else 0}")
    logger.info(f"[DEBUG] Agent output:\n{agent_output}")
    logger.info("=" * 80)

    sources = []
    web_search_queries = []
    search_entry_point = None
    grounding_supports = []

    logger.info("[Orchestrator Callback] Collecting grounding metadata from session events")

    for event in session.events:
        if not event.grounding_metadata:
            continue

        # Extract web sources (grounding_chunks)
        if event.grounding_metadata.grounding_chunks:
            for chunk in event.grounding_metadata.grounding_chunks:
                if chunk.web:
                    sources.append({
                        'uri': chunk.web.uri,
                        'title': chunk.web.title,
                        'domain': chunk.web.domain
                    })

        # Extract grounding supports (segment-to-source mapping for inline citations)
        if event.grounding_metadata.grounding_supports:
            for support in event.grounding_metadata.grounding_supports:
                if support.segment:
                    grounding_supports.append({
                        'segment': {
                            'start_index': support.segment.start_index,
                            'end_index': support.segment.end_index,
                            'text': support.segment.text
                        },
                        'grounding_chunk_indices': list(support.grounding_chunk_indices) if support.grounding_chunk_indices else []
                    })

        # Extract search queries (compliance requirement)
        if event.grounding_metadata.web_search_queries:
            web_search_queries.extend(event.grounding_metadata.web_search_queries)

        # Extract search entry point (compliance requirement)
        if event.grounding_metadata.search_entry_point:
            search_entry_point = {
                'rendered_content': event.grounding_metadata.search_entry_point.rendered_content
            }

    if sources or web_search_queries or search_entry_point or grounding_supports:
        callback_context.state['grounding_metadata'] = {
            'sources': sources,
            'web_search_queries': list(set(web_search_queries)),  # Deduplicate
            'search_entry_point': search_entry_point,
            'grounding_supports': grounding_supports  # For inline citation markers
        }

    return None
