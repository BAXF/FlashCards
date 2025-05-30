# FlashCards
A Django-based web application for creating, managing, and studying subject-specific flashcards with REST API support.

## Features

- **Web Interface**: Create, manage, and study flashcards through a user-friendly web interface
- **REST API**: Full CRUD operations for cards and card groups via REST API
- **User Authentication**: Secure user management with session-based authentication
- **Card Groups**: Organize flashcards into subject-specific groups
- **Image Support**: Upload images for both cards and card groups
- **Random Card Selection**: Get random cards for studying
- **Search Functionality**: Search cards by name or description
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository: 
    ```bash
    git clone https://github.com/mparvin/FlashCards.git
    ```
2. Enter the project directory:
    ```bash
    cd FlashCards
    ```

3. Build the Docker images:
    ```bash
    docker-compose build
    ```

4. Run the Docker containers:
    ```bash
    docker-compose up -d
    ```

This will start the PostgreSQL database, Adminer, Nginx, and Django application.

5. Open the application in your web browser:
    ```bash
    http://localhost:8000
    ```

6. Run migrations:
    ```bash
    docker-compose exec app python manage.py makemigrations
    docker-compose exec app python manage.py migrate
    ```
        
7. Create a superuser:
    ```bash
    docker-compose exec app python manage.py createsuperuser
    ```

## Making changes to Models
If you make changes to the Django models, you will need to create and apply migrations for those changes to take effect. Here are the steps:

1. Create migrations:
    ```bash
    docker-compose exec app python manage.py makemigrations
    ```
2. Apply migrations:
    ```bash
    docker-compose exec app python manage.py migrate
    ```

## Collect statics
To collect static files:
    ```bash
    docker-compose exec app python manage.py collectstatic
    ```

## Tips
- Always create and apply migrations whenever you make changes to your models.
- If you encounter issues with your database after changing your models, you may need to rebuild your Docker containers. You can do this with 
    ```bash
    docker-compose up -d --force-recreate --build app
    ```

## API Usage

The FlashCards application provides a comprehensive REST API for programmatic access to cards and card groups. The API is publicly accessible and does not require authentication.

### API Base URL
```
http://localhost:8000/api/
```

### Card Groups API

#### List all card groups
```bash
curl http://localhost:8000/api/groups/
```

#### Create a new card group
```bash
curl -X POST http://localhost:8000/api/groups/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Science", "image": null}'
```

#### Get a specific card group
```bash
curl http://localhost:8000/api/groups/1/
```

#### Update a card group
```bash
curl -X PATCH http://localhost:8000/api/groups/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Science"}'
```

#### Delete a card group
```bash
curl -X DELETE http://localhost:8000/api/groups/1/
```

#### Get all cards in a group
```bash
curl http://localhost:8000/api/groups/1/cards/
```

### Cards API

#### List all cards
```bash
curl http://localhost:8000/api/cards/
```

#### Create a new card
```bash
curl -X POST http://localhost:8000/api/cards/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pythagoras Theorem",
    "group": 1,
    "description": "a² + b² = c²",
    "status": "published"
  }'
```

#### Get a specific card
```bash
curl http://localhost:8000/api/cards/{card-uuid}/
```

#### Update a card
```bash
curl -X PATCH http://localhost:8000/api/cards/{card-uuid}/ \
  -H "Content-Type: application/json" \
  -d '{"description": "Updated description"}'
```

#### Delete a card
```bash
curl -X DELETE http://localhost:8000/api/cards/{card-uuid}/
```

### Special Card Endpoints

#### Get cards from a specific group
```bash
curl "http://localhost:8000/api/cards/by_group/?group_id=1"
```

#### Get a random card (optionally from a specific group)
```bash
# Random card from all cards
curl http://localhost:8000/api/cards/random/

# Random card from specific group
curl "http://localhost:8000/api/cards/random/?group_id=1"
```

#### Search cards
```bash
curl "http://localhost:8000/api/cards/search/?q=math"
```

### JavaScript/Frontend Integration

```javascript
// Create a new card
fetch('/api/cards/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'New Card',
        group: 1,
        description: 'Card description',
        status: 'published'
    })
})
.then(response => response.json())
.then(data => console.log('Card created:', data))
.catch(error => console.error('Error:', error));

// Get all cards
fetch('/api/cards/')
.then(response => response.json())
.then(data => console.log('Cards:', data.results))
.catch(error => console.error('Error:', error));

// Get a random card
fetch('/api/cards/random/')
.then(response => response.json())
.then(data => console.log('Random card:', data))
.catch(error => console.error('Error:', error));

// Search for cards
fetch('/api/cards/search/?q=mathematics')
.then(response => response.json())
.then(data => console.log('Search results:', data.results))
.catch(error => console.error('Error:', error));

// Get cards from a specific group
fetch('/api/cards/by_group/?group_id=1')
.then(response => response.json())
.then(data => console.log('Group cards:', data.results))
.catch(error => console.error('Error:', error));
```

### Response Format

All API responses are in JSON format. List endpoints include pagination:

```json
{
    "count": 10,
    "next": "http://localhost:8000/api/cards/?page=2",
    "previous": null,
    "results": [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Sample Card",
            "group": 1,
            "group_name": "Math",
            "description": "Sample description",
            "image": "http://localhost:8000/media/cards/sample.jpg",
            "created_at": "2025-05-31T10:00:00Z",
            "updated_at": "2025-05-31T10:00:00Z",
            "user": 1,
            "user_username": "john_doe",
            "status": "published"
        }
    ]
}
```

### Card Status Values
- `draft`: Card is in draft mode
- `published`: Card is published and active
- `archived`: Card is archived

### Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).