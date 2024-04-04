# FlashCards
A Django-based web application for creating, managing, and studying subject-specific flashcards.

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