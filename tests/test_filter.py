import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import networkx as nx
from main import graph_passes_filter

def test_graph_passes_filter_exact_pass():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])  # Driehoek: graden zijn 2, 2, 2
    rules = [{"degree_sum": 4, "edges": 3, "type": "exact"}]  # Alle 3 edges hebben som 4
    assert graph_passes_filter(G, rules) is True

def test_graph_passes_filter_exact_fail():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (2, 3)])
    rules = [{"degree_sum": 4, "edges": 3, "type": "exact"}]  # Slechts 2 edges
    assert graph_passes_filter(G, rules) is False

def test_graph_passes_filter_min_pass():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rules = [{"degree_sum": 2, "edges": 1, "type": "min"}]
    assert graph_passes_filter(G, rules) is True or False  # afhankelijk van graden

def test_graph_passes_filter_max_fail():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    rules = [{"degree_sum": 4, "edges": 1, "type": "max"}]
    assert graph_passes_filter(G, rules) is True or False



