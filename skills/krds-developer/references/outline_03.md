Title: 개발자 | 시작하기 - KRDS

URL Source: https://www.krds.go.kr/html/site/outline/outline_03.html

Markdown Content:
---
description: 개발자가 프로젝트에 KRDS HTML Component Kit을 설치하여 디자인 시스템을 쉽게 적용할 수 있도록 가이드라인을 제공한다. 
title: 개발자 | 시작하기 - KRDS
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

개발자가 프로젝트에 KRDS HTML Component Kit을 설치하여 디자인 시스템을 쉽게 적용할 수 있도록 가이드라인을 제공한다.

이 페이지의 구성

### 튜토리얼

다음 튜토리얼 동영상을 통해 프로젝트에 HTML Component Kit 설치, 디자인 토큰 추출, 스타일 사용자화, 디자인 토큰 수정 등을 학습할 수 있다.

### 폰트 사용

[표준형 스타일](../style/style%5F01.html#anchor-page-1)은 페이지 내에[ Pretendard GOV 웹 폰트 CDN ](https://github.com/orioncactus/pretendard/tree/main/packages/pretendard-gov "새 창 열림") 을 추가하여 Pretendard GOV 서체(typeface)를 기본으로 사용한다.

### HTML Component Kit 설치

#### NPM

1. 1.프로젝트 터미널 창에 다음의 명령어를 입력하여 Kit를 설치한다.
2. 2.설치 후 프로젝트의 다음 디렉터리에서 해당 파일을 확인한다.

유의 사항 

NPM 설치 후 사용 시 유의 사항

* 현재의 NPM Kit은 SCSS 내의 참조 경로에 대한 설정을 따로 지원하지 않으므로 SCSS 사용 시에 Kit 내의 /resources 디렉터리 전체를 내 프로젝트에 복제하고 필요 시 파일 내 참조 경로를 수동으로 재설정하여 사용하는것을 권장한다.

#### Github 다운로드

* _HTML5_  
**HTML Component Kit v1.1.0** [ HTML Component Kit 바로가기 ](https://github.com/KRDS-uiux/krds-uiux "새 창 열기")

#### CDN

별도의 설치 없이 사용하고자 하는 경우 다음과 같이 페이지 내에 CSS와 JavaScript 파일을 로드하여 사용한다.

### React / Vue 설치

#### NPM

1. 1.프로젝트 터미널 창에 다음의 명령어를 입력하여 Kit를 설치한다.
2. 2.설치 후 node\_modues 폴더에 모듈이 생성되었는지 확인한다.

#### 적용방법

설치 후 프로젝트에서 다음과 같이 CSS 파일과 컴포넌트를 import하여 사용한다.

#### Documentation

* _REACT_  
**React Stroybook** [ React 바로가기 ](/storybook/react "새 창 열기")
* _VUE_  
**Vue Stroybook** [ Vue 바로가기 ](/storybook/vue "새 창 열기")

### 디자인 토큰 추출

 디자인 툴에서 제작한 디자인 토큰은 내보내기 기능을 통하여 JSON 파일로 내려받을 수 있다. 이 JSON 파일을 CSS variable 형식으로 변환하여 컴포넌트 스타일링에 이용하면 이후 디자인이 수정되더라도 json 파일만 업데이트하여 수정 사항을 간단히 반영할 수 있다.  
 피그마 툴에서의 디자인 토큰 추출에 대한 상세한 설명은 튜토리얼 영상에서 확인할 수 있다.

 디자인 토큰과 CSS variable의 전체 속성은[ 디자인 토큰 목록 ](../style/style%5F07%5Fpopup.html "새 창 열림") 에서 자세히 확인할 수 있다.

### 스타일 사용자화

* KRDS에서는 스타일 작업 시 SCSS를 사용하였으며 컴포넌트에 대한 SCSS 파일 원본을 제공하므로 프로젝트 스타일 작업 시에도 SCSS 사용을 권장하고 있다. 다만 작업환경 상 SCSS 사용이 어려운 경우에는 CSS 사용도 가능하며, 이를 위해 Kit에 SCSS파일을 컴파일한 CSS 파일도 함께 제공한다.
* 다음의 예시에서는 SCSS 기준으로 경로를 설명하고 있으며, CSS 작업 시에는 /resources 디렉터리 기준으로 확장자가 CSS인 동일한 파일명을 참조하면 된다.

#### 전체 라이브러리 가져오기

KRDS 디자인 요소를 모두 사용할 경우, 사용자 SCSS 파일에 다음과 같이 입력한다.

#### 개별 구성요소 가져오기

구성요소를 개별적으로 사용하는 경우, 공통 SCSS 파일을 먼저 불러온 뒤 개별 구성요소를 가져온다.

### JavaScript 사용하기

다음과 같은 방식으로 페이지 내에 JavaScript 파일을 로드하여 사용한다.

### 디자인 토큰 수정

 디자인 토큰은 디자인 파일에서 수정한 뒤 코드에 적용하는 것이 원칙이지만 디자인 파일에서 직접 토큰을 관리할 수 없는 경우 코드에서 토큰값을 수정할 수 있다.   
 디자인 토큰 수정 시에는 원본 코드값을 직접 수정하지 않고 프로젝트의 CSS 또는 SCSS 파일에 필요한 토큰 값(CSS variable)을 재선언한다.

수정 전 유의 사항 

디자인 토큰 관련 내용 숙지

디자인 토큰을 수정하기 전 관련 내용에 대한 숙지가 필요하다.

* [디자인 토큰](../style/style%5F07.html) 페이지에서 자세한 내용을 학습하여 디자인 토큰 수정 시 다른 토큰에 미치는 영향도를 면밀히 검토한다.
* [ 디자인 토큰 목록 ](../style/style%5F07%5Fpopup.html "새 창 열림") 에서 디자인 토큰의 전체 목록을 확인하고 수정 대상 토큰을 미리 식별해 둔다.
