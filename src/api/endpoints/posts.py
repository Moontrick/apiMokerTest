from typing import Optional, Dict, Any
from requests import Response
from ..client import APIClient
from ..models import Post, PostCreate, PostUpdate, Like
from ..utils.logger import get_logger

logger = get_logger(__name__)


class PostsAPI:

    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/posts"
        logger.info("PostsAPI initialized")

    def get_all_posts(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> Response:
        params = {}
        if page is not None:
            params["_page"] = page
        if limit is not None:
            params["_limit"] = limit
        if user_id is not None:
            params["userId"] = user_id
            
        logger.info(f"Getting all posts with params: {params}")
        return self.client.get(self.endpoint, params=params)

    def get_post_by_id(self, post_id: int) -> Response:
        endpoint = f"{self.endpoint}/{post_id}"
        logger.info(f"Getting post with ID: {post_id}")
        return self.client.get(endpoint)

    def create_post(self, post_data: Dict[str, Any]) -> Response:
        logger.info(f"Creating post with data: {post_data}")
        return self.client.post(self.endpoint, json=post_data)

    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> Response:
        endpoint = f"{self.endpoint}/{post_id}"
        logger.info(f"Updating post {post_id} with data: {post_data}")
        return self.client.put(endpoint, json=post_data)

    def partial_update_post(
        self,
        post_id: int,
        post_data: Dict[str, Any],
    ) -> Response:
        endpoint = f"{self.endpoint}/{post_id}"
        logger.info(f"Partially updating post {post_id} with data: {post_data}")
        return self.client.patch(endpoint, json=post_data)

    def delete_post(self, post_id: int) -> Response:
        endpoint = f"{self.endpoint}/{post_id}"
        logger.info(f"Deleting post {post_id}")
        return self.client.delete(endpoint)

    def get_post_likes(self, post_id: int) -> Response:
        endpoint = f"{self.endpoint}/{post_id}/likes"
        logger.info(f"Getting likes for post {post_id}")
        return self.client.get(endpoint)

    def add_like_to_post(
        self,
        post_id: int,
        like_data: Optional[Dict[str, Any]] = None,
    ) -> Response:
        endpoint = f"{self.endpoint}/{post_id}/likes"
        logger.info(f"Adding like to post {post_id} with data: {like_data}")
        return self.client.post(endpoint, json=like_data or {})
