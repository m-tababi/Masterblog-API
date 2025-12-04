from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data, partial=False):
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

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Create a new blog post with the provided data.
    """
    new_post = request.get_json()

    if not new_post:
        return jsonify({"error": "Request body must be JSON."}), 400

    validation_errors = validate_post_data(new_post)

    if validation_errors:
        return jsonify({
            "error": "Invalid post data",
            "details": validation_errors
        }), 400

    if validation_errors:
        return jsonify({"error": "Invalid post data", "details": validation_errors}), 400

    new_id = max((post["id"] for post in POSTS), default=0) + 1

    created_post = {
        "id": new_id,
        "title": new_post["title"],
        "content": new_post["content"]
    }

    POSTS.append(created_post)
    return jsonify(created_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
