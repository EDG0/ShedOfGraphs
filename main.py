import sys
import json
import networkx as nx
from history import HistoryLogger

def load_filter(filename="filter.json"):
    with open(filename) as f:
        return json.load(f)["rules"]

def count_edges_with_degree_sum(G, target_sum):
    count = 0
    for u, v in G.edges():
        deg_sum = G.degree[u] + G.degree[v]
        if deg_sum == target_sum:
            count += 1
    return count

def graph_passes_filter(G, rules):
    for rule in rules:
        # Verplicht aanwezige sleutels
        if "degree_sum" not in rule or "edges" not in rule or "type" not in rule:
            raise KeyError("Filterregel mist 'degree_sum', 'edges' of 'type'")

        deg_sum = rule["degree_sum"]
        required_edges = rule["edges"]
        rule_type = rule["type"]

        count = count_edges_with_degree_sum(G, deg_sum)

        if rule_type == "min":
            if count < required_edges:
                return False
        elif rule_type == "max":
            if count > required_edges:
                return False
        elif rule_type == "exact":
            if count != required_edges:
                return False
        else:
            raise ValueError(f"Ongeldig filtertype: {rule_type}")

    return True

def main():
    rules = load_filter()
    logger = HistoryLogger()
    input_lines = []
    passed = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        input_lines.append(line)
        try:
            G = nx.from_graph6_bytes(line.encode())
            if graph_passes_filter(G, rules):
                print(line)
                passed.append(line)
        except Exception as e:
            print(f"Fout bij verwerken van graaf: {e}", file=sys.stderr)

    logger.log(len(input_lines), len(passed), rules, passed)

if __name__ == "__main__":
    main()

