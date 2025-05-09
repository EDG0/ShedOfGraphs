import sys
import os
import tempfile

# Voeg hoofdmap toe aan het importpad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from update_history import log_history

def test_update_history_adds_line():
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp:
        path = tmp.name

    try:
        input_count = 10
        output_count = 2
        filter_used = [{"degree_sum": 3, "edges": 1, "type": "min"}]
        passed_graphs = ["ABC@", "DEF@"]

        log_history(input_count, output_count, filter_used, passed_graphs, file_path = path)

        with open(path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 1
        assert "ABC@" in lines[0] and "DEF@" in lines[0]
        assert "10" in lines[0] and "2" in lines[0]

    finally:
        os.remove(path)

def test_update_history_with_empty_passed_graphs():
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp:
        path = tmp.name

    try:
        log_history(5, 0, [{"degree_sum": 2, "edges": 1, "type": "min"}], [], file_path = path)

        with open(path, "r") as f:
            lines = f.readlines()

        assert len(lines) == 0

    finally:
        os.remove(path)



