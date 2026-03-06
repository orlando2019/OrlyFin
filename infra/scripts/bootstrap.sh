#!/usr/bin/env bash
set -euo pipefail

echo "[bootstrap] Verificando entorno..."
bash infra/scripts/check-env.sh

echo "[bootstrap] Instalando dependencias backend..."
if command -v pip >/dev/null 2>&1; then
  (cd backend && pip install -e .)
else
  echo "[bootstrap] pip no encontrado, omitiendo backend"
fi

echo "[bootstrap] Instalando dependencias frontend..."
if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm install)
else
  echo "[bootstrap] npm no encontrado, omitiendo frontend"
fi

echo "[bootstrap] Listo"
