#!/bin/bash

# Audio Transcription Shell Wrapper
# Makes it easier to run the Python script

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if the Python script exists
if [ ! -f "audio_transcription.py" ]; then
    echo "Error: audio_transcription.py not found in current directory"
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import requests" &> /dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Run the Python script with all arguments passed through
python3 audio_transcription.py "$@"
