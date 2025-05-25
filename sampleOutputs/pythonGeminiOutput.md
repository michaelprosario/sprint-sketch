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
Okay, here are the user story tasks based on the provided user story, done conditions, and team standards, formatted as a bulleted list in Markdown:

```markdown
### User Story Tasks: View Blog

*   **Task: Core - Define Blog Post Domain Model (Core/models/)**
    *   Create `BlogPost` dataclass/Pydantic model with attributes: `id` (int, optional), `title` (str), `author_name` (str), `date` (datetime), `content` (str).  Ensure Pydantic validation rules are implemented, such as required fields, date format validation, and maximum content length.

*   **Task: Core - Define Blog Post Schema (Core/schemas/)**
    *   Create request and response schemas (Pydantic models) for creating, retrieving, and listing blog posts (`CreateBlogPostRequest`, `BlogPostDto`, `ListBlogPostResponse`). Include necessary validation and transformation logic.

*   **Task: Core - Define Blog Post Repository Interface (Core/interfaces/)**
    *   Create `BlogPostRepository` protocol with methods: `get_all` (returns list of `BlogPost` in reverse chronological order), `get_by_id` (returns a `BlogPost` or `None`), `create` (creates a new `BlogPost`), and `update` (updates an existing `BlogPost`).

*   **Task: Core - Define Blog Post Service (Core/services/)**
    *   Create `BlogPostService` class that implements business logic for retrieving and displaying blog posts. Implement methods:
        *   `list_published_posts()`: Retrieves all published blog posts from the repository in reverse chronological order and returns a `Result[List[BlogPostDto]]`.
        *   `get_post(post_id: int)`: Retrieves a blog post by ID and returns a `Result[BlogPostDto]`.
    * Ensure this service has no direct database calls, and only depends on the `BlogPostRepository` interface.

*   **Task: Infrastructure - Implement Blog Post Repository (Infrastructure/repositories/)**
    *   Create `SqlAlchemyBlogPostRepository` class that implements the `BlogPostRepository` protocol using SQLAlchemy.
    *   Implement methods to interact with the database: `get_all`, `get_by_id`, `create`, and `update`. Ensure data is mapped correctly between SQLAlchemy models and domain models using `to_domain()` and `from_domain()` methods.

*   **Task: Infrastructure - Define Blog Post SQLAlchemy Model (Infrastructure/database/)**
    *   Create `BlogPostModel` class in `database/models.py` that represents the `blog_posts` table. Include columns for `id`, `title`, `author_name`, `date`, and `content`.  Use appropriate column types (e.g., `String` for text, `DateTime` for dates).

*   **Task: Infrastructure - Set up Alembic Migrations**
    *   Configure Alembic to manage database migrations.
    *   Create an initial migration script to create the `blog_posts` table with the defined schema.

*   **Task: Presentation (FastAPI) - Create Blog Post API Endpoints**
    *   Create FastAPI endpoints for:
        *   `GET /posts`: Returns a list of published blog posts (using `BlogPostService.list_published_posts()`).
        *   `GET /posts/{post_id}`: Returns a specific blog post by ID (using `BlogPostService.get_post()`).
    *   Implement dependency injection to inject the `BlogPostService` into the endpoints.
    *   Handle request/response serialization and error handling, returning appropriate HTTP status codes and error messages.

*   **Task: Presentation (FastAPI) - Dependency Injection Configuration**
    *   Configure FastAPI's dependency injection system to provide instances of `BlogPostService` and `SqlAlchemyBlogPostRepository`, including database session management.

*   **Task: Unit Tests - Blog Post Service (Core/services/)**
    *   Write unit tests for the `BlogPostService` using pytest.
    *   Mock the `BlogPostRepository` to isolate the service logic.
    *   Test scenarios for successful retrieval of posts, handling of errors, and correct ordering of posts.

*   **Task: Integration Tests - Blog Post Repository (Infrastructure/repositories/)**
    *   Write integration tests for the `SqlAlchemyBlogPostRepository` using a test database (e.g., SQLite in-memory).
    *   Test database interactions for creating, retrieving, and updating blog posts.

*   **Task: API Endpoint Tests - Blog Post Endpoints**
    *   Write API endpoint tests using FastAPI's `TestClient`.
    *   Test the `GET /posts` and `GET /posts/{post_id}` endpoints.
    *   Verify that the endpoints return the correct data and HTTP status codes.

*   **Task: UI Integration (If applicable - depends on how the "view blog" is presented)**
    *   Integrate the API endpoints with the front-end to display the list of blog posts on the homepage.
    *   Implement navigation to a detailed view of a specific blog post when clicked.

*   **Task: Code Review and Refactoring**
    *   Conduct code reviews to ensure adherence to team standards and best practices.
    *   Refactor code as needed to improve readability, maintainability, and performance.

```
**Explanation of Tasks and how they align with the Standards**

