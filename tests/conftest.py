import sys
from pathlib import Path
import pytest
import allure

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from api import APIClient, UsersAPI, PostsAPI, TodosAPI, CommentsAPI, get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def api_client():
    with allure.step("Подключение к API"):
        client = APIClient(base_url="https://apimocker.com", timeout=10)
        logger.info("Подключение создано")
        yield client
        client.close()
        logger.info("Подключение закрыто")


@pytest.fixture
def users_api(api_client):
    with allure.step("Тесты пользователя"):
        return UsersAPI(api_client)


@pytest.fixture
def posts_api(api_client):
    with allure.step("Тесты постов"):
        return PostsAPI(api_client)


@pytest.fixture
def todos_api(api_client):
    with allure.step("Тесты Todo"):
        return TodosAPI(api_client)


@pytest.fixture
def comments_api(api_client):
    with allure.step("Тесты комментариев"):
        return CommentsAPI(api_client)


@pytest.fixture
def test_user_data():
    return {
        "name": "John Doe",
      "username": "johndoe",
      "email": "john.doe@example.com",
      "phone": "+1-555-0123",
      "website": "https://johndoe.dev",
      "address": {
        "geo": {
          "lat": "40.7128",
          "lng": "-74.0060"
        },
        "city": "New York",
        "suite": "Apt 4B",
        "street": "123 Main St",
        "zipcode": "10001"
      },
      "company": {
        "bs": "harness real-time e-markets",
        "name": "Tech Solutions Inc",
        "catchPhrase": "Innovating the future"
      },
    }


@pytest.fixture
def test_post_data():
    return {
        "userId": 1,
        "title": "Тест поста",
        "body": "Тест етст етстетафы.",
    }


@pytest.fixture
def test_todo_data():
    return {
        "userId": 1,
        "title": "Fix bug in authentication module",
        "completed": False,
    }


@pytest.fixture
def test_comment_data():
    return {
        "postId": 1,
        "name": "fdsafsdaf",
        "email": "comment@example.com",
        "body": "hgfdhahhf.",
    }
