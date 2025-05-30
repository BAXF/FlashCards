# FlashCards API Documentation

This document describes the RESTful API endpoints for the FlashCards application.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API is publicly accessible and does not require authentication.

## API Endpoints

### Card Groups

#### List All Card Groups
- **URL**: `/api/groups/`
- **Method**: `GET`
- **Description**: Retrieve all card groups
- **Response**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Math",
            "image": "http://localhost:8000/media/card_groups/math.jpg",
            "created_at": "2025-05-31T10:00:00Z",
            "updated_at": "2025-05-31T10:00:00Z"
        }
    ]
}
```

#### Create Card Group
- **URL**: `/api/groups/`
- **Method**: `POST`
- **Description**: Create a new card group
- **Request Body**:
```json
{
    "name": "Science",
    "image": "base64_encoded_image_or_file"
}
```

#### Get Specific Card Group
- **URL**: `/api/groups/{id}/`
- **Method**: `GET`
- **Description**: Retrieve a specific card group

#### Update Card Group
- **URL**: `/api/groups/{id}/`
- **Method**: `PUT/PATCH`
- **Description**: Update a card group

#### Delete Card Group
- **URL**: `/api/groups/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a card group

#### Get Cards in Group
- **URL**: `/api/groups/{id}/cards/`
- **Method**: `GET`
- **Description**: Get all cards in a specific group

### Cards

#### List User's Cards
- **URL**: `/api/cards/`
- **Method**: `GET`
- **Description**: Retrieve all cards for the authenticated user
- **Response**:
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Pythagoras Theorem",
            "group": 1,
            "group_name": "Math",
            "description": "a² + b² = c²",
            "image": "http://localhost:8000/media/cards/pythagoras.jpg",
            "created_at": "2025-05-31T10:00:00Z",
            "updated_at": "2025-05-31T10:00:00Z",
            "user": 1,
            "user_username": "john_doe",
            "status": "published"
        }
    ]
}
```

#### Create Card
- **URL**: `/api/cards/`
- **Method**: `POST`
- **Description**: Create a new card
- **Request Body**:
```json
{
    "name": "Einstein's E=mc²",
    "group": 2,
    "description": "Energy equals mass times the speed of light squared",
    "image": "base64_encoded_image_or_file",
    "status": "published"
}
```

#### Get Specific Card
- **URL**: `/api/cards/{uuid}/`
- **Method**: `GET`
- **Description**: Retrieve a specific card

#### Update Card
- **URL**: `/api/cards/{uuid}/`
- **Method**: `PUT/PATCH`
- **Description**: Update a card
- **Request Body** (PATCH example):
```json
{
    "description": "Updated description",
    "status": "archived"
}
```

#### Delete Card
- **URL**: `/api/cards/{uuid}/`
- **Method**: `DELETE`
- **Description**: Delete a card

### Special Card Endpoints

#### Get Cards by Group
- **URL**: `/api/cards/by_group/?group_id={group_id}`
- **Method**: `GET`
- **Description**: Get all cards in a specific group for the authenticated user
- **Query Parameters**:
  - `group_id` (required): The ID of the card group

#### Get Random Card
- **URL**: `/api/cards/random/`
- **Method**: `GET`
- **Description**: Get a random card, optionally from a specific group
- **Query Parameters**:
  - `group_id` (optional): The ID of the card group to get random card from

#### Search Cards
- **URL**: `/api/cards/search/?q={query}`
- **Method**: `GET`
- **Description**: Search cards by name or description
- **Query Parameters**:
  - `q` (required): Search query string

## Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Card Status Options

Cards can have the following status values:
- `draft`: Card is in draft mode
- `published`: Card is published and active
- `archived`: Card is archived

## Example Usage

### Using cURL

#### Create a new card:
```bash
curl -X POST http://localhost:8000/api/cards/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Card",
    "group": 1,
    "description": "Test description",
    "status": "published"
  }'
```

#### Get a random card from a specific group:
```bash
curl -X GET "http://localhost:8000/api/cards/random/?group_id=1"
```

#### Search for cards:
```bash
curl -X GET "http://localhost:8000/api/cards/search/?q=math"
```

### Using JavaScript (fetch)

```javascript
// Get all cards
fetch('/api/cards/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => console.log(data));

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
.then(data => console.log(data));
```

## Notes

- The API is publicly accessible and does not require authentication
- Images can be uploaded as files or base64 encoded data
- The API supports pagination for list endpoints