*   **Core Tasks:** These tasks are focused on defining the business logic, domain models, and interfaces in the `Core` package.  They ensure that the core logic is independent of the infrastructure and presentation layers. We are defining the data model, service, schemas, and interfaces that interact with the other layers. The repository interface will be used by both the service and infrastructure layers.
*   **Infrastructure Tasks:** These tasks implement the interfaces defined in the `Core` package using SQLAlchemy to interact with the database.  This keeps the database-specific implementation separate from the business logic. We are also using Alembic to handle database migrations, as specified in the team standards.
*   **Presentation (FastAPI) Tasks:** These tasks expose the blog post functionality through API endpoints using FastAPI.  Dependency injection is used to inject the `BlogPostService`, ensuring that the endpoints have minimal business logic and adhere to the team's architecture.
*   **Testing Tasks:**  These tasks cover both unit tests for the business logic in the `BlogPostService` and integration tests for the `SqlAlchemyBlogPostRepository`.  API endpoint tests are also included to ensure the API is functioning correctly. Mocking will be used to test dependencies and the tests are built to use a test database.
*   **Other Tasks:** The code review and UI Integration tasks ensure code quality and a working application.
*   **Naming Conventions:** The tasks implicitly adhere to naming conventions (e.g., `PascalCase` for classes, `snake_case` for functions). The naming of classes follows `PascalCase` and the usage follows that convention in code examples.
*   **Result Pattern:** The service methods `list_published_posts()` and `get_post()` return a `Result` object, which is consistent with the team's error handling strategy.

