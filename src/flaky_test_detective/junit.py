import re
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize_identifier(classname, name):
    raw = f"{classname}.{name}" if classname else name
    raw = re.sub(r"\s+", " ", (raw or "<unnamed>").strip())
    raw = re.sub(r"\[(?:iteration|run|retry)[^]]*\]", "", raw, flags=re.I)
    raw = re.sub(r"\b(?:retry|rerun)[_-]?\d+\b", "", raw, flags=re.I)
    raw = re.sub(r"\s+", " ", raw).strip(" .")
    return re.sub(r"\s*\.\s*", ".", raw)


def parse_file(path):
    root = ET.parse(path).getroot()
    records = []
    suites = [root] if root.tag.rsplit("}", 1)[-1] == "testsuite" else list(root.iter())
    for suite in suites:
        if suite.tag.rsplit("}", 1)[-1] != "testsuite":
            continue
        suite_name = suite.attrib.get("name", "")
        for case in suite.findall(".//testcase"):
            classname = case.attrib.get("classname") or suite_name
            name = case.attrib.get("name", "<unnamed>")
            status = "fail" if case.find("failure") is not None or case.find("error") is not None else "pass"
            if case.find("skipped") is not None:
                status = "skipped"
            records.append((normalize_identifier(classname, name), status))
    return records


def analyze_files(paths):
    totals = {}
    for path in paths:
        for identifier, status in parse_file(path):
            item = totals.setdefault(identifier, {"runs": 0, "pass": 0, "fail": 0, "skipped": 0})
            item["runs"] += 1
            item[status] += 1
    intermittent = []
    for identifier, item in sorted(totals.items()):
        observed = item["pass"] + item["fail"]
        fail_rate = item["fail"] / observed if observed else 0.0
        pass_rate = item["pass"] / observed if observed else 0.0
        if item["pass"] and item["fail"]:
            intermittent.append({
                "test": identifier, "runs": item["runs"], "observed_runs": observed,
                "pass": item["pass"], "fail": item["fail"], "skipped": item["skipped"],
                "flake_rate": round(fail_rate, 6),
                "pass_rate": round(pass_rate, 6),
            })
    return {
        "definition": "Flake/intermittent result: a test with both pass and fail outcomes across observed (non-skipped) JUnit runs.",
        "intermittent": intermittent,
        "totals": totals,
    }
