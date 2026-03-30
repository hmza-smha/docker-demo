from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="App1 - User Service")

class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/")
def read_root():
    return {"message": "Welcome to App1 - User Service"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe", "email": "john@example.com"}

@app.post("/users")
def create_user(user: User):
    return {"message": "User created", "user": user}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "app1"}
