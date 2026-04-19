"""
하네스 로거

사용법:
  python agents/logger.py --event critic --feature login --round 1 --result PASS
  python agents/logger.py --event file_changed --file docs/plans/login/plan.md --tool Write
  python agents/logger.py --event session_stop

로그 위치: logs/harness.jsonl
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path("logs/harness.jsonl")


def write(entry: dict) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)
    entry["ts"] = datetime.now(timezone.utc).isoformat()
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="하네스 로거")
    parser.add_argument("--event", required=True, help="이벤트 종류")
    parser.add_argument("--feature", default="", help="feature 이름")
    parser.add_argument("--round", type=int, default=0, help="비평 회차")
    parser.add_argument("--result", default="", help="PASS|FAIL|ERROR")
    parser.add_argument("--issues", default="[]", help="issues JSON 문자열")
    parser.add_argument("--file", default="", help="변경 파일 경로")
    parser.add_argument("--tool", default="", help="툴 이름 (Write/Edit 등)")
    parser.add_argument("--context", default="", help="추가 맥락")
    args = parser.parse_args()

    entry: dict = {"event": args.event}

    if args.feature:
        entry["feature"] = args.feature
    if args.round:
        entry["round"] = args.round
    if args.result:
        entry["result"] = args.result
    if args.issues and args.issues != "[]":
        try:
            entry["issues"] = json.loads(args.issues)
        except json.JSONDecodeError:
            entry["issues"] = [args.issues]
    if args.file:
        entry["file"] = args.file
    if args.tool:
        entry["tool"] = args.tool
    if args.context:
        entry["context"] = args.context

    write(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
