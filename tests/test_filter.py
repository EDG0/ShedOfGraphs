import pytest
import networkx as nx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import graph_passes_filter, count_edges_with_degree_sum

# === Correct gedrag tests ===

def test_count_edges_with_degree_sum():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])
    assert count_edges_with_degree_sum(G, 3) == 2  # 0-1 (1+2), 2-3 (2+1)

def test_graph_passes_filter_exact_match():
    G = nx.path_graph(4)
    rules = [{"degree_sum": 3, "edges": 2, "type": "exact"}]
    assert graph_passes_filter(G, rules) is True

# === Foute input tests ===

def test_graph_passes_filter_missing_type():
    G = nx.path_graph(4)
    rules = [{"degree_sum": 3, "edges": 2}]  # Missing 'type'
    with pytest.raises(KeyError):
        graph_passes_filter(G, rules)

def test_graph_passes_filter_invalid_type():
    G = nx.path_graph(4)
    rules = [{"degree_sum": 3, "edges": 2, "type": "invalid"}]
    with pytest.raises(ValueError):
        graph_passes_filter(G, rules)

def test_graph_passes_filter_missing_degree_sum():
    G = nx.path_graph(4)
    rules = [{"edges": 2, "type": "min"}]  # Missing degree_sum
    with pytest.raises(KeyError):
        graph_passes_filter(G, rules)

def test_graph_passes_filter_missing_edges():
    G = nx.path_graph(4)
    rules = [{"degree_sum": 3, "type": "max"}]  # Missing edges
    with pytest.raises(KeyError):
        graph_passes_filter(G, rules)

def test_invalid_graph6_string(monkeypatch, capfd):
    from main import main

    # Simuleer ongeldige input via stdin
    monkeypatch.setattr("sys.stdin", iter(["invalid_graph6"]))
    main()

    # Lees de foutuitvoer
    out, err = capfd.readouterr()
    assert "Fout bij verwerken van graaf" in err


