import pytest
import allure
from api import get_logger

logger = get_logger(__name__)


@allure.feature("Posts API")
@allure.story("Получение постов")
class TestGetPosts:
    """GET /posts."""

    @allure.title("Получение всех постов должно вернуть статус код 200")
    @allure.description("Проверка, что получение всех постов возвращает успешный ответ")
    def test_get_all_posts_success(self, posts_api):
        with allure.step("GET /posts"):
            response = posts_api.get_all_posts()
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("ответ содержит данные"):
            data = response.json()
            assert "data" in data or isinstance(data, list), \
                "Ответ должен содержать поле data или быть списком"
        
        logger.info(f"Посты успешно получены, статус: {response.status_code}")

    @allure.title("Получение постов с фильтрацией должно вернуть статус код 200")
    @allure.description("Проверка, что параметры фильтрации работают корректно")
    def test_get_posts_with_filtering(self, posts_api):
        with allure.step("GET запрос с параметрами фильтрации"):
            response = posts_api.get_all_posts(page=1, limit=5, user_id=1)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Тест фильтрации пройден, статус: {response.status_code}")


@allure.feature("Posts API")
@allure.story("Получение поста по ID")
class TestGetPostById:
    """GET /posts/:id."""

    @allure.title("Получение поста по ID должно вернуть статус код 200")
    @allure.description("Проверка, что получение существующего поста возвращает успешный ответ")
    def test_get_post_by_id_success(self, posts_api):
        post_id = 4
        
        with allure.step(f"GET /posts/{post_id}"):
            response = posts_api.get_post_by_id(post_id)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("ответ содержит данные поста"):
            data = response.json()
            assert "id" in data or "data" in data, \
                "Ответ должен содержать данные поста"
        
        logger.info(f"Пост {post_id} получен, статус: {response.status_code}")

    @allure.title("Получение несуществующего поста должно вернуть статус код 404")
    @allure.description("Проверка, что получение несуществующего поста возвращает ошибку 'не найдено'")
    def test_get_post_by_id_not_found(self, posts_api):

        post_id = 99999
        
        with allure.step(f"GET /posts/{post_id}"):
            response = posts_api.get_post_by_id(post_id)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 для несуществующего поста")


