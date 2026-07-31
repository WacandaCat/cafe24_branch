# cafe24_branch

**slbs.shop (Cafe24 스마트디자인) 소스 보관소.**

Cafe24 스마트디자인은 Git/API를 지원하지 않습니다. 편집창 저장 = 즉시 실서버 배포이며,
되돌리기 기능도 없습니다. 이 저장소는 그 편집창 내용을 **수동으로 미러링**해 변경 이력과
복구 지점을 남기기 위한 곳입니다.

> ⚠️ **이 저장소에 push해도 slbs.shop에는 아무 일도 일어나지 않습니다.**
> 반영은 항상 Cafe24 편집창에 직접 붙여넣어야 합니다. 아래 "반영 절차" 참고.

---

## 디렉터리 구조

```
layout/basic/          Cafe24 레이아웃 파일 (편집창에 붙여넣을 최신본)
docs/                  인계·작업 문서
backup/YYYY-MM-DD/     수정 전 원본 스냅샷 (복구용)
```

## 파일 지도

| 저장소 경로 | Cafe24 편집창 표시명 | 역할 |
|---|---|---|
| `layout/basic/layout.html` | 공통 레이아웃 | `@import`로 조각 로드. 패치 없음 |
| `layout/basic/navigation.html` | 레이아웃 (상단 메뉴) | PC GNB + `[SLBS PATCH]` 전체 (유일본) |
| `layout/basic/sidebar.html` | 레이아웃 (슬라이딩) | 모바일 햄버거 메뉴 (`<aside id="aside">`) |
| `docs/SLBS_GNB_핸드오프_v2.md` | — | GNB 개편 인계 문서 (2026-07-30 작성) |

`layout.html` 이 실제로 불러오는 조각은 다음과 같습니다. 파일명 확정의 근거입니다.

```html
<!--@import(/layout/basic/top_roll.html)-->
<!--@import(/layout/basic/state_login.html)-->
<!--@import(/layout/basic/navigation.html)-->   ← 상단 메뉴 (PC GNB + SLBS PATCH)
<!--@import(/layout/basic/sidebar.html)-->      ← 모바일 슬라이딩 메뉴
<!--@import(/layout/basic/footer.html)-->
```

> 📌 **핸드오프 문서 53행 정정**: 슬라이딩 파일을 `/layout/basic/menu.html` 로 기재하고 있으나,
> `menu.html` 은 `layout.html` 어디에서도 import되지 않습니다. 실제 파일은 `sidebar.html` 입니다.
> `[SLBS PATCH]` 가 쓰는 셀렉터가 `#aside li.menu`, `.ul--side-navigation` 인 것과도 일치합니다.
> (같은 표 52행의 `navigation.html` 은 "추정" 표기였으나 import 목록으로 확정되었습니다.)

---

## 현재 상태 (2026-07-31)

### 진행 중: 중고폰 GNB 복구

2026-07-29~30에 숨김 처리했던 중고폰 메뉴를 다시 노출하는 작업입니다.
숨김이 **PC/모바일 두 파일에 각각** 걸려 있어 양쪽 다 손봐야 합니다.

| 파일 | 작업 | 상태 |
|---|---|---|
| `layout/basic/navigation.html` | 주석 해제 + ReSLBS 스크립트 수정 | ✅ 완료 (**미배포**) |
| `layout/basic/sidebar.html` | `REFURBISHED: 모바일 메뉴 숨김` 주석 해제 | ✅ 완료 (**미배포**) |

> ⚠️ 두 파일 모두 **아직 실서버에 반영되지 않은 상태**입니다.
> 현재 slbs.shop에 올라가 있는 것은 `backup/2026-07-31/` 쪽입니다.
> 배포 후 이 문단을 갱신하세요.

복구 후 메뉴 구성:

```
PC:     SHOP · COLLECTION · SHOWROOM · CUSTOM · 중고폰 · BRAND
모바일:  SHOWROOM · SHOP · COLLECTION · CUSTOM · BRAND · 중고폰
ReSLBS 페이지: 중고폰이 SHOP 앞으로 이동 (PC/모바일 공통)
```

