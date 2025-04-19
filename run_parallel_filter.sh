#!/bin/bash

# Check of er precies 1 argument is (aantal knopen)
if [ "$#" -ne 1 ]; then
    echo "Gebruik: $0 <aantal_knopen>"
    exit 1
fi

n=$1
modulo=4

echo "Starten van $modulo parallelle filters voor $n knopen..."

for ((i=0; i<modulo; i++)); do
    echo "unning: ./geng -d0D$i $n $i:$i > output_$i.txt"
    ./geng -d0D$i "$n" "$i:$i" > "output_$i.txt" &
done

wait

echo "Klaar! Resultaten in: output_0.txt ... output_3.txt"

