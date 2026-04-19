#!/usr/bin/env bash
# PostToolUse hook: Write/Edit 시 변경 파일 로깅

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE" ]]; then
  exit 0
fi

agents/.venv/bin/python agents/logger.py \
  --event file_changed \
  --file "$FILE" \
  --tool "$TOOL_NAME" 2>/dev/null

exit 0
