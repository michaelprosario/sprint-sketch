from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Blog:
    """
    Domain model representing a blog post
    """
    title: str
    author: str
    date: datetime
    content: str
    id: Optional[int] = None
    excerpt: Optional[str] = None
    category: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Validation logic
        if not self.title:
            raise ValueError("Blog title cannot be empty")
        if not self.author:
            raise ValueError("Blog author cannot be empty")
        if not self.content:
            raise ValueError("Blog content cannot be empty")
        
        # Create excerpt if not provided
        if not self.excerpt:
            self.excerpt = self.content[:200] + "..." if len(self.content) > 200 else self.content
