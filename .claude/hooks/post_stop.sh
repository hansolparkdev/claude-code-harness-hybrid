#!/usr/bin/env bash
# Stop hook: 세션 종료 시 로깅

INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')

# 무한 루프 방지
if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  exit 0
fi

agents/.venv/bin/python agents/logger.py \
  --event session_stop 2>/dev/null

exit 0
