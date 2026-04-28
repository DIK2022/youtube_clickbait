import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from youtube_clickbait.cli import main, parse_args

def test_parse_args_valid():
    args = parse_args(["--files", "a.csv", "b.csv", "--report", "clickbait"])
    assert args.files == ["a.csv", "b.csv"]
    assert args.report == "clickbait"

def test_parse_args_missing_required():
    with pytest.raises(SystemExit):
        parse_args([])

@patch("youtube_clickbait.cli.read_csv_files")
@patch("youtube_clickbait.cli.get_report")
@patch("pathlib.Path.is_file")
def test_main_success(mock_is_file, mock_get_report, mock_read_csv_files, capsys):
    # Mock file existence check
    mock_is_file.return_value = True
    
    mock_read_csv_files.return_value = [{"title": "Test", "ctr": 20.0, "retention_rate": 35.0}]
    mock_report_func = lambda x: "FAKE TABLE"
    mock_get_report.return_value = mock_report_func

    with patch("sys.argv", ["cli", "--files", "dummy.csv", "--report", "clickbait"]):
        main()

    captured = capsys.readouterr()
    assert "FAKE TABLE" in captured.out
    mock_read_csv_files.assert_called_once()
    mock_get_report.assert_called_once_with("clickbait")

@patch("pathlib.Path.is_file")
def test_main_file_not_found(mock_is_file, capsys):
    mock_is_file.return_value = False
    with patch("sys.argv", ["cli", "--files", "missing.csv", "--report", "clickbait"]):
        with pytest.raises(SystemExit):
            main()
    captured = capsys.readouterr()
    assert "File not found" in captured.err

@patch("youtube_clickbait.cli.read_csv_files")
@patch("youtube_clickbait.cli.get_report")
@patch("pathlib.Path.is_file")
def test_main_unknown_report(mock_is_file, mock_get_report, mock_read_csv_files, capsys):
    mock_is_file.return_value = True
    mock_read_csv_files.return_value = [{"title": "Test", "ctr": 20.0, "retention_rate": 35.0}]
    mock_get_report.side_effect = ValueError("Unknown report type: invalid")
    
    with patch("sys.argv", ["cli", "--files", "dummy.csv", "--report", "invalid"]):
        with pytest.raises(SystemExit):
            main()
    captured = capsys.readouterr()
    assert "Unknown report type" in captured.err