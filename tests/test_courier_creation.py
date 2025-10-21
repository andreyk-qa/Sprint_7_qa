import pytest
import requests
import allure
from data import ResponseMessages, Url


class TestCourierCreation:

    @allure.title("Проверка создания курьера")
    @allure.description("Проверяется, что при передаче соответствующих требованиям данных, курьер успешно создается. По окончанию проверки задействуется код очистки данных.")
    def test_successful_creation_courier(self, register_new_courier, cleanup_courier):
        payload = register_new_courier
        with allure.step(f"Отправить POST-запрос на создание курьера по адресу {Url.MAIN_URL}{Url.CREATE_COURIER} с логином '{payload['login']}'"):
            response = requests.post(
                f'{Url.MAIN_URL}{Url.CREATE_COURIER}',
                json=payload
            )
        with allure.step("Проверить код ответа 201 и тело ответа 'ok: True'"):
            assert response.status_code == 201
            assert response.json()['ok'] == ResponseMessages.COURIER_CREATED_SUCCESS
        cleanup_courier(payload)

    @allure.title("Проверка создания двух одинаковых курьеров")
    @allure.description("Проверяется, что при использовании данных уже созданного ранее курьера, система не даст создать его повторно.")
    def test_repeated_creation_courier(self, setup_courier_for_cleanup):
        payload = setup_courier_for_cleanup
        with allure.step(f"Отправить повторный POST-запрос на создание курьера по адресу {Url.MAIN_URL}{Url.CREATE_COURIER} с логином '{payload['login']}'"):
            response = requests.post(
                f'{Url.MAIN_URL}{Url.CREATE_COURIER}',
                json=setup_courier_for_cleanup
            )
        with allure.step("Проверить код ответа 409 и сообщение об ошибке"):
            assert response.status_code == 409
            assert response.json()['message'] == ResponseMessages.COURIER_LOGIN_ALREADY

    @allure.title("Проверка создания курьера без обязательных полей (логин/пароль)")
    @allure.description("Проверяется, что при отсутствии обязательного поля ('login' или 'password'), система возвращает код 400.")
    @pytest.mark.parametrize("missing_field, default_value", [("login", "test_login"), ("password", "test_pass")])
    def test_creation_courier_without_required_fields(self, register_new_courier, missing_field, default_value):
        payload = register_new_courier
        payload.pop(missing_field, default_value)
        with allure.step(f"Отправить POST-запрос на создание курьера по адресу {Url.MAIN_URL}{Url.CREATE_COURIER} без поля '{missing_field}'"):
            response = requests.post(
                f'{Url.MAIN_URL}{Url.CREATE_COURIER}',
                json=payload
            )
        with allure.step("Проверить код ответа 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()['message'] == ResponseMessages.COURIER_NOT_ENOUGH_DATA

    @allure.title("Проверка создания курьера с уже используемым логином")
    @allure.description("Проверяется, что при использовании логина уже созданного ранее курьера, система не даст создать нового курьера.")
    def test_creation_courier_with_used_login(self, setup_courier_for_cleanup, register_new_courier_with_used_login):
        used_login = setup_courier_for_cleanup["login"]
        payload = register_new_courier_with_used_login
        payload["login"] = used_login
        with allure.step(f"Отправить POST-запрос на создание курьера по адресу {Url.MAIN_URL}{Url.CREATE_COURIER} с уже использованным логином '{used_login}'"):
            response = requests.post(
                f'{Url.MAIN_URL}{Url.CREATE_COURIER}',
                json=payload
            )
        with allure.step("Проверить код ответа 409 и сообщение об ошибке"):
            assert response.status_code == 409
            assert response.json()['message'] == ResponseMessages.COURIER_LOGIN_ALREADY
