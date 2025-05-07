#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Gebruik: ./run_filter.sh <aantal_knopen> [--skip-history]"
    exit 1
fi

N=$1
SHIFT_ARGS=${@:2}  # alles behalve het eerste argument

# Voer filtering uit met optioneel extra argument
./geng -d0D4 $N | python3 main.py $SHIFT_ARGS
