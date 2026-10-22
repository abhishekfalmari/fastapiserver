"""
FastAPI Boilerplate Application with PostgreSQL integration
A minimal but production-ready FastAPI application structure.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import models
import os
from database import get_db, create_tables
from sqlalchemy.orm import Session

# Create database tables
create_tables()

app = FastAPI(
    title="FastAPI Boilerplate API",
    description="""A production-ready FastAPI boilerplate application with essential features for quick development.

## Features

- **CRUD Operations**: Complete RESTful API for item management
- **Automatic Documentation**: Interactive API docs via Swagger UI and ReDoc
- **Validation**: Request/response validation with Pydantic models
- **Search & Filter**: Query items by name and price range
- **Health Check**: Monitoring endpoint for deployment health
- **Error Handling**: Proper HTTP status codes and error messages

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces provide:
- Interactive API exploration
- Request/response examples
- Code generation snippets
- Try-it-out functionality for testing endpoints directly from the browser
    """,
    version="0.1.0",
    contact={
        "name": "Developer",
        "url": "https://github.com/yourusername/fastapiserver",
        "email": "developer@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://example.com/terms/",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    model_config = {
        "from_attributes": True
    }




@app.get("/", tags=["root"])
async def root():
    """Root endpoint providing API information and documentation links."""
    return {
        "message": "Welcome to the FastAPI Boilerplate API",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "version": "0.1.0"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


@app.get("/items", response_model=List[Item], tags=["items"])
async def get_items(db: Session = Depends(get_db)):
    """Retrieve all items."""
    return db.query(models.ItemDB).all()


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific item by ID."""
    item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=201, tags=["items"])
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item."""
    db_item = models.ItemDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    """Update an existing item."""
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item."""
    db_item = db.query(models.ItemDB).filter(models.ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return None


@app.get("/items/search/", response_model=List[Item], tags=["items"])
async def search_items(q: Optional[str] = None, min_price: Optional[float] = None, db: Session = Depends(get_db)):
    """Search items by query and minimum price."""
    query = db.query(models.ItemDB)
    if q:
        query = query.filter(models.ItemDB.name.ilike(f"%{q}%"))
    if min_price is not None:
        query = query.filter(models.ItemDB.price >= min_price)
    return query.all()