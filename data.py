class Url:
    MAIN_URL = 'https://qa-scooter.praktikum-services.ru'
    CREATE_COURIER = '/api/v1/courier'
    DELETE_COURIER = '/api/v1/courier/'
    LOGIN_COURIER = '/api/v1/courier/login'
    ORDER_CREATION = '/api/v1/orders'

class ResponseMessages:
    COURIER_CREATED_SUCCESS = True
    COURIER_LOGIN_ALREADY = 'Этот логин уже используется. Попробуйте другой.'
    COURIER_NOT_ENOUGH_DATA = 'Недостаточно данных для создания учетной записи'
    COURIER_NOT_LOGIN_DATA = 'Недостаточно данных для входа'
    COURIER_NOT_FOUND = 'Учетная запись не найдена'
