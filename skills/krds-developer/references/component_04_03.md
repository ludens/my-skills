Title: 달력 (Calendar) | 컴포넌트 - KRDS

URL Source: https://www.krds.go.kr/html/site/component/component_04_03.html

Markdown Content:
---
description: 달력은 날짜와 관련된 정보와 기능을 제공하는 데 사용한다.
title: 달력 (Calendar) | 컴포넌트 - KRDS
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

달력은 날짜와 관련된 정보와 기능을 제공하는 데 사용한다.

* 개요
* 접근성
* 코드

이 페이지의 구성

### 구조

1. 1.**연/월** 달력의 연도, 월 정보 달력 유형에 따라 연도나 월을 선택하기 위한 컨트롤이 제공될 수 있음
2. 2.**연/월 탐색 버튼** 이전 또는 다음 연도, 월을 탐색하기 위한 버튼
3. 3.**달력 그리드** 요일과 여러 상태의 날짜 정보를 표시하는 시각적인 그리드
4. 4.**요일** 한 주의 요일 정보로 시작 요일은 주사용자의 지역/언어에 따라 달라질 수 있음
5. 5.**날짜** 가장 기본적인 상태의 날짜 정보로 버튼으로 사용될 수 있음
6. 6.**오늘 날짜** 현재 날짜로 다른 상태의 날짜와 구분하기 위한 별도의 식별자와 함께 사용됨
7. 7\. **선택된 날짜(선택)** 사용자가 선택한 날짜로 다른 상태의 날짜와 구분하기 위한 별도의 식별자와 함께 사용됨
8. 8.**선택할 수 없는 날짜(선택)** 사용자가 선택할 수 없는 날짜
9. 9.**활성화되지 않은 날짜** 이전 달 또는 다음 달에 속한 날짜로 사용자가 선택할 수 있음
10. 10.**이벤트(선택)** 날짜와 관련하여 사용자에게 안내하고자 하는 데이터로 텍스트, 식별자, 텍스트와 식별자가 조합된 형태로 사용할 수 있음

### 용례

#### 사용하기 적합한 경우

* 날짜별로 신청 가능한 서비스가 정기적으로 제공되는 경우
* 사용자가 날짜를 입력하는 과정에서 여러 가지 날짜 정보를 비교하여 선택해야 하는 경우
* 사용자가 현재와 가까운 날짜 관련 정보를 확인하거나 선택해야 하는 경우

#### 사용하기 적합하지 않은 경우

* 정기적으로 업데이트되는 정보가 아니거나 한 달에 2개 이하의 이벤트만 있는 경우

### 사용성 가이드라인

날짜의 여러 가지 상태, 정보의 범례는 일관성 있게 표현한다.

달력이 여러 개의 섹션이나 페이지에 반복적으로 사용될 경우 날짜의 여러 가지 상태 정보(오늘 날짜, 선택된 날짜, 활성화되지 않은 날짜, 선택할 수 없는 날짜), 날짜에 표현된 정보의 범례(예 - 휴관일, 공휴일 등)를 시각적, 구조적으로 일관성 있게 표현하여 사용자가 학습 없이 효율적으로 콘텐츠를 확인할 수 있도록 해야 한다.

날짜의 여러 가지 상태 정보가 서로 명확하게 구분되도록 표현한다.

날짜의 상태를 표현하는 경우 여러 가지 상태는 날짜의 텍스트, 배경색으로만 구분하지 않고 텍스트 굵기, 밑줄, 배경의 형태, 부가적인 식별자를 제공하여 명확하게 구분해야 한다. 오늘 날짜, 사용자가 선택한 날짜에는 별도의 텍스트 설명을 제공하여 보다 직관적으로 다른 날짜와 구분할 수 있다.

모범 사례

피해야 할 사례

이벤트 정보가 복잡한 경우 정보를 손실 없이 확인할 수 있는 수단을 제공한다.

