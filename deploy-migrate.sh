#!/bin/bash
docker compose build
docker compose up -d
docker compose exec api alembic revision --autogenerate -m "$1"
docker compose exec api alembic upgrade head
echo "Migration complete!"
