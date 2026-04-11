# My Skills Repository

Codex에서 재사용할 개인 스킬을 관리하는 저장소입니다.

## 현재 스킬

| Skill | 설명 |
| --- | --- |
| `split-commit` | 뒤섞인 작업 트리를 논리적인 커밋 단위로 나누고, Conventional Commits 형식의 메시지까지 정리합니다. |
| `krds-developer` | 대한민국 정부 디자인 시스템(KRDS) 기준으로 공공 웹사이트·앱 UI를 설계, 구현, 점검, 개선합니다. |
| `pre-push-review` | 푸시, 릴리스, 배포, PR 머지 직전에 작업 트리, 누락 파일, 테스트 품질, 버전업 필요 여부를 점검합니다. |
| `seoul-metro-realtime` | `uvx seoul-metro-realtime`로 서울 지하철 역별 실시간 도착 정보를 조회합니다. |

## 설치

`npx skills`는 GitHub shorthand(`owner/repo`)를 지원합니다.

```bash
npx skills add ludens/my-skills --all
```

특정 스킬만 설치하려면 `--skill` 옵션에 스킬 이름을 지정합니다.

```bash
npx skills add ludens/my-skills --skill split-commit krds-developer
```