하나의 날짜에 여러 개의 이벤트가 존재하는 경우 이벤트 제목이 유사하여 구분이 어려울 수 있으며, 달력과 날짜 영역의 공간적 제약으로 인해 복잡한 이벤트 정보는 텍스트가 생략될 수 있다. 이 경우, 표나 목록 컴포넌트를 활용한 별도의 이벤트 목록을 제공하여 사용자가 정보를 정확하게 인지할 수 있도록 해야 한다. 달력의 표시 단위를 월이 아닌 주 또는 일로 변경하여 이벤트 정보 표시 영역을 확장하는 방법도 활용할 수 있다.

모범 사례

달력 그리드에 헤딩(요일) 정보를 반드시 제공한다.

달력에 헤딩 없이 날짜 정보만 제공하게 되면 콘텐츠가 날짜임을 직관적으로 이해하기 어려우며, 한 주의 시작 요일을 명확하게 인지하기 어렵다.

### 접근성 가이드라인

날짜 및 관련 정보의 의미를 색상으로만 구분하지 않는다.

여러 가지 날짜 및 관련 정보에 대한 의미를 색상 이외의 수단으로 구분할 수 있는 시각적 단서를 제공해야 한다. 밑줄 제공, 1px 이상의 테두리 차이, 식별자 제공 등의 방법으로 크기나 형태 차원에서 정보를 구분하는 방법을 사용할 수 있다.

* KWCAG 2.2 색에 무관한 콘텐츠 인식
* WCAG 2.1 Use of Color (A)

날짜 및 관련 정보의 의미를 스크린 리더에서 확인할 수 있도록 한다.

시각적으로 표현된 날짜 관련 여러 가지 상태 정보(오늘 날짜, 선택된 날짜, 활성화되지 않은 날짜, 선택할 수 없는 날짜), 날짜에 표현된 정보의 범례(예 - 일정 있음, 휴관일, 공휴일 등)에 대한 대체 텍스트를 제공해야 한다.

* KWCAG 2.2 적절한 대체 텍스트 제공
* WCAG 2.1 Non-text Content (A)

달력에서 제공되는 모든 기능을 키보드로 실행할 수 있도록 한다.

달력에서 제공되는 모든 기능은 마우스뿐만 아니라 키보드, 터치 인터페이스로 실행할 수 있어야 한다.

* KWCAG 2.2 키보드 사용 보장
* WCAG 2.1 Keyboard (A)

달력에서 제공되는 모든 기능에 키보드 초점이 명확하게 표시되도록 한다.

달력에서 제공되는 모든 사용자 인터페이스(버튼, 링크)는 초점을 받은 상태가 시각적으로 명확하게 구분되어야 한다.

* KWCAG 2.2 초점 이동과 표시
* WCAG 2.1 Focus Visible (AA)

### 상호작용 가이드라인

#### 날짜 링크 탐색

__상호작용 가이드라인 날짜 링크 탐색에 대한 표로 구분/설명으로 구성되어있으며 구분 항목은 Tab, Shift + Tab 로 구성되어있음__
| 구분               | 설명                         |
| ---------------- | -------------------------- |
| Tab, Shift + Tab | 달력 내 인터페이스 요소를 순차적으로 탐색한다. |

#### 기능 실행 또는 이동

__상호작용 가이드라인 기능 실행 또는 이동에 대한 표로 이동에 대한 표로 구분/설명으로 구성되어있으며 구분 항목은 Click, Enter 로 구성되어있음__
| 구분    | 설명                                  |
| ----- | ----------------------------------- |
| Click | 달력 내 액션 버튼의 기능이 실행되거나 링크 목적지로 이동한다. |
| Enter | 달력 내 액션 버튼의 기능이 실행되거나 링크 목적지로 이동한다. |

### 예시

#### 기본

기간선택 

달력 열기 

이전 달 

2024년 

