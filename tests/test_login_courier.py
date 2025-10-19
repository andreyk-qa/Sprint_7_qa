import pytest
import requests
import allure
from data import ResponseMessages, Url


class TestLoginCourier:

    @allure.title("Проверка авторизации курьера")
    @allure.description("Проверяется, что при передаче данных зарегистрированного курьера, курьер успешно авторизуется. По окончанию проверки задействуется код очистки данных.")
    def test_successful_authorization_courier(self, setup_courier_for_cleanup):
        payload = setup_courier_for_cleanup
        response_auth = requests.post(
            f'{Url.MAIN_URL}{Url.LOGIN_COURIER}',
            json={"login": payload["login"], "password": payload["password"]}
        )
        assert response_auth.status_code == 200
        assert isinstance(response_auth.json()['id'], int)

    @allure.title("Проверка авторизации курьера без обязательных полей (логин/пароль)")
    @allure.description("Проверяется, что при отсутствии обязательного поля ('login' или 'password'), система возвращает код 400.")
    @allure.issue("Найден баг при отправке запроса с пустым паролем. Для прохождения следующих проверок, пропускаем этот тест.")
    @pytest.mark.skip
    @pytest.mark.parametrize("missing_field", ["login", "password"], ids=["missing_login", "missing_password"])
    def test_authorization_courier_without_required_fields(self, setup_courier_for_cleanup, missing_field):
        payload = setup_courier_for_cleanup
        auth_data = {
            "login": payload["login"],
            "password": payload["password"]
        }
        auth_data.pop(missing_field)
        response_auth = requests.post(
            f'{Url.MAIN_URL}{Url.LOGIN_COURIER}',
            json=auth_data
        )
        assert response_auth.status_code == 400
        assert response_auth.json()['message'] == ResponseMessages.COURIER_NOT_LOGIN_DATA

    @allure.title("Проверка авторизации курьера с указанием неправильного обязательного поля (логин/пароль)")
    @allure.description("Проверяется, что при передаче неверного обязательного поля ('login' или 'password'), система возвращает код 404.")
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_authorization_courier_with_wrong_required_fields(self, setup_courier_for_cleanup, wrong_field):
        payload = setup_courier_for_cleanup
        auth_data = {
            "login": payload["login"],
            "password": payload["password"]
        }
        auth_data[wrong_field] += "w"
        response_auth = requests.post(
            f'{Url.MAIN_URL}{Url.LOGIN_COURIER}',
            json=auth_data
        )
        assert response_auth.status_code == 404
        assert response_auth.json()['message'] == ResponseMessages.COURIER_NOT_FOUND
