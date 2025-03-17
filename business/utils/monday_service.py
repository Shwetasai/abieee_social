import requests
import json
from django.conf import settings
import datetime
MONDAY_API_KEY = settings.MONDAY_API_KEY
url = "https://api.monday.com/v2"

headers = {
    "Authorization": f"Bearer {MONDAY_API_KEY}",
    "Content-Type": "application/json"
}
def get_boards():
    query = """{
        boards {
            id
            business_name
            activity
        }
    }"""
    response = requests.post(url, headers=headers, json={"query": query})
    return response.json()

def create_item(board_id,business_name, field_of_activity,business_description,target_audience):
    created_date = datetime.date.today().isoformat()

    column_values =json.dumps({
        "text_mkp4fs9t":field_of_activity,
        "text_mkp4meq3":business_description,
        "text_mkp41dj9":target_audience,
        "date4": {"date": created_date}
    })
    column_values_json = column_values  

    query = f"""
    mutation {{
        create_item (board_id: {board_id}, item_name: "{business_name}", column_values: {json.dumps(column_values)}) {{
        id
        }}
    }}
    """
    response = requests.post(url, json={"query": query}, headers=headers)
    try:
        response_data = response.json()
    except json.JSONDecodeError:
        return None

    if "errors" in response_data:
        print("GraphQL Error:", response_data["errors"])

    return response_data
