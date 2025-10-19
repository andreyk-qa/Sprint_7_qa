import pytest
import requests
import allure
from data import Url
from conftest import get_order_body


class TestOrderCreation:

    @allure.title("Проверка создания заказа с различными вариантами цветов")
    @allure.description("Проверяется, что заказ можно создать, указав BLACK, GREY, оба цвета, или не указав цвет совсем. Проверяется код ответа 201 и наличие трек-номера track в теле ответа.")
    @pytest.mark.parametrize("color_options", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []], ids=["color_black", "color_grey", "color_both", "color_none"])
    def test_order_creation_with_color_options(self, color_options):
        payload = get_order_body(color_options)
        response = requests.post(
            f'{Url.MAIN_URL}{Url.ORDER_CREATION}',
            json=payload
        )
        assert response.status_code == 201
        assert isinstance(response.json()["track"], int)
