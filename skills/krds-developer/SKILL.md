---
name: krds-developer
description: 대한민국 정부 디자인 시스템(KRDS)을 기준으로 공공 웹사이트·앱의 UI를 설계, 구현, 점검, 개선한다. 정부 서비스 화면, 컴포넌트, 입력폼, 신청·로그인·검색 플로, 디자인 토큰, 접근성, KRDS HTML Component Kit 적용, 체크리스트 기반 준수 검토가 필요할 때 사용한다.
---

# krds-developer

KRDS를 참고해 화면을 만들거나 고칠 때는 임의의 UI 관습보다 KRDS 문서에 먼저 맞춘다. 스타일, 컴포넌트, 기본 패턴, 서비스 패턴, 체크리스트를 한 번에 다 읽지 말고, 과업에 맞는 계층만 좁혀 읽는다.

## 시작 순서

처음에는 아래 5개 문서를 먼저 읽어 전체 구조를 잡는다.

- `references/utility_01.md`
- `references/outline_03.md`
- `references/component_summary.md`
- `references/global_summary.md`
- `references/service_summary.md`

이 다섯 문서를 읽은 뒤 작업을 아래 네 범주 중 하나로 분류한다.

1. 스타일과 토큰
2. 개별 컴포넌트
3. 기본 패턴
4. 서비스 플로

## 문서 선택 규칙

### 스타일과 토큰

- 색상, 서체, 형태, 아이콘, 레이아웃, 엘리베이션은 `references/style_01.md`부터 읽는다.
- 디자인 토큰 구조와 수정 원칙은 `references/style_07.md`를 읽는다.
- 토큰·파일·변수 이름 규칙은 `references/utility_03.md`를 읽는다.
- 접근성 기준을 함께 봐야 하면 `references/utility_04.md`를 읽는다.
- KRDS 도입 범위와 역할 구분이 필요하면 `references/utility_01.md`를 다시 확인한다.

### 개별 컴포넌트

- 먼저 `references/component_summary.md`에서 대상 컴포넌트를 찾는다.
- 그 다음 해당 `component_XX_YY.md` 문서를 읽고 구조, 유형, 사용성, 상호작용, 접근성 항목을 확인한다.
- 사이트 공통 영역을 다루면 헤더, 푸터, 공식 배너, 건너뛰기 링크를 우선 확인한다.

### 기본 패턴

- 먼저 `references/global_summary.md`에서 과업 유형을 찾는다.
- 폼, 동의, 오류, 목록 탐색, 필터링·정렬처럼 여러 컴포넌트가 결합된 흐름이면 해당 `global_XX.md`를 읽는다.
- 사용자가 여러 단계를 거쳐 데이터를 입력하면 입력폼 패턴을 우선 검토한다.

### 서비스 플로

- 먼저 `references/service_summary.md`에서 서비스군을 찾는다.
- 방문, 검색, 로그인, 신청, 정책정보 확인 중 어느 여정인지 정한 뒤 해당 `service_XX_YY.md`를 읽는다.
- 서비스 패턴은 `필수(Do)`, `권장(Better)`, `우수(Best)` 수준을 구분해 적용한다. 최소한 필수 수준은 지킨다.

### 구현과 설치

- KRDS HTML Component Kit 설치, CDN 사용, React/Vue 적용, 토큰 추출, SCSS 사용 방식은 `references/outline_03.md`를 읽는다.
- KRDS는 SCSS 기반 사용을 권장한다. 가능하면 토큰과 원본 구조를 유지하고, 임의 CSS 덮어쓰기는 최소화한다.
- SCSS 경로 문제가 있으면 Kit의 `resources` 디렉터리를 프로젝트로 복제해 참조 경로를 명시적으로 관리한다.

## 문서 인덱스

`rg`로 다시 찾기 전에 아래 인덱스에서 필요한 문서를 바로 고른다. 요약 문서에서 이름을 찾고, 아래 파일 인덱스에서 실제 파일을 열면 된다.

### 공통·시작 문서

- `references/utility_01.md`: KRDS 소개, 구성 요소, 역할 구분
- `references/utility_03.md`: 토큰·파일·컴포넌트 네이밍 원칙
- `references/utility_04.md`: 디지털 포용, 접근성 참고 방법
- `references/utility_07.md`: UI/UX 가이드라인 목적, 적용 수준(필수/권장/우수)
- `references/outline_03.md`: 개발자 설치 가이드, NPM/CDN/React/Vue/SCSS
- `references/디지털 정부 서비스 UIUX 가이드라인 자체 검증 체크리스트.md`: 최종 자체 검증

