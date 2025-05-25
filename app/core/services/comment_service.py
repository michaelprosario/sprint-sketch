from datetime import datetime, timedelta
from typing import List
from app.core.interfaces.comment_repository import CommentRepository
from app.core.models.comment import Comment
from app.core.result import Result
from app.core.schemas.comment_schemas import CreateCommentRequest, CommentDto


class CommentService:
    """
    Service for comment-related operations
    """
    
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
    
    def get_comments_for_post(self, post_id: int) -> Result[List[CommentDto]]:
        """
        Get all comments for a specific blog post
        """
        try:
            comments = self.comment_repository.get_by_post_id(post_id)
            comment_dtos = [CommentDto.model_validate(comment) for comment in comments]
            return Result.success(comment_dtos)
        except Exception as e:
            return Result.failure(f"Failed to get comments: {str(e)}")
    
    def create_comment(self, request: CreateCommentRequest) -> Result[CommentDto]:
        """
        Create a new comment
        """
        try:
            # Create a Comment domain model from the request
            comment = Comment(
                post_id=request.post_id,
                name=request.name,
                message=request.message,
                created_at=datetime.now()
            )
            
            # Check for duplicate comments within a short time window
            recent_comments = self.comment_repository.get_by_post_id(request.post_id)
            for recent_comment in recent_comments:
                if (recent_comment.name == comment.name and
                        recent_comment.message == comment.message and
                        datetime.now() - recent_comment.created_at < timedelta(minutes=5)):
                    return Result.failure("Duplicate comment detected. Please wait before posting the same comment again.")
            
            # Save the comment
            created_comment = self.comment_repository.create(comment)
            
            # Return the created comment as a DTO
            return Result.success(CommentDto.model_validate(created_comment))
        except ValueError as e:
            return Result.failure(f"Validation error: {str(e)}")
        except Exception as e:
            return Result.failure(f"Failed to create comment: {str(e)}")
    
    def delete_comment(self, comment_id: int) -> Result[bool]:
        """
        Delete a comment by its ID
        """
        try:
            result = self.comment_repository.delete(comment_id)
            if not result:
                return Result.failure(f"Failed to delete comment with ID {comment_id}")
            
            return Result.success(True)
        except Exception as e:
            return Result.failure(f"Failed to delete comment: {str(e)}")
