from typing import Optional, Dict, Any
from requests import Response
from ..client import APIClient
from ..models import Comment, CommentCreate, CommentUpdate
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CommentsAPI:
    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/comments"
        logger.info("CommentsAPI initialized")

    def get_all_comments(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        post_id: Optional[int] = None,
    ) -> Response:
        params = {}
        if page is not None:
            params["_page"] = page
        if limit is not None:
            params["_limit"] = limit
        if post_id is not None:
            params["postId"] = post_id
            
        logger.info(f"Getting all comments with params: {params}")
        return self.client.get(self.endpoint, params=params)

    def get_comment_by_id(self, comment_id: int) -> Response:

        endpoint = f"{self.endpoint}/{comment_id}"
        logger.info(f"Getting comment with ID: {comment_id}")
        return self.client.get(endpoint)

    def create_comment(self, comment_data: Dict[str, Any]) -> Response:

        logger.info(f"Creating comment with data: {comment_data}")
        return self.client.post(self.endpoint, json=comment_data)

    def update_comment(
        self,
        comment_id: int,
        comment_data: Dict[str, Any],
    ) -> Response:
        endpoint = f"{self.endpoint}/{comment_id}"
        logger.info(f"Updating comment {comment_id} with data: {comment_data}")
        return self.client.put(endpoint, json=comment_data)

    def partial_update_comment(
        self,
        comment_id: int,
        comment_data: Dict[str, Any],
    ) -> Response:
        endpoint = f"{self.endpoint}/{comment_id}"
        logger.info(f"Partially updating comment {comment_id} with data: {comment_data}")
        return self.client.patch(endpoint, json=comment_data)

    def delete_comment(self, comment_id: int) -> Response:
        endpoint = f"{self.endpoint}/{comment_id}"
        logger.info(f"Deleting comment {comment_id}")
        return self.client.delete(endpoint)
