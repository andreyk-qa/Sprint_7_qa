import pytest
import requests
from data import Url
from helpers import generate_random_string, get_courier_id, delete_courier


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
