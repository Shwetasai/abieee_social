import requests
import json
from django.conf import settings
import datetime

MONDAY_API_KEY = settings.MONDAY_API_KEY
MONDAY_API_URL = settings.MONDAY_API_URL
DETAILS_BOARD_ID = settings.DETAILS_BOARD_ID
DETAILS_FIELD_OF_ACTIVITY = "text_mkp4fs9t"
DETAILS_BUSINESS_DESCRIPTION = "text_mkp4meq3"
DETAILS_TARGET_AUDIENCE = "text_mkp41dj9"
DETAILS_EMAIL_COLUMN = "text_mkp64yd3"
DETAILS_BUSINESS_NAME="text_mkp89hyx"
DETAILS_DATE_COLUMN = "date4"


headers = {
    "Authorization": f"Bearer {MONDAY_API_KEY}",
    "Content-Type": "application/json"
}

def get_item_id_by_email(email, board_id):
    query = f"""
    query {{
        boards (ids: {board_id}) {{
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
                if column['id'] == DETAILS_EMAIL_COLUMN and column['text'] == email:
                    return item['id']
    return None

def business_details_board(business_name, field_of_activity, business_description, target_audience, email):
    created_date = datetime.date.today().isoformat()
    item_id = get_item_id_by_email(email, DETAILS_BOARD_ID)

    if item_id:
        column_values = {
            DETAILS_FIELD_OF_ACTIVITY: field_of_activity,
            DETAILS_BUSINESS_DESCRIPTION: business_description,
            DETAILS_TARGET_AUDIENCE: target_audience,
            DETAILS_BUSINESS_NAME: business_name,
            DETAILS_DATE_COLUMN: {"date": created_date}
        }
        column_values_str = json.dumps(column_values).replace('"', '\\"')

        query = f"""
        mutation {{
            change_multiple_column_values (
                board_id: {DETAILS_BOARD_ID},
                item_id: {item_id},
                column_values: "{column_values_str}"
            ) {{
                id
            }}
        }}
        """

        response = requests.post(MONDAY_API_URL, json={"query": query}, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    else:
        column_values = {
            DETAILS_EMAIL_COLUMN: email,
            DETAILS_FIELD_OF_ACTIVITY: field_of_activity,
            DETAILS_BUSINESS_DESCRIPTION: business_description,
            DETAILS_TARGET_AUDIENCE: target_audience,
            DETAILS_BUSINESS_NAME: business_name,
            DETAILS_DATE_COLUMN: {"date": created_date},
        }
        column_values_str = json.dumps(column_values).replace('"', '\\"')

        query = f"""
        mutation {{
            create_item(board_id: {DETAILS_BOARD_ID}, item_name: "{business_name}", column_values: "{column_values_str}") {{
                id
            }}
        }}
        """

        response = requests.post(MONDAY_API_URL, json={"query": query}, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}