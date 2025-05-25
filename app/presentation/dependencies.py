from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.services.blog_service import BlogService
from app.core.services.comment_service import CommentService
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.blog_repository import SqlAlchemyBlogRepository
from app.infrastructure.repositories.comment_repository import SqlAlchemyCommentRepository


def get_blog_repository(db: Session = Depends(get_db)) -> SqlAlchemyBlogRepository:
    """
    Get a BlogRepository instance
    """
    return SqlAlchemyBlogRepository(db)


def get_comment_repository(db: Session = Depends(get_db)) -> SqlAlchemyCommentRepository:
    """
    Get a CommentRepository instance
    """
    return SqlAlchemyCommentRepository(db)


def get_blog_service(
    blog_repository: SqlAlchemyBlogRepository = Depends(get_blog_repository)
) -> BlogService:
    """
    Get a BlogService instance
    """
    return BlogService(blog_repository)


def get_comment_service(
    comment_repository: SqlAlchemyCommentRepository = Depends(get_comment_repository)
) -> CommentService:
    """
    Get a CommentService instance
    """
    return CommentService(comment_repository)
