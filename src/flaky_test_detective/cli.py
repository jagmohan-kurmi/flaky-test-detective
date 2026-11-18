import argparse
import glob
import json
from pathlib import Path
from .junit import analyze_files


def expand(paths):
    result=[]
    for value in paths:
        matched=glob.glob(value, recursive=True)
        result.extend(matched or [value])
    return [Path(p) for p in result]


def main(argv=None):
    parser=argparse.ArgumentParser(description="Analyze JUnit XML runs for intermittent pass/fail tests")
    sub=parser.add_subparsers(dest="command", required=True)
    report=sub.add_parser("report")
    report.add_argument("files", nargs="+", help="JUnit XML files or glob patterns")
    report.add_argument("--format", choices=["json","text"], default="text")
    args=parser.parse_args(argv)
    result=analyze_files(expand(args.files))
    if args.format=="json":
        print(json.dumps(result, indent=2))
    else:
        print(result["definition"])
        for row in result["intermittent"]:
            print(f"{row['test']}: {row['pass']} pass / {row['fail']} fail "
                  f"(flake_rate={row['flake_rate']:.3%}, observed_runs={row['observed_runs']})")
        if not result["intermittent"]:
            print("No intermittent pass/fail tests found.")
    return 0