> PC는 CUSTOM과 BRAND 사이, 모바일은 BRAND 뒤입니다. 원본 마크업 위치를 그대로 살린
> 결과이며, 통일하려면 `sidebar.html` 의 `li#refur-menu-mobile` 을 CUSTOM `<li>` 뒤로
> 옮기면 됩니다.

### sidebar.html 변경 내역 (원본 대비 1건)

- `<!-- REFURBISHED: 모바일 메뉴 숨김 2026-07-30 ... -->` 주석 해제 (편집창 147·151행)
- 152~155행의 `REFURBISHED BUY` 주석은 별개 건이므로 **그대로 유지**

### navigation.html 변경 내역 (원본 대비 3건)

1. **PC GNB 주석 해제** — `<!-- REFURBISH: 메뉴 숨김 2026-07-29 ... -->` 제거.
   GNB가 `SHOP · COLLECTION · SHOWROOM · CUSTOM · 중고폰 · BRAND` 가 됩니다.
2. **무의미한 CSS 제거** — `#aside li.menu:has(> a[href*="event-re-all"])` 숨김 규칙.
   모바일 링크가 `event-refurbishALL.html` 이라 애초에 매칭되지 않던 죽은 규칙입니다.
3. **ReSLBS 스크립트 수정** — 중고폰 메뉴를 `createElement`로 **새로 만들던 것**을
   레이아웃의 `<li>`를 **찾아서 이동**시키는 방식으로 변경. ①로 마크업이 살아났기 때문에
   그대로 두면 ReSLBS 페이지에서 메뉴가 2개로 중복됩니다.
   모바일 셀렉터도 `li#refur-menu-mobile` 우선으로 교체(링크 이원화 대응).

### 알려진 이슈

- **PC/모바일 중고폰 링크 이원화** — PC `event-re-all.html` / 모바일 `event-refurbishALL.html`.
  이 때문에 `[href*="event-re-all"]` 셀렉터는 모바일에서 절대 매칭되지 않습니다.
  통일하는 게 맞지만 현재는 이원화 상태 그대로 두고 셀렉터 쪽에서 흡수했습니다.
- `docs/SLBS_GNB_핸드오프_v2.md` 는 2026-07-30 시점 문서입니다. 5장(중고폰 숨김/복구)과
  `[SLBS PATCH ReSLBS]` 블록 설명이 현재 코드와 어긋나므로, 복구 완료 후 갱신 필요.

---

## 반영 절차

1. **백업 먼저.** 편집창의 현재 내용을 통째로 복사해 `backup/YYYY-MM-DD/` 에 저장하고 커밋
2. `layout/basic/` 의 해당 파일 내용을 **전체 선택 → 편집창에 통째 교체**
   (라인 단위 부분 편집은 괄호·주석이 깨지기 쉬움)
3. 저장 후 **시크릿 창 + Ctrl+Shift+R** 로 확인. 캐시 시차로 몇 분 걸릴 수 있음
4. 반영 안 보이면 `Ctrl+U` 소스에서 고유 문자열 검색 → 0건이면 저장/스킨/캐시 순으로 의심

## 편집 시 주의 (사고 이력 기반)

- CSS는 반드시 `<style>`~`</style>` 안에. `<script>` 안에 넣으면 패치 전체가 죽습니다 (3회 발생)
- HTML 주석 중첩 금지. 감싸기 전에 안쪽 기존 주석을 먼저 제거
- `module=`, `{$...}`, `<!--@...-->` 는 Cafe24 문법이므로 수정 금지
- `/slbs/assets/js/header.js` 는 외주 코드, 수정 금지
- 같은 파일 사본이 여러 곳(편집창·로컬·대화)에 생기므로, **저장 직후 편집창 내용이 기준본**

자세한 내용은 `docs/SLBS_GNB_핸드오프_v2.md` 8장 참고.
