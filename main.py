from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Кітапхана API", version="1.0.0")

# ----------------------------
# 1️⃣ Модельдер (мәліметтер құрылымы)
# ----------------------------
class BookIn(BaseModel):
    title: str
    author: str
    year: int

class Book(BookIn):
    id: int

# ----------------------------
# 2️⃣ Мәліметтер базасы (памятьта)
# ----------------------------
books: List[Book] = []
next_id = 1

# ----------------------------
# 3️⃣ Endpoint-тер
# ----------------------------

# Барлық кітаптарды көру
@app.get("/books", response_model=List[Book])
def list_books():
    return books

# ID бойынша кітапты көру
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Кітап табылмады")

# Жаңа кітап қосу
@app.post("/books", response_model=Book, status_code=201)
def create_book(data: BookIn):
    global next_id
    new_book = Book(id=next_id, **data.model_dump())
    books.append(new_book)
    next_id += 1
    return new_book

# Кітапты жаңарту
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, data: BookIn):
    for book in books:
        if book.id == book_id:
            book.title = data.title
            book.author = data.author
            book.year = data.year
            return book
    raise HTTPException(status_code=404, detail="Кітап табылмады")

# Кітапты жою
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            del books[i]
            return
    raise HTTPException(status_code=404, detail="Кітап табылмады")
