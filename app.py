import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


# --- Data Loading and Saving Functions ---

def load_blog_posts():
    """Reads the list of blog posts from posts.json."""
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_blog_posts(posts):
    """Writes the current list of blog posts back to posts.json."""
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


# --- Helper Function ---

def fetch_post_by_id(post_id):
    """Finds a single post by its ID."""
    blog_posts = load_blog_posts()
    # next() is used for efficient searching in a list of dicts
    return next((p for p in blog_posts if p['id'] == post_id), None)


# --- Routes ---

@app.route('/')
def index():
    """Displays all blog posts."""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handles displaying the add post form (GET) and processing the new post submission (POST)."""
    if request.method == 'POST':
        blog_posts = load_blog_posts()

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Generate a unique ID
        new_id = 1
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)
        save_blog_posts(blog_posts)

        return redirect(url_for('view_post', post_id=new_id))

    return render_template('add.html')


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Displays a single blog post based on its ID."""
    post = fetch_post_by_id(post_id)

    if post is None:
        abort(404)

    return render_template('view_post.html', post=post)


# NEW ROUTE: Update a post (Handles both GET to show form and POST to save changes)
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handles updating an existing post based on its ID."""

    blog_posts = load_blog_posts()

    # 1. Fetch the post to update (used for both GET and POST)
    post_to_update = fetch_post_by_id(post_id)

    if post_to_update is None:
        # Post not found
        abort(404)

    if request.method == 'POST':
        # --- Handle POST request (Form Submission) ---

        # Find the index of the post in the list
        post_index = next((i for i, p in enumerate(blog_posts) if p['id'] == post_id), -1)

        if post_index != -1:
            # Update the post data in the list using form input
            blog_posts[post_index]['author'] = request.form.get('author')
            blog_posts[post_index]['title'] = request.form.get('title')
            blog_posts[post_index]['content'] = request.form.get('content')

            # Save the updated list back to the JSON file
            save_blog_posts(blog_posts)

            # Redirect to the updated post's view page
            return redirect(url_for('view_post', post_id=post_id))

    # --- Handle GET request (Display Form) ---
    # Render the update.html page, passing the existing post data
    return render_template('update.html', post=post_to_update)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a blog post with the given ID and redirects to the index."""

    blog_posts = load_blog_posts()

    # Find the index of the post to delete
    post_index_to_delete = next((i for i, post in enumerate(blog_posts) if post['id'] == post_id), -1)

    if post_index_to_delete != -1:
        blog_posts.pop(post_index_to_delete)
        save_blog_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)