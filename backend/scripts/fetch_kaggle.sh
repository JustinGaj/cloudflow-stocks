#!/usr/bin/env bash
set -euo pipefail

# Downloads Kaggle dataset and optionally extracts a sample subset
# expects KAGGLE_CONFIG_DIR or ~/.kaggle/kaggle.json to be present

WORKDIR=$(pwd)
OUT_DIR="${WORKDIR}/backend/data"
TMP_DIR="/tmp/kaggle_dataset"

mkdir -p "${OUT_DIR}" "${TMP_DIR}"

echo "Downloading dataset (jacksoncrow/stock-market-dataset) to ${TMP_DIR}..."
kaggle datasets download -d jacksoncrow/stock-market-dataset -p "${TMP_DIR}" --unzip

# The dataset contains many files; choose a main CSV — example: 'all_stocks_5yr.csv' or adapt as needed
CSV_FILE=$(ls ${TMP_DIR} | grep -iE '\.csv$' | head -n1)
if [ -z "${CSV_FILE}" ]; then
  echo "No CSV found in ${TMP_DIR}; aborting"
  exit 1
fi

echo "Processing ${CSV_FILE}..."
python backend/scripts/process_dataset.py "${TMP_DIR}/${CSV_FILE}" "${OUT_DIR}/sample.csv"

echo "Dataset processed to ${OUT_DIR}/sample.csv"
ls -l "${OUT_DIR}"
