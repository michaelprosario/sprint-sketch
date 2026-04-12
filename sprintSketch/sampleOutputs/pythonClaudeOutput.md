Reading sprint backlog from: backlog.xlsx
========================================
SPRINT BACKLOG
========================================

--- Item #1 ---
Work Item ID: 1
Story Name: view blog
Story: As a visitor, I want to read blog posts so that I can stay informed and engaged.
Done Conditions: - The homepage displays a list of published blog posts.
- Each blog post has a title, author name, date, and content.
- Clicking on a post opens a detailed view with the full content.
- Posts are displayed in reverse chronological order.
----------------------------------------
===============
## User Story Tasks: View Blog

### Core Package Tasks

**Domain Models & Schemas**
- Create `BlogPost` domain model with id, title, author_name, published_date, content, and is_published fields using dataclass
- Create `BlogPostDto` Pydantic schema for API responses with proper validation
- Create `BlogPostListDto` schema for homepage list view containing summary fields

**Service Interfaces**
- Define `BlogPostRepository` protocol with methods for getting published posts and retrieving by ID
- Create `BlogPostService` business service to handle blog post retrieval logic with proper Result[T] return types

**Business Logic**
- Implement `get_published_posts()` method in BlogPostService to return posts in reverse chronological order
- Implement `get_post_by_id()` method in BlogPostService with validation for published status

### Infrastructure Package Tasks

**Database Models**
- Create `BlogPostModel` SQLAlchemy model with proper column types and indexes for efficient querying
- Implement `to_domain()` and `from_domain()` conversion methods on BlogPostModel
- Create database migration for blog_posts table with published_date index

**Repository Implementation**
- Implement `SqlAlchemyBlogPostRepository` with method to fetch published posts ordered by date descending
- Implement repository method to get single blog post by ID with published status filtering

### Web Framework Tasks

**API Endpoints**
- Create GET `/api/blog/posts` endpoint to return list of published blog posts using BlogPostService
- Create GET `/api/blog/posts/{id}` endpoint to return detailed blog post view
- Implement proper error handling for non-existent or unpublished posts with appropriate HTTP status codes

**Dependency Injection**
- Set up dependency injection for BlogPostService in FastAPI dependencies module

### Testing Tasks

**Unit Tests**
- Write unit tests for BlogPostService methods using mocked repository dependencies
- Test business logic for filtering published posts and chronological ordering

**Integration Tests**
- Create integration tests for BlogPostRepository with test database setup
- Write API endpoint tests using TestClient to verify complete request/response flow

--- Item #2 ---
Work Item ID: 2
Story Name: create posts
Story: As an author, I want to create and publish blog posts so that I can share my thoughts and insights.
Done Conditions: - Authors can access a “Create Post” page.
- The post editor allows formatting text, adding images, and previewing content.
- There is a “Publish” button that makes the post publicly visible.
- Posts must include a title, body, and category.
- Authors receive confirmation upon successful publication.
----------------------------------------
===============
## User Story Tasks: Create Posts

### Core Package Tasks

• Create `Post` domain model in `core/models/` with fields for id, title, body, category, author_id, published status, and timestamps
• Define `PostRepository` protocol in `core/interfaces/` with methods for create, get_by_id, get_by_author, and update operations
• Implement `PostService` in `core/services/` with business logic for creating, validating, and publishing posts
• Create request/response DTOs in `core/schemas/` including `CreatePostRequest`, `UpdatePostRequest`, and `PostDto`
• Add business validation rules to `PostService` ensuring title, body, and category are required for publication
• Implement post publishing logic in `PostService` that updates post status and sets publication timestamp

### Infrastructure Package Tasks

• Create `PostModel` SQLAlchemy model in `infrastructure/database/` with proper column types and relationships
• Implement `SqlAlchemyPostRepository` in `infrastructure/repositories/` following the repository pattern
• Add domain model conversion methods (`to_domain()` and `from_domain()`) to `PostModel`
• Create database migration for posts table using Alembic
• Add database indexes for common query patterns (author_id, category, published status)

