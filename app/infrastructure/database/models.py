from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.core.models.blog import Blog
from app.core.models.comment import Comment
from app.infrastructure.database.connection import Base


# Association table for blog tags (many-to-many relationship)
blog_tag_association = Table(
    'blog_tag',
    Base.metadata,
    Column('blog_id', Integer, ForeignKey('blogs.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class TagModel(Base):
    """
    SQLAlchemy model for a tag
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)


class BlogModel(Base):
    """
    SQLAlchemy model for a blog post
    """
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    author = Column(String(100))
    date = Column(DateTime)
    content = Column(Text)
    excerpt = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    
    # Relationships
    tags = relationship("TagModel", secondary=blog_tag_association)
    comments = relationship("CommentModel", back_populates="blog")

    def to_domain(self) -> Blog:
        """
        Convert SQLAlchemy model to domain model
        """
        return Blog(
            id=self.id,
            title=self.title,
            author=self.author,
            date=self.date,
            content=self.content,
            excerpt=self.excerpt,
            category=self.category,
            tags=[tag.name for tag in self.tags]
        )

    @classmethod
    def from_domain(cls, blog: Blog) -> 'BlogModel':
        """
        Create SQLAlchemy model from domain model
        """
        return cls(
            id=blog.id,
            title=blog.title,
            author=blog.author,
            date=blog.date,
            content=blog.content,
            excerpt=blog.excerpt,
            category=blog.category,
            # Tags are handled separately
        )


class CommentModel(Base):
    """
    SQLAlchemy model for a comment
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blogs.id"))
    name = Column(String(100))
    message = Column(Text)
    created_at = Column(DateTime)
    
    # Relationships
    blog = relationship("BlogModel", back_populates="comments")

    def to_domain(self) -> Comment:
        """
        Convert SQLAlchemy model to domain model
        """
        return Comment(
            id=self.id,
            post_id=self.post_id,
            name=self.name,
            message=self.message,
            created_at=self.created_at
        )

    @classmethod
    def from_domain(cls, comment: Comment) -> 'CommentModel':
        """
        Create SQLAlchemy model from domain model
        """
        return cls(
            id=comment.id,
            post_id=comment.post_id,
            name=comment.name,
            message=comment.message,
            created_at=comment.created_at
        )
