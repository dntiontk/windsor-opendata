#!/bin/bash

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for f in data/precipitation/*
do
    echo "sanitizing $f"
    python sanitize_precipitation.py $f
done
IFS=$SAVEIFS