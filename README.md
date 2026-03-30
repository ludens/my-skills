# My Skills Repository

Codex에서 재사용할 개인 스킬을 관리하는 저장소입니다.

## 구조

```text
.
├── docs/
│   └── conventions.md
└── skills/
    ├── _template/
    └── example-skill/
```

## 규칙

- 스킬 하나당 `skills/<skill-name>/` 디렉터리 하나를 사용합니다.
- 각 스킬의 진입점은 반드시 `SKILL.md`입니다.
- 큰 설명은 `references/`로 분리하고, 보조 스크립트는 `scripts/`에 둡니다.
- 이미지나 샘플 파일이 필요하면 `assets/`에 둡니다.

## 새 스킬 만들기

1. `skills/_template`를 복사해 새 디렉터리를 만듭니다.
2. `SKILL.md`의 이름, 설명, 워크플로를 수정합니다.
3. 필요한 참고 문서나 스크립트를 추가합니다.

## 권장 명명

- 디렉터리명: kebab-case
- 스킬 이름: 짧고 구체적으로
- 파일명: 목적이 드러나게 작성
