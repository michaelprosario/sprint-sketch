from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CommentDto(BaseModel):
    """
    Data Transfer Object for a comment
    """
    id: Optional[int] = None
    post_id: int
    name: str
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateCommentRequest(BaseModel):
    """
    Request model for creating a comment
    """
    post_id: int
    name: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=1000)
    
    @field_validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v
    
    @field_validator('message')
    def message_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Message must not be empty')
        return v
