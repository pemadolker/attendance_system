from flask import Flask, jsonify
from prisma import Prisma
from fastapi import APIRouter

router = APIRouter()

app = Flask(__name__)
prisma = Prisma()

@router.get('/profile/{userid}/editpf')
async def edit_profile(username):
    try:
        following = await prisma.user.find_unique(
            where={
                'username': username,
            },
            select={
                'username': True,
                'bio': True,
            },
        )
        return jsonify(following)
    except Exception as error:
        return jsonify({'error': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)