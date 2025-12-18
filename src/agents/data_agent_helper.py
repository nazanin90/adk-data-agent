'''
File: data_agent_helper.py
Project: adk-data-analytics
File Created: Saturday, 8th November 2025 8:32:11 pm
Author: Dinesh Selvaraj (dineshselva@google.com)
-------------------------------------------------------------
Last Modified: Saturday, 8th November 2025 8:33:31 pm
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

import pandas as pd
import proto
from google.protobuf.json_format import MessageToDict

from .utils_google_logging import get_logger

logger = get_logger(__name__)


def handle_text_response(resp):
    return {"text": "".join(resp.parts)}

def handle_schema_response(resp):
    if 'query' in resp:
        return {"query": resp.query.question}
    elif 'result' in resp:
        datasources = []
        for datasource in resp.result.datasources:
            if 'studio_datasource_id' in datasource:
                source_name = datasource.studio_datasource_id
            elif 'looker_explore_reference' in datasource:
                source_name = f"lookmlModel: {datasource.looker_explore_reference.lookml_model}, explore: {datasource.looker_explore_reference.explore}"
            else:
                source_name = f"{datasource.bigquery_table_reference.project_id}.{datasource.bigquery_table_reference.dataset_id}.{datasource.bigquery_table_reference.table_id}"
            datasources.append(source_name)
        return {"schema_resolved": {"datasources": datasources}}
    return {}

def handle_data_response(resp):
    if 'query' in resp:
        query = resp.query
        datasources = []
        for datasource in query.datasources:
            if 'studio_datasource_id' in datasource:
                source_name = datasource.studio_datasource_id
            elif 'looker_explore_reference' in datasource:
                source_name = f"lookmlModel: {datasource.looker_explore_reference.lookml_model}, explore: {datasource.looker_explore_reference.explore}"
            else:
                source_name = f"{datasource.bigquery_table_reference.project_id}.{datasource.bigquery_table_reference.dataset_id}.{datasource.bigquery_table_reference.table_id}"
            datasources.append(source_name)
        return {
            "retrieval_query": {
                "query_name": query.name,
                "question": query.question,
                "datasources": datasources,
            }
        }
    elif 'generated_sql' in resp:
        return {"sql_generated": resp.generated_sql}
    elif 'result' in resp:
        fields = [field.name for field in resp.result.schema.fields]
        d = {}
        for el in resp.result.data:
            for field in fields:
                if field in d:
                    d[field].append(el[field])
                else:
                    d[field] = [el[field]]
        return {"data_retrieved": pd.DataFrame(d).to_dict()}
    return {}

def handle_chart_response(resp):
    def _value_to_dict(v):
        if isinstance(v, proto.marshal.collections.maps.MapComposite):
            return _map_to_dict(v)
        elif isinstance(v, proto.marshal.collections.RepeatedComposite):
            return [_value_to_dict(el) for el in v]
        elif isinstance(v, (int, float, str, bool)):
            return v
        else:
            return MessageToDict(v)

    def _map_to_dict(d):
        out = {}
        for k in d:
            if isinstance(d[k], proto.marshal.collections.maps.MapComposite):
                out[k] = _map_to_dict(d[k])
            else:
                out[k] = _value_to_dict(d[k])
        return out

    if 'query' in resp:
        return {"chart_query": resp.query.instructions}
    elif 'result' in resp:
        vegaConfig = resp.result.vega_config
        vegaConfig_dict = _map_to_dict(vegaConfig)
        return {"chart_result": vegaConfig_dict}
    return {}

def show_message(msg):
    m = msg.system_message
    if 'text' in m:
        return handle_text_response(m.text)
    elif 'schema' in m:
        return handle_schema_response(m.schema)
    elif 'data' in m:
        return handle_data_response(m.data)
    elif 'chart' in m:
        return handle_chart_response(m.chart)
    return {}
