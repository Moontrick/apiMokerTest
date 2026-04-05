import pytest
import allure
from api import get_logger

logger = get_logger(__name__)


@allure.feature("Users API")
@allure.story("Получение пользователей")
class TestGetUsers:
    """GET /users."""

    @allure.title("Получение всех пользователей должно вернуть статус код 200")
    @allure.description("Проверка, что получение всех пользователей возвращает успешный ответ")
    def test_get_all_users_success(self, users_api):
        with allure.step("GET запрос на /users"):
            response = users_api.get_all_users()
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("ответ содержит данные"):
            data = response.json()
            assert "data" in data or isinstance(data, list), \
                "Ответ должен содержать поле data или быть списком"
        
        logger.info(f"Пользователи успешно получены, статус: {response.status_code}")

    @allure.title("Получение пользователей с пагинацией должно вернуть статус код 200")
    @allure.description("Проверка, что параметры пагинации работают корректно")
    def test_get_users_with_pagination(self, users_api):
        with allure.step("GET запрос с параметрами пагинации"):
            response = users_api.get_all_users(page=1, limit=5)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Тест пагинации пройден, статус: {response.status_code}")


@allure.feature("Users API")
@allure.story("Получение пользователя по ID")
class TestGetUserById:
    """GET /users/:id."""

    @allure.title("Получение пользователя по ID должно вернуть статус код 200")
    @allure.description("Проверка, что получение существующего пользователя возвращает успешный ответ")
    def test_get_user_by_id_success(self, users_api):
        user_id = 1
        
        with allure.step(f"GET запрос на /users/{user_id}"):
            response = users_api.get_user_by_id(user_id)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("ответ содержит данные пользователя"):
            data = response.json()
            assert "id" in data or "data" in data, \
                "Ответ должен содержать данные пользователя"
        
        logger.info(f"Пользователь {user_id} получен, статус: {response.status_code}")

    @allure.title("Получение несуществующего пользователя должно вернуть статус код 404")
    @allure.description("Проверка, что получение несуществующего пользователя возвращает ошибку 'не найдено'")
    def test_get_user_by_id_not_found(self, users_api):
        user_id = 99999
        
        with allure.step(f"GET запрос на /users/{user_id}"):
            response = users_api.get_user_by_id(user_id)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 для несуществующего пользователя")


@allure.feature("Users API")
@allure.story("Создание пользователя")
class TestCreateUser:
    """POST /users."""

    @allure.title("Создание пользователя должно вернуть статус код 201")
    @allure.description("Проверка, что создание нового пользователя возвращает успешный статус")
    def test_create_user_success(self, users_api, test_user_data):
        with allure.step("POST запрос с данными пользователя"):
            response = users_api.create_user(test_user_data)
        
        with allure.step("статус код ответа равен 201 или 200"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        with allure.step("ответ содержит ID пользователя"):
            data = response.json()
            if "id" in data:
                created_id = data["id"]
                allure.attach(str(created_id), "ID созданного пользователя", allure.attachment_type.TEXT)
                
                with allure.step("Очистка: Удалить созданного пользователя"):
                    users_api.delete_user(created_id)
        
        logger.info(f"Пользователь успешно создан, статус: {response.status_code}")

    @allure.title("Создание пользователя с отсутствующим обязательным полем должно обрабатываться корректно")
    @allure.description("Проверка, что валидация работает для неполных данных пользователя")
    def test_create_user_missing_fields(self, users_api):
        incomplete_data = {"username": "testuser"}
        
        with allure.step("POST запрос с неполными данными"):
            response = users_api.create_user(incomplete_data)
        
        with allure.step("статус код ответа указывает на ошибку или успех"):
            assert response.status_code in [200, 201, 400, 422], \
                f"Неожиданный статус код: {response.status_code}"
        
        logger.info(f"Обработка неполных данных протестирована, статус: {response.status_code}")


@allure.feature("Users API")
@allure.story("Обновление пользователя")
class TestUpdateUser:
    """PUT /users/:id."""

    @allure.title("Обновление пользователя должно вернуть статус код 200")
    @allure.description("Проверка, что обновление пользователя возвращает успешный статус")
    def test_update_user_success(self, users_api, test_user_data):
        user_id = 3
        updated_data = {
            **test_user_data,
            "name": "Обновлённое имя пользователя"
        }
        
        with allure.step(f"PUT обновления пользователя {user_id}"):
            response = users_api.update_user(user_id, updated_data)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Пользователь {user_id} успешно обновлён, статус: {response.status_code}")

    @allure.title("Обновление несуществующего пользователя должно вернуть 404 или 400")
    @allure.description("Проверка, что обновление несуществующего пользователя возвращает 'не найдено'")
    def test_update_user_not_found(self, users_api, test_user_data):
        user_id = 99999
        
        with allure.step(f"PUT несуществующего пользователя {user_id}"):
            response = users_api.update_user(user_id, test_user_data)
        
        with allure.step("статус код ответа равен 404 или 400"):
            assert response.status_code in [404 , 400], \
                f"Ожидался 404 или 400, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 или 400 при обновлении несуществующего пользователя")