This detailed breakdown should provide a clear roadmap for implementing the "view blog" user story while adhering to the specified team standards.


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
```markdown
*   **Frontend - Create Post Page:**
    *   Create a new route/page for creating posts accessible to authors. (Presentation)
    *   Implement a post editor component allowing text formatting (bold, italics, headings, lists, etc.). (Presentation)
    *   Integrate image upload functionality into the post editor. (Presentation)
    *   Implement a preview feature that displays the post content as it will appear when published. (Presentation)
    *   Implement a form with fields for title, body (using the editor), and category selection. (Presentation)
    *   Implement client-side validation for title, body, and category fields ensuring they are not empty. (Presentation)
    *   Implement a "Publish" button. (Presentation)
    *   Display a success confirmation message to the author upon successful post publication. (Presentation)
    *   Write UI tests to verify functionality and ensure elements render correctly. (Dev Testing)

*   **Backend - Post Creation API:**
    *   Define a `CreatePostRequest` schema (title, body, category). (Core/Schemas)
    *   Define a `PostDto` schema for the response (including id, title, body, category, author_id, publication date). (Core/Schemas)
    *   Create a `Post` domain model. (Core/Models)
    *   Define a `PostRepository` interface with a `create` method to persist posts. (Core/Interfaces)
    *   Implement a `PostService` with a `create_post` method that: (Core/Services)
        *   Validates the `CreatePostRequest`.
        *   Creates a `Post` domain object.
        *   Uses the `PostRepository` to persist the post.
        *   Returns a `Result[PostDto]`.
        *   Handles errors and returns appropriate error messages in the `Result`.
    *   Implement `SqlAlchemyPostRepository` that implements the `PostRepository` interface using SQLAlchemy. (Infrastructure/Repositories)
        *   Define a `PostModel` SQLAlchemy model with fields for id, title, body, category, author_id, and publication date. (Infrastructure/Database)
        *   Implement methods on the `PostModel` for converting to and from the domain model. (Infrastructure/Database)
    *   Create an API endpoint (e.g., `/posts`) that accepts a `CreatePostRequest`, injects the `PostService`, and returns a `PostDto` or an error. (Presentation - FastAPI/Flask)
    *   Write unit tests for the `PostService`, mocking the `PostRepository`. (Dev Testing)
    *   Write integration tests for the `SqlAlchemyPostRepository` using a test database. (Dev Testing)
    *   Write API endpoint tests using TestClient to ensure correct request/response handling and error handling. (Dev Testing)

*   **Data Model and Database:**
    *   Create a database migration using Alembic to create the `posts` table with appropriate columns and data types (including text for body). (Infrastructure/Database)
    *   Define relationships between `PostModel` and other relevant models (e.g., `UserModel` for author). (Infrastructure/Database)

*   **Authentication and Authorization:**
    *   Ensure only authenticated authors can access the "Create Post" page and create posts (This assumes that the authentication mechanism already exists). (Presentation and Core/Services)
    *   Associate the created post with the currently logged-in author. (Core/Services)

*   **Configuration:**
    *   Configure dependency injection for the `PostService` and `SqlAlchemyPostRepository`. (Presentation - FastAPI/Flask and Dependencies)

*   **Error Handling and Logging:**
    *   Implement proper error handling in the `PostService` and API endpoint.
    *   Add logging for errors and significant events.

*   **Deployment:**
    *   Update deployment scripts/processes to include database migrations.
```

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
Okay, here are the user story tasks broken down, actionable, and aligned with the provided Python team standards:

