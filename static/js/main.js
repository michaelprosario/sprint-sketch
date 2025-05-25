// Main JavaScript file for the blog application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the search functionality
    initializeSearch();
    
    // Initialize the comment form
    initializeCommentForm();
});

/**
 * Initialize the search functionality
 */
function initializeSearch() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const keyword = document.querySelector('.search-input').value.trim();
            if (keyword) {
                window.location.href = `/api/blogs/search?keyword=${encodeURIComponent(keyword)}`;
            }
        });
    }
}

/**
 * Initialize the comment form
 */
function initializeCommentForm() {
    const commentForm = document.querySelector('.comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.querySelector('#name').value.trim();
            const message = document.querySelector('#message').value.trim();
            const postId = document.querySelector('#post_id').value;
            
            // Validation
            if (!name) {
                showError('Please enter your name');
                return;
            }
            
            if (!message) {
                showError('Please enter a comment');
                return;
            }
            
            // Submit the comment via API
            submitComment(postId, name, message);
        });
    }
}

/**
 * Submit a comment to the API
 */
async function submitComment(postId, name, message) {
    try {
        const response = await fetch('/api/comments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                post_id: parseInt(postId),
                name,
                message
            }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Comment was successfully posted
            showSuccess('Your comment was posted successfully!');
            
            // Clear the form
            document.querySelector('#name').value = '';
            document.querySelector('#message').value = '';
            
            // Reload the comments section or append the new comment
            refreshComments(postId);
        } else {
            // There was an error
            showError(data.detail || 'Failed to post comment');
        }
    } catch (error) {
        showError('An error occurred while posting your comment');
        console.error('Error posting comment:', error);
    }
}

/**
 * Refresh the comments section after posting a new comment
 */
async function refreshComments(postId) {
    try {
        const response = await fetch(`/api/comments/post/${postId}`);
        const comments = await response.json();
        
        const commentsContainer = document.querySelector('.comments-list');
        if (commentsContainer) {
            // Clear existing comments
            commentsContainer.innerHTML = '';
            
            // Add new comments
            comments.forEach(comment => {
                const commentElement = createCommentElement(comment);
                commentsContainer.appendChild(commentElement);
            });
            
            // Update the comments count
            const commentsCount = document.querySelector('.comments-count');
            if (commentsCount) {
                commentsCount.textContent = `${comments.length} Comment${comments.length !== 1 ? 's' : ''}`;
            }
        }
    } catch (error) {
        console.error('Error refreshing comments:', error);
    }
}

/**
 * Create a comment element
 */
function createCommentElement(comment) {
    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment';
    
    const date = new Date(comment.created_at);
    const formattedDate = date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    commentDiv.innerHTML = `
        <div class="comment-meta">
            <span class="comment-author">${escapeHtml(comment.name)}</span>
            <span class="comment-date">${formattedDate}</span>
        </div>
        <div class="comment-body">
            ${escapeHtml(comment.message)}
        </div>
    `;
    
    return commentDiv;
}

/**
 * Show an error message
 */
function showError(message) {
    const alertElement = document.createElement('div');
    alertElement.className = 'alert alert-error';
    alertElement.textContent = message;
    
    const form = document.querySelector('.comment-form');
    form.insertBefore(alertElement, form.firstChild);
    
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
}

/**
 * Show a success message
 */
function showSuccess(message) {
    const alertElement = document.createElement('div');
    alertElement.className = 'alert alert-success';
    alertElement.textContent = message;
    
    const form = document.querySelector('.comment-form');
    form.insertBefore(alertElement, form.firstChild);
    
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
}

/**
 * Escape HTML to prevent XSS attacks
 */
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
