import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


# --- Data Loading and Saving Functions ---

def load_blog_posts():
    """Reads the list of blog posts from posts.json."""
    try:
        # Open the file and load the JSON data
        with open('posts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty list if the file doesn't exist or is corrupted
        return []


def save_blog_posts(posts):
    """Writes the current list of blog posts back to posts.json."""
    with open('posts.json', 'w') as f:
        # Use indent=4 for readable JSON formatting
        json.dump(posts, f, indent=4)


# --- Routes ---

@app.route('/')
def index():
    """Displays all blog posts."""
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handles displaying the add post form (GET)
    and processing the new post submission (POST).
    """
    if request.method == 'POST':
        blog_posts = load_blog_posts()

        # Get data from the submitted form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Generate a unique ID (max existing ID + 1, or 1 if list is empty)
        new_id = 1
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1

        # Create the new post dictionary
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)
        save_blog_posts(blog_posts)

        # Redirect to the new post's page (or index)
        return redirect(url_for('view_post', post_id=new_id))

        # Handle GET request: just show the form
    return render_template('add.html')


@app.route('/post/<int:post_id>')
def view_post(post_id):
    """Displays a single blog post based on its ID."""
    blog_posts = load_blog_posts()

    # Use a generator expression to find the post efficiently
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        # If the post is not found
        abort(404)

    return render_template('view_post.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a blog post with the given ID and redirects to the index."""

    blog_posts = load_blog_posts()

    # Find the index of the post to delete
    post_index_to_delete = -1
    for i, post in enumerate(blog_posts):
        if post['id'] == post_id:
            post_index_to_delete = i
            break

    if post_index_to_delete != -1:
        # Remove the post from the list
        blog_posts.pop(post_index_to_delete)

        # Save the updated list back to the JSON file
        save_blog_posts(blog_posts)

    # Redirect back to the homepage
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True)