---
name: create-pi-subagent
description: Use when 사용자가 pi 서브에이전트를 만들거나, 특정 역할의 전문가 에이전트 정의 파일을 생성·추가해달라고 요청할 때. 서브에이전트, agent, 전문가 에이전트, 하위 에이전트 생성 시 사용한다.
---

# 서브에이전트 생성

pi-subagents의 에이전트는 YAML frontmatter + system prompt로 된 markdown 파일 하나다. 파일 생성 전에 **반드시 스코프(프로젝트/유저)를 먼저 정한다**.

## 필수: 스코프부터 결정

생성 전 사용자에게 스코프를 묻는다. 확인 없이 파일을 만들면 안 된다.

| 스코프 | 경로 | 특징 |
|---|---|---|
| User | `~/.pi/agent/agents/<name>.md` | 모든 프로젝트 공유, 개인 전역 |
| Project | `.pi/agents/<name>.md` | 해당 저장소 전용, git에 커밋됨 |

질문 예시: "서브에이전트를 프로젝트 전용(`.pi/agents/`)으로 만들까요, User 전역(`~/.pi/agent/agents/`)으로 만들까요?"

- 사용자가 명시하지 않으면 추측하지 말고 묻는다.
- 레거시 프로젝트는 `.agents/*.md`도 인식되지만, 신규 생성은 `.pi/agents/`를 쓴다.
- 같은 이름이면 Project 정의가 User를 이긴다.

## 파일 구조

```markdown
---
name: my-agent
description: 언제 쓰는지 서술 (3인칭, 트리거만)
tools: read, bash
---

여기에 system prompt.
```

## 핵심 frontmatter 필드

| 필드 | 의미 |
|---|---|
| `name` | 필수. 소문자·숫자·하이픈만 |
| `description` | 필수. "언제 쓰는지"(트리거)만 서술 |
| `tools` | 생략=기본 도구. 지정=엄격 allowlist. 빈값=도구 없음 |
| `model` | 기본 모델 |
| `systemPromptMode` | `replace`(기본) / `append` |
| `inheritProjectContext` | 저장소 AGENTS.md 상속 여부 |
| `inheritGlobalContext` | `~/.pi/agent/AGENTS.md` 상속. `inheritProjectContext: true`일 때만 동작 |
| `inheritSkills` | 스킬 카탈로그 상속 |
| `skills` | 특정 스킬만 선택 |
| `async` | 백그라운드 실행 기본값 |
| `output` | 결과 저장 파일 |
| `acceptanceRole` | `read-only` / `writer` |
| `advertise` | `true`면 부모 프롬프트에 카탈로그 노출 |
| `allowNestedSubagents` | 중첩 위임 허용 |
| `allowedAgents` | 이 에이전트가 띄울 수 있는 하위 에이전트 제한 |

## 주의

- 빌트인과 같은 이름의 커스텀 에이전트는 빌트인을 **통째로 대체**한다. 생략된 frontmatter(특히 `acceptanceRole`)는 상속되지 않는다. writer 승인이 필요하면 `acceptanceRole: writer`를 명시한다.
- `tools`를 지정하면 `read`가 없으면 스킬 파일을 읽을 수 없다. 스킬을 쓰는 에이전트엔 `read`를 포함한다.
- `description`은 "무엇을 하는지" 요약이 아니라 "언제 쓰는지" 트리거만 쓴다. workflow를 요약하면 에이전트가 본문 대신 description만 따라간다.

## 전체 참조

모든 필드·스코프·우선순위 규칙은 [pi-subagents 문서](https://github.com/nicobailon/pi-subagents/blob/main/docs/agents.md)를 참조한다.
