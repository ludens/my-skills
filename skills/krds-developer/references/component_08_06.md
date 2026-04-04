Title: 음성지원 (TTS) | 컴포넌트 - KRDS

URL Source: https://www.krds.go.kr/html/site/component/component_08_06.html

Markdown Content:
---
description: TTS 기능이란 화면에 표시된 주요 안내, 입력 서식 설명, 업무 진행 상태 등의 텍스트를 사용자가 요청했을 때 음성으로 읽어주는 보조적 사용자 지원 기능을 말하며, 이는 시각 정보의 대체가 아닌 보완 수단으로서 다른 접근성 기능(글자 크기 조절, 대비 향상, 쉬운모드 등)과 함께 제공되는 것을 원칙으로 한다.
title: 음성지원 (TTS) | 컴포넌트 - KRDS
image: https://www.krds.go.kr/resources/img/guide/KRDS_Open_Graph.png
---

[본문 바로가기](#breadcrumb-home) 

이 누리집은 대한민국 공식 전자정부 누리집입니다. 

##  글자·화면 표시 설정

### 글자·화면 표시 설정

작게 

보통 

조금 크게 

크게 

가장 크게 

### 화면 표시 모드

기본 (밝은 배경) 

선명하게 (어두운 배경) 

시스템 설정 

초기화 닫기 

닫기 

# page title

TTS 기능이란 화면에 표시된 주요 안내, 입력 서식 설명, 업무 진행 상태 등의 텍스트를 사용자가 요청했을 때 음성으로 읽어주는 보조적 사용자 지원 기능을 말하며, 이는 시각 정보의 대체가 아닌 보완 수단으로서 다른 접근성 기능(글자 크기 조절, 대비 향상, 쉬운모드 등)과 함께 제공되는 것을 원칙으로 한다.

* 개요
* 코드

이 페이지의 구성

### 구조

1. 1.**음성 안내** 아이콘 버튼과 및 텍스트 레이블
2. 2.**음성 제어** 음성 안내를 제어할 수 있는 버튼

### 유형

#### 페이지 단위 음성지원

페이지 상단 또는 주요 타이틀 근처에 배치하여 이 페이지의 목적, 주요 기능, 이용 순서 등을 요약하여 낭독   
 (예: 민원 신청 첫 화면, 복잡한 안내 페이지 등)

#### 영역 단위 음성 지원

카드, 서브 타이틀, 약관 등 독립된 정보 단위 옆에 배치하여 해당 영역 텍스트를 요약하여 낭독  
 (예: 신청 안내, 도움 안내 등)

### 용례

#### 사용하기 적합한 경우

* 페이지 전체 흐름을 요약·설명해야 하는 경우
* 특정 영역(신청 단계 등)의 내용을 음성으로 설명할 때
* 디지털 취약계층·고령자·외국인을 대상으로, 텍스트 이해를 보완해야 할 때
* 튜토리얼/도움말 플로우에서 단계별로 화면 사용법을 읽어줄 때

#### 사용하기 적합하지 않은 경우

* 전체페이지를 의미 없이 읽어주어 재생되는 음성이 실질적인 정보나 도움을 제공하지 않는 경우
* 음성 보조기구(스크린리더 등)와 동일한 내용을 중복해서 제공하는 경우

### 사용성 가이드라인

명확한 레이블을 제공한다.

사용자자가 제공되는 정보를 정확하게 인지할 수 있도록 동작과 목적이 드러나도록버튼 레이블을 붙인다.

모범 사례

피해야 할 사례

자동재생을 금지한다.

화면 전환 시 사용자의 조작 없이 자동으로 실행되지 않도록 한다. 또한 언제든지 일시정지, 정지할 수 있어야 한다.

너무 긴 내용을 읽어주지 않도록 한다.

음성 지원은 음성 보조기구(스크린리더 등)와 동일한 내용을 중복해서 제공하지 않도록 하고, 사용자에게 꼭 필요한 정보를 요약된 형태로 제공한다. (예 : 무엇을 할 수 있는지, 어떤 순서로 진행하면 되는지, 안내 및 주의 사항 등)

### 예시

#### 기본

레이블 재생 레이블 

##### 기본 코드 확인하기

<!-- KRDS-CODE:START 기본 코드 확인하기 -->
<!-- Source: https://www.krds.go.kr/html/code/tts.html -->
```html
<!-- TTS 버튼 - Default 타입 -->
<button type="button" class="krds-tts medium"
  onclick="krds_playTts('TTS 기능이란 화면에 표시된 주요 안내, 입력 서식 설명, 업무 진행 상태 등의 텍스트를 사용자가 요청했을 때 음성으로 읽어주는 보조적 사용자 지원 기능을 말하며, 이는 시각 정보의 대체가 아닌 보완 수단으로서 다른 접근성 기능(글자 크기 조절, 대비 향상, 쉬운모드 등)과 함께 제공되는 것을 원칙으로 한다.', this)">
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-volume"></i>
  </span>
  <span class="krds-tts-text">레이블</span>
</button>

<!-- TTS 버튼 - Play 타입 -->
<button type="button" class="krds-tts medium play"
  onclick="krds_playTts('TTS 기능이란 화면에 표시된 주요 안내, 입력 서식 설명, 업무 진행 상태 등의 텍스트를 사용자가 요청했을 때 음성으로 읽어주는 보조적 사용자 지원 기능을 말하며, 이는 시각 정보의 대체가 아닌 보완 수단으로서 다른 접근성 기능(글자 크기 조절, 대비 향상, 쉬운모드 등)과 함께 제공되는 것을 원칙으로 한다.', this)">
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-play"></i>
  </span>
  <span class="krds-tts-text">재생</span>
</button>

<!-- TTS 버튼 - 상태 예시 -->
<button type="button" class="krds-tts medium" disabled>
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-volume"></i>
  </span>
  <span class="krds-tts-text">레이블</span>
</button>
<!-- //TTS 버튼 -->
```
<!-- KRDS-CODE:END 기본 코드 확인하기 -->

#### 사이즈

 Xsmall TTS Small TTS Medium TTS 

##### 사이즈 코드 확인하기

<!-- KRDS-CODE:START 사이즈 코드 확인하기 -->
<!-- Source: https://www.krds.go.kr/html/code/tts_size.html -->
```html
<!-- TTS 버튼 - Default 타입 -->
<button type="button" class="krds-tts xsmall">
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-volume"></i>
  </span>
  <span class="krds-tts-text"> Xsmall TTS</span>
</button>
<button type="button" class="krds-tts small">
  <span class="krds-tts-icon">
    <i class="svg-icon ico-volume"></i>
  </span>
  <span class="krds-tts-text">Small TTS</span>
</button>
<button type="button" class="krds-tts medium">
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-volume"></i>
  </span>
  <span class="krds-tts-text">Medium TTS</span>
</button>
```
<!-- KRDS-CODE:END 사이즈 코드 확인하기 -->

#### 아이콘 버튼

##### 아이콘 버튼 코드 확인하기

<!-- KRDS-CODE:START 아이콘 버튼 코드 확인하기 -->
<!-- Source: https://www.krds.go.kr/html/code/tts_icon.html -->
```html
<!-- TTS 버튼 - Default 타입 -->
<button type="button" class="krds-tts medium">
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-volume"></i>
  </span>
</button>

<!-- TTS 버튼 - Play 타입 -->
<button type="button" class="krds-tts medium play">
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-play"></i>
  </span>
</button>

<!-- TTS 버튼 - 상태 예시 -->
<button type="button" class="krds-tts medium" disabled>
  <span class="krds-tts-icon" aria-hidden="true">
    <i class="svg-icon ico-volume"></i>
  </span>
</button>
<!-- //TTS 버튼 -->
```
<!-- KRDS-CODE:END 아이콘 버튼 코드 확인하기 -->

### 마크업 가이드

#### CSS 선택자

__마크업 가이드 CSS 선택자에 대한 표로 필수 로 구성되어있으며 구분 항목은 전체영역구성되어있음__
| 필수   | 선택        |         |        |       |
| ---- | --------- | ------- | ------ | ----- |
| 전체영역 | .krds-tts | 타입      | 플레이 타입 | .play |
| 사이즈  | 더 작게      | .xsmall |        |       |
| 작게   | .small    |         |        |       |
| 중간   | .medium   |         |        |       |

#### JS

__마크업 가이드js 함수 대한 표로 구성되어있으며 구분 항목은 내용__
| 함수명           | 내용                           |
| ------------- | ---------------------------- |
| krds\_playTts | krds\_playTts('읽을 내용', this) |
