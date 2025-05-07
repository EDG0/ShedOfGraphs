import argparse
import os
import networkx as nx
import matplotlib.pyplot as plt


def export_graphs(input_file, output_folder, image_format):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, "r") as f:
        lines = f.readlines()

    graph_counter = 0
    for i, line in enumerate(lines):
        graph_str = line.strip()
        try:
            # probeer regel als graph6 in te lezen
            G = nx.from_graph6_bytes(graph_str.encode())
            nx.draw(G, with_labels=True, node_size=300, font_size=10)
            path = os.path.join(output_folder, f"graph_{graph_counter}.{image_format}")
            plt.savefig(path)
            plt.clf()
            print(f"✅ Graph {graph_counter} opgeslagen als {path}")
            graph_counter += 1
        except Exception as e:
            print(f"⚠️  Fout bij graf {i}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporteer graph6 grafen naar afbeeldingsbestanden")
    parser.add_argument("--input", required=True, help="Pad naar inputbestand met graph6-grafen")
    parser.add_argument("--export", required=True, help="Folder om afbeeldingen in op te slaan")
    parser.add_argument("--image_format", required=True, help="Afbeeldingsformaat (bv. png, svg)")

    args = parser.parse_args()
    export_graphs(args.input, args.export, args.image_format)







