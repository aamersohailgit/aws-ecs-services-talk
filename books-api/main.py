from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID
import httpx

app = FastAPI()


class Book(BaseModel):
    id: Optional[UUID] = uuid4()
    title: str
    author: str
    description: Optional[str] = None
    price: float


class Author(BaseModel):
    name: str
    email: str


# In-memory 'database' for the example
books_db: List[Book] = []


async def get_author_details(author_id: UUID) -> Optional[Author]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://users-api:9001/users/{author_id}")
        if response.status_code == 200:
            return Author(**response.json())
        else:
            return None


@app.get("/books", response_model=List[Book])
def read_books():
    return books_db


@app.post("/books", response_model=Book, status_code=201)
def create_book(book: Book):
    books_db.append(book)
    return book


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: UUID):
    book = next((book for book in books_db if book.id == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: UUID, book: Book):
    idx = next((i for i, b in enumerate(books_db) if b.id == book_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[idx] = book
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: UUID):
    idx = next((i for i, b in enumerate(books_db) if b.id == book_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db.pop(idx)
    return {"message": "Book deleted successfully"}
