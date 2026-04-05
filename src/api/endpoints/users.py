from typing import Optional, List, Dict, Any
from requests import Response
from ..client import APIClient
from ..models import User, UserCreate, UserUpdate
from ..utils.logger import get_logger

logger = get_logger(__name__)


class UsersAPI:
    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/users"
        logger.info("UsersAPI initialized")

    def get_all_users(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Response:
        params = {}
        if page is not None:
            params["_page"] = page
        if limit is not None:
            params["_limit"] = limit
            
        logger.info(f"Getting all users with params: {params}")
        return self.client.get(self.endpoint, params=params)

    def get_user_by_id(self, user_id: int) -> Response:
        endpoint = f"{self.endpoint}/{user_id}"
        logger.info(f"Getting user with ID: {user_id}")
        return self.client.get(endpoint)

    def create_user(self, user_data: Dict[str, Any]) -> Response:
        logger.info(f"Creating user with data: {user_data}")
        return self.client.post(self.endpoint, json=user_data)

    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Response:
        endpoint = f"{self.endpoint}/{user_id}"
        logger.info(f"Updating user {user_id} with data: {user_data}")
        return self.client.put(endpoint, json=user_data)

    def partial_update_user(
        self,
        user_id: int,
        user_data: Dict[str, Any],
    ) -> Response:
        endpoint = f"{self.endpoint}/{user_id}"
        logger.info(f"Partially updating user {user_id} with data: {user_data}")
        return self.client.patch(endpoint, json=user_data)

    def delete_user(self, user_id: int) -> Response:
        endpoint = f"{self.endpoint}/{user_id}"
        logger.info(f"Deleting user {user_id}")
        return self.client.delete(endpoint)
