#!/bin/bash

# Check of er een argument is
if [ -z "$1" ]; then
  echo "Gebruik: ./run_filter.sh <aantal knopen>"
  exit 1
fi

ORDER=$1

# Genereer grafen en filter ze
./geng $1 | python3 main.py

