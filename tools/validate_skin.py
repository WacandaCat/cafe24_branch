#!/usr/bin/env python3
"""Cafe24 스킨 파일 사전 검증.

배포 전에 깨진 파일이 실서버로 나가는 것을 막는다.
이 저장소에서 실제로 겪은 사고들을 그대로 검사 항목으로 옮겼다.

  - <script> 블록 JS 문법 오류 (괄호 짝, DOMContentLoaded 줄 실종 등)
  - HTML 주석 짝 불일치 (숨김 주석 해제하다 여는/닫는 표시가 어긋남)
  - <li> 태그 짝 불일치
  - CSS 가 <script> 안에 들어간 경우 (핸드오프 문서 8장 2번, 3회 발생)
  - GNB 최상위 메뉴의 클래스 충돌 (ul--top-navigation / ul--new 중복 사용)

사용: python3 tools/validate_skin.py layout/basic/*.html
종료코드 0 = 통과, 1 = 실패
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

# SHOP / COLLECTION 메가메뉴 전용 클래스. 다른 최상위 메뉴가 쓰면 header.js 의
# make() 가 엉뚱한 메뉴를 재조립해 메가메뉴가 통째로 죽는다. README 참고.
RESERVED_MENU_CLASSES = ("ul--top-navigation", "ul--new")


def check_js(src, errors):
    """<script> 블록마다 node --check 로 문법 검사."""
    if not src.strip():
        return
    blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", src, re.S)
    for i, block in enumerate(blocks, 1):
        if not block.strip():
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as fh:
            fh.write(block)
            tmp = fh.name
        try:
            r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            if r.returncode != 0:
                detail = r.stderr.strip().replace(tmp, f"<script> #{i}")
                errors.append(f"script #{i} 문법 오류\n{detail}")
        finally:
            Path(tmp).unlink(missing_ok=True)

        # CSS 가 script 안에 들어간 경우 — node 는 통과시킬 수도 있어 따로 본다
        if re.search(r"^\s*[.#@][\w-]+[^\n{]*\{", block, re.M):
            errors.append(
                f"script #{i} 안에 CSS 로 보이는 코드가 있음. "
                "CSS 는 반드시 <style>~</style> 안에 둘 것"
            )


def check_comment_balance(src, errors):
    opened, closed = src.count("<!--"), src.count("-->")
    if opened != closed:
        errors.append(f"HTML 주석 짝 불일치: <!-- {opened}개 / --> {closed}개")


def strip_comments(src):
    return re.sub(r"<!--.*?-->", "", src, flags=re.S)


def strip_code_blocks(src):
    """<script>/<style> 내용 제거. JS 주석 안의 <li> 같은 게 태그로 세어지는 걸 막는다."""
    src = re.sub(r"<script[^>]*>.*?</script>", "", src, flags=re.S)
    return re.sub(r"<style[^>]*>.*?</style>", "", src, flags=re.S)


def check_li_balance(src, errors):
    body = strip_comments(strip_code_blocks(src))
    opened = len(re.findall(r"<li[\s>]", body))
    closed = body.count("</li>")
    if opened != closed:
        errors.append(f"<li> 태그 짝 불일치: <li> {opened}개 / </li> {closed}개")


def check_menu_class_collision(src, errors):
    """GNB 최상위 <li> 들이 예약 클래스를 중복해서 쓰는지 본다."""
    body = strip_comments(src)
    if "navigation__category" not in body:
        return
    try:
        gnb = body.split('<div class="navigation__category">', 1)[1]
        gnb = gnb.split('<div class="site-info', 1)[0]
    except IndexError:
        return

    for cls in RESERVED_MENU_CLASSES:
        owners = [
            m.group(1).strip()
            for m in re.finditer(
                r"<li[^>]*>\s*(?:<i[^>]*></i>\s*)?<a[^>]*>([^<]+)</a>\s*<ul[^>]*\b"
                + re.escape(cls)
                + r"\b",
                gnb,
            )
        ]
        if len(owners) > 1:
            errors.append(
                f"클래스 '{cls}' 를 최상위 메뉴 {len(owners)}개가 함께 사용: {owners}. "
                "header.js 의 make() 가 첫 매칭 하나만 재조립하므로 메가메뉴가 죽는다. "
                "일반 메뉴는 클래스 없는 <ul> 을 쓸 것 (README 참고)"
            )


def validate(path):
    src = Path(path).read_text(encoding="utf-8")
    errors = []
    check_comment_balance(src, errors)
    check_li_balance(src, errors)
    check_js(src, errors)
    check_menu_class_collision(src, errors)
    return errors


def main(argv):
    targets = [Path(p) for p in argv[1:]]
    if not targets:
        print("사용법: python3 tools/validate_skin.py <파일...>", file=sys.stderr)
        return 2

    failed = 0
    for path in targets:
        if not path.is_file():
            print(f"✗ {path} — 파일 없음")
            failed += 1
            continue
        errors = validate(path)
        if errors:
            failed += 1
            print(f"✗ {path}")
            for e in errors:
                print(f"    - {e}")
        else:
            print(f"✓ {path}")

    if failed:
        print(f"\n{failed}개 파일에서 문제 발견. 배포를 중단한다.")
        return 1
    print(f"\n{len(targets)}개 파일 모두 통과.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
