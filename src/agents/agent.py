'''
File: agent.py
Project: adk-fastapi-template
File Created: Tuesday, 16th September 2025 4:26:58 am
Author: Dinesh Selvaraj (dineshselva@google.com)
-------------------------------------------------------------
Last Modified: Monday, 10th November 2025 4:26:51 am
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
# from __future__ import annotations


from google.adk.agents import LlmAgent
from google.adk.planners.built_in_planner import BuiltInPlanner
from google.adk.tools import agent_tool, google_search

from .medication_data_agent import medication_data_agent_tool
from .patient_data_agent import patient_data_agent_tool
from .pbm_data_agent import pbm_data_agent_tool
from .utils_google_logging import get_logger

from . import callback, prompt, config_model

logger = get_logger(__name__)

# ============================================================================
# A2A SERVICE AGENTS (Patient & Medication)
# ============================================================================

patient_encounters_agent = LlmAgent(
    model=config_model.GEMINI_MODEL_TO_USE,
    #planner=BuiltInPlanner(thinking_config=config_model.GEMINI_THINKING_CONFIG),
    name='patient_encounters_agent',
    description=prompt.PATIENT_RECORDS_ANALYTICS_DESCRIPTION,
    instruction=prompt.PATIENT_RECORDS_ANALYTICS_INSTRUCTION,
    tools=[patient_data_agent_tool],
    output_key='patient_agent_output',
    # output_schema=CADataAnalyticsResponse,
    before_agent_callback=callback.check_before_agent,
    after_agent_callback=callback.after_patient_agent_callback,
    before_tool_callback=callback.check_before_tool_patient,
    after_tool_callback=callback.check_after_tool,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

medication_inventory_agent = LlmAgent(
    model=config_model.GEMINI_MODEL_TO_USE,
    #planner=BuiltInPlanner(thinking_config=config_model.GEMINI_THINKING_CONFIG),
    name='medication_inventory_agent',
    description=prompt.MEDICATION_INVENTORY_DESCRIPTION,
    instruction=prompt.MEDICATION_INVENTORY_INSTRUCTION,
    tools=[medication_data_agent_tool],
    output_key='medication_agent_output',
    # output_schema=CADataAnalyticsResponse,
    before_agent_callback=callback.check_before_agent,
    after_agent_callback=callback.after_medication_agent_callback,
    before_tool_callback=callback.check_before_tool_medication,
    after_tool_callback=callback.check_after_tool,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

pbm_agent = LlmAgent(
    model=config_model.GEMINI_MODEL_TO_USE,
    #planner=BuiltInPlanner(thinking_config=config_model.GEMINI_THINKING_CONFIG),
    name='pbm_agent',
    description=prompt.PBM_DESCRIPTION,
    instruction=prompt.PBM_INSTRUCTION,
    tools=[pbm_data_agent_tool],
    output_key='pbm_agent_output',
    # output_schema=CADataAnalyticsResponse,
    before_agent_callback=callback.check_before_agent,
    after_agent_callback=callback.after_pbm_agent_callback,
    before_tool_callback=callback.check_before_tool_pbm,
    after_tool_callback=callback.check_after_tool,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

# ============================================================================
# GOOGLE SEARCH AGENT
# ============================================================================

google_search_agent = LlmAgent(
    model=config_model.GEMINI_MODEL_TO_USE,
    name='google_search_agent',
    instruction=prompt.GOOGLE_SEARCH_AGENT_INSTRUCTION,
    tools=[google_search],
    after_agent_callback=callback.collect_search_sources_callback,
)

# ============================================================================
# HEALTHCARE ORCHESTRATOR AGENT
# ============================================================================

# Create agent tools for the orchestrator
search_agent = agent_tool.AgentTool(agent=google_search_agent)
patient_agent_tool = agent_tool.AgentTool(agent=patient_encounters_agent)
medication_agent_tool = agent_tool.AgentTool(agent=medication_inventory_agent)
pbm_agent_tool = agent_tool.AgentTool(agent=pbm_agent)

# Healthcare Orchestrator Agent
# This agent coordinates queries across patient and medication data systems
root_agent = LlmAgent(
    model=config_model.GEMINI_MODEL_TO_USE,
    #planner=BuiltInPlanner(thinking_config=config_model.GEMINI_THINKING_CONFIG),
    name="healthcare_orchestrator",
    description=prompt.HEALTHCARE_ORCHESTRATOR_DESCRIPTION,
    instruction=prompt.HEALTHCARE_ORCHESTRATOR_INSTRUCTION,
    tools=[patient_agent_tool, medication_agent_tool, search_agent, pbm_agent_tool],
    output_key="agent_output",
    before_agent_callback=callback.before_agent_callback,
    before_tool_callback=callback.before_tool_callback,
    after_tool_callback=callback.after_tool_callback,
    after_agent_callback=callback.after_orchestrator_callback,
)

