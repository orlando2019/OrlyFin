#!/usr/bin/env bash
set -euo pipefail

required=(
  ENVIRONMENT
  BACKEND_PORT
  API_V1_PREFIX
  DATABASE_URL
  NEXT_PUBLIC_API_BASE_URL
)

if [[ ! -f .env ]]; then
  echo "[check-env] No existe .env. Puedes copiar .env.example -> .env"
  exit 1
fi

# shellcheck disable=SC1091
source .env

missing=0
for key in "${required[@]}"; do
  if [[ -z "${!key:-}" ]]; then
    echo "[check-env] Falta variable: ${key}"
    missing=1
  fi
done

if [[ "$missing" -eq 1 ]]; then
  exit 1
fi

echo "[check-env] Variables mínimas presentes"
