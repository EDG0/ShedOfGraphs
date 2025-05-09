from flask import Flask, render_template, request, redirect
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import subprocess

app = Flask(__name__)

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.txt")
GRAPH_IMG_DIR = os.path.join("static", "graphs")
FILTER_FILE = os.path.join(os.path.dirname(__file__), "filter.json")

os.makedirs(GRAPH_IMG_DIR, exist_ok=True)
    
def parse_history_line(line):
    try:
        parts = line.strip().split('\t')
        if len(parts) < 5:
            return None
        _, _, _, rule_json, graphs = parts
        raw = json.loads(rule_json.replace("'", '"'))
        rule = raw["rules"] if isinstance(raw, dict) and "rules" in raw else raw
        graph_list = graphs.split(",") if graphs else []
        return rule, graph_list
    except Exception as e:
        print(f"[DEBUG] Fout bij history-regel: {line} -> {e}")
        return None


def get_recent_graphs(n=20):
    if not os.path.exists(HISTORY_FILE):
        print("[DEBUG] history.txt niet gevonden.")
        return []

    seen_graphs = set()
    graph_infos = []

    with open(HISTORY_FILE, "r") as f:
        lines = reversed(f.readlines())

    for line in lines:
        parsed = parse_history_line(line)
        if not parsed:
            continue
        rule, graphs = parsed
        for graph6 in graphs:
            if graph6 not in seen_graphs:
                seen_graphs.add(graph6)
                filename = f"{graph6}.png"
                path = os.path.join(GRAPH_IMG_DIR, filename)
                if not os.path.exists(path):
                    try:
                        G = nx.from_graph6_bytes(graph6.encode())
                        plt.figure(figsize=(2.5, 2.5))
                        nx.draw(G, with_labels=True, node_size=300)
                        plt.savefig(path)
                        plt.close()
                    except Exception as e:
                        print(f"[DEBUG] Kon {graph6} niet visualiseren: {e}")
                        continue
                graph_infos.append({
                    "graph6": graph6,
                    "img": filename,
                    "rule": rule
                })
                if len(graph_infos) == n:
                    return graph_infos
    return graph_infos

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            rule_count = int(request.form.get("rule_count", "1"))
            rules = []
            for i in range(rule_count):
                deg_sum = request.form.get(f"degree_sum_{i}")
                count = request.form.get(f"count_{i}")
                rtype = request.form.get(f"type_{i}")
                if deg_sum and count and rtype:
                    rules.append({
                        "degree_sum": int(deg_sum),
                        "edges": int(count),
                        "type": rtype
                    })
            filter_data = {"rules": rules}
            with open(FILTER_FILE, "w") as f:
                json.dump(filter_data, f)

            # ⬇️ HIER de shellscript aanroepen
            subprocess.run(["bash", "./run_parallel_filter.sh", "5"], check=True)

            return redirect("/")
        except Exception as e:
            print(f"[DEBUG] Fout in formulierverwerking: {e}")
            return "Ongeldige invoer", 400

    recent_graphs = get_recent_graphs()
    return render_template("index.html", graphs=recent_graphs)

if __name__ == "__main__":
    app.run(debug=True)






