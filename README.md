# FastAPI Server Boilerplate

A production-ready FastAPI boilerplate application with essential features for quick development.

## Features

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management
- Automatic API documentation with Swagger UI and ReDoc
- RESTful endpoints for CRUD operations
- Health check endpoint
- Search and filtering capabilities
- Proper error handling
- Clean, organized code structure

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fastapiserver
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
fastapiserver/
├── main.py          # Main application entry point
├── requirements.txt # Python dependencies
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## API Endpoints

### Root
- `GET /` - Welcome message and API information

### Health Check
- `GET /health` - Returns application health status

### Items
- `GET /items` - Retrieve all items
- `GET /items/{item_id}` - Retrieve a specific item by ID
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an existing item
- `DELETE /items/{item_id}` - Delete an item
- `GET /items/search/` - Search items by query and minimum price

## Item Model

```json
{
  "name": "string",
  "description": "string (optional)",
  "price": "float",
  "tax": "float (optional)",
  "id": "integer (auto-generated)"
}
```

## Development

To modify the application:
1. Edit `main.py` to add new endpoints or modify existing ones
2. Update Pydantic models as needed for your data structure
3. Restart the server to see changes (with `--reload` flag, changes are automatic)

## Production Deployment

For production, consider using:
- Gunicorn with Uvicorn workers:
  ```bash
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
  ```
- Docker containerization
- Proper environment variable management
- Database integration (replace in-memory storage)

## License

MIT License - feel free to use this boilerplate for your projects.