# claude-harness

Claude Code 기반 AI 개발 워크플로우 하네스.

에이전트·스킬·훅·규칙 문서를 새 프로젝트에 그대로 이식할 수 있는 템플릿입니다.

## 구성

```
.claude/
  agents/         에이전트 6개 (기획·아키텍트·개발·리뷰어·테스터·비평)
  skills/         스킬 4개 (/init · /planning · /spec · /dev)
  hooks/          Claude Code 훅 (파일 수정 전 ESLint, 서버 중복 기동 차단)
  settings.json   훅 등록 설정

docs/
  harness.md      훅·에이전트 설계 개념
  rules/
    dev-workflow.md     에이전트별 워크플로우 규율 (고정)
    dev-flow.md         SDD 트랙 정의 (고정)
    forbidden-patterns.md   금지 패턴 (프로젝트별 작성)
    folder-conventions.md   폴더 규약 (프로젝트별 작성)
    commands.md             명령어 (프로젝트별 작성)
```

## 워크플로우

```
/planning {기능명}   기획서 작성 (기획 에이전트 + 비평 에이전트)
/spec {기능명}       스펙 산출 (아키텍트 에이전트)
/dev {기능명}        개발·리뷰·테스트·아카이브 자동 수행
```

## 새 프로젝트에 적용

1. 이 레포의 `.claude/`와 `docs/` 폴더를 프로젝트 루트에 복사
2. `/init` 실행 → CLAUDE.md + `docs/rules/` 3개 파일 자동 생성
3. `/planning` → `/spec` → `/dev` 순서로 개발 시작
