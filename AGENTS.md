# Repository Guidelines

## Project Structure & Module Organization

이 저장소는 Codex에서 재사용할 개인 스킬을 관리한다. 각 스킬은 `skills/<skill-name>/` 아래에 두며, 진입점은 반드시 `SKILL.md`다. 스킬 전용 에이전트 설정은 필요할 때 `skills/<skill-name>/agents/*.yaml`에 둔다. 긴 참고 자료나 원문은 해당 스킬의 `references/` 하위 디렉터리에 둔다. 현재 주요 스킬은 `skills/calver-versioning/`, `skills/split-commit/`, `skills/pre-push-review/`다.

## Build, Test, and Development Commands

전용 빌드 단계는 없다. Markdown과 YAML 중심 저장소이므로 변경 전후 아래 명령으로 구조와 참조를 점검한다.

```bash
rg --files
rg "skill-name|old-reference"
git status --short
git diff --stat
```

설치 동작은 README의 `npx skills` 예시를 기준으로 확인한다.

```bash
npx skills add ludens/my-skills --all
npx skills add ludens/my-skills --skill calver-versioning
```

## Coding Style & Naming Conventions

스킬 디렉터리는 소문자 kebab-case를 사용한다. 예: `calver-versioning`, `pre-push-review`, `split-commit`. `SKILL.md`는 YAML front matter로 시작하고 `name`, `description`을 명확히 작성한다. 본문은 사용 시점, 절차, 출력 형식을 짧은 섹션으로 나눈다. 명령 예시는 fenced code block에 넣고, 저장소 문서는 기본적으로 한국어로 작성한다.

## Testing Guidelines

현재 자동 테스트 프레임워크는 없다. 변경 검증은 문서 구조와 설치 참조 점검으로 수행한다. 새 스킬을 추가하거나 삭제할 때는 `rg "<skill-name>"`으로 README, lock 파일, 참조 문서에 오래된 이름이 남지 않았는지 확인한다. YAML 파일을 수정하면 들여쓰기와 필수 필드를 수동 확인한다.

## Commit & Pull Request Guidelines

Git 히스토리는 Conventional Commits 형식을 따른다. 예: `docs(readme): document skills and installation`, `feat: add pre-push review skill`, `chore: remove task checklist artifact`. 커밋은 한 의도만 담고, 문서 변경은 `docs`, 유지보수 변경은 `chore`, 새 스킬은 `feat`를 우선 사용한다. PR에는 변경한 스킬 목록, 삭제한 잔여 참조, 실행한 검증 명령을 적는다. 사용자에게 보이는 문서 변경이면 예시 명령도 함께 갱신한다.

## Agent-Specific Instructions

작업 시작 시 superpowers 지침을 확인하고 적용한다. 사용자에게 제공하는 설명과 결과물은 기본적으로 한국어로 작성한다. 응답은 caveman 스타일처럼 짧고 고신호로 유지하되, 파일에 작성하는 공식 문서는 자연스럽고 전문적인 문장으로 쓴다.
