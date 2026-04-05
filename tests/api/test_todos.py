import pytest
import allure
from api import get_logger

logger = get_logger(__name__)


@allure.feature("Todos API")
@allure.story("Получение задач")
class TestGetTodos:
    """GET /todos."""

    @allure.title("Получение всех задач должно вернуть статус код 200")
    @allure.description("Проверка, что получение всех задач возвращает успешный ответ")
    def test_get_all_todos_success(self, todos_api):
        with allure.step("GET запрос на /todos"):
            response = todos_api.get_all_todos()
        
        with allure.step("Проверить, что статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("Проверить, что ответ содержит данные"):
            data = response.json()
            assert "data" in data or isinstance(data, list), \
                "Ответ должен содержать поле data или быть списком"
        
        logger.info(f"Задачи успешно получены, статус: {response.status_code}")

    @allure.title("Получение задач с фильтрацией по статусу выполнения должно вернуть 200")
    @allure.description("Проверка, что параметр фильтрации по выполнению работает корректно")
    def test_get_todos_with_completion_filter(self, todos_api):
        with allure.step("GET запрос с фильтром по выполнению"):
            response = todos_api.get_all_todos(completed=False)
        
        with allure.step("Проверить, что статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Тест фильтрации по выполнению пройден, статус: {response.status_code}")


@allure.feature("Todos API")
@allure.story("Получение задачи по ID")
class TestGetTodoById:
    """GET /todos/:id."""

    @allure.title("Получение задачи по ID должно вернуть статус код 200")
    @allure.description("Проверка, что получение существующей задачи возвращает успешный ответ")
    def test_get_todo_by_id_success(self, todos_api):
        todo_id = 1
        
        with allure.step(f"GET запрос на /todos/{todo_id}"):
            response = todos_api.get_todo_by_id(todo_id)
        
        with allure.step("Проверить, что статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("Проверить, что ответ содержит данные задачи"):
            data = response.json()
            assert "id" in data or "data" in data, \
                "Ответ должен содержать данные задачи"
        
        logger.info(f"Задача {todo_id} получена, статус: {response.status_code}")

    @allure.title("Получение несуществующей задачи должно вернуть статус код 404")
    @allure.description("Проверка, что получение несуществующей задачи возвращает ошибку 'не найдено'")
    def test_get_todo_by_id_not_found(self, todos_api):
        todo_id = 99999
        
        with allure.step(f"GET запрос на /todos/{todo_id}"):
            response = todos_api.get_todo_by_id(todo_id)
        
        with allure.step("Проверить, что статус код ответа равен 404"):
            assert response.status_code in [404, 400], \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 для несуществующей задачи")


@allure.feature("Todos API")
@allure.story("Создание задачи")
class TestCreateTodo:
    """POST /todos."""

    @allure.title("Создание задачи должно вернуть статус код 201")
    @allure.description("Проверка, что создание новой задачи возвращает успешный статус")
    def test_create_todo_success(self, todos_api, test_todo_data):
        with allure.step("POST запрос с данными задачи"):
            response = todos_api.create_todo(test_todo_data)
        
        with allure.step("Проверить, что статус код ответа равен 201 или 200"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        with allure.step("Проверить, что ответ содержит ID задачи"):
            data = response.json()
            if "id" in data:
                created_id = data["id"]
                allure.attach(str(created_id), "ID созданной задачи", allure.attachment_type.TEXT)
                
                with allure.step("Очистка: Удалить созданную задачу"):
                    todos_api.delete_todo(created_id)
        
        logger.info(f"Задача успешно создана, статус: {response.status_code}")

    @allure.title("Создание задачи со статусом выполнения должно быть успешным")
    @allure.description("Проверка, что создание задачи с флагом completed работает")
    def test_create_todo_with_completed_status(self, todos_api):
        todo_data = {
            "title": "Выполненная задача",
            "completed": True
        }
        
        with allure.step("POST запрос со статусом выполнения"):
            response = todos_api.create_todo(todo_data)
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        logger.info(f"Задача со статусом выполнения создана, статус: {response.status_code}")


@allure.feature("Todos API")
@allure.story("Обновление задачи")
class TestUpdateTodo:
    """PUT /todos/:id."""

    @allure.title("Обновление задачи должно вернуть статус код 200")
    @allure.description("Проверка, что обновление задачи возвращает успешный статус")
    def test_update_todo_success(self, todos_api, test_todo_data):
        todo_id = 1
        updated_data = {
            **test_todo_data,
            "title": "Обновлённый заголовок задачи"
        }
        
        with allure.step(f"PUT обновления задачи {todo_id}"):
            response = todos_api.update_todo(todo_id, updated_data)
        
        with allure.step("Проверить, что статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Задача {todo_id} успешно обновлена, статус: {response.status_code}")

    @allure.title("Обновление несуществующей задачи должно вернуть 404")
    @allure.description("Проверка, что обновление несуществующей задачи возвращает 'не найдено'")
    def test_update_todo_not_found(self, todos_api, test_todo_data):
        todo_id = 99999
        
        with allure.step(f"PUT несуществующей задачи {todo_id}"):
            response = todos_api.update_todo(todo_id, test_todo_data)
        
        with allure.step("Проверить, что статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при обновлении несуществующей задачи")


@allure.feature("Todos API")
@allure.story("Частичное обновление задачи")
class TestPartialUpdateTodo:
    """PATCH /todos/:id."""

    @allure.title("Частичное обновление задачи должно вернуть статус код 200")
    @allure.description("Проверка, что частичное обновление задачи возвращает успешный статус")
    def test_partial_update_todo_success(self, todos_api):
        todo_id = 1
        update_data = {"completed": True}
        
        with allure.step(f"PATCH частичного обновления задачи {todo_id}"):
            response = todos_api.partial_update_todo(todo_id, update_data)
        
        with allure.step("Проверить, что статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Задача {todo_id} частично обновлена, статус: {response.status_code}")

    @allure.title("Частичное обновление несуществующей задачи должно вернуть 404")
    @allure.description("Проверка, что PATCH несуществующей задачи возвращает 'не найдено'")
    def test_partial_update_todo_not_found(self, todos_api):
        todo_id = 99999
        update_data = {"completed": False}
        
        with allure.step(f"PATCH несуществующей задачи {todo_id}"):
            response = todos_api.partial_update_todo(todo_id, update_data)
        
        with allure.step("Проверить, что статус код ответа равен 404"):
            assert response.status_code in [404, 400], \
                f"Ожидался 404 или 400, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при PATCH несуществующей задачи")


@allure.feature("Todos API")
@allure.story("Удаление задачи")
class TestDeleteTodo:
    """DELETE /todos/:id."""

    # @allure.title("Удаление задачи должно вернуть статус код 200")
    # @allure.description("Проверка, что удаление задачи возвращает успешный статус")
    # def test_delete_todo_success(self, todos_api, test_todo_data):
    #     with allure.step("Создать тестовую задачу"):
    #         create_response = todos_api.create_todo(test_todo_data)
    #         if create_response.status_code in [200, 201]:
    #             data = create_response.json()
    #             todo_id = data.get("id", 1)
    #         else:
    #             todo_id = 1
        
    #     with allure.step(f"DELETE удаления задачи {todo_id}"):
    #         response = todos_api.delete_todo(todo_id)
        
    #     with allure.step("Проверить, что статус код ответа равен 200"):
    #         assert response.status_code == 200, \
    #             f"Ожидался 200, получен {response.status_code}"
        
    #     logger.info(f"Задача {todo_id} успешно удалена, статус: {response.status_code}")

    @allure.title("Удаление несуществующей задачи должно вернуть 404")
    @allure.description("Проверка, что удаление несуществующей задачи возвращает 'не найдено'")
    def test_delete_todo_not_found(self, todos_api):
        todo_id = 99999
        
        with allure.step(f"DELETE несуществующей задачи {todo_id}"):
            response = todos_api.delete_todo(todo_id)
        
        with allure.step("Проверить, что статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при удалении несуществующей задачи")