from datetime import datetime
from typing import List, Optional
from app.core.interfaces.blog_repository import BlogRepository
from app.core.models.blog import Blog
from app.core.result import Result
from app.core.schemas.blog_schemas import CreateBlogPostRequest, UpdateBlogPostRequest, BlogPostDto


class BlogService:
    """
    Service for blog-related operations
    """
    
    def __init__(self, blog_repository: BlogRepository):
        self.blog_repository = blog_repository
    
    def list_posts(self) -> Result[List[BlogPostDto]]:
        """
        Get all blog posts in reverse chronological order
        """
        try:
            blogs = self.blog_repository.get_all()
            # Sort blogs by date in reverse chronological order
            blogs.sort(key=lambda x: x.date, reverse=True)
            # Convert to DTOs
            blog_dtos = [BlogPostDto.model_validate(blog) for blog in blogs]
            return Result.success(blog_dtos)
        except Exception as e:
            return Result.failure(f"Failed to list posts: {str(e)}")
    
    def get_post(self, blog_id: int) -> Result[BlogPostDto]:
        """
        Get a blog post by its ID
        """
        try:
            blog = self.blog_repository.get_by_id(blog_id)
            if not blog:
                return Result.failure(f"Blog post with ID {blog_id} not found")
            return Result.success(BlogPostDto.model_validate(blog))
        except Exception as e:
            return Result.failure(f"Failed to get post: {str(e)}")
    
    def create_post(self, request: CreateBlogPostRequest) -> Result[BlogPostDto]:
        """
        Create a new blog post
        """
        try:
            # Create a Blog domain model from the request
            blog = Blog(
                title=request.title,
                author=request.author,
                content=request.content,
                date=datetime.now(),
                category=request.category,
                tags=request.tags
            )
            
            # Save the blog post
            created_blog = self.blog_repository.create(blog)
            
            # Return the created blog post as a DTO
            return Result.success(BlogPostDto.model_validate(created_blog))
        except ValueError as e:
            return Result.failure(f"Validation error: {str(e)}")
        except Exception as e:
            return Result.failure(f"Failed to create post: {str(e)}")
    
    def update_post(self, blog_id: int, request: UpdateBlogPostRequest) -> Result[BlogPostDto]:
        """
        Update an existing blog post
        """
        try:
            # Get the existing blog post
            existing_blog = self.blog_repository.get_by_id(blog_id)
            if not existing_blog:
                return Result.failure(f"Blog post with ID {blog_id} not found")
            
            # Update the fields that are provided in the request
            if request.title is not None:
                existing_blog.title = request.title
            if request.author is not None:
                existing_blog.author = request.author
            if request.content is not None:
                existing_blog.content = request.content
                # Update excerpt as well
                existing_blog.excerpt = request.content[:200] + "..." if len(request.content) > 200 else request.content
            if request.category is not None:
                existing_blog.category = request.category
            if request.tags is not None:
                existing_blog.tags = request.tags
            
            # Save the updated blog post
            updated_blog = self.blog_repository.update(existing_blog)
            if not updated_blog:
                return Result.failure(f"Failed to update blog post with ID {blog_id}")
            
            # Return the updated blog post as a DTO
            return Result.success(BlogPostDto.model_validate(updated_blog))
        except ValueError as e:
            return Result.failure(f"Validation error: {str(e)}")
        except Exception as e:
            return Result.failure(f"Failed to update post: {str(e)}")
    
    def delete_post(self, blog_id: int) -> Result[bool]:
        """
        Delete a blog post by its ID
        """
        try:
            # Check if the blog post exists
            existing_blog = self.blog_repository.get_by_id(blog_id)
            if not existing_blog:
                return Result.failure(f"Blog post with ID {blog_id} not found")
            
            # Delete the blog post
            result = self.blog_repository.delete(blog_id)
            if not result:
                return Result.failure(f"Failed to delete blog post with ID {blog_id}")
            
            return Result.success(True)
        except Exception as e:
            return Result.failure(f"Failed to delete post: {str(e)}")
    
    def search_posts(self, keyword: str) -> Result[List[BlogPostDto]]:
        """
        Search for blog posts with the given keyword
        """
        try:
            if not keyword.strip():
                return Result.failure("Search keyword cannot be empty")
            
            # Search in titles and excerpts
            title_excerpt_results = self.blog_repository.search_posts(keyword)
            
            # Search in content
            content_results = self.blog_repository.search_content(keyword)
            
            # Combine results and remove duplicates
            all_results = {}
            for blog in title_excerpt_results + content_results:
                if blog.id not in all_results:
                    all_results[blog.id] = blog
            
            # Convert to DTOs
            blog_dtos = [BlogPostDto.model_validate(blog) for blog in all_results.values()]
            
            return Result.success(blog_dtos)
        except Exception as e:
            return Result.failure(f"Failed to search posts: {str(e)}")
