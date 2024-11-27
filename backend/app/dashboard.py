from flask import Flask, jsonify
from fastapi import APIRouter, Depends
from .database import get_db
from .models import Post

router = APIRouter()

app = Flask(__name__)

@router.get('/{userid}/dashboard')
async def get_dashboard(userid: int, db=Depends(get_db), page: int = 1, limit: int = 5):
    offset = (page - 1) * limit
    posts = db.query(Post).filter(Post.user_id == userid).offset(offset).limit(limit).all()
    return jsonify(posts)
if __name__ == '__main__':
    app.run(debug=True)