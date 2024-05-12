from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# MongoDB connection
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
client = MongoClient(MONGO_DB_URL)
db = client["blog"]
posts_collection = db["posts"]
comments_collection = db["comments"]

class Post(BaseModel):
    id: int
    title: str
    content: str
    likes: int = 0
    dislikes: int = 0

class Comment(BaseModel):
    id: int
    post_id: int
    content: str

def get_post(post_id: int) -> dict:
    """Get a post by ID"""
    post = posts_collection.find_one({"id": post_id})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found with the specific post_id")
    return post

def validate_post_id(post_id: int) -> None:
    """Validate post ID existence"""
    if not get_post(post_id):
        raise HTTPException(status_code=404, detail="Post not found with the specific post_id")

@app.post("/posts/")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = str(posts_collection.insert_one(post_dict).inserted_id)
    return JSONResponse(content={"message": "Post created successfully"}, status_code=201)

@app.get("/posts/")
async def read_posts():
    posts = posts_collection.find()
    res = []
    for post in posts:
        del post["_id"]
        res.append(post)
    return JSONResponse(content={"posts": res}, status_code=200)

@app.get("/posts/{post_id}")
async def read_post(post_id: int):
    post = get_post(post_id)
    del post["_id"]
    return JSONResponse(content={"post": post}, status_code=200)

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    validate_post_id(post_id)
    posts_collection.update_one({"id": post_id}, {"$set": post.dict()})
    return JSONResponse(content={"message": "Post updated successfully"}, status_code=200)

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    validate_post_id(post_id)
    posts_collection.delete_one({"id": post_id})
    return JSONResponse(content={"message": "Post deleted successfully"}, status_code=200)

@app.post("/posts/{post_id}/comments/")
async def create_comment(post_id: int, comment: Comment):
    validate_post_id(post_id)
    comment_dict = comment.dict()
    comment_dict["post_id"] = post_id
    comment_dict["id"] = str(comments_collection.insert_one(comment_dict).inserted_id)
    return JSONResponse(content={"message": "Comment created successfully"}, status_code=201)

@app.get("/posts/{post_id}/comments/")
async def read_comments(post_id: int):
    validate_post_id(post_id)
    comments = comments_collection.find({"post_id": post_id})
    res = []
    for comment in comments:
        del comment["_id"]
        res.append(comment)
    return JSONResponse(content={"comments": res}, status_code=200)

@app.put("/posts/{post_id}/like/")
async def like_post(post_id: int):
    validate_post_id(post_id)
    posts_collection.update_one({"id": post_id}, {"$inc": {"likes": 1}})
    return JSONResponse(content={"message": "Post liked successfully"}, status_code=200)

@app.put("/posts/{post_id}/dislike/")
async def dislike_post(post_id: int):
    validate_post_id(post_id)   
    posts_collection.update_one({"id": post_id}, {"$inc": {"dislikes": 1}})
    return JSONResponse(content={"message": "Post disliked successfully"}, status_code=200)