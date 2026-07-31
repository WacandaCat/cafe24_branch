# SLBS.shop GNB 개편 핸드오프 문서 (v2 — 최종)

> 작성: 2026-07-30 / Claude.ai 세션 → 새 세션 인계용
> 담당: Danny (Park Sung-bae), SLBS 디렉터
> 이전 버전(v1, slbs-menu-handoff.md)을 대체함

---

## 1. 프로젝트 개요와 현재 상태

- 대상: **slbs.shop** — Cafe24 반응형 스킨 (PC/모바일 동일 스킨, SKIN_CODE=skin14, 대표디자인 SLBS-KOREAN)
- **2026-07-28~30 작업 완료.** GNB가 하드코딩에서 자동화 체계로 전환됨
- 제약: Cafe24 스마트디자인은 Git/API 미지원. 편집창 저장 = 즉시 실서버 배포. Vercel/GitHub 프로젝트들과 달리 git push 배포 아님

### 현재 GNB (완성 상태)
```
PC:     SHOP | COLLECTION | SHOWROOM | CUSTOM | BRAND
모바일:  SHOWROOM(Click Here!) | SHOP | COLLECTION | CUSTOM | BRAND | 1:1 Q&A
```
- **중고폰은 메뉴에서 숨김** (주석 처리, 삭제 아님). 진입은 단축주소만: `slbs.shop/reslbs.html`, `slbs.shop/ReSLBS.html` (대소문자 구분됨, 둘 다 생성)

## 2. 분류 체계 (2026-07-30 기준)

**평행 이중 축**: ALL PRODUCT(465)=기종 축, COLLECTION(472)=IP 축. 둘 다 최상위 대분류.
- **472는 "메인분류 표시상태" OFF** → module 출력에서 빠져 SHOP 메뉴에 안 섞임 (핵심 설정!)
- CUSTOM(14), 정리폴더도 표시 OFF 상태

```
ALL PRODUCT (465)
 ├ Samsung (468) ─ Z 시리즈(474→하위 458 Flip8, 459 Fold8, 460 Fold8 Ultra...), S 시리즈(57→394 S26...), A 시리즈(298), 워치(62)
 ├ Apple (469) ─ 아이폰(287→349 17시리즈...), 에어팟(288)
 ├ iPhone PRSM CASE (388) → PRSM CASE (389)
 ├ 삼성 갤럭시 버즈 (66), NFC 테마톡 (99), ACC (69→방수팩 450 등), 라이프스타일 TV (242)

COLLECTION (472)
 ├ SLBS (473) → Impression(485), Monoline(486), PRSM(487), SLBS Utopia(513)
 ├ Crocs (505) → Crocs(3)
 ├ Disney/Pixar (479) → Star Wars, Mickey's, Inside Out 2, Pixar Collection, Toy Story 5
 ├ Sanrio (488) → Sanrio(489), Pompompurin
 ├ Pokémon (491) → Pokémon(492)
 ├ Bebe The Ori (498), Warner Bros (495→톰과제리·해리포터·루니툰·위베어·슈퍼맨·배트맨)
 ├ Sticky Monster Lab (502), HERSHEY'S (503), The Simpsons (504), Voltron (507)
```

- 카테고리 API: `GET /exec/front/Product/SubCategory` (필드: cate_no, parent_cate_no, name, link_product_list). 표시 OFF여도 API에는 나옴
- ALL PRODUCT 진열: "최근 등록 상품이 위로" + 품절 맨 뒤 (2026-07-28 변경)

## 3. 파일 지도

| 편집창 표시명 | 실제 경로 | 역할 |
|---|---|---|
| 레이아웃 (상단 메뉴) | /layout/basic/navigation.html (추정) | PC GNB + **[SLBS PATCH] 전체가 여기** (유일본) |
| 레이아웃 (슬라이딩) | /layout/basic/menu.html | 모바일 햄버거 메뉴. 중고폰 주석 처리됨 |
| 공통 레이아웃 | /layout/basic/layout.html | @import로 조각 로드. 패치 없음 |
| 상품분류 | product/list.html | `id="slbs-cate-name"` 추가됨 (분류명 표시) |
| — | /slbs/assets/js/header.js | **외주 코드, 수정 금지.** `make()` 함수가 module 평면 출력을 2단으로 재조립. 패치는 그 결과를 후처리 |
| — | /reslbs.html, /ReSLBS.html | 중고폰 단축주소 리다이렉트 → event-re-01.html?cate_no=416 |

