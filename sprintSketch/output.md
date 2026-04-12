# User Stories - Untitled Project

**Generated:** 2026-04-12 19:27:40

## Scope

**Description:** A simple web-based platform for blogging

### Goals

- Implement core functionality

### Constraints

- Must be deployable within 2 months
- Use open-source tools where possible
- Technology stack: Python backend, Angular frontend

## User Stories

> **INVEST Principles:** Independent | Negotiable | Valuable | Estimable | Small | Testable

### # User Stories: Simple Web-Based Blogging Platform

As a user, I want complete the task, so that achieve the goal.

#### Acceptance Criteria
- [ ] A registration form accepts a unique email address, a display name, and a password (minimum 8 characters)
- [ ] Submitting a duplicate email displays a clear error message: *"An account with this email already exists"*
- [ ] Passwords are stored as hashed values (e.g., bcrypt); plain-text passwords are never persisted
- [ ] Upon successful registration, the user receives a confirmation message and is redirected to their dashboard
- [ ] Invalid or malformed email addresses are rejected with inline validation before form submission
- --
- **As a** registered user, **I want** to log in and log out of my account securely, **so that** my content and profile remain protected.
- **Acceptance Criteria:**
- [ ] A login form accepts a valid email and password and authenticates against stored credentials
- [ ] A failed login attempt displays a generic error message (*"Invalid email or password"*) without revealing which field is incorrect
- [ ] On successful login, the user receives a JWT token stored in an HTTP-only cookie and is redirected to their dashboard
- [ ] Clicking "Log Out" invalidates the session token and redirects the user to the homepage
- [ ] Accessing any authenticated route without a valid token redirects the user to the login page
- --
- **As a** logged-in user, **I want** to write and publish a blog post with a title and body content, **so that** I can share my ideas with readers.
- **Acceptance Criteria:**
- [ ] The post editor provides a title field (max 150 characters) and a rich-text or Markdown body field
- [ ] The user can save a post as a **draft** (not publicly visible) or **publish** it immediately
- [ ] Attempting to publish a post without a title or body displays a validation error and prevents submission
- [ ] A successfully published post is immediately accessible via its unique URL (e.g., `/posts/{id}`)
- [ ] The post creation timestamp is recorded and displayed on the published post
- --
- **As a** logged-in author, **I want** to edit or delete my own blog posts, **so that** I can correct mistakes or remove content I no longer want published.
- **Acceptance Criteria:**
- [ ] An author can navigate to any of their posts and enter an edit mode pre-populated with the current title and body
- [ ] Saving edits updates the post content and records a *"last updated"* timestamp visible on the post
- [ ] An author can delete their own post after confirming a deletion prompt; the post is removed from the database and its URL returns a 404
- [ ] A user cannot edit or delete posts authored by another user; attempting to do so returns a 403 Forbidden response
- [ ] Editing a post does not change its original publication date
- --
- **As a** visitor, **I want** to browse a paginated list of published blog posts, **so that** I can discover and read content without needing an account.
- **Acceptance Criteria:**
- [ ] The homepage displays published posts ordered by publication date, newest first
- [ ] Each list item shows the post title, author display name, publication date, and a short excerpt (first 200 characters)
- [ ] The list is paginated with a maximum of 10 posts per page, with navigation controls (Previous / Next)
- [ ] Draft posts are never visible in the public listing regardless of the viewer's login status
- [ ] The page loads and renders the post list within 2 seconds under normal conditions
- --
- **As a** visitor, **I want** to open and read a full blog post on its own page, **so that** I can consume the complete content.
- **Acceptance Criteria:**
- [ ] Clicking a post title from the listing navigates to the post's dedicated page at `/posts/{id}`
- [ ] The full post page displays the title, author name, publication date, and complete body content
- [ ] Navigating to the URL of a draft post as a non-author returns a 404 page
- [ ] The page includes a *"Back to all posts"* navigation link
- [ ] Page content is rendered correctly for both plain text and basic Markdown/HTML formatting
- --
- **As a** logged-in user, **I want** to view a personal dashboard listing all my posts, **so that** I can manage my drafts and published content in one place.
- **Acceptance Criteria:**
- [ ] The dashboard displays all posts belonging to the logged-in author, separated into **Published** and **Drafts** sections
- [ ] Each post entry shows its title, status, publication/creation date, and quick-action links for Edit and Delete
- [ ] If the author has no posts, a prompt is displayed encouraging them to create their first post
- [ ] The dashboard is only accessible to authenticated users; unauthenticated access redirects to the login page
- [ ] The post list on the dashboard updates immediately after a post is created, edited, or deleted without requiring a full page reload
- --
- **As a** visitor, **I want** to search for blog posts by keyword, **so that** I can quickly find content relevant to my interests.
- **Acceptance Criteria:**
- [ ] A search bar is accessible from the homepage and returns results matching keywords in the post title or body
- [ ] Search results display the same format as the main post listing (title, author, date, excerpt)
- [ ] If no results are found, the page displays a clear message: *"No posts found for '[keyword]'"*
- [ ] Only published posts are returned in search results
- [ ] Search queries fewer than 2 characters display an inline validation message and do not trigger a backend request
- --
- **As a** visitor using a mobile device, **I want** the platform to display correctly on small screens, **so that** I can read and navigate the blog comfortably without a desktop browser.
- **Acceptance Criteria:**
- [ ] All pages (homepage, post detail, login, registration, dashboard) are usable on screen widths of 375px and above
- [ ] Navigation links collapse into a mobile-friendly menu (e.g., hamburger menu) on screens narrower than 768px
- [ ] Text, images, and form inputs reflow correctly without horizontal scrolling on mobile viewports
- [ ] Touch targets (buttons, links) meet a minimum size of 44×44px for accessibility
- [ ] Responsive behaviour is verified on Chrome and Safari mobile viewports using browser developer tools
- --
- > **Note on Scope:** These 9 stories cover the critical path for an MVP blogging platform — authentication, full post lifecycle, public browsing, content discovery, and mobile access — all achievable within the stated 2-month constraint using Python (Django or FastAPI) and Angular with open-source libraries.

