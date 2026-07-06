import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected_stats():
    """Independently recompute the correct answer from access.log."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return total, len(ips), paths.most_common(1)[0][0]


def _load_report():
    assert REPORT_PATH.exists(), "no /app/report.json found (criterion 1)"
    text = REPORT_PATH.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        raise AssertionError("/app/report.json is not valid JSON (criterion 1)")


def test_report_is_valid_json():
    """Criterion 1: output is written to /app/report.json as valid JSON."""
    _load_report()


def test_total_requests_correct():
    """Criterion 2: total_requests matches the real count of log lines."""
    expected_total, _, _ = _expected_stats()
    report = _load_report()
    assert "total_requests" in report, "missing total_requests key"
    assert report["total_requests"] == expected_total, (
        f"expected total_requests={expected_total}, got {report['total_requests']}"
    )


def test_unique_ips_correct():
    """Criterion 3: unique_ips matches the real count of distinct client IPs."""
    _, expected_ips, _ = _expected_stats()
    report = _load_report()
    assert "unique_ips" in report, "missing unique_ips key"
    assert report["unique_ips"] == expected_ips, (
        f"expected unique_ips={expected_ips}, got {report['unique_ips']}"
    )


def test_top_path_correct():
    """Criterion 4: top_path matches the most frequently requested path."""
    _, _, expected_top = _expected_stats()
    report = _load_report()
    assert "top_path" in report, "missing top_path key"
    assert report["top_path"] == expected_top, (
        f"expected top_path={expected_top!r}, got {report['top_path']!r}"
    )