```markdown
### User Story Tasks: Search Blog

*   **Task 1: Core - Define Search Service Interface (Core/interfaces/)**
    *   Create a `BlogSearchService` protocol in `core/interfaces/blog_search_service.py` with a `search_posts` method that accepts a search term (string) and returns a `Result[List[BlogPostsDto]]` (or similar DTO). Consider pagination parameters as well, perhaps using DTOs for request and response.

*   **Task 2: Core - Implement Blog Post Domain Model (Core/models/)**
    *   Define `BlogPost` domain model using either a dataclass or Pydantic model, including fields like `id`, `title`, `excerpt`, and `content`. Ensure there are methods for working with the blog post if applicable.

*   **Task 3: Core - Implement Blog Search Service (Core/services/)**
    *   Create `BlogSearchService` class in `core/services/blog_search_service.py` that implements the `BlogSearchService` protocol. It should accept a `BlogPostRepository` dependency via constructor injection. The `search_posts` method should call the `BlogPostRepository`'s search method. Use the `Result[T]` pattern for error handling.

*   **Task 4: Core - Define Blog Post Repository Interface (Core/interfaces/)**
    *   Create a `BlogPostRepository` protocol in `core/interfaces/blog_post_repository.py` with a `search` method that accepts a search term (string) and returns a `List[BlogPost]`.  Also define methods for getting blog posts and their metadata and accessing the full content if needed.

*   **Task 5: Infrastructure - Implement Blog Post Repository (Infrastructure/repositories/)**
    *   Create `SqlAlchemyBlogPostRepository` class in `infrastructure/repositories/sqlalchemy_blog_post_repository.py` that implements the `BlogPostRepository` protocol. Use SQLAlchemy to query the database for blog posts matching the search term in the title or content.  Map the SQLAlchemy model to the Core `BlogPost` domain model.

*   **Task 6: Infrastructure - Define SQLAlchemy Blog Post Model (Infrastructure/database/)**
    *   Create `BlogPostModel` in `infrastructure/database/models.py` that represents the blog post table in the database.  Include columns for `id`, `title`, `excerpt`, `content`, and potentially other relevant metadata (e.g., publication date). Include `to_domain` and `from_domain` methods for conversion to core models. Use proper column types like `String`, `Text` (for content), and `DateTime`.

*   **Task 7: Infrastructure - Alembic Migration for Blog Post Table**
    *   Create an Alembic migration script to create the `blog_posts` table in the database, based on the `BlogPostModel` definition.

*   **Task 8: Web Framework - Create Search Endpoint (FastAPI/Flask)**
    *   Create a new API endpoint (e.g., `/blog/search`) that accepts a query parameter (e.g., `q`). Inject the `BlogSearchService` using FastAPI's dependency injection. Call the `BlogSearchService.search_posts` method with the search term. Serialize the results to DTOs and return them as a JSON response. Implement error handling (HTTPException with appropriate status codes).

*   **Task 9: Web Framework - Integrate Search Bar into Homepage**
    *   Update the blog homepage template to include a search bar.  The search bar should submit a GET request to the `/blog/search` endpoint with the search term as the `q` parameter.

*   **Task 10: Web Framework - Display Search Results**
    *   Update the homepage template (or create a separate search results template) to display the search results.  Each result should show the blog post title and excerpt. Make the title a link to the full blog post (implementing the navigation requirement).

*   **Task 11: Unit Test - BlogSearchService (Tests/)**
    *   Create unit tests for the `BlogSearchService` in `tests/core/services/test_blog_search_service.py`.  Mock the `BlogPostRepository` to isolate the service logic. Test cases should include:
        *   Successful search with matching posts
        *   Search with no matching posts
        *   Handling repository errors

*   **Task 12: Integration Test - SqlAlchemyBlogPostRepository (Tests/)**
    *   Create integration tests for the `SqlAlchemyBlogPostRepository` in `tests/infrastructure/repositories/test_sqlalchemy_blog_post_repository.py`. Use a test database (e.g., SQLite in-memory). Test cases should include:
        *   Searching for existing posts
        *   Searching with no matching posts
        *   Verifying correct mapping between database model and domain model

*   **Task 13: API Endpoint Test - /blog/search (Tests/)**
    *   Create API endpoint tests using TestClient for the `/blog/search` endpoint in `tests/web/test_blog_search_endpoint.py`. Test cases should include:
        *   Valid search query returns results
        *   Empty search query returns appropriate response (e.g., empty list or error)
        *   Error handling (e.g., invalid query parameters)

*   **Task 14: UI Testing (Optional)**
    *   If using a UI testing framework (e.g., Selenium, Playwright), create UI tests to verify the search bar is present, functional, and navigates to the correct blog post pages.

```


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
```markdown
### User Story Tasks: Add Comments

*   **Task 1: Core - Define Comment Domain Model:**
    *   Create `core/models/comment.py`.
    *   Define a `Comment` dataclass/Pydantic model with fields: `id` (Optional[int]), `post_id` (int), `name` (str), `message` (str), `created_at` (datetime).
    *   Implement data validation using Pydantic, enforcing constraints on `name` and `message` (e.g., max length).
    *   Include relevant business logic methods if applicable (e.g., check if comment is empty).
    *   Unit Test the comment model including validation logic

*   **Task 2: Core - Define Comment Schema:**
    *   Create `core/schemas/comment.py`.
    *   Define `CreateCommentRequest` (Pydantic model for comment submission) mirroring Comment model fields (except id).
    *   Define `CommentDto` (Pydantic model for API response) mirroring Comment model fields.

*   **Task 3: Core - Define Comment Repository Interface:**
    *   Create `core/interfaces/comment_repository.py`.
    *   Define `CommentRepository` protocol with methods:
        *   `get_by_post_id(post_id: int) -> List[Comment]`
        *   `create(comment: Comment) -> Comment`
        *   `delete(comment_id: int) -> bool`

*   **Task 4: Core - Implement Comment Service:**
    *   Create `core/services/comment_service.py`.
    *   Implement `CommentService` class.
    *   Inject `CommentRepository` as a dependency.
    *   Implement methods:
        *   `get_comments_for_post(post_id: int) -> Result[List[CommentDto]]`
        *   `create_comment(request: CreateCommentRequest, post_id: int) -> Result[CommentDto]`
        *   Implement empty comment and duplicate comment prevention logic within `create_comment`. Define what constitutes a duplicate comment
        *   Wrap logic in a `try...except` block, returning `Result.failure` on error.
        *   Return `Result.success` with `CommentDto` on success.
    *   Unit test the service using mocked repository. Focus on business logic, error handling (empty and duplicate comment). Use AAA pattern.

*   **Task 5: Infrastructure - Implement Comment Repository:**
    *   Create `infrastructure/repositories/sqlalchemy_comment_repository.py`.
    *   Implement `SqlAlchemyCommentRepository` that implements `CommentRepository` protocol.
    *   Use SQLAlchemy to interact with the database.

*   **Task 6: Infrastructure - Define Comment SQLAlchemy Model:**
    *   Create `infrastructure/database/models.py` (if it doesn't exist).
    *   Define `CommentModel` (SQLAlchemy model) mapping to the `comments` database table.
    *   Include columns: `id` (Integer, primary_key), `post_id` (Integer, ForeignKey to posts table), `name` (String), `message` (String), `created_at` (DateTime).
    *   Implement `to_domain()` (converts `CommentModel` to `Comment`) and `from_domain()` (converts `Comment` to `CommentModel`) methods.

*   **Task 7: Infrastructure - Database Migrations:**
    *   Create Alembic migrations to add the `comments` table to the database.

*   **Task 8: Presentation (FastAPI/Flask) - Create Comment Endpoint:**
    *   Create a new API endpoint (e.g., `/posts/{post_id}/comments`) for creating comments.
    *   Use dependency injection to inject `CommentService`.
    *   Handle request and response serialization using `CreateCommentRequest` and `CommentDto`.
    *   Implement error handling (return appropriate HTTP status codes on failure).
    *   Implement a GET endpoint to retrieve comments for a post.

*   **Task 9: Presentation (FastAPI/Flask) - Update Dependencies:**
    *   Update `dependencies.py` to include the function needed to get the `CommentService` with the dependency injection.

*   **Task 10: Integration Tests - Comment Repository:**
    *   Create integration tests for `SqlAlchemyCommentRepository` to verify database interactions (create, get by post id).

*   **Task 11: API Endpoint Tests:**
    *   Use TestClient to create integration tests for the comment API endpoints (create and get comments).

*   **Task 12: UI Integration:**
    *   (If applicable) Integrate the comment functionality into the frontend UI to display comments and allow users to submit new comments.  This will likely require frontend development not covered in the team standards, but the backend needs to be ready to support the frontend.

*   **Task 13: Documentation:**
    *   Document the new API endpoints (request/response formats, error codes).
    *   Update any relevant documentation (API documentation, system architecture).

*   **Task 14: Code Review:**
    *   Conduct thorough code reviews to ensure adherence to coding standards, test coverage, and functionality.
```

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
Okay, here are the user story tasks, broken down and formatted to adhere to the provided team standards, specifically targeting the Clean Architecture pattern and testing requirements.