* 2001년
* 2002년
* 2003년
* 2004년
* 2005년
* 2006년
* 2007년
* 2008년
* 2009년
* 2010년
* 2011년
* 2012년
* 2013년
* 2014년
* 2015년
* 2016년
* 2017년
* 2018년
* 2019년
* 2020년
* 2021년
* 2022년
* 2023년
* 2024년

12월 

* 01월
* 02월
* 03월
* 04월
* 05월
* 06월
* 07월
* 08월
* 09월
* 10월
* 11월
* 12월

다음 달 

__2024년 12월__
| 일  | 월  | 화  | 수  | 목  | 금  | 토  |
| -- | -- | -- | -- | -- | -- | -- |
| 26 | 27 | 28 | 29 | 30 | 1  | 2  |
| 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| 17 | 18 | 19 | 20 | 21 | 22 | 23 |
| 24 | 25 | 26 | 27 | 28 | 29 | 30 |
| 31 | 1  | 2  | 3  | 4  | 5  | 6  |

오늘 취소 확인 

##### 기본 코드 확인하기

<!-- KRDS-CODE:START 기본 코드 확인하기 -->
<!-- Source: https://www.krds.go.kr/html/code/calendar.html -->
```html
<!-- calendar -->
<div class="form-group">
  <div class="form-tit">
    <label for="cal">기간선택</label>
  </div>
  <div class="form-conts calendar-conts">
    <div class="calendar-input">
      <input type="number" class="krds-input datepicker cal" placeholder="YYYY.MM.DD" id="cal">
      <button type="button" class="krds-btn medium icon form-btn-datepicker">
        <span class="sr-only">달력 열기</span>
        <i class="svg-icon ico-calendar"></i>
      </button>
    </div>
    <div class="krds-calendar-area">
      <div class="calendar-wrap bottom single" aria-label="달력">
        <div class="calendar-head">
          <button type="button" class="btn-cal-move prev"><span class="sr-only">이전 달</span></button>
          <div class="calendar-switch-wrap">
            <div class="calendar-drop-down">
              <button type="button" class="btn-cal-switch year" aria-label="연도 선택">2024년</button>
              <div class="calendar-select calendar-year-wrap">
                <ul class="sel year">
                  <li>
                    <button type="button">2001년</button>
                  </li>
                  <li>
                    <button type="button" class="active">2002년</button>
                  </li>
                  <li>
                    <button type="button" disabled>2003년</button>
                  </li>
                  <li>
                    <button type="button">2004년</button>
                  </li>
                  <li>
                    <button type="button">2005년</button>
                  </li>
                  <li>
                    <button type="button">2006년</button>
                  </li>
                  <li>
                    <button type="button">2007년</button>
                  </li>
                  <li>
                    <button type="button">2008년</button>
                  </li>
                  <li>
                    <button type="button">2009년</button>
                  </li>
                  <li>
                    <button type="button">2010년</button>
                  </li>
                  <li>
                    <button type="button">2011년</button>
                  </li>
                  <li>
                    <button type="button">2012년</button>
                  </li>
                  <li>
                    <button type="button">2013년</button>
                  </li>
                  <li>
                    <button type="button">2014년</button>
                  </li>
                  <li>
                    <button type="button">2015년</button>
                  </li>
                  <li>
                    <button type="button">2016년</button>
                  </li>
                  <li>
                    <button type="button">2017년</button>
                  </li>
                  <li>
                    <button type="button">2018년</button>
                  </li>
                  <li>
                    <button type="button">2019년</button>
                  </li>
                  <li>
                    <button type="button">2020년</button>
                  </li>
                  <li>
                    <button type="button">2021년</button>
                  </li>
                  <li>
                    <button type="button">2022년</button>
                  </li>
                  <li>
                    <button type="button">2023년</button>
                  </li>
                  <li>
                    <button type="button">2024년</button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="calendar-drop-down">
              <button type="button" class="btn-cal-switch month" aria-label="월 선택">12월</button>
              <div class="calendar-select calendar-mon-wrap">
                <ul class="sel month">
                  <li>
                    <button type="button">01월</button>
                  </li>
                  <li>
                    <button type="button" disabled>02월</button>
                  </li>
                  <li>
                    <button type="button">03월</button>
                  </li>
                  <li>
                    <button type="button">04월</button>
                  </li>
                  <li>
                    <button type="button">05월</button>
                  </li>
                  <li>
                    <button type="button">06월</button>
                  </li>
                  <li>
                    <button type="button">07월</button>
                  </li>
                  <li>
                    <button type="button">08월</button>
                  </li>
                  <li>
                    <button type="button">09월</button>
                  </li>
                  <li>
                    <button type="button">10월</button>
                  </li>
                  <li>
                    <button type="button">11월</button>
                  </li>
                  <li>
                    <button type="button" class="active">12월</button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <button type="button" class="btn-cal-move next"><span class="sr-only">다음 달</span></button>
        </div>
        <div class="calendar-body">
          <div class="calendar-table-wrap">
            <table class="calendar-tbl">
              <caption>
                2024년 12월
              </caption>
              <thead>
                <tr>
                  <th>일</th>
                  <th>월</th>
                  <th>화</th>
                  <th>수</th>
                  <th>목</th>
                  <th>금</th>
                  <th>토</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="old day-off"><button type="button" class="btn-set-date"><span>26</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>27</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>28</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>29</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>30</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>1</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>2</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>3</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>4</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>5</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>6</span></button></td>
                  <td class="period start end"><button type="button" class="btn-set-date"><span>7</span></button></td>
                  <td class="day-event"><button type="button" class="btn-set-date"><span>8</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>9</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>10</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>11</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>12</span></button></td>
                  <td class="disabled"><button type="button" class="btn-set-date" disabled><span>13</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>14</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>15</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>16</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>17</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>18</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>19</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>20</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>21</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>22</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>23</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>24</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>25</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>26</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>27</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>28</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>29</span></button></td>
                  <td class="today"><button type="button" class="btn-set-date"><span>30</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>31</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>1</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>2</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>3</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>4</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>5</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>6</span></button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="calendar-footer">
          <div class="calendar-btn-wrap">
            <button type="button" class="krds-btn small text" id="get-today">오늘</button>
            <button type="button" class="krds-btn small tertiary">취소</button>
            <button type="button" class="krds-btn small primary">확인</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- //calendar -->
```
<!-- KRDS-CODE:END 기본 코드 확인하기 -->