- 편집창은 파일을 한글 별칭으로 표시. 파일명 검색 ≠ 소스 내용 검색 (별개 기능)
- 죽은 참조 `<!—@js(/layout/basic/js/navigation.js)—>` (전각 대시, 파일 없음) 두 파일에 존재 — 무해, 방치 중

## 4. [SLBS PATCH] 구조 (상단 메뉴 파일 내)

### 운영 설정 3종 (script 상단) — 일상 관리는 여기만
```javascript
// ① 분류번호별 뱃지
var BADGE_MAP = {
  '468': 'NEW',        // Samsung
  '474': 'NEW',        // Z 시리즈
  '458': 'NEW', '459': 'NEW', '460': 'NEW',   // Flip8/Fold8/Ultra
  '394': 'NEW',        // S26
  '349': 'NEW',        // 아이폰 17
  '388': 'Signature',  // PRSM (SHOP)
  '450': 'SALE',       // 방수팩 (할인 ~9/1, 종료 시 제거!)
  '485': 'NEW', '486': 'NEW',   // Impression, Monoline
  '489': 'HOT', '492': 'HOT'    // Sanrio, Pokémon (세부 항목 쪽)
};
// ② 최상위 메뉴 뱃지 (메뉴 글자 매칭)
var MENU_BADGE = { 'SHOWROOM': 'Click Here!' };
// ③ COLLECTION 기본 펼침 (applyCollection 안)
var OPEN_BY_DEFAULT = ['473', '488', '491'];  // SLBS+Sanrio+Pokémon
```

### 함수 구성
- `getCateNo(a)`: href에서 분류번호 추출 (/465/ 와 ?cate_no= 둘 다)
- `addNewBadge(el, no)`: BADGE_MAP 참조해 뱃지 span 부착
- `makeSubOl(kids)` / `attachToggle(li, subOl)`: 접이식 목록·± 토글 생성
- `apply(subMap)`: PC SHOP 재조립 (465 트리, 2차 strong 승격+3차 목록+4차 토글, 전체 뱃지 후처리)
- `applyMobile(subMap)`: 모바일 SHOP 동일 처리
- `applyCollection(subMap)`: **텍스트 매칭 방식** — 메뉴 글자가 정확히 'COLLECTION'인 li만 찾아 처리 (`.ul--new` 무차별 선택 금지! 모바일 중고폰이 같은 클래스라 침범 사고 있었음). 472 트리로 그룹+세부 조립, list.html 링크
- `menuBadgeLoop`: MENU_BADGE 적용, 0.5초×10회 재시도 (splt 애니메이션 대비)
- `$.ajax` success: 분류명 표시(slbs-cate-name 채움) → subMap 구성 → tryApply (doneP/doneM/doneC 각각 완료까지 0.3초×20회)

