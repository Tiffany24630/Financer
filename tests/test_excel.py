import pandas as pd

def test_dataframe():

    df = pd.DataFrame({
        "ventas": [100, 200]
    })

    assert len(df) == 2