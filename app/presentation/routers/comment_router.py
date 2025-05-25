from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.core.schemas.comment_schemas import CommentDto, CreateCommentRequest
from app.core.services.comment_service import CommentService
from app.presentation.dependencies import get_comment_service

router = APIRouter(prefix="/api/comments", tags=["comments"])


@router.get("/post/{post_id}", response_model=List[CommentDto])
async def get_comments_for_post(
    post_id: int,
    comment_service: CommentService = Depends(get_comment_service)
):
    """
    Get all comments for a specific blog post
    """
    result = comment_service.get_comments_for_post(post_id)
    if result.is_failure:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result.value


@router.post("", response_model=CommentDto, status_code=201)
async def create_comment(
    request: CreateCommentRequest,
    comment_service: CommentService = Depends(get_comment_service)
):
    """
    Create a new comment
    """
    result = comment_service.create_comment(request)
    if result.is_failure:
        raise HTTPException(status_code=400, detail=result.error)
    
    return result.value


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    comment_service: CommentService = Depends(get_comment_service)
):
    """
    Delete a comment by its ID (admin only)
    """
    result = comment_service.delete_comment(comment_id)
    if result.is_failure:
        raise HTTPException(status_code=500, detail=result.error)
    
    return None
