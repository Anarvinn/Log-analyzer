# Log Analyzer CLI

A high-performance, memory-efficient Command Line Interface (CLI) tool written in Python to parse, filter, analyze, and report on large log files.

Built with generator-based streaming processing, this tool handles multi-gigabyte log files cleanly without overloading system memory.

## Key Features

- **Streaming Architecture:** Uses Python generators to process log files line-by-line, ensuring minimal memory usage.
- **Robust Error Handling:** Tolerates empty, corrupt, or malformed log lines while keeping count of total invalid entries.
- **Flexible Filtering:** Combine filters seamlessly by:
  - Severity level (`INFO`, `DEBUG`, `WARNING`, `ERROR`)
  - Module name (e.g., `auth`, `payments`)
  - Substring search (case-insensitive)
  - Time interval (`--start` and `--stop` bounds)
- **Detailed Analytics:**
  - Aggregates log entry counts by severity level and module.
  - Generates hourly error distribution statistics.
  - Identifies top 5 most frequent `ERROR`-level messages.
- **Dual Output:** Displays formatted summaries directly in the terminal and exports full reports to structured JSON files.

## Log Format Standard

The analyzer expects log lines formatted with pipe (`|`) delimiters:

```text
YYYY-MM-DD HH:MM:SS | LEVEL | MODULE | MESSAGE
```

### Example Log Entries

```text
2026-10-03 14:25:10 | ERROR | payments | Payment process timed out
2026-10-03 14:26:05 | INFO | auth | User admin logged in successfully
2026-10-03 14:30:00 | WARNING | database | High connection pool usage
```

## Installation & Setup

### Prerequisites

- **Python 3.8+** installed on your system.

### Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/Anarvinn/log-analyzer.git
   cd log-analyzer
   ```

2. _(Optional)_ Set up and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

Run the script from your terminal using `main.py` with command-line arguments.

### Command Structure

```bash
python main.py --file <path_to_log_file> [OPTIONS]
```

### Command Line Arguments

- `--file` _(str, Required)_: Path to the log file to analyze.
- `--output` _(str, Default: `report.json`)_: Path/filename for saving the JSON report.
- `--level` _(str, Optional)_: Filter by severity level (`INFO`, `DEBUG`, `WARNING`, `ERROR`).
- `--module` _(str, Optional)_: Filter by module name (e.g., `payments`, `auth`).
- `--text` _(str, Optional)_: Case-insensitive text search inside messages.
- `--start` _(str, Optional)_: Filter logs starting from date/time (`YYYY-MM-DD HH`).
- `--stop` _(str, Optional)_: Filter logs ending at date/time (`YYYY-MM-DD HH`).

## Example Usage Scenarios

### 1. Basic Analysis

Analyze `app.log` and save the output to `report.json`:

```bash
python main.py --file app.log
```

### 2. Filter by Level and Module

Analyze only `ERROR` events occurring in the `payments` module:

```bash
python main.py --file app.log --level ERROR --module payments
```

### 3. Date & Time Range Filtering

Analyze logs generated between 12:00 and 15:00 on October 3rd, 2026:

```bash
python main.py --file app.log --start "2026-10-03 12" --stop "2026-10-03 15"
```

### 4. Text Search & Custom Output File

Find messages containing "failed" and save the report to `custom_report.json`:

```bash
python main.py --file app.log --text "failed" --output custom_report.json
```

## Output Example

### Console Output

```text
==== File Analysis Results ====
Total lines        : 1520
Invalid lines      : 3

==== Errors by Level ====
INFO      : 1100
WARNING   : 250
ERROR     : 167

==== Errors by Module ====
auth      : 500
payments  : 650
database  : 367

==== Top Frequent Errors ====
45 : Payment process timed out
32 : Connection to database lost
12 : Invalid authorization token
```

### Exported JSON Report Structure (`report.json`)

```json
{
  "total_lines": 1520,
  "invalid_lines": 3,
  "by_level": {
    "INFO": 1100,
    "WARNING": 250,
    "ERROR": 167
  },
  "by_module": {
    "auth": 500,
    "payments": 650,
    "database": 367
  },
  "top_errors": {
    "Payment process timed out": 45,
    "Connection to database lost": 32
  },
  "errors_by_hours": {
    "2026-10-03 12": 15,
    "2026-10-03 13": 42,
    "2026-10-03 14": 110
  }
}
```

## Project Structure

```text
├── main.py          # Main CLI application logic & entry point
├── app.log          # Sample log file for testing
├── .gitignore       # Git ignore rules for virtualenvs, logs & IDEs
└── README.md        # Project documentation
```
