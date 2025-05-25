from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class BlogPostDto(BaseModel):
    """
    Data Transfer Object for a blog post
    """
    id: Optional[int] = None
    title: str
    author: str
    date: datetime
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    
    class Config:
        from_attributes = True


class CreateBlogPostRequest(BaseModel):
    """
    Request model for creating a blog post
    """
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    tags: List[str] = []
    
    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title must not be empty')
        return v
    
    @field_validator('author')
    def author_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Author must not be empty')
        return v
    
    @field_validator('content')
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Content must not be empty')
        return v


class UpdateBlogPostRequest(BaseModel):
    """
    Request model for updating a blog post
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
