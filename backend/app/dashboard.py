from flask import Flask, jsonify
from fastapi import APIRouter, Depends
from .database import get_db
from .models import Post

router = APIRouter()

app = Flask(__name__)

@router.get('/{userid}/dashboard')
async def get_dashboard(userid: int, db=Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == userid).all()
    return jsonify(posts)
if __name__ == '__main__':
    app.run(debug=True)