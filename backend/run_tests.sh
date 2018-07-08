#!/usr/bin/env sh
clear
echo 'Running mamba for the first time...'
mamba --format=documentation
echo "Watching for file changes..."
. "./watch.sh" "mamba --format=documentation"