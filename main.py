import sys
import json
import networkx as nx

# Filter inlezen uit filter.json
def load_filter(filename="filter.json"):
    with open(filename) as f:
        return json.load(f)["rules"]

# Graadsom berekenen voor elke rand
def count_edges_with_degree_sum(G, target_sum):
    count = 0
    for u, v in G.edges():
        deg_sum = G.degree[u] + G.degree[v]
        if deg_sum == target_sum:
            count += 1
    return count

# Controleren of een graaf voldoet aan de filterregels
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

# Hoofdprogramma
def main():
    rules = load_filter()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            G = nx.parse_graph6(line)
            if graph_passes_filter(G, rules):
                print(line)
        except Exception as e:
            print(f"Fout bij verwerken van graaf: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
