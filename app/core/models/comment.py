from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """
    Domain model representing a comment on a blog post
    """
    post_id: int
    name: str
    message: str
    created_at: datetime
    id: Optional[int] = None
    
    def __post_init__(self):
        # Validation logic
        if not self.name:
            raise ValueError("Comment name cannot be empty")
        if not self.message:
            raise ValueError("Comment message cannot be empty")