*   **Core Development:**

    *   [ ] Define `Post` and `Comment` domain models in `core/models.py` with relevant attributes (e.g., `post_id`, `user_id`, `content`, `timestamp`). Ensure these models include methods for business logic, such as checking if a user is authorized to edit a post.
    *   [ ] Create `AdminService` in `core/services.py` with methods for:
        *   [ ] `edit_post(post_id: int, new_content: str)`: Edits the content of a post.
        *   [ ] `delete_post(post_id: int)`: Deletes a post.
        *   [ ] `remove_comment(comment_id: int)`: Removes a comment.
        *   These methods should return a `Result[bool]` indicating success or failure.
    *   [ ] Define protocols `PostRepository` and `CommentRepository` in `core/interfaces.py` with methods like `get_post_by_id`, `update_post`, `delete_post`, `get_comment_by_id`, and `delete_comment`.
    *   [ ] Create schemas (`core/schemas.py`) for request/response DTOs for editing/deleting posts and removing comments (e.g., `EditPostRequest`, `DeletePostRequest`, `RemoveCommentRequest`).
    *   [ ] Unit test the `AdminService` in `tests/core/test_admin_service.py` using mocked `PostRepository` and `CommentRepository`.  Ensure all business logic is thoroughly tested (e.g., check user authorization before editing).

