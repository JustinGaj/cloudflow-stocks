#!/usr/bin/env python3
import sys
import pandas as pd

def process(input_csv: str, out_csv: str):
    # Example: keep relevant columns and a limited date range
    df = pd.read_csv(input_csv)
    # Standardize column names if different dataset uses others:
    # If dataset has 'Name' or 'symbol' column, adapt:
    if 'Name' not in df.columns and 'Name' in df.columns:
        pass
    # For this dataset, try common names:
    possible_name_cols = [c for c in ['Name','name','Symbol','symbol'] if c in df.columns]
    if possible_name_cols:
        df.rename(columns={possible_name_cols[0]:'Name'}, inplace=True)
    # Basic cleaning: drop NA, limit to last year of data (if there's a 'date' column)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.sort_values('date')
    # save sample subset to reduce size
    sample = df.head(5000)
    sample.to_csv(out_csv, index=False)
    print(f"Saved processed sample to {out_csv}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: process_dataset.py <input_csv> <output_csv>")
        sys.exit(1)
    process(sys.argv[1], sys.argv[2])
