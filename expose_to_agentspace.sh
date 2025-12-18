### https://github.com/sokart/adk-agentengine-agentspace/blob/main/expose_to_agentspace.sh

export PROJECT_ID="project-agentspace-468314"  # String "hcls-agentspace" "project-agentspace-468314"
export PROJECT_NUMBER="7086336715" # String "404421411065" "7086336715"

export REASONING_ENGINE_ID="7425602355720093696" # String - Normally a 18-digit number
export REASONING_ENGINE_LOCATION="us-central1" # String - e.g. us-central1
export REASONING_ENGINE="projects/${PROJECT_ID}/locations/${REASONING_ENGINE_LOCATION}/reasoningEngines/${REASONING_ENGINE_ID}"

export AS_APP="argolis-demo-agent_1754925446094" # String - Find it in Google Cloud AI Applications "agentspace-all_1754522005743" "argolis-demo-agent_1754925446094"
export AS_LOCATION="global" # String - e.g. global, eu, us

export AGENT_DISPLAY_NAME="Data agent for NL2SQL" # String - this will appear as the name of the agent into your AgentSpace
AGENT_DESCRIPTION=$(cat <<EOF
This agent can be used to answer natural language questions about healthcare data stored in BigQuery.
EOF
)
export AGENT_DESCRIPTION
export TOOL_DESCRIPTION="You are a helpful assistant for NL2SQL."

DISCOVERY_ENGINE_PROD_API_ENDPOINT="https://discoveryengine.googleapis.com"


deploy_agent_to_agentspace_no_auth() {
    curl -X POST \
        -H "Authorization: Bearer $(gcloud auth print-access-token)" \
        -H "Content-Type: application/json" \
        -H "x-goog-user-project: ${PROJECT_ID}" \
        ${DISCOVERY_ENGINE_PROD_API_ENDPOINT}/v1alpha/projects/${PROJECT_ID}/locations/${AS_LOCATION}/collections/default_collection/engines/${AS_APP}/assistants/default_assistant/agents \
        -d '{
      "displayName": "'"${AGENT_DISPLAY_NAME}"'",
      "description": "'"${AGENT_DESCRIPTION}"'",
      "adk_agent_definition": {
        "tool_settings": {
          "toolDescription": "'"${TOOL_DESCRIPTION}"'",
        },
        "provisioned_reasoning_engine": {
          "reasoningEngine": "'"${REASONING_ENGINE}"'"
        },
      }
    }'
}


list_agents() { curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-H "X-Goog-User-Project: ${PROJECT_ID}" \
${DISCOVERY_ENGINE_PROD_API_ENDPOINT}/v1alpha/projects/${PROJECT_ID}/locations/${AS_LOCATION}/collections/default_collection/engines/${AS_APP}/assistants/default_assistant/agents
}

view_agent(){
curl -X GET \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-H "X-Goog-User-Project: ${PROJECT_ID}" \
"https://us-central1-aiplatform.googleapis.com/v1/${REASONING_ENGINE}"
}

delete_agent(){
  curl -X DELETE \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: ${PROJECT_ID}" \
  "https://discoveryengine.googleapis.com/v1alpha/projects/7086336715/locations/global/collections/default_collection/engines/argolis-demo-agent_1754925446094/assistants/default_assistant/agents/891660986716419186"
}


#delete_agent
deploy_agent_to_agentspace_no_auth
#list_agents
#view_agent


# For deleting
#"https://discoveryengine.googleapis.com/v1alpha/projects/7086336715/locations/global/collections/default_collection/engines/argolis-demo-agent_1754925446094/assistants/default_assistant/agents/5402614137179030513"
#"https://discoveryengine.googleapis.com/v1alpha/projects/404421411065/locations/global/collections/default_collection/engines/agentspace-all_1754522005743/assistants/default_assistant/agents/9429628436473679921"

