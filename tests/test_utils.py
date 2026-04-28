import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import csv
from io import StringIO
from youtube_clickbait.utils import read_csv_files

def test_read_csv_files_success():
    csv_content = """title,ctr,retention_rate,views
Video1,15.5,35.0,1000
Video2,20.0,40.0,2000
Video3,invalid,50.0,3000
Video4,25.0,invalid,4000
"""
    mock_file = mock_open(read_data=csv_content)
    
    with patch("builtins.open", mock_file):
        result = read_csv_files([Path("dummy.csv")])
    
    # Should skip invalid rows
    assert len(result) == 2
    assert result[0]["title"] == "Video1"
    assert result[0]["ctr"] == 15.5
    assert result[0]["retention_rate"] == 35.0
    assert result[1]["title"] == "Video2"
    assert result[1]["ctr"] == 20.0
    assert result[1]["retention_rate"] == 40.0

def test_read_csv_files_multiple():
    csv1 = """title,ctr,retention_rate
Video1,10.0,30.0
"""
    csv2 = """title,ctr,retention_rate
Video2,20.0,40.0
"""
    with patch("builtins.open") as mock_open_func:
        mock_open_func.side_effect = [
            mock_open(read_data=csv1).return_value,
            mock_open(read_data=csv2).return_value,
        ]
        result = read_csv_files([Path("file1.csv"), Path("file2.csv")])
    
    assert len(result) == 2
    assert result[0]["title"] == "Video1"
    assert result[1]["title"] == "Video2"

def test_read_csv_files_empty():
    csv_content = "title,ctr,retention_rate\n"
    mock_file = mock_open(read_data=csv_content)
    
    with patch("builtins.open", mock_file):
        result = read_csv_files([Path("empty.csv")])
    
    assert len(result) == 0