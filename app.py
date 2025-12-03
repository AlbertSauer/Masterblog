import json
from flask import Flask, render_template

app = Flask(__name__)


# Function to load the blog posts from the JSON file
def load_blog_posts():
    """Reads the list of blog posts from posts.json."""
    try:
        # Open the file and load the JSON data
        with open('posts.json', 'r') as f:
            blog_posts = json.load(f)
        return blog_posts
    except FileNotFoundError:
        print("Error: posts.json not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from posts.json.")
        return []


# Create the Index Route
@app.route('/')
def index():
    # Fetch the blog posts
    blog_posts = load_blog_posts()

    # Pass the list of posts to the template
    return render_template('index.html', posts=blog_posts)


# You would typically run the app at the end of the file
if __name__ == '__main__':
    app.run(debug=True)