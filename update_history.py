import time
import argparse
import json

HISTORY_FILE = "history.txt"

def log_history(input_count, output_count, filter_used, passed_graphs):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    passed_str = ",".join(passed_graphs[-20:])
    filter_repr = str(filter_used)

    line = f"{timestamp}\t{input_count}\t{output_count}\t{filter_repr}\t{passed_str}\n"
    with open(HISTORY_FILE, "a") as f:
        f.write(line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, help="Path to filtered graphs")
    parser.add_argument("--filter", required=True, help="Filter used (as JSON string)")
    parser.add_argument("--n", required=True, type=int, help="Input count")
    args = parser.parse_args()

    with open(args.inputs, "r") as f:
        passed_graphs = [line.strip() for line in f if line.strip()]

    input_count = args.n
    output_count = len(passed_graphs)
    filter_used = json.loads(args.filter)

    log_history(input_count, output_count, filter_used, passed_graphs)

if __name__ == "__main__":
    main()





