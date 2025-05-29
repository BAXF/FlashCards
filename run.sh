#!/bin/bash

# Clean up existing containers and volumes
# make clean

# Start containers with build and force recreate
make docker-up

# Run Django setup (migrations and collectstatic)
make django-setup

# Create superuser
make manage CMD='createsuperuser'
