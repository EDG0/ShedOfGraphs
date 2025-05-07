import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from update_history import log_history
import tempfile

def test_log_history_writes_line():
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmpfile:
        file_path = tmpfile.name
        passed = ["ABC", "DEF"]
        log_history(
            input_count=10,
            output_count=2,
            filter_used=[{"degree_sum": 3, "edges": 1, "type": "min"}],
            passed_graphs=passed,
            file_path=file_path
        )

    with open(file_path, "r") as f:
        content = f.read()
        assert "ABC" in content
        assert "DEF" in content
        assert "10" in content
        assert "2" in content

