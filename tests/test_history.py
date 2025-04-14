import os
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from history import HistoryLogger

def test_log_creates_file_and_writes_data(tmp_path):
    log_file = tmp_path / "history.txt"
    logger = HistoryLogger(filepath=str(log_file))

    logger.log(10, 4, {"type": "min", "degree_sum": 4, "edges": 2}, ["ABC", "DEF"])

    assert log_file.exists()
    content = log_file.read_text()
    assert "10" in content
    assert "4" in content
    assert "ABC" in content
    assert "DEF" in content

def test_log_appends_multiple_times(tmp_path):
    log_file = tmp_path / "history.txt"
    logger = HistoryLogger(filepath=str(log_file))

    logger.log(5, 3, {"type": "exact", "degree_sum": 5, "edges": 1}, ["AAA"])
    logger.log(7, 2, {"type": "max", "degree_sum": 6, "edges": 4}, ["BBB"])

    lines = log_file.read_text().splitlines()
    assert len(lines) == 2
    assert "AAA" in lines[0]
    assert "BBB" in lines[1]

def test_log_with_empty_graph_list(tmp_path):
    log_file = tmp_path / "history.txt"
    logger = HistoryLogger(filepath=str(log_file))

    logger.log(3, 0, {"type": "min", "degree_sum": 3, "edges": 1}, [])

    content = log_file.read_text()
    assert "[]" not in content  # Moet geen lijst printen
    assert "\t0\t0\t" in content or "\t3\t0\t" in content  # structuur klopt

def test_log_fails_on_invalid_path():
    logger = HistoryLogger(filepath="/invalid_path/history.txt")

    with pytest.raises(Exception):
        logger.log(1, 1, "filter", ["graph"])

def test_log_fails_on_bad_data_type(tmp_path):
    log_file = tmp_path / "bad_data.txt"
    logger = HistoryLogger(filepath=str(log_file))

    with pytest.raises(TypeError):
        logger.log("ten", 2, {}, ["abc"])