### Web Framework Tasks

• Create POST endpoint `/posts` for creating new posts that accepts `CreatePostRequest`
• Implement GET endpoint `/posts/create` to serve the create post page (if serving HTML)
• Add PUT endpoint `/posts/{post_id}/publish` for publishing draft posts
• Create GET endpoint `/posts/{post_id}/preview` for previewing post content before publication
• Implement dependency injection for `PostService` in the dependencies module
• Add proper error handling and HTTP status codes for all post-related endpoints

### Testing Tasks

• Write unit tests for `PostService` covering post creation, validation, and publishing scenarios
• Create integration tests for `SqlAlchemyPostRepository` using test database fixtures
• Add API endpoint tests using TestClient for all post creation and publishing flows
• Test validation scenarios including missing required fields and invalid data
• Write tests for post preview functionality and publication confirmation responses

### Additional Implementation Tasks

• Add post formatting support (if needed) by extending the `Post` domain model with formatting metadata
• Implement image upload handling (if required) by adding image URL fields to post model
• Create success confirmation response structure for post publication
• Add logging for post creation and publication events
• Implement proper error messages for validation failures and business rule violations

--- Item #3 ---
Work Item ID: 3
Story Name: search blog
Story: As a visitor, I want to search for blog posts so that I can easily find relevant content.
Done Conditions: - A search bar is present on the blog homepage.
- Users can enter keywords to find posts.
- Search results display matching blog posts with titles and excerpts.
- Clicking a result navigates to the full blog post.
----------------------------------------
===============
# Search Blog - User Story Tasks

## Core Package Tasks

• Create `BlogPost` domain model with fields for id, title, content, excerpt, published_date, and tags
• Define `BlogSearchRepository` protocol with methods for searching posts by keywords and retrieving post by id
• Implement `BlogSearchService` with business logic for keyword search, result ranking, and post retrieval
• Create request/response DTOs: `BlogSearchRequest`, `BlogSearchResult`, and `BlogPostDto` schemas
• Add unit tests for `BlogSearchService` using mocked repository dependencies

## Infrastructure Package Tasks

• Create `BlogPostModel` SQLAlchemy model with proper indexing on searchable fields (title, content, tags)
• Implement `SqlAlchemyBlogSearchRepository` with full-text search capabilities using database search features
• Add domain model conversion methods (`to_domain()` and `from_domain()`) for `BlogPostModel`
• Create database migration for blog posts table with search indexes
• Write integration tests for repository implementation using test database

## Web Framework Tasks

• Create FastAPI router with GET endpoint `/api/blog/search` accepting query parameters for search terms
• Implement GET endpoint `/api/blog/posts/{id}` for retrieving individual blog posts
• Set up dependency injection for `BlogSearchService` in dependencies module
• Add request validation and error handling for search endpoints
• Write API endpoint tests using FastAPI TestClient

## Frontend/Template Tasks

• Add search bar component to blog homepage with input field and search button
• Implement search results page displaying post titles, excerpts, and publication dates
• Create JavaScript functionality to handle search form submission and results display
• Add click handlers to navigate from search results to full blog post pages
• Style search components to match existing blog design

--- Item #4 ---
Work Item ID: 4
Story Name: add comments
Story: As a visitor, I want to leave comments on blog posts so that I can engage in discussions.
Done Conditions: - Each blog post includes a comment section.
- Visitors can submit comments with their name and message.
- Comments appear in chronological order under the post.
- The system prevents submission of empty or duplicate comments.
----------------------------------------
===============
## User Story Tasks: Add Comments

### Core Package Tasks

- Create `Comment` domain model in `core/models/` with fields for id, blog_post_id, author_name, message, and created_at timestamp
- Define `CommentRepository` protocol in `core/interfaces/` with methods for creating comments, retrieving comments by post ID, and checking for duplicate comments
- Create `CreateCommentRequest` and `CommentDto` schemas in `core/schemas/` for request/response handling
- Implement `CommentService` in `core/services/` with business logic for creating comments, validating non-empty fields, preventing duplicates, and retrieving comments in chronological order
- Add business validation methods to `Comment` model for ensuring message and author name are not empty or whitespace-only