*   **Infrastructure Development:**

    *   [ ] Create SQLAlchemy models for `Post` and `Comment` in `infrastructure/database/models.py` with appropriate column types (e.g., `Text` for content, `Integer` for IDs, `DateTime` for timestamps).  Implement `to_domain()` and `from_domain()` methods for conversion between SQLAlchemy models and Core domain models.
    *   [ ] Implement `SqlAlchemyPostRepository` and `SqlAlchemyCommentRepository` in `infrastructure/repositories.py`, implementing the `PostRepository` and `CommentRepository` protocols.  Use SQLAlchemy to interact with the database.
    *   [ ] Integration test the repository implementations in `tests/infrastructure/repositories/test_post_repository.py` and `tests/infrastructure/repositories/test_comment_repository.py` using a test database. Test CRUD operations.

*   **Web Framework (FastAPI) Development:**

    *   [ ] Create API endpoints for admin actions in a dedicated router (e.g., `/admin`).
    *   [ ] Implement endpoints:
        *   [ ] `PUT /admin/posts/{post_id}`: Edit a post.
        *   [ ] `DELETE /admin/posts/{post_id}`: Delete a post.
        *   [ ] `DELETE /admin/comments/{comment_id}`: Remove a comment.
    *   [ ] Inject `AdminService` into the endpoints using FastAPI's dependency injection.
    *   [ ] Implement dependency injection in `dependencies.py` to provide the `AdminService` with the appropriate repository implementations.
    *   [ ] Implement `get_db_session` to manage database sessions as a dependency (as defined in the team standards).
    *   [ ] Test the API endpoints using `TestClient` in `tests/api/test_admin_endpoints.py`.  Ensure proper authentication and authorization are simulated in the tests.

*   **Dashboard Development:**

    *   [ ] Implement an endpoint to retrieve published posts and user interactions (e.g., comments, likes) for the dashboard.  Consider pagination for large datasets.
    *   [ ] Define a DTO for the dashboard data (`DashboardDataDto` in `core/schemas.py`).
    *   [ ] Create a service method (e.g., `get_dashboard_data` in a `DashboardService`) to retrieve and aggregate the data.
    *   [ ] Implement the dashboard API endpoint in the presentation layer, calling the new service.
    *   [ ] Write unit tests for the `DashboardService`.

*   **Real-time Updates:**

    *   [ ] Investigate using WebSockets (or a similar technology) to push updates to the dashboard in real-time when admin actions occur. This likely requires integration with the `AdminService` and the dashboard endpoint. *(This is more of an investigation/spike initially. Decide on the implementation after some research.)*
    *   [ ]  Implement WebSocket endpoint for dashboard updates.
    *   [ ]  Modify `AdminService` to emit WebSocket events upon post/comment modification.

*   **Documentation:**

    *   [ ] Document all API endpoints using FastAPI's built-in documentation features (automatic OpenAPI generation).
    *   [ ] Document the architecture and design decisions made in the code (e.g., using docstrings).

**Important Considerations and Notes:**

*   **Error Handling:**  Pay close attention to error handling throughout the application, using the `Result[T]` pattern and proper logging.
*   **Authentication/Authorization:**  This user story assumes an existing authentication/authorization system. If not, that needs to be addressed separately.  Ensure that only authorized admins can access the admin endpoints.
*   **Immediate Effect:** Carefully consider the implications of changes taking effect immediately. If necessary, implement safeguards such as versioning or auditing.
*   **Testing:** Write thorough unit and integration tests to ensure the correctness and stability of the code. Use mocks and test databases to isolate the tests. Remember to use test driven development.
*   **Database Migrations**: Use Alembic to manage database schema changes.
*   **Asynchronous Operations:** The code snippets and standards assume usage of `asyncio` and `await`. Ensure this is consistently applied.

