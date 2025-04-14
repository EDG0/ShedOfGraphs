import time

class HistoryLogger:
    def __init__(self, filepath="history.txt"):
        self.filepath = filepath

    def log(self, input_count, output_count, filter_used, passed_graphs):

        if not isinstance(input_count, int):
            raise TypeError("input_count must be an int")
        if not isinstance(output_count, int):
            raise TypeError("output_count must be an int")
        if not isinstance(filter_used, (str, dict, list)):
            raise TypeError("filter_used must be a string, dict or list")
        if not isinstance(passed_graphs, list) or not all(isinstance(g, str) for g in passed_graphs):
            raise TypeError("passed_graphs must be a list of strings")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        passed_str = ",".join(passed_graphs)
        filter_repr = filter_used if isinstance(filter_used, str) else str(filter_used)

        line = f"{timestamp}\t{input_count}\t{output_count}\t{filter_repr}\t{passed_str}\n"

        with open(self.filepath, "a") as f:
            f.write(line)

