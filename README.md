# Sprint Sketch

A tool for processing sprint backlog data and generating markdown output of sprint tasks by stories.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variable:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Replace `backlog.xlsx` with your sprint backlog data.  In main.py, configure field names at the top of the file.
2. Run the application:
   ```bash
   python main.py > out.md
   ```

This will process your sprint backlog and generate the output in `out.md`.

## Requirements

- Python 3.x
- Gemini API key
- Excel file with sprint backlog data (`backlog.xlsx`)


Note: There's also a claude version of the script. ( see main_claude.py )