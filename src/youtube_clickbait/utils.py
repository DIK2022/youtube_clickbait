import csv
from pathlib import Path
from typing import Dict, List, Any


def read_csv_files(file_paths: List[Path]) -> List[Dict[str, Any]]:
    """Read multiple CSV file and return list of rows as dicts."""
    all_rows = []
    for file_path in file_paths:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                try:
                    row["ctr"] = float(row["ctr"])
                    row["retention_rate"] = float(row["retention_rate"])
                except(KeyError, ValueError) as e:
                    # Skip rows with missing or invalid numeric data
                    continue
                all_rows.append(row)
    return all_rows
