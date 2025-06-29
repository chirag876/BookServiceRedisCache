from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
import json
from app.cache import redis_client

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books", response_model=list[schemas.BookOut])
async def list_books(db: Session = Depends(get_db)):
    cache_key = "all_books"

    try:
        # Check Redis first
        cached_books = await redis_client.get(cache_key)
        if cached_books:
            print("Cache Hit")
            return json.loads(cached_books)
    except Exception as e:
        print("Redis not available, skipping cache", e)

    print("Cache Miss - Fetching from DB")
    books = crud.get_books(db)
    result = [schemas.BookOut.model_validate(book).model_dump() for book in books]


    # Cache it for 5 minutes
    try:
        await redis_client.setex(cache_key, 300, json.dumps(result))
    except Exception as e:
        print("Redis not available, couldn't set cache", e)

    return result


@router.post("/books", response_model=schemas.BookOut)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@router.get("/books/{book_id}/reviews", response_model=list[schemas.ReviewOut])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews_by_book_id(db, book_id)

@router.post("/books/{book_id}/reviews", response_model=schemas.ReviewOut)
def add_review(book_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.add_review(db, book_id, review)
