from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

# File to store user data
file_path = "file path"

# Ensure the file exists
if not os.path.exists(file_path):
    open(file_path, "w").close()

def read_users():
    """Read users from the file and return a dictionary."""
    users = {}
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(", ")
            if len(parts) == 2:
                name = parts[0].split(": ")[1]
                age = int(parts[1].split(": ")[1])
                users[name] = age
    return users

def write_users(users):
    """Write users dictionary back to the file."""
    with open(file_path, "w") as file:
        for name, age in users.items():
            file.write(f"Name: {name}, Age: {age}\n")

@app.post("/register")
def register(user: User):
    """Register a new user and store in a text file."""
    users = read_users()
    if user.name in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user.name] = user.age
    write_users(users)
    return {"message": f"User {user.name} registered successfully"}

@app.post("/login")
def login(user: User):
    """Login a user by checking if they exist in the text file."""
    users = read_users()
    if user.name not in users:
        raise HTTPException(status_code=401, detail="Invalid username or not registered")

    return {"message": f"User {user.name} logged in successfully"}

@app.put("/update")
def update_user(name: str, updated_user: User):
    """Update user details."""
    users = read_users()
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users.pop(name)  # Remove old entry
    users[updated_user.name] = updated_user.age  # Add updated entry
    write_users(users)

    return {"message": f"User {name} updated successfully"}
@app.put("/update_name")
def update_name(old_name: str, new_name: str):
    """Update only the user's name while keeping the same age."""
    users = read_users()
    
    if old_name not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    age = users.pop(old_name)  # Remove old name and get the existing age
    users[new_name] = age  # Add new name with the same age
    write_users(users)

    return {"message": f"User '{old_name}' updated to '{new_name}' successfully"}
@app.delete("/delete")
def delete_user(name: str):
    """Delete a user from the file."""
    users = read_users()
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users.pop(name)  # Remove the user
    write_users(users)

    return {"message": f"User {name} deleted successfully"}

@app.get("/dashboard")
def dashboard(name: str):
    """Show the dashboard only if the user is registered."""
    users = read_users()
    if name not in users:
        raise HTTPException(status_code=403, detail="Access denied. Please register first.")

    return {"message": f"Welcome {name} to the dashboard"}

@app.get("/users")
def get_users():
    """Retrieve all registered users from the file."""
    users = read_users()
    return {"users": users}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
