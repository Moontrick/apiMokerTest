"""Endpoints package for API endpoint wrappers."""
from .users import UsersAPI
from .posts import PostsAPI
from .todos import TodosAPI
from .comments import CommentsAPI

__all__ = ["UsersAPI", "PostsAPI", "TodosAPI", "CommentsAPI"]
