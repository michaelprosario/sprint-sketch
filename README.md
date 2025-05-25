# Sprint Sketch Blog Application

A full-featured blog application built with FastAPI, following clean architecture principles. This application implements the user stories from a sprint backlog.

## Features

- View blog posts in reverse chronological order
- Create and publish new blog posts
- Search for relevant content using keywords
- Add comments to blog posts
- Manage blog posts and comments (admin functionality)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create and apply database migrations (already done in the initial setup):
   ```bash
   alembic upgrade head
   ```

## Usage

1. Run the application:
   ```bash
   python run.py
   ```
   or
   ```bash
   uvicorn app.main:app --reload
   ```

2. Visit `http://localhost:8000` to see the home page
3. Visit `http://localhost:8000/docs` to see the API documentation and interact with the API

## Architecture

This application follows the principles of Clean Architecture:

- **Core Layer**: Contains business logic, domain models, and interfaces
  - Models: Domain entities
  - Interfaces: Repository interfaces (protocols)
  - Services: Business logic
  - Schemas: Data transfer objects (DTOs)

- **Infrastructure Layer**: Contains implementations of interfaces and technical details
  - Database: Database connection and models
  - Repositories: Implementation of repository interfaces

- **Presentation Layer**: Contains API endpoints and controllers
  - Routers: API endpoints
  - Dependencies: Dependency injection

## API Endpoints

### Blog Endpoints

- `GET /api/blogs`: Get all blog posts
- `GET /api/blogs/{blog_id}`: Get a specific blog post
- `POST /api/blogs`: Create a new blog post
- `PUT /api/blogs/{blog_id}`: Update a blog post
- `DELETE /api/blogs/{blog_id}`: Delete a blog post
- `GET /api/blogs/search?keyword={keyword}`: Search for blog posts

### Comment Endpoints

- `GET /api/comments/post/{post_id}`: Get all comments for a blog post
- `POST /api/comments`: Create a new comment
- `DELETE /api/comments/{comment_id}`: Delete a comment

## Requirements

- Python 3.x
- Gemini API key
- Excel file with sprint backlog data (`backlog.xlsx`)


Note: There's also a claude version of the script. ( see main_claude.py )