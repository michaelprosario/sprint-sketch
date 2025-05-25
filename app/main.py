import os
import uvicorn
import markdown
from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.infrastructure.database.connection import create_tables
from app.infrastructure.database.connection import get_db
from app.infrastructure.sample_data import load_sample_data
from app.presentation.routers import blog_router, comment_router
from app.infrastructure.backlog_reader import read_backlog_from_excel
from app.core.services.blog_service import BlogService
from app.core.services.comment_service import CommentService
from app.presentation.dependencies import get_blog_service, get_comment_service

# Create the FastAPI application
app = FastAPI(
    title="Blog API",
    description="A blog API supporting viewing, creating, and searching posts, as well as commenting",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(blog_router.router)
app.include_router(comment_router.router)

# Create templates directory for simple frontend
os.makedirs("templates", exist_ok=True)

# Setup templates and static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
except Exception as e:
    print(f"Static files setup error: {e}")
    print("Frontend will be limited.")
    templates = None

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request, 
    blog_service: BlogService = Depends(get_blog_service)
):
    """
    Home page displaying blog posts
    """
    if templates is None:
        return HTMLResponse(content="Templates not available")
    
    result = blog_service.list_posts()
    if result.is_failure:
        posts = []
    else:
        posts = result.value
    
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})


@app.get("/blog/{blog_id}", response_class=HTMLResponse)
async def blog_detail(
    request: Request, 
    blog_id: int,
    blog_service: BlogService = Depends(get_blog_service),
    comment_service: CommentService = Depends(get_comment_service)
):
    """
    Blog post detail page
    """
    if templates is None:
        return HTMLResponse(content="Templates not available")
    
    blog_result = blog_service.get_post(blog_id)
    if blog_result.is_failure:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    post = blog_result.value
    
    # Convert markdown content to HTML
    try:
        post.content = markdown.markdown(post.content)
    except:
        # If markdown conversion fails, use the raw content
        pass
    
    comments_result = comment_service.get_comments_for_post(blog_id)
    if comments_result.is_failure:
        comments = []
    else:
        comments = comments_result.value
    
    return templates.TemplateResponse(
        "post.html", 
        {
            "request": request, 
            "post": post,
            "comments": comments
        }
    )


@app.get("/create", response_class=HTMLResponse)
async def create_post_page(request: Request):
    """
    Create post page
    """
    if templates is None:
        return HTMLResponse(content="Templates not available")
    
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.get("/search", response_class=HTMLResponse)
async def search_page(
    request: Request,
    keyword: str = Query(...),
    blog_service: BlogService = Depends(get_blog_service)
):
    """
    Search results page
    """
    if templates is None:
        return HTMLResponse(content="Templates not available")
    
    result = blog_service.search_posts(keyword)
    if result.is_failure:
        posts = []
    else:
        posts = result.value
    
    return templates.TemplateResponse(
        "search.html", 
        {
            "request": request, 
            "posts": posts,
            "keyword": keyword
        }
    )


@app.get("/backlog", response_class=JSONResponse)
async def read_backlog():
    """
    Read the sprint backlog from the Excel file
    """
    backlog_items = read_backlog_from_excel("backlog.xlsx")
    return {"backlog": backlog_items}


@app.on_event("startup")
async def startup_event():
    """
    Create database tables and load sample data on startup
    """
    create_tables()
    
    # Load sample data
    db = next(get_db())
    load_sample_data(db)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)