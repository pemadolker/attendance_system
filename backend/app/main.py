from fastapi import FastAPI
from .database import Base, engine
from .auth import router as auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Attendance System ")

# Include auth routes
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Attendance System API"}
