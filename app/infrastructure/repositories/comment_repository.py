from typing import List
from sqlalchemy.orm import Session
from app.core.models.comment import Comment
from app.infrastructure.database.models import CommentModel


class SqlAlchemyCommentRepository:
    """
    Implementation of the CommentRepository interface using SQLAlchemy
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        """
        Get all comments for a specific blog post
        """
        comment_models = self.db.query(CommentModel).filter(
            CommentModel.post_id == post_id
        ).order_by(CommentModel.created_at).all()
        
        return [model.to_domain() for model in comment_models]
    
    def create(self, comment: Comment) -> Comment:
        """
        Create a new comment
        """
        comment_model = CommentModel.from_domain(comment)
        
        self.db.add(comment_model)
        self.db.commit()
        self.db.refresh(comment_model)
        
        return comment_model.to_domain()
    
    def delete(self, comment_id: int) -> bool:
        """
        Delete a comment by its ID
        """
        comment_model = self.db.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        
        if not comment_model:
            return False
        
        self.db.delete(comment_model)
        self.db.commit()
        
        return True
