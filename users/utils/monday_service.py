
import requests
import json
from django.conf import settings
import datetime
MONDAY_API_KEY = settings.MONDAY_API_KEY
MONDAY_API_URL = settings.MONDAY_API_URL

headers = {
    "Authorization": f"Bearer {MONDAY_API_KEY}", 
    "Content-Type": "application/json"
}


def get_boards():
    query = """{
        boards {
            id
            name
        }
    }"""
    response = requests.post(MONDAY_API_URL, headers=headers, json={"query": query})
    return response.json()

import requests
import json

def create_item(board_id, name, first_name, last_name, email, phone):
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": f"Bearer {MONDAY_API_KEY}",
        "Content-Type": "application/json"
    }
    created_date = datetime.date.today().isoformat() 
    column_values = json.dumps({
        "text_mkp0gzpx": first_name, 
        "text_mkp0vcxa": last_name,  
        "text_mkp0rbkf": email,
        "phone_mkp4v7zb": {"phone": phone, "countryShortName": "IN"},
        "date4": {"date": created_date}
    })
    column_values_json = json.dumps(column_values)
    query = f"""
    mutation {{
        create_item (board_id: {board_id}, item_name: "{name}", column_values: {json.dumps(column_values)}) {{
            id
        }}
    }}
    """
    response = requests.post(url, json={"query": query}, headers=headers)
    return response.json()
