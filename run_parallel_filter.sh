#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Gebruik: ./run_parallel_filter.sh <aantal_knopen>"
    exit 1
fi

N=$1
echo "Genereer grafen met $N knopen..."
./geng -d0D4 $N > all_graphs.txt

echo "Splitsen in 4 delen..."
split -n l/4 all_graphs.txt split_

echo "Start filtering in parallel..."
for file in split_*; do
    cat "$file" | python3 main.py --skip-history > "filtered_$file.txt" &
done

wait
echo "Filtering voltooid."

echo "Combineer resultaten..."
cat filtered_*.txt > filtered_combined.txt

echo "Update history..."
# Laad en toon filterinhoud
FILTER_CONTENT=$(<filter.json)
echo "DEBUG FILTER CONTENT:"
echo "$FILTER_CONTENT"

INPUT_COUNT=$(wc -l < all_graphs.txt)

# Roep update_history.py aan met correcte JSON-inhoud
python3 update_history.py --inputs filtered_combined.txt --filter "$FILTER_CONTENT" --n "$INPUT_COUNT"

echo "Opruimen van tijdelijke bestanden..."
rm all_graphs.txt split_* filtered_*.txt

echo "Alles voltooid!"
