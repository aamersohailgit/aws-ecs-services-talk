from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import uuid4, UUID

app = FastAPI()


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
    email: EmailStr
    is_active: bool = True


# In-memory 'database' for the example
users_db: List[User] = []


@app.get("/users", response_model=List[User])
def read_users():
    return users_db


@app.post("/users", response_model=User, status_code=201)
def create_user(user: User):
    users_db.append(user)
    return user


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: UUID):
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user: User):
    idx = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[idx] = user
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    idx = next((i for i, u in enumerate(users_db) if u.id == user_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.pop(idx)
    return {"message": "User deleted successfully"}
