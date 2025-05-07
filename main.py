import sys
import json
import argparse
import networkx as nx
from update_history import log_history

def load_filter(filename="filter.json"):
    with open(filename) as f:
        return json.load(f)["rules"]

def count_edges_with_degree_sum(G, target_sum):
    count = 0
    for u, v in G.edges():
        if G.degree[u] + G.degree[v] == target_sum:
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

def main(skip_history = False):
    rules = load_filter()
    passed = []
    input_count = 0
    output_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            input_count += 1
            G = nx.from_graph6_bytes(line.encode())
            if graph_passes_filter(G, rules):
                passed.append(line)
                print(line)
                output_count += 1
        except Exception as e:
            print(f"Fout bij verwerken van graaf: {e}", file=sys.stderr)

    if not skip_history:
        log_history(input_count, output_count, rules, passed)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-history", action="store_true")
    args = parser.parse_args()
    main(skip_history=args.skip_history)


