#!/bin/bash

# Check if no flag is provided
if [[ $# -eq 0 ]]; then
  echo "No flag provided. Please provide a valid flag."
  exit 1
fi

# Define the tasks for different flags
case $1 in
  "mesh")
    rm data/meshes/*-*.ply
    rm urbanAI.db
    ;;
  "pcd")
    rm data/pcds/*-*.pcd
    rm urbanAI.db
    ;;
  "both")
    rm data/meshes/*-*.ply
    rm data/pcds/*-*.pcd
    rm urbanAI.db
    ;;
  "tif")
    rm data/*-*.tif
    ;;
  "all")
    rm data/*.tif
    rm data/meshes/*-*.ply
    rm data/pcds/*-*.pcd
    rm urbanAI.db
    ;;
  *)
    echo "Invalid flag. Please provide a valid flag. mesh, pcd, both, tif, all"
    ;;
esac