### Infrastructure Package Tasks

- Create `CommentModel` SQLAlchemy model in `infrastructure/database/models/` with proper column types and foreign key relationship to blog posts
- Generate Alembic migration for the comments table with appropriate indexes on blog_post_id and created_at columns
- Implement `SqlAlchemyCommentRepository` in `infrastructure/repositories/` that fulfills the CommentRepository protocol
- Add domain model conversion methods (`to_domain()` and `from_domain()`) to the CommentModel class

### Web Framework Tasks

- Create FastAPI endpoint `POST /posts/{post_id}/comments` for submitting new comments with proper request validation
- Create FastAPI endpoint `GET /posts/{post_id}/comments` for retrieving comments in chronological order
- Implement dependency injection function `get_comment_service()` in dependencies module
- Add proper HTTP status codes and error responses for validation failures and duplicate comment attempts

### Testing Tasks

- Write unit tests for `CommentService` using mocked repository dependencies to test business logic validation
- Create integration tests for `SqlAlchemyCommentRepository` using test database to verify data persistence and retrieval
- Implement API endpoint tests using TestClient to verify comment submission and retrieval functionality
- Add test cases for edge cases including empty comments, duplicate detection, and chronological ordering

--- Item #5 ---
Work Item ID: 5
Story Name: quality management
Story: I want to manage blog posts and comments so that I can maintain content quality.
Done Conditions: - Admins can edit or delete any post.
- Admins can remove inappropriate comments.
- A dashboard displays published posts and user interactions.
- Changes made by admins take effect immediately.
----------------------------------------
===============
## Quality Management User Story Tasks

### Core Package Tasks

- Create `AdminUser` domain model in `core/models/` with role validation and permission checking methods
- Implement `PostService` in `core/services/` with methods for admin post editing, deletion, and status management
- Implement `CommentService` in `core/services/` with admin comment removal and moderation capabilities
- Create `DashboardService` in `core/services/` to aggregate post analytics and user interaction data
- Define `PostRepository` protocol in `core/interfaces/` with admin-specific query methods
- Define `CommentRepository` protocol in `core/interfaces/` with bulk operations and filtering capabilities
- Define `UserInteractionRepository` protocol in `core/interfaces/` for tracking engagement metrics
- Create request/response DTOs in `core/schemas/` for admin operations and dashboard data

### Infrastructure Package Tasks

- Implement `SqlAlchemyPostRepository` with admin query methods and immediate update capabilities
- Implement `SqlAlchemyCommentRepository` with batch deletion and moderation status tracking
- Implement `SqlAlchemyUserInteractionRepository` for aggregating user engagement data
- Create SQLAlchemy models for posts, comments, and user interactions with proper admin audit fields
- Add database migration for admin-specific columns and indexes on frequently queried fields

### Web Framework Tasks

- Create admin authentication middleware to verify admin permissions for protected endpoints
- Implement POST `/admin/posts/{id}` endpoint for editing posts with immediate effect
- Implement DELETE `/admin/posts/{id}` endpoint for post deletion with cascade handling
- Implement DELETE `/admin/comments/{id}` endpoint for removing inappropriate comments
- Implement GET `/admin/dashboard` endpoint returning published posts and interaction metrics
- Add proper error handling and validation for all admin operations

### Testing Tasks

- Write unit tests for `PostService` admin operations using mocked repository dependencies
- Write unit tests for `CommentService` moderation features with edge case coverage
- Write unit tests for `DashboardService` data aggregation with various interaction scenarios
- Create integration tests for admin repository implementations with test database
- Write API endpoint tests using TestClient to verify admin-only access and immediate changes
- Add fixtures for admin user authentication and test data setup
