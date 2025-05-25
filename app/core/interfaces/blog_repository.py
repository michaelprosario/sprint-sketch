from typing import Protocol, List, Optional
from app.core.models.blog import Blog


class BlogRepository(Protocol):
    """
    Interface for blog repository operations
    """
    
    def get_all(self) -> List[Blog]:
        """Get all blog posts"""
        ...
        
    def get_by_id(self, blog_id: int) -> Optional[Blog]:
        """Get a blog post by its ID"""
        ...
        
    def create(self, blog: Blog) -> Blog:
        """Create a new blog post"""
        ...
        
    def update(self, blog: Blog) -> Optional[Blog]:
        """Update an existing blog post"""
        ...
        
    def delete(self, blog_id: int) -> bool:
        """Delete a blog post by its ID"""
        ...
        
    def search_posts(self, keyword: str) -> List[Blog]:
        """Search for blog posts with the given keyword in the title and excerpt"""
        ...
        
    def search_content(self, keyword: str) -> List[Blog]:
        """Search for blog posts with the given keyword in the content"""
        ...