### 스타일 문서

- `references/style_01.md`: 스타일 전체 구조와 적용 범위
- `references/style_02.md`: 색상
- `references/style_03.md`: 타이포그래피
- `references/style_04.md`: 형태
- `references/style_05.md`: 레이아웃
- `references/style_06.md`: 아이콘
- `references/style_07.md`: 디자인 토큰
- `references/style_08.md`: 엘리베이션
- `references/style_09.md`: 선명한 화면 모드

### 컴포넌트 문서

- 아이덴티티
- `references/component_02_01.md`: 공식 배너
- `references/component_02_02.md`: 운영기관 식별자
- `references/component_02_03.md`: 헤더
- `references/component_02_04.md`: 푸터
- 탐색
- `references/component_03_01.md`: 건너뛰기 링크
- `references/component_03_02.md`: 메인 메뉴
- `references/component_03_03.md`: 브레드크럼
- `references/component_03_04.md`: 사이드 메뉴
- `references/component_03_05.md`: 콘텐츠 내 탐색
- `references/component_03_06.md`: 페이지네이션
- 레이아웃 및 표현
- `references/component_04_01.md`: 구조화 목록
- `references/component_04_02.md`: 긴급 공지
- `references/component_04_03.md`: 달력
- `references/component_04_04.md`: 디스클로저
- `references/component_04_05.md`: 모달
- `references/component_04_06.md`: 배지
- `references/component_04_07.md`: 아코디언
- `references/component_04_08.md`: 이미지
- `references/component_04_09.md`: 캐러셀
- `references/component_04_10.md`: 탭
- `references/component_04_11.md`: 표
- `references/component_04_13.md`: 텍스트 목록
- `references/component_04_14.md`: 파비콘
- 액션
- `references/component_05_01.md`: 링크
- `references/component_05_02.md`: 버튼
- `references/component_05_03.md`: 플로팅 버튼
- 선택
- `references/component_06_01.md`: 라디오 버튼
- `references/component_06_02.md`: 체크박스
- `references/component_06_03.md`: 셀렉트
- `references/component_06_04.md`: 태그
- `references/component_06_07.md`: 토글 스위치
- 피드백
- `references/component_07_01.md`: 단계 표시기
- `references/component_07_02.md`: 스피너
- 도움
- `references/component_08_01.md`: 도움 패널
- `references/component_08_02.md`: 따라하기 패널
- `references/component_08_03.md`: 맥락적 도움말
- `references/component_08_04.md`: 코치마크
- `references/component_08_05.md`: 툴팁
- `references/component_08_06.md`: 음성지원
- 입력
- `references/component_09_01.md`: 날짜 입력 필드
- `references/component_09_02.md`: 텍스트 영역
- `references/component_09_03.md`: 텍스트 입력 필드
- `references/component_09_04.md`: 파일 업로드
- 설정
- `references/component_10_01.md`: 언어 변경
- `references/component_10_02.md`: 화면 크기 조정
- 콘텐츠
- `references/component_11_01.md`: 접근 가능한 미디어
- `references/component_11_02.md`: 숨긴 콘텐츠
- 모바일
- `references/component_12_01.md`: 범위 슬라이드
- `references/component_12_02.md`: 뒤로가기 버튼
- `references/component_12_03.md`: 바텀시트
- `references/component_12_04.md`: 수량 토글
- `references/component_12_05.md`: 토스트
- `references/component_12_06.md`: 스낵바
- `references/component_12_07.md`: 탭바
- `references/component_12_08.md`: 스플래시 스크린

### 기본 패턴 문서

- `references/global_01.md`: 개인 식별 정보 입력
- `references/global_02.md`: 도움
- `references/global_03.md`: 동의
- `references/global_04.md`: 목록 탐색
- `references/global_05.md`: 사용자 피드백
- `references/global_06.md`: 상세 정보 확인
- `references/global_07.md`: 오류
- `references/global_08.md`: 입력폼
- `references/global_09.md`: 첨부파일
- `references/global_10.md`: 필터링·정렬
- `references/global_11.md`: 확인
- `references/global_12.md`: 모바일 알림
- `references/global_13.md`: 모바일 설정

### 서비스 패턴 문서

