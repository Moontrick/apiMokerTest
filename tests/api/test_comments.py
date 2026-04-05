import pytest
import allure
from api import get_logger

logger = get_logger(__name__)


@allure.feature("Comments API")
@allure.story("Получение комментариев")
class TestGetComments:
    """GET /comments."""

    @allure.title("Получение всех комментариев должно вернуть статус код 200")
    @allure.description("Проверка, что получение всех комментариев возвращает успешный ответ")
    def test_get_all_comments_success(self, comments_api):
        with allure.step("GET запрос на /comments"):
            response = comments_api.get_all_comments()
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("ответ содержит данные"):
            data = response.json()
            assert "data" in data or isinstance(data, list), \
                "Ответ должен содержать поле data или быть списком"
        
        logger.info(f"Комментарии успешно получены, статус: {response.status_code}")


@allure.feature("Comments API")
@allure.story("Получение комментария по ID")
class TestGetCommentById:
    """GET /comments/:id."""

    @allure.title("Получение комментария по ID должно вернуть статус код 200")
    @allure.description("Проверка, что получение существующего комментария возвращает успешный ответ")
    def test_get_comment_by_id_success(self, comments_api):
        comment_id = 11
        
        with allure.step(f"GET запрос на /comments/{comment_id}"):
            response = comments_api.get_comment_by_id(comment_id)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("ответ содержит данные комментария"):
            data = response.json()
            assert "id" in data or "data" in data, \
                "Ответ должен содержать данные комментария"
        
        logger.info(f"Комментарий {comment_id} получен, статус: {response.status_code}")

    @allure.title("Получение несуществующего комментария должно вернуть статус код 404")
    @allure.description("Проверка, что получение несуществующего комментария возвращает ошибку 'не найдено'")
    def test_get_comment_by_id_not_found(self, comments_api):
        comment_id = 99999
        
        with allure.step(f"GET запрос на /comments/{comment_id}"):
            response = comments_api.get_comment_by_id(comment_id)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 для несуществующего комментария")


@allure.feature("Comments API")
@allure.story("Создание комментария")
class TestCreateComment:
    """POST /comments."""

    @allure.title("Создание комментария должно вернуть статус код 201")
    @allure.description("Проверка, что создание нового комментария возвращает успешный статус")
    def test_create_comment_success(self, comments_api, test_comment_data):
        with allure.step("POST запрос с данными комментария"):
            response = comments_api.create_comment(test_comment_data)
        
        with allure.step("статус код ответа равен 201 или 200"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        with allure.step("ответ содержит ID комментария"):
            data = response.json()
            if "id" in data:
                created_id = data["id"]
                allure.attach(str(created_id), "ID созданного комментария", allure.attachment_type.TEXT)
                
                with allure.step("Очистка: Удалить созданный комментарий"):
                    comments_api.delete_comment(created_id)
        
        logger.info(f"Комментарий успешно создан, статус: {response.status_code}")

    @allure.title("Создание комментария с обязательными полями должно быть успешным")
    @allure.description("Проверка, что создание комментария с минимально необходимыми полями работает")
    def test_create_comment_minimal_data(self, comments_api):
        minimal_data = {
            "postId": 1,
            "name": "Тестовый комментарий",
            "body": "Тело тестового комментария",
            "email": "test@example.com"
        }
        
        with allure.step("POST запрос с минимальными данными"):
            response = comments_api.create_comment(minimal_data)
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        logger.info(f"Создание минимального комментария обработано, статус: {response.status_code}")


@allure.feature("Comments API")
@allure.story("Обновление комментария")
class TestUpdateComment:
    """PUT /comments/:id."""

    @allure.title("Обновление комментария должно вернуть статус код 200")
    @allure.description("Проверка, что обновление комментария возвращает успешный статус")
    def test_update_comment_success(self, comments_api, test_comment_data):
        comment_id = 12
        updated_data = {
            **test_comment_data,
            "body": "Обновлённое тело комментария"
        }
        
        with allure.step(f"PUT обновления комментария {comment_id}"):
            response = comments_api.update_comment(comment_id, updated_data)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Комментарий {comment_id} успешно обновлён, статус: {response.status_code}")

    @allure.title("Обновление несуществующего комментария должно вернуть 404")
    @allure.description("Проверка, что обновление несуществующего комментария возвращает 'не найдено'")
    def test_update_comment_not_found(self, comments_api, test_comment_data):
        comment_id = 99999
        
        with allure.step(f"PUT несуществующего комментария {comment_id}"):
            response = comments_api.update_comment(comment_id, test_comment_data)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при обновлении несуществующего комментария")


@allure.feature("Comments API")
@allure.story("Частичное обновление комментария")
class TestPartialUpdateComment:
    """PATCH /comments/:id."""

    @allure.title("Частичное обновление несуществующего комментария должно вернуть 404")
    @allure.description("Проверка, что PATCH несуществующего комментария возвращает 'не найдено'")
    def test_partial_update_comment_not_found(self, comments_api):
        comment_id = 99999
        update_data = {"body": "Ещё один обновлённый комментарий"}
        
        with allure.step(f"PATCH несуществующего комментария {comment_id}"):
            response = comments_api.partial_update_comment(comment_id, update_data)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code in [404, 400], \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при PATCH несуществующего комментария")


@allure.feature("Comments API")
@allure.story("Удаление комментария")
class TestDeleteComment:
    """DELETE /comments/:id."""

    # @allure.title("Удаление комментария должно вернуть статус код 200")
    # @allure.description("Проверка, что удаление комментария возвращает успешный статус")
    # def test_delete_comment_success(self, comments_api, test_comment_data):
    #     with allure.step("Создать тестовый комментарий"):
    #         create_response = comments_api.create_comment(test_comment_data)
    #         if create_response.status_code in [200, 201]:
    #             data = create_response.json()
    #             comment_id = data.get("id", 1)
    #         else:
    #             comment_id = 1
        
    #     with allure.step(f"DELETE удаления комментария {comment_id}"):
    #         response = comments_api.delete_comment(comment_id)
        
    #     with allure.step("статус код ответа равен 200"):
    #         assert response.status_code == 200, \
    #             f"Ожидался 200, получен {response.status_code}"
        
    #     logger.info(f"Комментарий {comment_id} успешно удалён, статус: {response.status_code}")

    @allure.title("Удаление несуществующего комментария должно вернуть 404")
    @allure.description("Проверка, что удаление несуществующего комментария возвращает 'не найдено'")
    def test_delete_comment_not_found(self, comments_api):
        comment_id = 99999
        
        with allure.step(f"DELETE несуществующего комментария {comment_id}"):
            response = comments_api.delete_comment(comment_id)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при удалении несуществующего комментария")