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
ReSLBS 페이지도 동일 (2026-07-31부터 순서 변경 없음 — 아래 "DOM 순서 변경 금지" 참고)
```

> PC는 CUSTOM과 BRAND 사이, 모바일은 BRAND 뒤입니다. 원본 마크업 위치를 그대로 살린
> 결과이며, 통일하려면 `sidebar.html` 의 `li#refur-menu-mobile` 위치를 마크업에서
> 옮기면 됩니다. **JS로 옮기지 마세요.**

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

### 🚫 GNB 최상위 `<li>` 를 JS로 옮기지 말 것

외주 스킨 코드(`header.js` / `nav.js` / `slide_menu.js`, **수정 금지**)가 메뉴와 드롭다운
패널을 **DOM 순서로 묶습니다.** `insertBefore` 등으로 최상위 `<li>` 를 옮기면 두 가지가
동시에 깨집니다.

1. `header.js` 의 `make()` 가 **첫 `.ul--top-navigation` 하나만** 재조립 → 순서가 바뀌면
   엉뚱한 메뉴를 집어가고 SHOP 메가메뉴가 통째로 죽음
2. hover 패널 인덱스가 한 칸씩 밀림 → **중고폰에 마우스를 올렸는데 SHOP 드롭다운이 뜸**

2026-07-29~31 사이 ReSLBS 페이지에서 중고폰을 SHOP 앞으로 옮기는 기능이 있었고,
위 두 증상이 그대로 재현되어 **2026-07-31 제거**했습니다. 되살리지 마세요.

메뉴 순서를 바꿔야 하면 **마크업에서 `<li>` 위치를 옮기거나**, 페이지별로 달라야 하면
**CSS(flex `order`)** 로 처리하세요. DOM 이동은 안 됩니다.

### ⚠️ 클래스 충돌 — 최상위 메뉴에 `ul--top-navigation` / `main-item` 금지

**증상**: ReSLBS 페이지에서만 SHOP 메가메뉴가 평면으로 나옴 (3·4차 미전개, 뱃지 없음).
일반 페이지는 정상.

**원인**: 외주 코드 `header.js` 의 `make()` 가 `.ul--top-navigation` 을 문서 전체에서 찾아
**첫 매칭 하나만** 재조립한다. 중고폰 메뉴가 SHOP 과 같은 클래스를 쓰고 있었고,
ReSLBS 페이지에서 그 메뉴가 SHOP **앞으로 이동**하면서 첫 매칭이 뒤바뀌었다.
→ `make()` 가 중고폰 메뉴를 처리 → SHOP 에 `.main-item` 이 생기지 않음
→ 그 위에 얹히는 `apply()` 도 통째로 무력화.

**확인 방법** (콘솔):

```js
[...document.querySelectorAll('.navigation__category .main-item')]
  .map(m => m.closest('.navigation__category > ul > li').querySelector('a').textContent.trim())
// 정상: ["SHOP", "COLLECTION", ...]   /  고장: SHOP 이 빠져 있음
```

**규칙**: GNB 최상위 메뉴의 서브 `<ul>` 에는 `ul--top-navigation`(SHOP 전용) 과
`ul--new`(COLLECTION 전용) 를 쓰지 말 것. 일반 메뉴는 BRAND 처럼 **클래스 없는 `<ul>`** 을 쓴다.
`main-item` 도 `make()`/`apply()` 가 만드는 것이므로 손으로 넣지 않는다.

> 핸드오프 문서 90행의 `.ul--new` 침범 사고와 **같은 패턴**이다.
> 기존 ReSLBS 스크립트가 메뉴를 `createElement` 로 새로 만들면서 클래스 없는 `<ul>` 을
> 쓴 것도 이 때문으로 보인다.

### 알려진 이슈

- **PC/모바일 중고폰 링크 이원화** — PC `event-re-all.html` / 모바일 `event-refurbishALL.html`.
  이 때문에 `[href*="event-re-all"]` 셀렉터는 모바일에서 절대 매칭되지 않습니다.
  통일하는 게 맞지만 현재는 이원화 상태 그대로 두고 셀렉터 쪽에서 흡수했습니다.
- `docs/SLBS_GNB_핸드오프_v2.md` 는 2026-07-30 시점 문서입니다. 5장(중고폰 숨김/복구)과
  `[SLBS PATCH ReSLBS]` 블록 설명이 현재 코드와 어긋나므로, 복구 완료 후 갱신 필요.

---

## 배포