### CSS 요점 (style 블록)
- SHOP: 2차 strong block, 2단 분할(column-count:2, data-patched 한정), ALL PRODUCT 제목 column-span
- COLLECTION: 그룹 볼드, slbs-sub 접이식, 2단 분할 + **모바일 1단** (`@media (max-width:1024px)`)
- 모바일: --h 고정높이 무력화, 인라인 정렬(!important), 한글 keep-all 줄바꿈, 서브 0.88em
- 뱃지: `.slbs-new` 전역(빨강 #ff2200, 9px, 위첨자), SHOWROOM 뱃지 PC 숨김(`.navigation__category > ul > li > .slbs-new { display:none }`)
- PRSM(388) 볼드, `:has()` 모바일 중고폰 숨김 CSS는 잔존하나 무의미(HTML 주석이 실제 처리)

## 5. 중고폰 숨김/복구 방법

숨김 위치 (둘 다 주석 처리, 날짜 표기됨):
1. 상단 메뉴 파일: `<!-- REFURBISH: 메뉴 숨김 2026-07-29 ... -->` (PC GNB 블록, a 태그 온전)
2. 슬라이딩 파일: `<!-- REFURBISHED: 모바일 메뉴 숨김 2026-07-30 ... -->` (li#refur-menu-mobile)

**복구**: 두 파일에서 여는/닫는 주석 표시만 제거. 링크 참고: PC는 event-re-all.html, 모바일은 event-refurbishALL.html (이원화 상태 그대로)

## 6. 일상 운영 가이드

- **분류 추가/삭제/순서**: 관리자 상품분류 관리에서만. 메뉴 자동 반영 (SHOP·COLLECTION 모두)
- **신규 IP 콜라보**: 472 아래 그룹 분류 생성 → 상품에 기종 분류+IP 분류 동시 지정 → 끝
- **뱃지**: BADGE_MAP에 번호:단어 추가/제거. 신기종 출시 시 추가, 철 지나면 **제거 잊지 말 것** (SALE은 할인 종료와 동기화)
- **번호 확인**: 관리자 분류 클릭 → 분류URL 숫자, 또는 콘솔 `$.get('/exec/front/Product/SubCategory', function(d){...})`

## 7. 잔여 과제

1. **Pokémon 등 그룹 분류 페이지 상품 미노출** — list.html?cate_no=491 접속 시 상품 확인 필요. 그룹 분류(직접 상품 0)의 "하위분류 상품진열: 진열함" 설정 점검
2. **[CUSTOM] Fold6 상품** — ALL PRODUCT 앞쪽 노출. CUSTOM 오픈 전까지 진열안함 권장 (미처리)
3. **슬라이딩 파일 SHOP 링크** — cate_no=57→465 교체 지시했으나 최종 검증 안 됨
4. **CUSTOM 메뉴** — 여전히 coming-soon.html. 오픈 시 링크 교체
5. **메인 KV 중고폰 배너** — 메뉴에서 뺐으니 배너 유지 여부 판단 필요
6. COLLECTION 대문(collection.html)은 공들인 기획 페이지라 **유지 확정** — 새 472 구조 반영해 내용 갱신은 별도 과제
7. 죽은 참조·COLLECTION 옛 주석 잔재 등 소소한 정리

## 8. 작업 수칙 (사고 사례 기반)

1. **수정 전 파일 전체 로컬 백업** (날짜 붙여서). 최종 백업 대상: 상단 메뉴 + 슬라이딩 두 파일
2. **CSS는 반드시 `<style>`~`</style>` 안** — script 안에 넣으면 `SyntaxError: Private field '#...'` 등으로 패치 전체 사망 (3회 발생한 사고)
3. **객체 항목 쉼표**: 마지막 항목만 쉼표 없음. `Unexpected string` 에러 = 쉼표 누락
4. **HTML 주석 중첩 금지** — 감싸기 전에 안쪽 기존 주석 제거
5. `module=`, `{$...}`, `<!--@...-->`는 Cafe24 문법 — 수정 금지
6. **확인은 항상 시크릿 창 + Ctrl+Shift+R**. 반영 안 보이면: Ctrl+U 소스에서 고유 문자열 검색 → 0/0이면 저장/스킨/캐시 순 의심. 캐시 시차로 몇 분 걸리는 경우 있었음
7. **같은 파일 사본이 여러 곳** (편집창 탭, 로컬, 대화) — 저장 직후 편집창 내용이 기준본
8. attachToggle 등 호출 중복 주의 (복붙 시 두 번 들어가 ± 두 개 사고 있었음)
9. Claude 대화로 코드 주고받을 때: **텍스트 문서 첨부는 자주 빈 내용으로 도착** → .html 파일 업로드 또는 채팅창 직접 붙여넣기 사용

## 9. 참고: 설치 확인된 마케팅/앱 (콘솔 로그 기반)

Facebook Pixel, GA Booster v4.3(GA4 연동), AlphaReview(CDP), 알파푸시, ekiki/adkiki, 채널톡, 네이버/구글 사이트 인증. 온라인래플 앱은 도메인 사망(ERR_NAME_NOT_RESOLVED) — 미사용 시 앱 삭제 권장. ※상세 광고 툴링 현황은 별도 문서(SLBS_광고툴링_작업지시서_v4) 참조
