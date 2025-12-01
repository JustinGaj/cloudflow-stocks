from app import etl
import pandas as pd
import os
import tempfile

def test_top_n_and_load_processed():
    # create a small dataframe
    df = pd.DataFrame({
        'Name': ['A', 'B', 'C'],
        'Open': [10, 20, 5],
        'Close': [11, 18, 7],
        'date': ['2020-01-01', '2020-01-02', '2020-01-03']
    })
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)
    data = etl.load_processed(tmp.name)
    assert isinstance(data, list)
    assert len(data) == 3
    top = etl.top_n(data, 2)
    assert len(top) == 2
    os.unlink(tmp.name)