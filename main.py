"""
FastAPI Boilerplate Application
A minimal but production-ready FastAPI application structure.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="FastAPI Boilerplate",
    description="A minimal FastAPI application for demonstration and extension",
    version="0.1.0",
    contact={
        "name": "Developer",
        "url": "https://github.com/yourusername/fastapiserver",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
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

    class Config:
        orm_mode = True


# In-memory storage for demonstration
items_db: List[Item] = []
next_id = 1


@app.get("/", tags=["root"])
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to the FastAPI Boilerplate API", "docs": "/docs"}


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


@app.get("/items", response_model=List[Item], tags=["items"])
async def get_items():
    """Retrieve all items."""
    return items_db


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def get_item(item_id: int):
    """Retrieve a specific item by ID."""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=Item, status_code=201, tags=["items"])
async def create_item(item: ItemCreate):
    """Create a new item."""
    global next_id
    new_item = Item(id=next_id, **item.dict())
    items_db.append(new_item)
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: int, item: ItemCreate):
    """Update an existing item."""
    for idx, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def delete_item(item_id: int):
    """Delete an item."""
    global items_db
    initial_length = len(items_db)
    items_db = [item for item in items_db if item.id != item_id]
    if len(items_db) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found")
    return None


@app.get("/items/search/", response_model=List[Item], tags=["items"])
async def search_items(q: Optional[str] = None, min_price: Optional[float] = None):
    """Search items by query and minimum price."""
    results = items_db
    if q:
        results = [item for item in results if q.lower() in item.name.lower()]
    if min_price is not None:
        results = [item for item in results if item.price >= min_price]
    return results