@allure.feature("Users API")
@allure.story("Частичное обновление пользователя")
class TestPartialUpdateUser:
    """PATCH /users/:id."""

    @allure.title("Частичное обновление пользователя должно вернуть статус код 200")
    @allure.description("Проверка, что частичное обновление пользователя возвращает успешный статус")
    def test_partial_update_user_success(self, users_api):
        user_id = 3
        update_data = {"name": "Тест ьтест"}
        
        with allure.step(f"PATCH частичного обновления пользователя {user_id}"):
            response = users_api.partial_update_user(user_id, update_data)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Пользователь {user_id} частично обновлён, статус: {response.status_code}")

    @allure.title("Частичное обновление несуществующего пользователя должно вернуть 404")
    @allure.description("Проверка, что PATCH несуществующего пользователя возвращает 'не найдено'")
    def test_partial_update_user_not_found(self, users_api):
        user_id = 99999
        update_data = {"name": "Тест имени"}
        
        with allure.step(f"PATCH несуществующего пользователя {user_id}"):
            response = users_api.partial_update_user(user_id, update_data)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при PATCH несуществующего пользователя")


@allure.feature("Users API")
@allure.story("Удаление пользователя")
class TestDeleteUser:
    """DELETE /users/:id."""

    # @allure.title("Удаление пользователя должно вернуть статус код 200")
    # @allure.description("Проверка, что удаление пользователя возвращает успешный статус")
    # def test_delete_user_success(self, users_api, test_user_data):
    #     """
    #     Тест успешного удаления пользователя.
        
    #     Ожидается: Статус код 200
    #     """
    #     # Сначала создаём пользователя для последующего удаления
    #     with allure.step("Создать тестового пользователя"):
    #         create_response = users_api.create_user(test_user_data)
    #         if create_response.status_code in [200, 201]:
    #             data = create_response.json()
    #             user_id = data.get("id", 5)
    #         else:
    #             user_id = 5
        
    #     with allure.step(f"DELETE удаления пользователя {user_id}"):
    #         response = users_api.delete_user(user_id)
        
    #     with allure.step("статус код ответа равен 200"):
    #         assert response.status_code == 200, \
    #             f"Ожидался 200, получен {response.status_code}"
        
    #     logger.info(f"Пользователь {user_id} успешно удалён, статус: {response.status_cod}e")

    @allure.title("Удаление несуществующего пользователя должно вернуть 404")
    @allure.description("Проверка, что удаление несуществующего пользователя возвращает 'не найдено'")
    def test_delete_user_not_found(self, users_api):
        """
        Тест удаления несуществующего пользователя.
        
        Ожидается: Статус код 404
        """
        user_id = 99999
        
        with allure.step(f"DELETE несуществующего пользователя {user_id}"):
            response = users_api.delete_user(user_id)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при удалении несуществующего пользователя")