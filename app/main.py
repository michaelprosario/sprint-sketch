import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.infrastructure.database.connection import create_tables
from app.infrastructure.database.connection import get_db
from app.infrastructure.sample_data import load_sample_data
from app.presentation.routers import blog_router, comment_router
from app.infrastructure.backlog_reader import read_backlog_from_excel

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

# Include routers
app.include_router(blog_router.router)
app.include_router(comment_router.router)

# Create templates directory for simple frontend
os.makedirs("templates", exist_ok=True)

# Setup templates
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
except:
    print("Static files directory not found. Frontend will be limited.")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Root endpoint returning a simple HTML page
    """
    # For now, return a simple HTML page
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blog API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                color: #333;
            }
            .endpoint {
                background-color: #f4f4f4;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }
            .method {
                font-weight: bold;
                color: #0066cc;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Blog API</h1>
            <p>Welcome to the Blog API. Use the following endpoints to interact with the blog:</p>
            
            <h2>Blog Endpoints</h2>
            <div class="endpoint">
                <p><span class="method">GET</span> /api/blogs - Get all blog posts</p>
            </div>
            <div class="endpoint">
                <p><span class="method">GET</span> /api/blogs/{blog_id} - Get a specific blog post</p>
            </div>
            <div class="endpoint">
                <p><span class="method">POST</span> /api/blogs - Create a new blog post</p>
            </div>
            <div class="endpoint">
                <p><span class="method">PUT</span> /api/blogs/{blog_id} - Update a blog post</p>
            </div>
            <div class="endpoint">
                <p><span class="method">DELETE</span> /api/blogs/{blog_id} - Delete a blog post</p>
            </div>
            <div class="endpoint">
                <p><span class="method">GET</span> /api/blogs/search?keyword={keyword} - Search for blog posts</p>
            </div>
            
            <h2>Comment Endpoints</h2>
            <div class="endpoint">
                <p><span class="method">GET</span> /api/comments/post/{post_id} - Get comments for a blog post</p>
            </div>
            <div class="endpoint">
                <p><span class="method">POST</span> /api/comments - Create a new comment</p>
            </div>
            <div class="endpoint">
                <p><span class="method">DELETE</span> /api/comments/{comment_id} - Delete a comment</p>
            </div>
            
            <h2>Documentation</h2>
            <p>Full API documentation is available at <a href="/docs">/docs</a> or <a href="/redoc">/redoc</a>.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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