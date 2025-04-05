# -*- coding: utf-8 -*-
import requests
import requests
import uuid

def api_chat_completions(api_url, api_key, model, message_id, user_message):
    """
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": model,
        "id": message_id,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            try:
              
                response_data = response.json()
              
                reply_content = response_data["choices"][0]["message"]["content"]
                return reply_content
            except KeyError as e:
                print(f"no keys: {e}")
        else:
            print(f"state: {response.status_code}, message: {response.text}")
    except requests.RequestException as e:

        return f"Error message: {e}"

