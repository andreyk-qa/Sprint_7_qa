import pytest
import requests
import allure
from data import Url


class TestOrderList:

    @allure.title("Проверка получения списка заказов")
    @allure.description("Проверяется, что при отправке GET-запроса к ручке /api/v1/orders, система возвращает код 200 и тело ответа содержит ключ 'orders', содержащий список заказов.")
    def test_get_order_list_success(self):
        response = requests.get(f'{Url.MAIN_URL}{Url.ORDER_CREATION}')
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