편집창·웹FTP를 쓰지 않습니다. **Git 이 원본이고, SFTP 로 밀어넣습니다.**

### 경로

```
로컬  layout/basic/navigation.html
원격  <REMOTE_PATH>/layout/basic/navigation.html
      예) /sde_design/skin14/layout/basic/navigation.html
```

`skin14` 는 SLBS 의 `SKIN_CODE`. 스킨을 바꾸면 이 번호도 바뀝니다.

### ① VS Code 에서 (일상 작업)

1. 확장 `SFTP` (게시자 **Natizyskunk**) 설치
2. `.vscode/sftp.json.example` → `sftp.json` 으로 복사 후 `host` / `username` / `remotePath` 채움
3. 파일 저장 → 자동 업로드

`sftp.json` 은 `.gitignore` 에 걸려 있어 커밋되지 않습니다. 비밀번호는 파일에 두지 말고
`promptForPassword` 를 쓰세요.

### ② GitHub Actions 에서 (자동 배포)

`main` 브랜치의 `layout/**` 이 바뀌면 자동 배포됩니다.
저장소 Settings › Secrets and variables › Actions 에 4개를 등록해야 합니다.

| Secret | 값 |
|---|---|
| `CAFE24_FTP_HOST` | `쇼핑몰아이디.cafe24.com` |
| `CAFE24_FTP_USER` | FTP 아이디 |
| `CAFE24_FTP_PASS` | FTP 비밀번호 |
| `CAFE24_REMOTE_PATH` | `/sde_design/skin14` |

> GitHub 러너는 해외 IP입니다. 쇼핑몰 관리자 › 운영 보안 관리 › IP 접속 제한 설정의
> **FTP 접속 지역**이 "국내+해외 접속 허용"이어야 동작합니다. 국내로 조이려면
> Actions 대신 VS Code(①)나 국내 고정 IP self-hosted runner 를 쓰세요.

### ③ 롤백

파일 덮어쓰기가 아니라 **커밋 되돌리기**입니다.

```bash
# 방법 1 — 되돌리는 커밋을 새로 쌓기 (이력 보존, 권장)
git revert <망친 커밋>
git push          # → 자동 배포

# 방법 2 — 특정 파일만 이전 상태로
git checkout <좋았던 커밋> -- layout/basic/navigation.html
git commit -m "Roll back navigation.html"
git push
```

**방법 3 — 배포만 되돌리기 (커밋 없이):**
Actions 탭 → `Deploy skin to Cafe24` → `Run workflow` → `ref` 에 되돌릴 커밋 SHA 입력.
그 시점 파일이 그대로 다시 올라갑니다.

`backup/` 폴더의 스냅샷을 편집창에 붙여넣는 수동 복구도 여전히 유효합니다.

### ④ 검증

배포 전에 `tools/validate_skin.py` 가 자동으로 돌며, 실패하면 업로드하지 않습니다.
로컬에서도 같은 걸 돌릴 수 있습니다.

```bash
python3 tools/validate_skin.py layout/basic/*.html
```

검사 항목은 이 저장소에서 실제로 겪은 사고들입니다 — `<script>` 문법 오류, HTML 주석 짝,
`<li>` 짝, CSS 가 `<script>` 안에 들어간 경우, GNB 메뉴 클래스 충돌.

### ⑤ 배포 후

시크릿 창 + **Ctrl+Shift+R**. 캐시 시차로 몇 분 걸릴 수 있습니다.
반영이 안 보이면 `Ctrl+U` 소스에서 고유 문자열 검색 → 0건이면 경로/스킨번호/캐시 순으로 의심.

> ⚠️ **편집창에서 직접 고치지 마세요.** 다음 배포 때 Git 내용으로 덮어써집니다.
> 급해서 편집창에서 고쳤다면, 그 내용을 반드시 저장소에도 반영하세요.

## 편집 시 주의 (사고 이력 기반)

- CSS는 반드시 `<style>`~`</style>` 안에. `<script>` 안에 넣으면 패치 전체가 죽습니다 (3회 발생)
- HTML 주석 중첩 금지. 감싸기 전에 안쪽 기존 주석을 먼저 제거
- `module=`, `{$...}`, `<!--@...-->` 는 Cafe24 문법이므로 수정 금지
- `/slbs/assets/js/header.js` 는 외주 코드, 수정 금지
- 같은 파일 사본이 여러 곳(편집창·로컬·대화)에 생기므로, **저장 직후 편집창 내용이 기준본**

자세한 내용은 `docs/SLBS_GNB_핸드오프_v2.md` 8장 참고.
