from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

# File to store user data
file_path = "//Name of Path"

# Ensure the file exists
if not os.path.exists(file_path):
    open(file_path, "w").close()

def save_to_file(data: str):
    """Helper function to save user data to a file."""
    with open(file_path, "a") as file:  # Append mode
        file.write(data + "\n")

def user_exists(name: str) -> bool:
    """Check if a user exists in the file by properly parsing the name field."""
    with open(file_path, "r") as file:
        users = file.readlines()
    for user in users:
        user_info = user.strip().split(", ")  # Split "Name: John, Age: 30"
        if len(user_info) > 0 and user_info[0] == f"Name: {name}":
            return True
    return False

@app.post("/register")
def register(user: User):
    """Register a new user and store in a text file."""
    if user_exists(user.name):
        raise HTTPException(status_code=400, detail="User already exists")

    user_data = f"Name: {user.name}, Age: {user.age}"
    save_to_file(user_data)
    return {"message": f"User {user.name} registered successfully"}

@app.post("/login")
def login(user: User):
    """Login a user by checking if they exist in the text file."""
    if not user_exists(user.name):
        raise HTTPException(status_code=401, detail="Invalid username or not registered")

    return {"message": f"User {user.name} logged in successfully"}

@app.get("/dashboard")
def dashboard(name: str):
    """Show the dashboard only if the user is registered."""
    if not user_exists(name):
        raise HTTPException(status_code=403, detail="Access denied. Please register first.")

    return {"message": f"Welcome {name} to the dashboard"}

@app.get("/users")
def get_users():
    """Retrieve all registered users from the file."""
    try:
        with open(file_path, "r") as file:
            users = file.readlines()
        return {"users": [user.strip() for user in users]}
    except FileNotFoundError:
        return {"message": "No users found"}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
