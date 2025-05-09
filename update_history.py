import time


HISTORY_FILE = "history.txt"

def log_history(input_count, output_count, filter_used, passed_graphs, file_path=HISTORY_FILE):
    print("DEBUG passed_graphs =", passed_graphs)

    
    if not passed_graphs:
        return  # niets loggen als er geen grafen zijn
    
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    passed_str = ",".join(passed_graphs[-20:])
    filter_repr = str(filter_used)

    line = f"{timestamp}\t{input_count}\t{output_count}\t{filter_repr}\t{passed_str}\n"
    with open(file_path, "a") as f:
        f.write(line)


if __name__ == "__main__":
    main()





