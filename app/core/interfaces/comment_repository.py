from typing import Protocol, List, Optional
from app.core.models.comment import Comment


class CommentRepository(Protocol):
    """
    Interface for comment repository operations
    """
    
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        """Get all comments for a specific blog post"""
        ...
        
    def create(self, comment: Comment) -> Comment:
        """Create a new comment"""
        ...
        
    def delete(self, comment_id: int) -> bool:
        """Delete a comment by its ID"""
        ...
