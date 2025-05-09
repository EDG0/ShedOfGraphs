import pytest
import networkx as nx
import sys
import os

# Voeg hoofdmap toe aan het importpad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import (
    load_filter,
    count_edges_with_degree_sum,
    graph_passes_filter,
)

# ---------------------------
# Test count_edges_with_degree_sum
# ---------------------------
def test_count_edges_with_degree_sum():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])  # Degrees: 1,2,2,1
    assert count_edges_with_degree_sum(G, 3) == 2  # Edges (0,1) and (2,3)
    assert count_edges_with_degree_sum(G, 4) == 1  # Edge (1,2)
    assert count_edges_with_degree_sum(G, 5) == 0  # None match

# ---------------------------
# Test graph_passes_filter: type = min
# ---------------------------
def test_graph_passes_filter_min():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rules = [{"type": "min", "degree_sum": 3, "edges": 1}]
    assert graph_passes_filter(G, rules) is True

def test_graph_fails_filter_min():
    G = nx.Graph()
    G.add_edges_from([(0, 1)])
    rules = [{"type": "min", "degree_sum": 3, "edges": 1}]
    assert graph_passes_filter(G, rules) is False

# ---------------------------
# Test graph_passes_filter: type = max
# ---------------------------
def test_graph_passes_filter_max():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rules = [{"type": "max", "degree_sum": 3, "edges": 2}]
    assert graph_passes_filter(G, rules) is True

def test_graph_fails_filter_max():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])
    rules = [{"type": "max", "degree_sum": 3, "edges": 1}]
    assert graph_passes_filter(G, rules) is False

# ---------------------------
# Test graph_passes_filter: type = exact
# ---------------------------
def test_graph_passes_filter_exact():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])  # Degrees: 1,2,2,1
    rules = [{"type": "exact", "degree_sum": 3, "edges": 2}]
    assert graph_passes_filter(G, rules) is True

def test_graph_fails_filter_exact():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])
    rules = [{"type": "exact", "degree_sum": 3, "edges": 1}]
    assert graph_passes_filter(G, rules) is False

# ---------------------------
# Test unknown filter type
# ---------------------------
def test_unknown_filter_type_ignored():
    G = nx.Graph()
    G.add_edges_from([(0, 1)])
    rules = [{"type": "invalid_type", "degree_sum": 2, "edges": 1}]
    # Verwacht dat onbekend type niets doet (silent ignore of fail-safe True)
    assert graph_passes_filter(G, rules) is True

# ---------------------------
# Test ongeldige graph6 invoer
# ---------------------------
def test_invalid_graph6_input():
    with pytest.raises(Exception):
        nx.from_graph6_bytes(b"!invalid")

# ---------------------------
# Test load_filter
# ---------------------------
def test_load_filter(tmp_path):
    # Tijdelijk json-bestand
    f = tmp_path / "filter.json"
    f.write_text('{"rules": [{"type": "min", "degree_sum": 2, "edges": 1}]}')
    rules = load_filter(f)
    assert isinstance(rules, list)
    assert rules[0]["type"] == "min"





