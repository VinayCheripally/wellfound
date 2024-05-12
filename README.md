To get started, clone the repository:

git clone https://github.com/VinayCheripally/wellfound.git

Setup and Running Instructions

Install the required dependencies:

cd wellfound
pip install fastapi uvicorn pymongo pydantic

Replace <your_mongodb_connection_string> with your MongoDB connection string in the .env file.

Run the API using the following command:

uvicorn main:app --reload

Access the API at http://127.0.0.1:8000.

API Documentation

The API has the following endpoints:

    POST /posts/: Create a new post.
    GET /posts/: Get all posts.
    GET /posts/{post_id}: Get a specific post by ID.
    PUT /posts/{post_id}: Update a specific post by ID.
    DELETE /posts/{post_id}: Delete a specific post by ID.
    POST /posts/{post_id}/comments/: Create a new comment for a post.
    GET /posts/{post_id}/comments/: Get all comments for a post.
    PUT /posts/{post_id}/like/: Like a specific post by ID.
    PUT /posts/{post_id}/dislike/: Dislike a specific post by ID.

Data Models

    Post:
        id: int (unique identifier for the post).
        title: str (title of the post).
        content: str (content of the post).
        likes: int (number of likes for the post).
        dislikes: int (number of dislikes for the post).

    Comment:
        id: int (unique identifier for the comment).
        post_id: int (ID of the post the comment belongs to).
        content: str (content of the comment).

Additional Notes

    The API uses FastAPI, a modern, fast web framework for building APIs with Python.
    The API uses Pydantic for data validation and serialization.
    The API uses MongoDB as the database.
    The API uses Uvicorn as the ASGI server.
    The API uses the .env file for configuration.
    The API uses the jsonable_encoder from FastAPI for encoding Pydantic models to JSON.
    The API uses a context manager to handle MongoDB connections.
    The API uses custom functions for error handling and input validation.
    The API uses docstrings for API documentation.
    The API uses the HTTPException class from FastAPI for error handling.
    The API uses the JSONResponse class from FastAPI for returning JSON responses.
