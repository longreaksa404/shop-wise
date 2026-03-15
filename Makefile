.PHONY: help build up upd down restart logs shell bash migrate makemigrations superuser test clean tools
help:
	@echo ""
	@echo "  ShopWise Dev Commands"
	@echo "  ─────────────────────────────────────────────"
	@echo "  make build           Build Docker images"
	@echo "  make up              Start all services (foreground)"
	@echo "  make upd             Start all services (background)"
	@echo "  make down            Stop all services"
	@echo "  make restart         Restart all services"
	@echo "  make logs            Follow web container logs"
	@echo "  make shell           Open Django shell"
	@echo "  make bash            Open bash in web container"
	@echo "  make migrate         Run database migrations"
	@echo "  make makemigrations  Create new migrations"
	@echo "  make superuser       Create Django superuser"
	@echo "  make test            Run test suite"
	@echo "  make tools           Start with pgAdmin on :5050"
	@echo "  make clean           Remove containers + volumes"
	@echo ""

# ── Docker ────────────────────────────────────────────────────────────────────
build:
	docker compose build

up:
	docker compose up

upd:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down && docker compose up -d

logs:
	docker compose logs -f web

# ── Django ────────────────────────────────────────────────────────────────────
startapp:
	mkdir -p apps/$(name)
	docker compose exec web python manage.py startapp $(name) apps/$(name)

shell:
	docker compose exec web python manage.py shell

bash:
	docker compose exec web bash

makemigrations:
	docker compose exec -u root web python manage.py makemigrations
	sudo chown -R $(USER):$(USER) .

migrate:
	docker compose exec -u root web python manage.py migrate
	sudo chown -R $(USER):$(USER) .

superuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web python manage.py test --verbosity=2

# ── Optional tools ────────────────────────────────────────────────────────────
tools:
	docker compose --profile tools up -d

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	docker compose down -v --rmi local
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete