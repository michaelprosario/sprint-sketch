from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.models.blog import Blog
from app.infrastructure.database.models import BlogModel, TagModel


class SqlAlchemyBlogRepository:
    """
    Implementation of the BlogRepository interface using SQLAlchemy
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Blog]:
        """
        Get all blog posts
        """
        blog_models = self.db.query(BlogModel).all()
        return [model.to_domain() for model in blog_models]
    
    def get_by_id(self, blog_id: int) -> Optional[Blog]:
        """
        Get a blog post by its ID
        """
        blog_model = self.db.query(BlogModel).filter(BlogModel.id == blog_id).first()
        return blog_model.to_domain() if blog_model else None
    
    def create(self, blog: Blog) -> Blog:
        """
        Create a new blog post
        """
        # Create the blog model
        blog_model = BlogModel.from_domain(blog)
        
        # Handle tags
        self._set_tags(blog_model, blog.tags)
        
        # Add and commit to the database
        self.db.add(blog_model)
        self.db.commit()
        self.db.refresh(blog_model)
        
        return blog_model.to_domain()
    
    def update(self, blog: Blog) -> Optional[Blog]:
        """
        Update an existing blog post
        """
        # Check if the blog post exists
        blog_model = self.db.query(BlogModel).filter(BlogModel.id == blog.id).first()
        if not blog_model:
            return None
        
        # Update the fields
        blog_model.title = blog.title
        blog_model.author = blog.author
        blog_model.content = blog.content
        blog_model.excerpt = blog.excerpt
        blog_model.category = blog.category
        
        # Handle tags
        self._set_tags(blog_model, blog.tags)
        
        # Commit changes
        self.db.commit()
        self.db.refresh(blog_model)
        
        return blog_model.to_domain()
    
    def delete(self, blog_id: int) -> bool:
        """
        Delete a blog post by its ID
        """
        blog_model = self.db.query(BlogModel).filter(BlogModel.id == blog_id).first()
        if not blog_model:
            return False
        
        self.db.delete(blog_model)
        self.db.commit()
        
        return True
    
    def search_posts(self, keyword: str) -> List[Blog]:
        """
        Search for blog posts with the given keyword in the title and excerpt
        """
        blog_models = self.db.query(BlogModel).filter(
            or_(
                BlogModel.title.contains(keyword),
                BlogModel.excerpt.contains(keyword)
            )
        ).all()
        
        return [model.to_domain() for model in blog_models]
    
    def search_content(self, keyword: str) -> List[Blog]:
        """
        Search for blog posts with the given keyword in the content
        """
        blog_models = self.db.query(BlogModel).filter(
            BlogModel.content.contains(keyword)
        ).all()
        
        return [model.to_domain() for model in blog_models]
    
    def _set_tags(self, blog_model: BlogModel, tag_names: List[str]):
        """
        Helper method to set tags for a blog post
        """
        # Clear existing tags
        blog_model.tags = []
        
        # Add new tags
        for tag_name in tag_names:
            tag = self.db.query(TagModel).filter(TagModel.name == tag_name).first()
            if not tag:
                tag = TagModel(name=tag_name)
                self.db.add(tag)
            
            blog_model.tags.append(tag)
