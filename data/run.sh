#!/bin/bash
# run.sh — runs the Python script and logs output safely

BASE_DIR="/media/nghia/G3 Plus/Work/Chatbot for selling product/chatbot-system"

# Activate virtual environment
source "$BASE_DIR/venv/bin/activate"

# Run the Python scripts with proper quoting and logging
python3 "$BASE_DIR/data/scrape_link.py" >> "$BASE_DIR/data/myscript_link.log" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] scrape_link.py executed and logged to myscript_link.log" >> "$BASE_DIR/data/myscript_link.log"

python3 "$BASE_DIR/data/scrap_info.py" >> "$BASE_DIR/data/myscript_info.log" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] scrap_info.py executed and logged to myscript_info.log" >> "$BASE_DIR/data/myscript_info.log"
