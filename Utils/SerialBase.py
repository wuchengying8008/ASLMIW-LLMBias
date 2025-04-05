import pickle
import base64
import json
import DeepSeekAPI
import NLPConstant
import ESUtil
from ESUtil import get_elasticsearch_client, index_document, search_elasticsearch, get_document

def textSerial(data, fieldsToExclude):
    try:
        result_parts = []

        def is_empty_value(value):
            return value is None or (isinstance(value, (list, dict)) and not value)

        def process_value(value):
            if isinstance(value, dict):
                sub_parts = []
                for sub_key, sub_value in value.items():
                    if sub_key not in fieldsToExclude and not is_empty_value(sub_value):
                        sub_parts.append(f"{sub_key}: {process_value(sub_value)}")
                return ", ".join(sub_parts).rstrip() + ";" if sub_parts else ""
            elif isinstance(value, list):
                list_parts = []
                for item in value:
                    if not is_empty_value(item):
                        part = process_value(item).rstrip(';,')
                        if part:
                            list_parts.append(part)
                return "; ".join(list_parts).rstrip(';')
            return str(value)

        for key, value in data.items():
            if key not in fieldsToExclude and not is_empty_value(value):
                result_parts.append(f"{key}: {process_value(value)}")

        result = "; ".join(result_parts).rstrip(',;') + "。"
        print(result)
        return result
    except Exception as e:
        print(f"Error Message: {e}")
        return None

# textSerial(json_str,fieldsToExclude)
