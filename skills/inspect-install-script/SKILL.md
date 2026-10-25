---
name: inspect-install-script
description: Use when reviewing an installation script, curl|bash one-liner, setup script, or bootstrap script to assess security, persistence, and reversibility before running it.
license: MIT
allowed-tools: Bash Read Grep
---

# 설치 스크립트 검사

## 개요

설치 스크립트를 실행하기 전에 **무엇을 다운로드하고, 무엇을 변경하고, 무엇을 남기고, 어떻게 되돌리는지** 를 정리합니다. 스크립트를 신뢰하기 전에 반드시 이 5가지 항목을 채웁니다.

## 사용 시점

- `curl ... | bash`, `wget ... | sh` 형태의 원라이너를 실행하려 할 때
- 서드파티 설치 스크립트(`install.sh`, `setup.sh`, `bootstrap.sh`)를 검토할 때
- "이 스크립트 안전한가?" 질문을 받았을 때
- 스크립트 실행 전 리스크 요약이 필요할 때

## 스크립트 확보

분석 대상이 URL이면 **절대 `curl | bash`로 실행하지 않는다.** 먼저 파일로 저장한 뒤 분석한다.

```bash
curl -fsSL <URL> -o /tmp/install-script.sh
```

저장한 파일을 읽고 아래 5개 섹션을 채운다. 로컬 파일이 주어진 경우 그대로 읽는다.

## 검사 절차

스크립트를 읽고 아래 5개 섹션을 **모두** 채운다. 항목이 없으면 "없음"으로 명시한다 (생략 금지).

### 1. 네트워크 다운로드

스크립트가 네트워크로 가져오는 모든 항목을 나열.

- URL, 프로토콜(HTTPS/HTTP), 호스트
- 다운로드 방식: `curl`, `wget`, `git clone`, 패키지 매니저(`apt`, `brew`, `pip`, `npm`)
- 다운로드한 파일의 실행 여부(직접 실행 / 저장 후 실행 / 소스 빌드)
- 체크섬/서명 검증 여부 (없으면 "검증 없음"으로 표기)
- 리다이렉트/동적 URL (변수로 조립된 URL) 여부

### 2. sudo/root 권한 변경

root 권한으로 수행되는 모든 작업.

- `sudo`, `su`, root 소유 파일 쓰기
- 시스템 디렉터리 변경: `/usr`, `/etc`, `/opt`, `/bin`, `/lib`, `/var`
- 패키지 설치/제거, 서비스 등록, 커널 모듈
- 파일 권한/소유자 변경(`chmod`, `chown`)

### 3. 환경 변수·시크릿

읽거나 전송하는 값.

- 읽는 변수: `$HOME`, `$PATH`, `$USER`, `$SHELL`, `$SSH_*`, `$AWS_*`, `$GITHUB_TOKEN` 등
- 하드코딩된 토큰/키/비밀번호
- 외부로 전송하는 데이터: 텔레메트리, 분석, 에러 리포팅, 설치 통계
- 전송 대상 엔드포인트와 전송 내용

### 4. 시스템에 남는 잔여물

실행 후 지속되는 항목.

- 파일/디렉터리: 설치 경로, 캐시, 로그, 설정 파일
- 서비스: systemd unit, launchd plist, init.d 스크립트
- 스케줄러: cron, at, anacron
- 셸 설정 변경: `.bashrc`, `.zshrc`, `.profile`에 추가된 PATH/alias
- 커널/부팅 항목: 모듈, 부팅 스크립트

### 5. 제거(언인스톨) 체크리스트

되돌려야 할 항목을 실행 가능한 명령으로 나열.

- 삭제할 파일/디렉터리
- 중지/비활성화할 서비스
- 제거할 cron 항목
- 되돌릴 셸 설정 변경
- 제거할 패키지
- (스크립트가 uninstall 기능을 제공하면 그 사용법도 기재)

## 출력 형식

아래 템플릿을 그대로 사용한다.

```markdown
## 설치 스크립트 검사: <파일명/URL>

### 1. 네트워크 다운로드
- ...

### 2. sudo/root 권한 변경
- ...

### 3. 환경 변수·시크릿
- ...

### 4. 시스템 잔여물
- ...

### 5. 제거 체크리스트
- [ ] ...
```

## 주의 사항

- 스크립트가 난독화/인코딩되어 있으면 디코딩 후 분석한다
- `eval`, `base64 -d`, 변수 치환으로 숨겨진 명령을 반드시 펼쳐 확인한다
- 의심스러운 항목은 "확인 필요"로 표기하고 실행을 권장하지 않는다
- 실행 권장 여부를 마지막에 명시: **실행 가능 / 조건부 / 비권장**