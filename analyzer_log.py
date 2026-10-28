from datetime import datetime
import json
import argparse


parser = argparse.ArgumentParser(
    description="Log Analyzer: parses log files, applies filters, and exports statistics to JSON."
)

parser.add_argument(
    '--file',
    required=True,
    type=str,
    help="Path to the input log file (required)"
)

parser.add_argument(
    '--output',
    type=str,
    help="Path to output JSON report file (default: report.json)"
)

parser.add_argument(
    '--level',
    type=str,
    default=None,
    choices=["INFO", "DEBUG", "WARNING", "ERROR"],
    help='Filter logs by severity level'
)

parser.add_argument(
    '--module',
    type=str,
    default=None,
    help="Filter logs by module name (e.g., auth, payments)"
)

parser.add_argument(
    '--text',
    type=str,
    default=None,
    help="Search text inside log message (case-insensitive)"
)

parser.add_argument(
    '--start',
    type=str,
    default=None,
    help="Start datetime filter in 'YYYY-MM-DD HH' format"
)

parser.add_argument(
    '--stop',
    type=str,
    default=None,
    help="End datetime filter in 'YYYY-MM-DD HH:MM:SS' format"
)

args = parser.parse_args()


def main_console(file, output, **kwargs):
    report = {'total_lines': 0,
              'invalid_lines': 0,
              'by_level': {},
              'by_module': {},
              'top_errors': {},
              'errors_by_hours': {}}

    for line in file_reader(file):
        report['total_lines'] += 1
        if line_is_valid(line):
            data = line_reader(line)

            report['by_level'].setdefault(data['level'], 0)
            report['by_level'][data['level']] += 1

            report['by_module'].setdefault(data['module'], 0)
            report['by_module'][data['module']] += 1

            if data['level'] == 'ERROR':
                report['top_errors'].setdefault(data['message'], 0)
                report['top_errors'][data['message']] += 1

            report['errors_by_hours'].setdefault(data['date'], 0)
            report['errors_by_hours'][data['date']] += 1
        else:
            report['invalid_lines'] += 1

    report['top_errors'] = dict(
        sorted(report['top_errors'].items(), key=lambda x: x[1], reverse=True)[:5])

    report = filter_report(report, **kwargs)

    print_report_in_console(report)
    save_report(report, output)


def file_reader(file):
    try:
        with open(file, 'r') as file_read:
            for line in file_read:
                yield line
    except FileNotFoundError:
        print("File not found")


def line_is_valid(line):
    if line.count('|') == 3:
        try:
            data = line.split(' | ')
            datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
            if not data[1] in ['INFO', 'DEBUG', 'WARNING', 'ERROR']:
                return False
            return True
        except ValueError:
            return False
    else:
        return False


def line_reader(line):
    date, level, module, message = line.split('|')
    data = {
        'level': level.strip(),
        'module': module.strip(),
        'date': date[:13].strip(),
        'message': message.strip()
    }
    return data


def filter_report(data, level, module, text, start, stop):
    if level:
        if level in data['by_level']:
            data['by_level'] = {level: data['by_level'][level]}
        else:
            data['by_level'] = {level: 0}

    if module:
        if module in data['by_module']:
            data['by_module'] = {module: data['by_module'][module]}
        else:
            data['by_module'] = {module: 0}

    if text:
        res = {}
        text = text.lower()
        for k, v in data['text_error'].items():
            if text in k.lower():
                res[k] = v
        data['text_error'] = res

    if start:
        res = {}
        start = start[:13]
        for date, value in data['errors_by_hours'].items():
            if date >= start:
                res[date] = value
        data['errors_by_hours'] = res

    if stop:
        res = {}
        stop = stop[:13]
        for date, value in data['errors_by_hours'].items():
            if date <= stop:
                res[date] = value
        data['errors_by_hours'] = res

    return data


def print_report_in_console(report):
    print("\n==== File Analysis Results ====")
    print(f"Total lines        : {report['total_lines']}")
    print(f"Invalid lines      : {report['invalid_lines']}")

    print("\n==== Errors by Level ====")
    if not report['by_level']:
        print("No data available")
    else:
        for level, count in report['by_level'].items():
            print(f"{level:<10}: {count}")

    print("\n==== Errors by Module ====")
    if not report['by_module']:
        print("No data available")
    else:
        for module, count in report['by_module'].items():
            print(f"{module:<10}: {count}")

    print("\n==== Top Frequent Errors ====")
    if not report['top_errors']:
        print("No data available")
    else:
        for error, count in report['top_errors'].items():
            print(f"{count:<3}: {error}")
    print()


def save_report(data, output):
    if output is None:
        output = 'report.json'
    with open(output, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    main_console(**vars(args))
