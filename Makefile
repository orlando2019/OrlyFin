SHELL := /bin/zsh

.PHONY: check-env bootstrap backend-dev frontend-dev test-backend tree

check-env:
	bash infra/scripts/check-env.sh

bootstrap:
	bash infra/scripts/bootstrap.sh

backend-dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	cd frontend && npm run dev

test-backend:
	cd backend && pytest -q

tree:
	find . -maxdepth 4 -type d | sort
