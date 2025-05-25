from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.schemas.blog_schemas import BlogPostDto, CreateBlogPostRequest, UpdateBlogPostRequest
from app.core.services.blog_service import BlogService
from app.presentation.dependencies import get_blog_service

router = APIRouter(prefix="/api/blogs", tags=["blogs"])


@router.get("", response_model=List[BlogPostDto])
async def list_posts(blog_service: BlogService = Depends(get_blog_service)):
    """
    Get all blog posts in reverse chronological order
    """
    result = blog_service.list_posts()
    if result.is_failure:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result.value


@router.get("/search", response_model=List[BlogPostDto])
async def search_posts(
    keyword: str = Query(..., description="The keyword to search for"),
    blog_service: BlogService = Depends(get_blog_service)
):
    """
    Search for blog posts with the given keyword
    """
    result = blog_service.search_posts(keyword)
    if result.is_failure:
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.get("/{blog_id}", response_model=BlogPostDto)
async def get_post(blog_id: int, blog_service: BlogService = Depends(get_blog_service)):
    """
    Get a blog post by its ID
    """
    result = blog_service.get_post(blog_id)
    if result.is_failure:
        raise HTTPException(status_code=404, detail=result.error)
    
    return result.value


@router.post("", response_model=BlogPostDto, status_code=201)
async def create_post(
    request: CreateBlogPostRequest,
    blog_service: BlogService = Depends(get_blog_service)
):
    """
    Create a new blog post
    """
    result = blog_service.create_post(request)
    if result.is_failure:
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.put("/{blog_id}", response_model=BlogPostDto)
async def update_post(
    blog_id: int,
    request: UpdateBlogPostRequest,
    blog_service: BlogService = Depends(get_blog_service)
):
    """
    Update an existing blog post
    """
    result = blog_service.update_post(blog_id, request)
    if result.is_failure:
        if "not found" in result.error:
            raise HTTPException(status_code=404, detail=result.error)
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.delete("/{blog_id}", status_code=204)
async def delete_post(blog_id: int, blog_service: BlogService = Depends(get_blog_service)):
    """
    Delete a blog post by its ID
    """
    result = blog_service.delete_post(blog_id)
    if result.is_failure:
        if "not found" in result.error:
            raise HTTPException(status_code=404, detail=result.error)
        raise HTTPException(status_code=500, detail=result.error)
    
    return None
