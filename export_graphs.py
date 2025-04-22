import argparse
import os
import networkx as nx
import matplotlib.pyplot as plt

def parse_graph6_line(line):
    try:
        return nx.from_graph6_bytes(line.strip().encode('utf-8'))
    except Exception as e:
        print(f"Fout bij parsen van regel: {line.strip()} — {e}")
        return None

def export_graphs(input_file, export_dir, image_format):
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    with open(input_file, 'r') as f:
        for i, line in enumerate(f):
            G = parse_graph6_line(line)
            if G is None:
                continue

            plt.figure(figsize=(3, 3))
            nx.draw(G, with_labels=True, node_size=300)
            output_path = os.path.join(export_dir, f'graph_{i}.{image_format}')
            plt.savefig(output_path, format=image_format)
            plt.close()
            print(f"Graph {i} geëxporteerd naar {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporteer grafen als afbeelding.")
    parser.add_argument("--input", required=True, help="Pad naar het .txt bestand met grafen (één per regel in graph6-formaat)")
    parser.add_argument("--export", required=True, help="Output map waar de afbeeldingen worden opgeslagen")
    parser.add_argument("--image_format", default="png", help="Formaat (bv. png, jpg, svg)")

    args = parser.parse_args()
    export_graphs(args.input, args.export, args.image_format)
