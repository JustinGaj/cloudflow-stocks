import pandas as pd
from typing import List, Dict

def load_processed(path: str) -> List[Dict]:
    df = pd.read_csv(path)
    # small normalization
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # produce top-per-stock aggregated metrics
    grouped = df.groupby('Name').agg({
        'Close': 'last',
        'Open': 'first',
    }).reset_index()
    grouped['change'] = (grouped['Close'] - grouped['Open']) / grouped['Open'] * 100.0
    grouped = grouped.sort_values('change', ascending=False).fillna(0)
    # convert to list of dicts
    result = grouped.head(200).to_dict(orient='records')
    return result

def top_n(data: List[Dict], n: int = 10):
    return data[:n]