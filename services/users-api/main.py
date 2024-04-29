from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI()


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    is_active: bool = True


users_db: List[User] = []
user_id_counter: int = 1


@app.get("/users", response_model=List[User])
def read_users():
    return users_db


@app.post("/users", response_model=User, status_code=201)
def create_user(user: User):
    global user_id_counter
    user.id = user_id_counter
    user_id_counter += 1
    users_db.append(user)
    return user


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):  # Changed from UUID to int
    idx = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[idx] = user
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):  # Changed from UUID to int
    idx = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.pop(idx)
    return {"message": "User deleted successfully"}