- 방문
- `references/service_01_01.md`: 개요
- `references/service_01_02.md`: 방문
- 검색
- `references/service_02_01.md`: 개요
- `references/service_02_02.md`: 검색 기능 찾기
- `references/service_02_03.md`: 검색어 입력
- `references/service_02_04.md`: 검색 결과 확인
- `references/service_02_05.md`: 상세 검색
- `references/service_02_06.md`: 검색 결과 이용
- `references/service_02_07.md`: 재검색
- `references/service_02_08.md`: 검색 종료
- 로그인
- `references/service_03_01.md`: 개요
- `references/service_03_02.md`: 로그인 기능 찾기
- `references/service_03_03.md`: 로그인 안내
- `references/service_03_04.md`: 로그인 방식 확인/선택
- `references/service_03_05.md`: 로그인 정보 입력
- `references/service_03_06.md`: 로그인 완료
- `references/service_03_07.md`: 서비스 이용
- `references/service_03_08.md`: 로그아웃
- 신청
- `references/service_04_01.md`: 개요
- `references/service_04_02.md`: 신청 대상 탐색
- `references/service_04_03.md`: 서비스 정보 확인
- `references/service_04_04.md`: 유의 사항/자격 확인
- `references/service_04_05.md`: 신청서 작성
- `references/service_04_06.md`: 확인·확정
- `references/service_04_07.md`: 완료
- `references/service_04_08.md`: 신청 결과 확인
- 정책정보 확인
- `references/service_05_01.md`: 개요
- `references/service_05_02.md`: 정책 탐색
- `references/service_05_03.md`: 정보 확인
- `references/service_05_04.md`: 정책 자료 탐색

## 빠른 선택표

### 이런 요청이면 이 문서를 먼저 연다

- 색상, 대비, 브랜드 컬러, 상태색: `references/style_02.md`
- 글자 크기, 행간, 본문/제목 계층: `references/style_03.md`
- 라운드, 모서리, shape 언어: `references/style_04.md`
- 레이아웃, 간격, 그리드, 반응형: `references/style_05.md`
- 아이콘 규칙: `references/style_06.md`
- 토큰 구조, CSS 변수, 시멘틱 토큰: `references/style_07.md`
- 선명한 화면 모드: `references/style_09.md`
- 헤더, 푸터, 정부 식별, 배너: `references/component_02_01.md`, `references/component_02_02.md`, `references/component_02_03.md`, `references/component_02_04.md`
- 메뉴, 브레드크럼, 페이지 이동: `references/component_03_02.md`, `references/component_03_03.md`, `references/component_03_04.md`, `references/component_03_06.md`
- 모달, 탭, 아코디언, 표, 배지: `references/component_04_05.md`, `references/component_04_10.md`, `references/component_04_07.md`, `references/component_04_11.md`, `references/component_04_06.md`
- 버튼, 링크, 플로팅 액션: `references/component_05_01.md`, `references/component_05_02.md`, `references/component_05_03.md`
- 라디오, 체크박스, 셀렉트, 토글: `references/component_06_01.md`, `references/component_06_02.md`, `references/component_06_03.md`, `references/component_06_07.md`
- 툴팁, 도움말, 코치마크: `references/component_08_01.md`, `references/component_08_03.md`, `references/component_08_04.md`, `references/component_08_05.md`
- 입력 필드, 텍스트 영역, 파일 첨부: `references/component_09_01.md`, `references/component_09_02.md`, `references/component_09_03.md`, `references/component_09_04.md`
- 에러 메시지, 오류 복구: `references/global_07.md`
- 동의, 확인, 제출 전 검토: `references/global_03.md`, `references/global_11.md`
- 목록, 검색 결과, 필터, 정렬: `references/global_04.md`, `references/global_10.md`, `references/service_02_04.md`, `references/service_02_05.md`, `references/service_02_06.md`
- 긴 입력 절차, 신청서, 단계형 폼: `references/global_08.md`, `references/service_04_05.md`, `references/service_04_06.md`, `references/service_04_07.md`
- 로그인 전 과정: `references/service_03_02.md`부터 `references/service_03_08.md`까지
- 신청 전 과정: `references/service_04_02.md`부터 `references/service_04_08.md`까지
- 정책/정보형 서비스: `references/service_05_02.md`, `references/service_05_03.md`, `references/service_05_04.md`
- 설치, Kit 적용, React/Vue, SCSS 경로: `references/outline_03.md`
- 접근성 전반 점검: `references/utility_04.md`와 각 상세 문서의 `접근성 가이드라인`

## 작업 절차

