#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(pwd)
ARTIFACT_DIR="${ROOT_DIR}/artifacts"
mkdir -p "${ARTIFACT_DIR}"

VERSION=$(./scripts/generate_version.sh)
ARTNAME="artifact_${VERSION}.zip"
echo "Building artifact ${ARTNAME} ..."

# Build frontend locally (if not in CI)
pushd frontend
npm install --no-audit --no-fund
npm run build
popd

# Ensure backend build folder present (we include backend Dockerfile rather than image)
mkdir -p build
# Copy built frontend
rm -rf build/frontend || true
cp -r frontend/build build/frontend

# Copy docs (include compiled report PDF if present)
mkdir -p build/docs
cp -r docs build/docs

# Copy backend package and Dockerfile
mkdir -p build/backend
cp -r backend build/backend

pushd build
zip -r "${ARTIFACT_DIR}/${ARTNAME}" .
popd

echo "Artifact created: ${ARTIFACT_DIR}/${ARTNAME}"
