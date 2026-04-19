# claude-code-harness-hybrid

Claude Code 하네스에 Python 기반 외부 모델(GPT-4o-mini 등)을 혼합한 하이브리드 에이전트 워크플로우.

## 핵심 아이디어

기존 하네스는 모든 에이전트를 Claude 서브에이전트로 실행합니다. 매번 서브에이전트를 열면 시스템 프롬프트·툴 정의 등 고정 비용(~17k 토큰)이 반복 소모되고, 메인 컨텍스트를 거치는 왕복 구조가 토큰 낭비와 컨텍스트 오염을 유발합니다.

**비평·리뷰처럼 입출력이 단순한 역할**은 Python 스크립트로 분리해 에이전트 내부에서 직접 호출합니다. 메인을 거치지 않으므로 왕복이 사라지고, Claude 고정 비용 없이 더 저렴한 모델로 처리할 수 있습니다.

## 구조 변경

**기존**
```
개발 에이전트 → 메인 → 리뷰어 에이전트 → 메인 → 개발 에이전트
기획 에이전트 → 메인 → 비평 에이전트  → 메인 → 기획 에이전트
```

**개선**
```
개발 에이전트 → python agents/reviewer.py → 피드백 → 내부 수정
기획 에이전트 → python agents/critic.py  → 피드백 → 내부 수정
```

## 트레이드오프

| | 기존 | 개선 |
|--|------|------|
| 리뷰·비평 토큰 | Claude 고정비용 매번 | Python 호출, 고정비용 없음 |
| 메인 컨텍스트 | 왕복마다 오염 | 보호됨 |
| 피드백 정확도 | 메인 거쳐서 희석 | 에이전트가 직접 수신 |
| 모델 다양성 | Claude 단일 | GPT-4o-mini 등 교차 검증 |
| 의존성 | 없음 | Python 환경 필요 |

## 구성

```
.claude/
  agents/
    developer.md      Claude 서브에이전트 (TDD 구현)
    planner.md        Claude 서브에이전트 (기획서 작성)
    architect.md      Claude 서브에이전트 (스펙 산출)
    tester.md         Claude 서브에이전트 (E2E)
  skills/
    dev/SKILL.md      리뷰어 호출을 python으로 변경
    planning/SKILL.md 비평 호출을 python으로 변경

agents/               Python 에이전트
  reviewer.py         GPT-4o-mini 기반 코드 리뷰
  critic.py           GPT-4o-mini 기반 기획서 비평

docs/
  hybrid-design.md    설계 상세
  harness.md          훅·에이전트 설계 개념
  rules/              워크플로우 규율
```

## 워크플로우

```
/planning → 기획 에이전트 → critic.py → 피드백 반영 → plan.md
/spec     → 아키텍트 에이전트 → 스펙 산출
/dev      → 개발 에이전트 → reviewer.py → 피드백 반영 → 완료
```

자세한 설계는 [docs/hybrid-design.md](docs/hybrid-design.md) 참조.
