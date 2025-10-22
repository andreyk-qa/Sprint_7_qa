import requests
import random
import string
from data import Url


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_courier_id(payload):
    try:
        login_response = requests.post(
            f'{Url.MAIN_URL}{Url.LOGIN_COURIER}',
            json={"login": payload["login"], "password": payload["password"]}
        )
        if login_response.status_code == 200 and 'id' in login_response.json():
            return login_response.json()['id']
    except Exception:
        return None
    return None

def delete_courier(courier_id):
    if courier_id:
        requests.delete(f'{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}')

def get_order_body(color_list):
    return {
        "firstName": generate_random_string(5),
        "lastName": generate_random_string(5),
        "address": f"Улица {generate_random_string(7)}, 1",
        "metroStation": 1,
        "phone": "+7 999 000 11 11",
        "rentTime": 5,
        "deliveryDate": "2025-10-30",
        "comment": "Тестовый комментарий",
        "color": color_list
    }
