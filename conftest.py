import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent
SRC_PATH = str(PROJECT_ROOT / "src")

if SRC_PATH in sys.path:
    sys.path.remove(SRC_PATH)
sys.path.insert(0, SRC_PATH)

load_dotenv()


def pytest_configure(config):
    allure_dir = PROJECT_ROOT / "allure-results"
    allure_dir.mkdir(exist_ok=True)


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "test_users" in str(item.fspath):
            item.add_marker(pytest.mark.users)
        elif "test_posts" in str(item.fspath):
            item.add_marker(pytest.mark.posts)
        elif "test_todos" in str(item.fspath):
            item.add_marker(pytest.mark.todos)
        elif "test_comments" in str(item.fspath):
            item.add_marker(pytest.mark.comments)

        if "test_get" in item.name:
            item.add_marker(pytest.mark.get)
        elif "test_post" in item.name:
            item.add_marker(pytest.mark.post)
        elif "test_put" in item.name:
            item.add_marker(pytest.mark.put)
        elif "test_patch" in item.name:
            item.add_marker(pytest.mark.patch)
        elif "test_delete" in item.name:
            item.add_marker(pytest.mark.delete)

        if "test_" in item.name and "error" not in item.name:
            item.add_marker(pytest.mark.regression)
