import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .reports import get_report
from .utils import read_csv_files


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YouTube analytics report generator")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to CSV file with vide metrics",
    )    
    parser.add_argument(
        "--report",
        required=True,
        help="Report type (e.g., clickbait)",
    )
    return parser.parse_args(args)

def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    
    # Validate files exist
    file_paths = []
    for f in args.files:
        path = Path(f)
        if not path.is_file():
            print(f"Error: File not found: {f}", file=sys.stderr)
            sys.exit(1)
        file_paths.append(path)
        
    # Read all data
    try:
        data = read_csv_files(file_paths)
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)
        
    if not data:
        print("No valid data found in the provided file.", file=sys.stderr)
        sys.exit(0)
    
    #Generate report
    try:
        report_func = get_report(args.report)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
        
    output = report_func(data)
    print(output)
    
    
if __name__ == "__main__":
    main()
    
            