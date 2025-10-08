.PHONY: help install dev build docker-build docker-up docker-down clean test lint

help:
	@echo "📑 Smart Invoice Analyzer - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install all dependencies"
	@echo "  make dev           - Run development servers"
	@echo "  make build         - Build for production"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker images"
	@echo "  make docker-up     - Start Docker containers"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         - Clean cache and build files"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"

install:
	@echo "📦 Installing backend dependencies..."
	python -m venv venv || true
	./venv/bin/pip install -r requirements.txt || venv\Scripts\pip install -r requirements.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend-nextjs && npm install

dev:
	@echo "🚀 Starting development servers..."
	@bash run.sh || run.bat

build:
	@echo "🔨 Building for production..."
	cd frontend-nextjs && npm run build

docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🚀 Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "📊 Viewing Docker logs..."
	docker-compose logs -f

clean:
	@echo "🧹 Cleaning cache and build files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf frontend-nextjs/.next 2>/dev/null || true
	rm -rf backend.log frontend.log 2>/dev/null || true
	@echo "✅ Cleanup complete"

test:
	@echo "🧪 Running tests..."
	./venv/bin/pytest backend/ || venv\Scripts\pytest backend/
	cd frontend-nextjs && npm test

lint:
	@echo "🔍 Running linters..."
	./venv/bin/flake8 backend/ || venv\Scripts\flake8 backend/
	cd frontend-nextjs && npm run lint