#### Date Range

 날짜선택

* \-
달력 열기 

이전 달 

2024년 

* 2001년
* 2002년
* 2003년
* 2004년
* 2005년
* 2006년
* 2007년
* 2008년
* 2009년
* 2010년
* 2011년
* 2012년
* 2013년
* 2014년
* 2015년
* 2016년
* 2017년
* 2018년
* 2019년
* 2020년
* 2021년
* 2022년
* 2023년
* 2024년

12월 

* 01월
* 02월
* 03월
* 04월
* 05월
* 06월
* 07월
* 08월
* 09월
* 10월
* 11월
* 12월

다음 달 

__2024년 12월__
| 일  | 월  | 화  | 수  | 목  | 금  | 토  |
| -- | -- | -- | -- | -- | -- | -- |
| 26 | 27 | 28 | 29 | 30 | 1  | 2  |
| 3  | 4  | 5  | 6  | 7  | 8  | 9  |
| 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| 17 | 18 | 19 | 20 | 21 | 22 | 23 |
| 24 | 25 | 26 | 27 | 28 | 29 | 30 |
| 31 | 1  | 2  | 3  | 4  | 5  | 6  |

오늘 취소 확인 

##### Date Range 코드 확인하기

<!-- KRDS-CODE:START Date Range 코드 확인하기 -->
<!-- Source: https://www.krds.go.kr/html/code/calendar_range.html -->
```html
<!-- calendar -->
<div class="form-group">
  <div class="form-tit">
    날짜선택
  </div>
  <div class="form-conts calendar-conts">
    <div class="calendar-input">
      <ul class="input-group range set">
        <li>
          <input type="number" class="krds-input datepicker" placeholder="시작날짜" title="시작날짜 입력">
        </li>
        <li class="mark">-</li>
        <li>
          <input type="number" class="krds-input datepicker" placeholder="종료날짜" title="종료날짜 입력">
        </li>
      </ul>
      <button type="button" class="krds-btn medium icon form-btn-datepicker">
        <span class="sr-only">달력 열기</span>
        <i class="svg-icon ico-calendar"></i>
      </button>
    </div>
    <div class="krds-calendar-area">
      <div class="calendar-wrap bottom" aria-label="달력">
        <div class="calendar-head">
          <button type="button" class="btn-cal-move prev"><span class="sr-only">이전 달</span></button>
          <div class="calendar-switch-wrap">
            <div class="calendar-drop-down">
              <button type="button" class="btn-cal-switch year" aria-label="연도 선택">2024년</button>
              <div class="calendar-select calendar-year-wrap">
                <ul class="sel year">
                  <li>
                    <button type="button">2001년</button>
                  </li>
                  <li>
                    <button type="button">2002년</button>
                  </li>
                  <li>
                    <button type="button" disabled>2003년</button>
                  </li>
                  <li>
                    <button type="button">2004년</button>
                  </li>
                  <li>
                    <button type="button">2005년</button>
                  </li>
                  <li>
                    <button type="button">2006년</button>
                  </li>
                  <li>
                    <button type="button">2007년</button>
                  </li>
                  <li>
                    <button type="button">2008년</button>
                  </li>
                  <li>
                    <button type="button">2009년</button>
                  </li>
                  <li>
                    <button type="button">2010년</button>
                  </li>
                  <li>
                    <button type="button" class="active">2011년</button>
                  </li>
                  <li>
                    <button type="button">2012년</button>
                  </li>
                  <li>
                    <button type="button">2013년</button>
                  </li>
                  <li>
                    <button type="button">2014년</button>
                  </li>
                  <li>
                    <button type="button">2015년</button>
                  </li>
                  <li>
                    <button type="button">2016년</button>
                  </li>
                  <li>
                    <button type="button">2017년</button>
                  </li>
                  <li>
                    <button type="button">2018년</button>
                  </li>
                  <li>
                    <button type="button">2019년</button>
                  </li>
                  <li>
                    <button type="button">2020년</button>
                  </li>
                  <li>
                    <button type="button">2021년</button>
                  </li>
                  <li>
                    <button type="button">2022년</button>
                  </li>
                  <li>
                    <button type="button">2023년</button>
                  </li>
                  <li>
                    <button type="button">2024년</button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="calendar-drop-down">
              <button type="button" class="btn-cal-switch month" aria-label="월 선택">12월</button>
              <div class="calendar-select calendar-mon-wrap">
                <ul class="sel month">
                  <li>
                    <button type="button" disabled>01월</button>
                  </li>
                  <li>
                    <button type="button" class="active">02월</button>
                  </li>
                  <li>
                    <button type="button">03월</button>
                  </li>
                  <li>
                    <button type="button">04월</button>
                  </li>
                  <li>
                    <button type="button">05월</button>
                  </li>
                  <li>
                    <button type="button">06월</button>
                  </li>
                  <li>
                    <button type="button">07월</button>
                  </li>
                  <li>
                    <button type="button">08월</button>
                  </li>
                  <li>
                    <button type="button">09월</button>
                  </li>
                  <li>
                    <button type="button">10월</button>
                  </li>
                  <li>
                    <button type="button">11월</button>
                  </li>
                  <li>
                    <button type="button">12월</button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <button type="button" class="btn-cal-move next"><span class="sr-only">다음 달</span></button>
        </div>
        <div class="calendar-body">
          <div class="calendar-table-wrap">
            <table class="calendar-tbl">
              <caption>
                2024년 12월
              </caption>
              <thead>
                <tr>
                  <th>일</th>
                  <th>월</th>
                  <th>화</th>
                  <th>수</th>
                  <th>목</th>
                  <th>금</th>
                  <th>토</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="old day-off"><button type="button" class="btn-set-date"><span>26</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>27</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>28</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>29</span></button></td>
                  <td class="old"><button type="button" class="btn-set-date"><span>30</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>1</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>2</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>3</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>4</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>5</span></button></td>
                  <td class="day-event"><button type="button" class="btn-set-date"><span>6</span></button></td>
                  <td class="period start"><button type="button" class="btn-set-date"><span>7</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>8</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>9</span></button></td>
                </tr>
                <tr>
                  <td class="period day-off"><button type="button" class="btn-set-date"><span>10</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>11</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>12</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>13</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>14</span></button></td>
                  <td class="period"><button type="button" class="btn-set-date"><span>15</span></button></td>
                  <td class="period end"><button type="button" class="btn-set-date"><span>16</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>17</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>18</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>19</span></button></td>
                  <td class="today"><button type="button" class="btn-set-date"><span>20</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>21</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>22</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>23</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>24</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>25</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>26</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>27</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>28</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>29</span></button></td>
                  <td><button type="button" class="btn-set-date"><span>30</span></button></td>
                </tr>
                <tr>
                  <td class="day-off"><button type="button" class="btn-set-date"><span>31</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>1</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>2</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>3</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>4</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>5</span></button></td>
                  <td class="new"><button type="button" class="btn-set-date"><span>6</span></button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="calendar-footer">
          <div class="calendar-btn-wrap">
            <button type="button" class="krds-btn small text" id="get-today">오늘</button>
            <button type="button" class="krds-btn small tertiary">취소</button>
            <button type="button" class="krds-btn small primary">확인</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- //calendar -->
```
<!-- KRDS-CODE:END Date Range 코드 확인하기 -->