1. 현재 작업이 스타일, 컴포넌트, 기본 패턴, 서비스 플로 중 무엇인지 먼저 정한다.
2. 요약 문서에서 후보를 고른 뒤 해당 상세 문서만 읽는다.
3. 표준형인지 확장형인지 판단한다.
4. 새 UI를 만들기보다 KRDS 구조와 상태를 그대로 재사용하는 쪽을 먼저 검토한다.
5. 스타일 값은 하드코딩보다 토큰으로 연결한다.
6. 구현 후 체크리스트로 다시 검증한다.

## 구현 원칙

- KRDS에서 정의한 구조와 상태 이름을 유지한다.
- 프리미티브 토큰을 직접 남발하지 말고 시멘틱 토큰 또는 컴포넌트 토큰으로 연결한다.
- 색상만으로 상태를 구분하지 않는다.
- 아이콘 버튼과 아이콘 링크에는 텍스트 레이블 또는 접근 가능한 이름을 제공한다.
- 플레이스홀더를 레이블 대용으로 쓰지 않는다.
- 키보드 탐색, 초점 이동, 스크린 리더 이름을 기본 요구사항으로 본다.
- 헤더, 푸터, 공식 배너, 건너뛰기 링크처럼 서비스 공통 골격은 임의 변형을 피한다.
- 여러 단계 입력은 정말 필요한 경우에만 쓴다. 한 화면에서 해결 가능한 복잡도라면 점진적 공개를 먼저 검토한다.
- 파일 업로드, 오류, 확인, 동의처럼 실수 비용이 큰 구간은 관련 패턴 문서를 반드시 읽고 구현한다.

## 빠른 판단 기준

### 먼저 확인할 항목

- 공공 웹사이트 전체 구조인가
- 단일 컴포넌트 수정인가
- 폼 입력과 제출 흐름인가
- 로그인, 신청, 검색 같은 대표 과업인가
- 토큰, 색상, 서체, 간격 수정인가
- 접근성 지적 사항을 수정하는 일인가

### 자주 걸리는 위반

- KRDS 토큰 대신 임의 색상과 간격을 직접 넣는 경우
- 헤더, 푸터, 배너, 건너뛰기 링크를 생략하거나 구조를 바꾸는 경우
- 플레이스홀더를 레이블처럼 쓰는 경우
- 필터링·정렬 컨트롤을 숨기거나 현재 상태를 불명확하게 만드는 경우
- 드롭다운 메뉴를 마우스오버 중심으로 여는 경우
- 현재 상태, 오류, 선택 상태를 색상만으로 표현하는 경우
- 파일 업로드 후 자동 제출하거나 제약 조건 안내를 생략하는 경우

## 검증 방법

최종 검토 전 `references/디지털 정부 서비스 UIUX 가이드라인 자체 검증 체크리스트.md`를 읽고 관련 항목만 추려 점검한다.

- 스타일 검토: 색상, 서체, 형태
- 컴포넌트 검토: 헤더, 푸터, 입력, 탐색, 도움, 모바일
- 기본 패턴 검토: 입력폼, 개인 식별 정보, 첨부파일, 필터링·정렬
- 서비스 검토: 방문, 검색, 로그인, 신청, 정책정보 확인

체크리스트는 가능한 한 “통과/수정 필요/해당 없음”으로 짧게 판정한다. 문제가 있으면 어느 문서의 어느 계층에서 어긋났는지 함께 적는다.

## 검색은 마지막 수단

위 인덱스로도 문서를 못 찾았을 때만 검색한다. 기본 동작은 `요약 문서 -> 파일 인덱스 -> 상세 문서` 순서다.

```bash
rg --files references
rg "헤더|푸터|공식 배너|건너뛰기 링크" references/component_*.md
rg "입력폼|개인 식별 정보|필터링·정렬|오류" references/global_*.md
rg "로그인|신청|검색|방문" references/service_*.md
rg "디자인 토큰|서체|색상 팔레트|접근성" references/style_*.md references/utility_*.md
```

문서를 읽을 때는 아래 순서로 훑는다.

1. `# page title`
2. `구조`, `유형`, `용례`
3. `사용성 가이드라인`
4. `상호작용 가이드라인`
5. `접근성 가이드라인`

## 응답 방식

- KRDS 기준에 맞는 안과 맞지 않는 안을 구분해 설명한다.
- 가능하면 “어떤 문서를 봤고, 그래서 무엇을 적용했다”까지 짧게 남긴다.
- 새 코드를 제안할 때는 토큰, 상태, 접근성 속성, 반응형 대응을 함께 점검한다.
- KRDS 문서에 없는 임의 패턴을 도입해야 한다면 그 사실을 명시하고, 기존 KRDS 패턴으로 대체 가능한지 먼저 검토한다.
