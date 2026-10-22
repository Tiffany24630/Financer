from types import SimpleNamespace
from unittest.mock import patch
import pandas as pd
from backend.excel_processor import (
    dataframe_to_text,
    get_summary,
    read_excel,
)
from backend.validations import validate_dataframe, validate_file

def test_validate_file_rejects_missing_file():
    valid, message = validate_file(None)

    assert valid is False
    assert message

def test_validate_file_accepts_file_at_size_limit():
    file_at_limit = SimpleNamespace(size=10 * 1024 * 1024)

    valid, message = validate_file(file_at_limit)

    assert valid is True
    assert message

def test_validate_file_rejects_file_over_size_limit():
    oversized_file = SimpleNamespace(size=(10 * 1024 * 1024) + 1)

    valid, message = validate_file(oversized_file)

    assert valid is False
    assert message

def test_validate_dataframe_rejects_empty_dataframe():
    valid, message = validate_dataframe(pd.DataFrame())

    assert valid is False
    assert message

def test_validate_dataframe_rejects_dataframe_with_fewer_than_two_columns():
    dataframe = pd.DataFrame({"ventas": [100, 200]})

    valid, message = validate_dataframe(dataframe)

    assert valid is False
    assert message

def test_validate_dataframe_accepts_dataframe_with_two_columns():
    dataframe = pd.DataFrame({
        "ventas": [100, 200],
        "costos": [50, 75],
    })

    valid, message = validate_dataframe(dataframe)

    assert valid is True
    assert message

def test_read_excel_delegates_to_pandas():
    uploaded_file = object()
    expected_dataframe = pd.DataFrame({"ventas": [100, 200]})

    with patch(
        "backend.excel_processor.pd.read_excel",
        return_value=expected_dataframe,
    ) as read_excel_mock:
        result = read_excel(uploaded_file)

    assert result is expected_dataframe
    read_excel_mock.assert_called_once_with(uploaded_file)

def test_dataframe_to_text_returns_dataframe_representation():
    dataframe = pd.DataFrame({"ventas": [100, 200]})

    result = dataframe_to_text(dataframe)

    assert result == dataframe.to_string()

def test_get_summary_reports_rows_columns_and_null_values():
    dataframe = pd.DataFrame({
        "ventas": [100, None],
        "costos": [50, 75],
    })

    assert get_summary(dataframe) == {
        "rows": 2,
        "columns": 2,
        "null_values": 1,
    }