### 마크업 가이드

#### CSS 선택자

__마크업 가이드 CSS 선택자에 대한 표로 필수/선택으로 구성되어있으며 구분 항목은 전체영역, 달력, 단일 날짜 선택, 연/월 탐색, 달력 그리드, 선택된 날짜, 선택할 수 없는 날짜, 이벤트, 오늘 날짜, 달력 하단으로 구성되어있음__
| 필수          | 선택                        |          |                       |
| ----------- | ------------------------- | -------- | --------------------- |
| 전체영역        | .calendar-conts           |          |                       |
| 달력          | .krds-calendar-area       | 단일 날짜 선택 | .calendar-wrap.single |
| 연/월 탐색      | .calendar-head            |          |                       |
| 달력 그리드      | .calendar-body            | 선택된 날짜   | td.period.start.end   |
| 선택할 수 없는 날짜 | td.old td.new td.disabled |          |                       |
| 이벤트         | td.day-event              |          |                       |
| 오늘          | td.today                  |          |                       |
| 공휴일         | td.day-off                |          |                       |
| 달력 하단       | .calendar-footer          |          |                       |

#### JS

__마크업 가이드 JS에 대한 표로 함수명/설명으로 구성되어있음__
| 함수명                   | 설명     |                 |
| --------------------- | ------ | --------------- |
| krds\_calendar        | init() | 초기화 및 주요 이벤트 실행 |
| openDatePicker()      | 달력 열기  |                 |
| closeAllDatePickers() | 달력 닫기  |                 |
| toggleDateSelector()  | 연/월 탐색 |                 |

##### 코드 확인하기 

#### 개발 시 접근성 관련 주의 사항

* 키보드 탐색 시 모든 버튼 및 링크에 초점이 순차적으로 이동하는지 확인한다.

### 컴포넌트 토큰 (css variable)
