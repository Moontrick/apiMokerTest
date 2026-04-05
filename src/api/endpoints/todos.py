from typing import Optional, Dict, Any
from requests import Response
from ..client import APIClient
from ..models import Todo, TodoCreate, TodoUpdate
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TodosAPI:
    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/todos"
        logger.info("TodosAPI initialized")

    def get_all_todos(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        completed: Optional[bool] = None,
    ) -> Response:
        params = {}
        if page is not None:
            params["_page"] = page
        if limit is not None:
            params["_limit"] = limit
        if completed is not None:
            params["completed"] = completed
            
        logger.info(f"Getting all todos with params: {params}")
        return self.client.get(self.endpoint, params=params)

    def get_todo_by_id(self, todo_id: int) -> Response:
        endpoint = f"{self.endpoint}/{todo_id}"
        logger.info(f"Getting todo with ID: {todo_id}")
        return self.client.get(endpoint)

    def create_todo(self, todo_data: Dict[str, Any]) -> Response:
        logger.info(f"Creating todo with data: {todo_data}")
        return self.client.post(self.endpoint, json=todo_data)

    def update_todo(self, todo_id: int, todo_data: Dict[str, Any]) -> Response:
        endpoint = f"{self.endpoint}/{todo_id}"
        logger.info(f"Updating todo {todo_id} with data: {todo_data}")
        return self.client.put(endpoint, json=todo_data)

    def partial_update_todo(
        self,
        todo_id: int,
        todo_data: Dict[str, Any],
    ) -> Response:
        endpoint = f"{self.endpoint}/{todo_id}"
        logger.info(f"Partially updating todo {todo_id} with data: {todo_data}")
        return self.client.patch(endpoint, json=todo_data)

    def delete_todo(self, todo_id: int) -> Response:
        endpoint = f"{self.endpoint}/{todo_id}"
        logger.info(f"Deleting todo {todo_id}")
        return self.client.delete(endpoint)
