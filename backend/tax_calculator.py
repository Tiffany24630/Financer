def calculate_basic_metrics(df):

    numeric_columns = df.select_dtypes(include="number")

    totals = {}

    for column in numeric_columns.columns:
        totals[column] = float(df[column].sum())

    return totals