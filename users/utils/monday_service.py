
import requests
import json
from django.conf import settings
import datetime
MONDAY_API_KEY = settings.MONDAY_API_KEY
MONDAY_API_URL = settings.MONDAY_API_URL
REGISTER_BOARD_ID = settings.REGISTER_BOARD_ID 
DETAILS_BOARD_ID = settings.DETAILS_BOARD_ID
id_COLUMN_ID = "text_mkp7aqty"
EMAIL_COLUMN_ID = "text_mkp0rbkf" 
DETAILS_ID_COLUMN = "text_mkp7yyhs" 
DETAILS_EMAIL_COLUMN = "text_mkp64yd3" 

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
def get_latest_id():
    query = f"""
    query {{
        boards (ids: {REGISTER_BOARD_ID}) {{
            items_page {{
                items {{
                    id
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """

    response = requests.post(MONDAY_API_URL, json={"query": query}, headers=headers)
    data = response.json()

    existing_ids = []
    if "data" in data and "boards" in data["data"]:
        for item in data["data"]["boards"][0]["items_page"]["items"]:
            for column in item["column_values"]:
                if column["id"] == id_COLUMN_ID and column["text"]:
                    try:
                        existing_ids.append(int(column["text"]))
                    except ValueError:
                        pass 

    new_id = max(existing_ids, default=0) + 1
    return new_id
def save_to_details_board(new_id, email):
    column_values = {
        DETAILS_ID_COLUMN: str(new_id), 
        DETAILS_EMAIL_COLUMN: email 
    }
    column_values_json = json.dumps(column_values)

    query = f"""
    mutation {{
        create_item (board_id: {DETAILS_BOARD_ID}, item_name: "{new_id}", column_values: {json.dumps(column_values_json)}) {{
            id
        }}
    }}
    """
    response = requests.post(MONDAY_API_URL, json={"query": query}, headers=headers)
    data = response.json()
    if "errors" in data:
        print("Error saving to details board:", data["errors"])
        return {"success": False, "error": data["errors"]}

    return {"success": True, "data": data}

def register_monday_item(name, first_name, last_name, email, phone, is_email_verified):
    url = "https://api.monday.com/v2"

    created_date = datetime.date.today().isoformat()

    item_id = get_item_id_by_email(email, REGISTER_BOARD_ID)

    if item_id:
        column_values = {
            "text_mkp0gzpx": first_name,
            "text_mkp0vcxa": last_name,
            "phone_mkp4v7zb": {"phone": phone, "countryShortName": "IN"},
            "date4": {"date": created_date},
            "boolean_mkp6bddq": {"checked": "true" if is_email_verified else "false"}
        }

        column_values_str = json.dumps(column_values).replace('"', '\\"')

        query = f"""
        mutation {{
            change_multiple_column_values (
                board_id: {REGISTER_BOARD_ID},
                item_id: {item_id},
                column_values: "{column_values_str}"
            ) {{
                id
            }}
        }}
        """

        response = requests.post(url, json={"query": query}, headers=headers)
        data = response.json()
        if "data" in data and "change_multiple_column_values" in data["data"]:
            return item_id
        return None  

    else:
        new_id = get_latest_id()
        print(f"Generated ID: {new_id}")

        column_values = {
            "text_mkp7aqty": str(new_id),
            "text_mkp0gzpx": first_name,
            "text_mkp0vcxa": last_name,
            "text_mkp0rbkf": email,
            "phone_mkp4v7zb": {"phone": phone, "countryShortName": "IN"},
            "date4": {"date": created_date},
            "boolean_mkp6bddq": {"checked": "true" if is_email_verified else "false"}
        }

        query = f"""
        mutation {{
            create_item (board_id: {REGISTER_BOARD_ID}, item_name: "{name}", column_values: {json.dumps(json.dumps(column_values))}) {{
                id
            }}
        }}
        """

        response = requests.post(url, json={"query": query}, headers=headers)
        data = response.json()
        if "data" in data and "create_item" in data["data"]:
            item_id = data["data"]["create_item"]["id"]

            save_to_details_board(new_id, email)

            return item_id
        return None
def get_item_id_by_email(email,REGISTER_BOARD_ID):
    query = f"""
    query {{
        boards (ids: {REGISTER_BOARD_ID}) {{
            items_page {{
                items {{
                    id
                    column_values {{
                        id
                        text
                    }}
                }}
            }}
        }}
    }}
    """
    
    response = requests.post(MONDAY_API_URL, json={"query": query}, headers=headers)
    data = response.json()
    if 'data' in data and 'boards' in data['data']:
        for item in data['data']['boards'][0]['items_page']['items']:
            for column in item['column_values']:
                if column['id'] == "text_mkp0rbkf" and column['text'] == email:
                    return item['id']
    return None

def update_verification_status(email):
    try:
        item_id = get_item_id_by_email(email,REGISTER_BOARD_ID)

        if not item_id:
            return {"error": "User not found in Monday.com"}

        item_id = int(item_id)
        value_json = json.dumps({"checked": "true"})

        query = f"""
        mutation {{
            change_column_value (
                board_id: {REGISTER_BOARD_ID},
                item_id: {item_id}, 
                column_id: "boolean_mkp6bddq", 
                value: {json.dumps(value_json)}
            ) {{
                id
            }}
        }}
        """

        response = requests.post(MONDAY_API_URL, json={"query": query}, headers=headers)
        data = response.json()
        return data
    
    except ValueError as e:
        return {"error": f"Invalid REGISTER_BOARD_ID or item_id: {e}"}
    