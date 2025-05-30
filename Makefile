# Variables for deployment configuration
REMOTE_HOST = fift
REMOTE_USER = root
DEPLOY_PATH = /opt/src/flashcards
PROJECT_NAME = flashcards

# Rsync options
RSYNC_OPTIONS = -avz --delete --progress
EXCLUDE_DIRS = --exclude='.git' --exclude='.idea' --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.pytest_cache'

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  deploy            - Full deployment (sync + django setup + docker up)"
	@echo "  sync              - Sync files to remote server"
	@echo "  django-setup      - Run Django migrations and collectstatic on remote"
	@echo "  makemigrations    - Create Django migrations on remote server"
	@echo "  migrate           - Apply Django migrations on remote server"
	@echo "  collectstatic     - Collect static files on remote server"
	@echo "  docker-up         - Run docker compose up on remote server"
	@echo "  docker-down       - Stop containers on remote server"
	@echo "  docker-restart    - Restart containers on remote server"
	@echo "  logs              - Show docker logs from remote server"
	@echo "  status            - Check container status"
	@echo "  shell             - Open Django shell on remote server"
	@echo "  reset             - Complete reset: remove migrations, sync, rebuild database and containers"
	@echo "  clean             - Clean up remote deployment"
	@echo "  help              - Show this help message"

# Sync files to remote server
.PHONY: sync
sync:
	@echo "Syncing files to $(REMOTE_USER)@$(REMOTE_HOST):$(DEPLOY_PATH)..."
	rsync $(RSYNC_OPTIONS) $(EXCLUDE_DIRS) ./ $(REMOTE_USER)@$(REMOTE_HOST):$(DEPLOY_PATH)/
	@echo "Files synced successfully!"

# Create Django migrations on remote server
.PHONY: makemigrations
makemigrations:
	@echo "Creating Django migrations on remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose exec -T app python manage.py makemigrations"
	@echo "Migrations created successfully!"

# Apply Django migrations on remote server
.PHONY: migrate
migrate:
	@echo "Applying Django migrations on remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose exec -T app python manage.py migrate"
	@echo "Migrations applied successfully!"

# Collect static files on remote server
.PHONY: collectstatic
collectstatic:
	@echo "Collecting static files on remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose exec -T app python manage.py collectstatic --noinput"
	@echo "Static files collected successfully!"

# Run all Django setup commands
.PHONY: django-setup
django-setup: migrate collectstatic
	@echo "Django setup completed successfully!"

# Run docker compose up on remote server
.PHONY: docker-up
docker-up:
	@echo "Running docker compose up on remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose up -d --build --remove-orphans"
	@echo "Docker containers started successfully!"

# Stop docker containers on remote server
.PHONY: docker-down
docker-down:
	@echo "Stopping docker containers on remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose down"
	@echo "Docker containers stopped!"

# Restart docker containers on remote server
.PHONY: docker-restart
docker-restart: docker-down docker-up
	@echo "Docker containers restarted successfully!"

# Full deployment: sync + docker up + django setup
.PHONY: deploy
deploy: sync docker-up django-setup
	@echo "Full deployment completed successfully!"

# Show logs from remote docker containers
.PHONY: logs
logs:
	@echo "Fetching logs from remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose logs -f"

# Check status of remote containers
.PHONY: status
status:
	@echo "Checking container status on remote server..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose ps"

# Open Django shell on remote server
.PHONY: shell
shell:
	@echo "Opening Django shell on remote server..."
	ssh -t $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose exec app python manage.py shell"

# Run Django management commands on remote server
.PHONY: manage
manage:
	@echo "Running Django management command: $(CMD)"
	@if [ -z "$(CMD)" ]; then \
		echo "Usage: make manage CMD='your_command'"; \
		echo "Example: make manage CMD='createsuperuser'"; \
	else \
		ssh -t $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose exec app python manage.py $(CMD)"; \
	fi

# Clean up remote deployment
.PHONY: clean
clean:
	@echo "Cleaning up remote deployment..."
	ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd $(DEPLOY_PATH) && docker compose down -v --remove-orphans"

# Complete reset: remove migrations, sync, rebuild database and containers
.PHONY: reset
reset:
	@echo "Starting complete reset..."
	@echo "Step 1: Removing all migration files locally (keeping __init__.py)..."
	find ./cards/migrations/ -name "*.py" ! -name "__init__.py" -delete
	@echo "Step 2: Syncing cleaned files to remote server..."
	$(MAKE) sync
	@echo "Step 3: Stopping containers and removing volumes..."
	make clean
	@echo "Step 4: Starting fresh containers..."
	make docker-up
	@echo "Step 5: Waiting for containers to be ready..."
	sleep 10
	@echo "Step 6: Creating fresh migrations..."
	make makemigrations
	@echo "Step 7: Applying migrations..."
	make migrate
	@echo "Step 8: Collecting static files..."
	make collectstatic
	@echo "Reset completed successfully!"