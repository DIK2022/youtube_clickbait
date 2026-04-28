from typing import List, Dict, Any, Callable
from tabulate import tabulate

ReportFunc = Callable[[List[Dict[str, Any]]], str]

def report_clickbait(data: List[Dict[str, Any]]) -> str:
    """Filter: ctr > 15, retention_rate < 40. Sort by ctr desc."""
    filtered = [
        row for row in data
        if row.get("ctr", 0) > 15 and row.get("retention_rate", 100) < 40
    ]
    # Sort by ctr descending
    filtered.sort(key=lambda x: x["ctr"], reverse=True)

    # Prepare table
    table = [(row["title"], row["ctr"], row["retention_rate"]) for row in filtered]
    headers = ["title", "ctr", "retention_rate"]
    return tabulate(table, headers=headers, tablefmt="grid")


# Registry for reports
_REPORTS = {
    "clickbait": report_clickbait,
}

def register_report(name: str, func: ReportFunc) -> None:
    _REPORTS[name] = func

def get_report(name: str) -> ReportFunc:
    if name not in _REPORTS:
        raise ValueError(f"Unknown report type: {name}. Available: {list(_REPORTS.keys())}")
    return _REPORTS[name]