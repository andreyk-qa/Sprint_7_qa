import pytest
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

@pytest.fixture
def register_new_courier():
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    return payload

@pytest.fixture
def cleanup_courier(request):
    couriers_to_delete = []
    def finalizer():
        for payload in couriers_to_delete:
            courier_id = get_courier_id(payload)
            delete_courier(courier_id)
    request.addfinalizer(finalizer)
    def _register_for_cleanup(payload):
        couriers_to_delete.append(payload)
    return _register_for_cleanup

@pytest.fixture
def setup_courier_for_cleanup(register_new_courier):
    payload = register_new_courier
    courier_id = None
    requests.post(f'{Url.MAIN_URL}{Url.CREATE_COURIER}', json=payload)
    try:
        courier_id = get_courier_id(payload)
        yield payload
    finally:
        delete_courier(courier_id)

@pytest.fixture
def register_new_courier_with_used_login():
    payload = {
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    return payload