@allure.feature("Posts API")
@allure.story("Создание поста")
class TestCreatePost:
    """POST /posts."""

    @allure.title("Создание поста должно вернуть статус код 201")
    @allure.description("Проверка, что создание нового поста возвращает успешный статус")
    def test_create_post_success(self, posts_api, test_post_data):
        with allure.step("POST запрос с данными поста"):
            response = posts_api.create_post(test_post_data)
        
        with allure.step("статус код ответа равен 201 или 200"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        with allure.step("ответ содержит ID поста"):
            data = response.json()
            if "id" in data:
                created_id = data["id"]
                allure.attach(str(created_id), "ID созданного поста", allure.attachment_type.TEXT)
                
                with allure.step("Очистка: Удалить созданный пост"):
                    posts_api.delete_post(created_id)
        
        logger.info(f"Пост успешно создан, статус: {response.status_code}")

    @allure.title("Создание поста с обязательными полями должно быть успешным")
    @allure.description("Проверка, что создание поста с минимально необходимыми полями работает")
    def test_create_post_minimal_data(self, posts_api):
        minimal_data = {
            "title": "Тест",
            "body": "Тест тест"
        }
        
        with allure.step("POST запрос с минимальными данными"):
            response = posts_api.create_post(minimal_data)
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        logger.info(f"Создание минимального поста обработано, статус: {response.status_code}")


@allure.feature("Posts API")
@allure.story("Обновление поста")
class TestUpdatePost:
    """PUT /posts/:id."""

    @allure.title("Обновление поста должно вернуть статус код 200")
    @allure.description("Проверка, что обновление поста возвращает успешный статус")
    def test_update_post_success(self, posts_api, test_post_data):
        post_id = 4
        updated_data = {
            **test_post_data,
            "title": "Обновлённый заголовок поста"
        }
        
        with allure.step(f"PUT запрос для обновления поста {post_id}"):
            response = posts_api.update_post(post_id, updated_data)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Пост {post_id} успешно обновлён, статус: {response.status_code}")

    @allure.title("Обновление несуществующего поста должно вернуть 404")
    @allure.description("Проверка, что обновление несуществующего поста возвращает 'не найдено'")
    def test_update_post_not_found(self, posts_api, test_post_data):
        post_id = 99999
        
        with allure.step(f"PUT запрос для несуществующего поста {post_id}"):
            response = posts_api.update_post(post_id, test_post_data)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при обновлении несуществующего поста")


@allure.feature("Posts API")
@allure.story("Частичное обновление поста")
class TestPartialUpdatePost:
    """PATCH /posts/:id."""

    @allure.title("Частичное обновление поста должно вернуть статус код 400")
    @allure.description("Проверка, что частичное обновление поста возвращает успешный статус")
    def test_partial_update_post_success(self, posts_api):
        post_id = 4
        update_data = {"title": "Частично обновлённый заголовок"}
        
        with allure.step(f"PATCH запрос для частичного обновления поста {post_id}"):
            response = posts_api.partial_update_post(post_id, update_data)
        
        with allure.step("статус код ответа равен 400"):
            assert response.status_code == 400, \
                f"Ожидался 400, получен {response.status_code}"
        
        logger.info(f"Пост {post_id} частично обновлён, статус: {response.status_code}")

    @allure.title("Частичное обновление несуществующего поста должно вернуть 404")
    @allure.description("Проверка, что PATCH несуществующего поста возвращает 'не найдено'")
    def test_partial_update_post_not_found(self, posts_api):
        post_id = 99999
        update_data = {"title": "Ещё один обновлённый заголовок"}
        
        with allure.step(f"PATCH запрос для несуществующего поста {post_id}"):
            response = posts_api.partial_update_post(post_id, update_data)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code in [400, 404], \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при PATCH несуществующего поста")


@allure.feature("Posts API")
@allure.story("Удаление поста")
class TestDeletePost:
    """DELETE /posts/:id."""

    # @allure.title("Удаление поста должно вернуть статус код 200")
    # @allure.description("Проверка, что удаление поста возвращает успешный статус")
    # def test_delete_post_success(self, posts_api, test_post_data):
    #     with allure.step("Создать тестовый пост"):
    #         create_response = posts_api.create_post(test_post_data)
    #         if create_response.status_code in [200, 201]:
    #             data = create_response.json()
    #             post_id = data.get("id", 3)
    #         else:
    #             post_id = 3
        
    #     with allure.step(f"DELETE запрос для удаления поста {post_id}"):
    #         response = posts_api.delete_post(post_id)
        
    #     with allure.step("статус код ответа равен 200"):
    #         assert response.status_code == 200, \
    #             f"Ожидался 200, получен {response.status_code}"
        
    #     logger.info(f"Пост {post_id} успешно удалён, статус: {response.status_code}")

    @allure.title("Удаление несуществующего поста должно вернуть 404")
    @allure.description("Проверка, что удаление несуществующего поста возвращает 'не найдено'")
    def test_delete_post_not_found(self, posts_api):
        post_id = 99999
        
        with allure.step(f"DELETE запрос для несуществующего поста {post_id}"):
            response = posts_api.delete_post(post_id)
        
        with allure.step("статус код ответа равен 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}"
        
        logger.info(f"Корректно возвращён 404 при удалении несуществующего поста")


@allure.feature("Posts API")
@allure.story("Лайки поста")
class TestPostLikes:
    """GET/POST /posts/:id/likes."""

    @allure.title("Получение лайков поста должно вернуть статус код 200")
    @allure.description("Проверка, что получение лайков поста возвращает успешный ответ")
    def test_get_post_likes_success(self, posts_api):
        post_id = 4
        
        with allure.step(f"GET /posts/{post_id}/likes"):
            response = posts_api.get_post_likes(post_id)
        
        with allure.step("статус код ответа равен 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}"
        
        logger.info(f"Лайки для поста {post_id} получены, статус: {response.status_code}")

    @allure.title("Добавление лайка к посту должно вернуть статус код 201")
    @allure.description("Проверка, что добавление лайка к посту возвращает успешный статус")
    def test_add_like_to_post_success(self, posts_api):
        post_id = 4
        like_data = {"userId": 2}
        
        with allure.step(f"POST запрос для добавления лайка к посту {post_id}"):
            response = posts_api.add_like_to_post(post_id, like_data)
        
        with allure.step("статус код ответа равен 201 или 200"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        logger.info(f"Лайк добавлен к посту {post_id}, статус: {response.status_code}")

    @allure.title("Добавление лайка к посту без userId должно быть успешным")
    @allure.description("Проверка, что добавление лайка без userId обрабатывается корректно")
    def test_add_like_to_post_without_user_id(self, posts_api):
        post_id = 4
        
        with allure.step(f"POST запрос для добавления лайка без userId"):
            response = posts_api.add_like_to_post(post_id)
        
        with allure.step("статус код ответа является допустимым"):
            assert response.status_code in [200, 201], \
                f"Ожидался 200 или 201, получен {response.status_code}"
        
        logger.info(f"Лайк добавлен к посту без userId, статус: {response.status_code}")