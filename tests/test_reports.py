import pytest
from youtube_clickbait.reports import report_clickbait, get_report, register_report

@pytest.fixture
def sample_data():
    return [
        {"title": "A", "ctr": 20.0, "retention_rate": 35.0},
        {"title": "B", "ctr": 10.0, "retention_rate": 80.0},
        {"title": "C", "ctr": 25.0, "retention_rate": 30.0},
        {"title": "D", "ctr": 18.0, "retention_rate": 45.0},  # retention too high
        {"title": "E", "ctr": 30.0, "retention_rate": 20.0},
    ]

def test_clickbait_filtering(sample_data):
    result = report_clickbait(sample_data)
    
    # Check that all expected videos are in result
    # E (30.0), C (25.0), A (20.0)
    assert "E" in result
    assert "30" in result  # Check without .0 because tabulate might format differently
    assert "C" in result
    assert "25" in result
    assert "A" in result
    assert "20" in result
    
    # Check that non-matching videos are not in result
    assert "B" not in result
    assert "D" not in result
    
    # Check order - E should come before C, C before A
    lines = result.split("\n")
    # Find positions of each video in the table
    positions = {}
    for i, line in enumerate(lines):
        if "E" in line and "30" in line:
            positions["E"] = i
        elif "C" in line and "25" in line:
            positions["C"] = i
        elif "A" in line and "20" in line:
            positions["A"] = i
    
    # Check order (lower line number = appears earlier)
    assert positions["E"] < positions["C"] < positions["A"]

def test_clickbait_empty_data():
    result = report_clickbait([])
    # Should return table with only headers
    assert "title" in result
    assert "ctr" in result
    assert "retention_rate" in result
    # Should have only header and borders, no data rows
    lines = [line for line in result.split("\n") if line.strip()]
    # With grid format, there should be 3 lines for empty table: top border, header, bottom border
    assert len(lines) >= 3

def test_clickbait_no_matches():
    data = [
        {"title": "X", "ctr": 10.0, "retention_rate": 50.0},
        {"title": "Y", "ctr": 20.0, "retention_rate": 50.0},  # retention too high
        {"title": "Z", "ctr": 10.0, "retention_rate": 30.0},  # ctr too low
    ]
    result = report_clickbait(data)
    # Should return table with only headers (no data rows)
    assert "title" in result
    assert "ctr" in result
    assert "retention_rate" in result
    # Check that no data rows (with titles) are present
    assert "X" not in result
    assert "Y" not in result
    assert "Z" not in result

def test_clickbait_with_float_precision():
    data = [
        {"title": "Test1", "ctr": 15.1, "retention_rate": 39.9},
        {"title": "Test2", "ctr": 15.0, "retention_rate": 39.9},  # ctr not > 15 (excluded)
        {"title": "Test3", "ctr": 15.1, "retention_rate": 40.0},  # retention not < 40 (excluded)
    ]
    result = report_clickbait(data)
    assert "Test1" in result
    assert "Test2" not in result
    assert "Test3" not in result

def test_get_report_known():
    func = get_report("clickbait")
    assert func is report_clickbait

def test_get_report_unknown():
    with pytest.raises(ValueError, match="Unknown report type: invalid"):
        get_report("invalid")

def test_register_report():
    def dummy(data):
        return "dummy"
    register_report("dummy", dummy)
    assert get_report("dummy") is dummy
    # Clean up
    global _REPORTS
    from youtube_clickbait.reports import _REPORTS
    del _REPORTS["dummy"]