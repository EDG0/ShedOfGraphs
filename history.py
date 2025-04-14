import time

class HistoryLogger:
    def __init__(self, filepath="history.txt"):
        self.filepath = filepath

    def log(self, input_count, output_count, filter_used, passed_graphs):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        passed_str = ",".join(passed_graphs)
        filter_repr = filter_used if isinstance(filter_used, str) else str(filter_used)

        line = f"{timestamp}\t{input_count}\t{output_count}\t{filter_repr}\t{passed_str}\n"

        with open(self.filepath, "a") as f:
            f.write(line)

