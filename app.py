import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# --- Data Loading and Saving Functions ---

def load_blog_posts():
    """Reads the list of blog posts from posts.json."""
    try:
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
        # 1. Load existing posts
        blog_posts = load_blog_posts()

        # 2. Get data from the submitted form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # 3. Generate a unique ID (max existing ID + 1, or 1 if list is empty)
        new_id = 1
        if blog_posts:
            # Get the maximum existing ID and add 1
            new_id = max(post['id'] for post in blog_posts) + 1

        # 4. Create the new post dictionary
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        # 5. Add the new post to the list
        blog_posts.append(new_post)

        # 6. Save the updated list back to the JSON file
        save_blog_posts(blog_posts)

        # 7. Redirect to the homepage to see the new post
        return redirect(url_for('index'))

    # Handle GET request: just show the form
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)