#!/usr/bin/env bash
set -euo pipefail
MAJOR_MINOR=$(cat VERSION)
CL=$(git rev-parse --short HEAD 2>/dev/null || echo "${BUILD_NUMBER:-local}")
echo "${MAJOR_MINOR}.${CL}"
