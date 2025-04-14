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
        deg_sum = rule["degree_sum"]
        required_edges = rule["edges"]
        count = count_edges_with_degree_sum(G, deg_sum)

        if rule["type"] == "min" and count < required_edges:
            return False
        elif rule["type"] == "max" and count > required_edges:
            return False
        elif rule["type"] == "exact" and count != required_edges:
            return False
    return True

def main():
    rules = load_filter()
    passed_graphs = []
    total_graphs = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        total_graphs += 1
        try:
            G = nx.from_graph6_bytes(line.encode())
            if graph_passes_filter(G, rules):
                print(line)
                passed_graphs.append(line)
        except Exception as e:
            print(f"Fout bij verwerken van graaf: {e}", file=sys.stderr)

    logger = HistoryLogger()
    logger.log(
        input_count=total_graphs,
        output_count=len(passed_graphs),
        filter_used=rules,
        passed_graphs=passed_graphs
    )

if __name__ == "__main__":
    main()
