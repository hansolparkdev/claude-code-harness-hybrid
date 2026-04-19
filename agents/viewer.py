"""
하네스 로그 뷰어

사용법:
  python agents/viewer.py

결과: viewer/index.html 생성
"""

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path("logs/harness.jsonl")
OUT_PATH = Path("viewer/index.html")


def load_logs() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    entries = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return entries


def group_by_date(logs: list[dict]) -> dict:
    by_date = defaultdict(list)
    for entry in logs:
        ts = entry.get("ts", "")
        try:
            dt = datetime.fromisoformat(ts)
            date = dt.astimezone().strftime("%Y-%m-%d")
        except Exception:
            date = "날짜 불명"
        by_date[date].append(entry)
    return dict(sorted(by_date.items(), reverse=True))


def result_badge(result: str) -> str:
    colors = {"PASS": "#16a34a", "FAIL": "#dc2626", "ERROR": "#d97706"}
    color = colors.get(result, "#6b7280")
    return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px">{result}</span>'


def render_entry(entry: dict) -> str:
    event = entry.get("event", "")
    ts = entry.get("ts", "")
    try:
        dt = datetime.fromisoformat(ts).astimezone()
        time_str = dt.strftime("%H:%M:%S")
    except Exception:
        time_str = ""

    if event == "critic":
        feature = entry.get("feature", "")
        round_ = entry.get("round", "")
        result = entry.get("result", "")
        issues = entry.get("issues", [])
        issues_html = ""
        if issues:
            items = "".join(f"<li>{i}</li>" for i in issues)
            issues_html = f'<ul style="margin:4px 0 0 16px;color:#6b7280;font-size:13px">{items}</ul>'
        return f"""
        <div style="padding:8px 12px;border-left:3px solid #6366f1;margin:4px 0;background:#f8f8ff">
          <span style="color:#6b7280;font-size:12px">{time_str}</span>
          <strong style="margin:0 8px">critic</strong>
          <span style="color:#374151">{feature}</span>
          <span style="color:#9ca3af;margin:0 6px">round {round_}</span>
          {result_badge(result)}
          {issues_html}
        </div>"""

    if event == "reviewer":
        context = entry.get("context", "")
        result = entry.get("result", "")
        issues = entry.get("issues", [])
        issues_html = ""
        if issues:
            items = "".join(
                f'<li><span style="color:#dc2626">[{i.get("severity","")}]</span> {i.get("file","")} — {i.get("message","")}</li>'
                if isinstance(i, dict) else f"<li>{i}</li>"
                for i in issues
            )
            issues_html = f'<ul style="margin:4px 0 0 16px;color:#6b7280;font-size:13px">{items}</ul>'
        return f"""
        <div style="padding:8px 12px;border-left:3px solid #0ea5e9;margin:4px 0;background:#f0f9ff">
          <span style="color:#6b7280;font-size:12px">{time_str}</span>
          <strong style="margin:0 8px">reviewer</strong>
          <span style="color:#374151">{context}</span>
          {result_badge(result)}
          {issues_html}
        </div>"""

    if event == "file_changed":
        file_ = entry.get("file", "")
        tool = entry.get("tool", "")
        return f"""
        <div style="padding:6px 12px;border-left:3px solid #d1d5db;margin:4px 0;color:#6b7280;font-size:13px">
          <span>{time_str}</span>
          <span style="margin:0 8px;background:#e5e7eb;padding:1px 6px;border-radius:3px">{tool}</span>
          <code>{file_}</code>
        </div>"""

    if event == "session_stop":
        return f"""
        <div style="padding:6px 12px;margin:4px 0;color:#9ca3af;font-size:12px">
          <span>{time_str}</span> 세션 종료
        </div>"""

    return f"""
    <div style="padding:6px 12px;margin:4px 0;color:#9ca3af;font-size:12px">
      <span>{time_str}</span> {event}
    </div>"""


def render_html(by_date: dict) -> str:
    body = ""
    for date, entries in by_date.items():
        rows = "".join(render_entry(e) for e in entries)
        body += f"""
        <details open>
          <summary style="cursor:pointer;padding:10px 16px;background:#f3f4f6;border-radius:6px;font-weight:600;margin-bottom:8px">
            {date} <span style="color:#9ca3af;font-weight:400;font-size:13px">({len(entries)}건)</span>
          </summary>
          <div style="padding:0 8px">{rows}</div>
        </details>"""

    generated = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Harness Log Viewer</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f9fafb; color: #111827; padding: 24px; }}
    h1 {{ font-size: 20px; margin-bottom: 4px; }}
    .meta {{ color: #6b7280; font-size: 13px; margin-bottom: 24px; }}
    .empty {{ color: #9ca3af; text-align: center; padding: 48px; }}
  </style>
</head>
<body>
  <h1>Harness Log Viewer</h1>
  <div class="meta">생성: {generated} · {LOG_PATH}</div>
  {"".join(body) if by_date else '<div class="empty">로그 없음</div>'}
</body>
</html>"""


def main() -> int:
    logs = load_logs()
    by_date = group_by_date(logs)
    html = render_html(by_date)

    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"✓ {OUT_PATH} 생성 ({len(logs)}건)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
