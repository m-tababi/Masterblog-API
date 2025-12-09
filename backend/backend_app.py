from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

# Swagger UI configuration
SWAGGER_URL = "/api/docs"  # URL for exposing Swagger UI
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog-API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def validate_post_data(data, partial: bool = False):
    """
    Validate blog post data.

    required fields (if partial=False):
      - title
      - content

    If partial=True:
      - only check fields that are provided

    Returns:
      list of errors, or None if valid.
    """
    required_fields = ["title", "content"]
    errors = []

    for field in required_fields:
        value = data.get(field)

        # If field is missing and full validation is required
        if value is None:
            if not partial:
                errors.append(f"{field.capitalize()} is required.")
            continue

        # If field exists but is not a valid non-empty string
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field.capitalize()} must be a non-empty string.")

    return errors if errors else None


def find_post_by_id(post_id: int):
    """Return the post dict with the given id, or None if not found."""
    return next((post for post in POSTS if post['id'] == post_id), None)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Return all blog posts, optionally sorted by title or content."""
    sort = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    results = POSTS.copy()

    if sort is None:
        return jsonify(results), 200

    if sort not in ["title", "content"]:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    if direction not in ["asc", "desc"]:
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    reverse = direction == "desc"
    results.sort(key=lambda post: post[sort].lower(), reverse=reverse)

    return jsonify(results), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Create a new blog post with the provided data."""
    new_post = request.get_json()

    if not new_post:
        return jsonify({"error": "Request body must be JSON."}), 400

    validation_errors = validate_post_data(new_post)

    if validation_errors:
        return jsonify({
            "error": "Invalid post data",
            "details": validation_errors
        }), 400

    new_id = max((post["id"] for post in POSTS), default=0) + 1

    created_post = {
        "id": new_id,
        "title": new_post["title"],
        "content": new_post["content"]
    }

    POSTS.append(created_post)
    return jsonify(created_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int):
    """Delete a blog post by id."""
    global POSTS
    post = find_post_by_id(post_id)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    POSTS = [p for p in POSTS if p["id"] != post_id]
    return (
        jsonify(
            {"message": f"Post with id {post_id} has been deleted successfully."}
        ),
        200,
    )


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id: int):
    """Update an existing blog post by id."""
    post = find_post_by_id(post_id)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    updated_data = request.get_json()

    if not updated_data:
        return jsonify({"error": "No data provided for update"}), 400

    validation_errors = validate_post_data(updated_data, partial=True)

    if validation_errors:
        return jsonify(
            {
                "error": "Invalid post data",
                "details": validation_errors,
            }
        ), 400

    if "title" in updated_data:
        post["title"] = updated_data["title"]
    if "content" in updated_data:
        post["content"] = updated_data["content"]

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Search for blog posts by title or content."""
    title = request.args.get('title', '').lower()
    content = request.args.get('content', '').lower()

    results = []

    for post in POSTS:
        if (
            (title and title in post['title'].lower()) or
            (content and content in post['content'].lower())
        ):
            results.append(post)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
