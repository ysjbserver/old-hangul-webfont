# old-hangul-webfont

Small woff2 webfonts for displaying **Old Hangul** (옛한글), made by subsetting
[Noto Sans CJK KR / Noto Serif CJK KR](https://github.com/notofonts/noto-cjk).

> This is an **unofficial** subset based on Noto CJK.
> It is not affiliated with or endorsed by Google, Adobe, or the Noto project.

[한국어 설명은 아래에 있습니다.](#한국어)

## Why

Old Hangul syllables can only be written as sequences of conjoining jamo
(e.g. U+1112 U+119E U+11AB), and they display correctly only when the font
composes them with OpenType features (`ljmo`, `vjmo`, `tjmo`, `ccmp`).
Many systems have no such font by default, and Safari does not let web pages
use fonts the user installed.

This project was started for [Korean Wikisource](https://ko.wikisource.org/),
with the goal of providing these fonts through the MediaWiki
[UniversalLanguageSelector](https://www.mediawiki.org/wiki/Universal_Language_Selector/WebFonts)
webfonts feature. The full Noto CJK fonts are 16–25 MB each, which is too
large for a webfont, so only the Hangul part is kept.

## Files

| File | Size |
|---|---|
| `fonts/NotoSansCJKKROldHangul-Regular.woff2` | 597 KB |
| `fonts/NotoSansCJKKROldHangul-Bold.woff2` | 621 KB |
| `fonts/NotoSerifCJKKROldHangul-Regular.woff2` | 1095 KB |
| `fonts/NotoSerifCJKKROldHangul-Bold.woff2` | 1189 KB |

SHA-256 checksums are in [`fonts/SHA256SUMS`](fonts/SHA256SUMS).

### Character coverage (11,626 characters, 13,483 glyphs)

| Range | Contents |
|---|---|
| U+1100–11FF | Hangul Jamo |
| U+302E–302F | Hangul tone marks |
| U+3131–318E | Hangul Compatibility Jamo |
| U+A960–A97F | Hangul Jamo Extended-A |
| U+AC00–D7A3 | Hangul Syllables |
| U+D7B0–D7FF | Hangul Jamo Extended-B |
| U+25CC | Dotted circle |

The precomposed syllables (U+AC00–D7A3) are included on purpose.
MediaWiki stores text in Unicode NFC, which turns U+1100 U+1161 U+11EB into
U+AC00 U+11EB. Both characters must come from the same font to compose;
without the syllables, such text is split into two cells.

## Changes from upstream

| | Upstream | This subset |
|---|---|---|
| Source | Noto Sans CJK KR 2.004 (`Sans2.004` tag), Noto Serif CJK KR 2.003 (`Serif2.003` tag) | — |
| Glyphs | 65,535 | 13,483 (outlines unchanged) |
| OpenType features | all | `ccmp`, `locl`, `ljmo`, `vjmo`, `tjmo`, `calt`, `liga` |
| Scripts in GSUB/GPOS | all | `DFLT`, `hang` |
| Hinting | yes | removed |
| CFF subroutines | yes | flattened (better woff2 compression) |
| Family name | Noto Sans/Serif CJK KR | Noto Sans/Serif CJK KR Old Hangul |
| Format | OTF | woff2 |

Removing hinting may make small text look slightly softer on Windows.

## Build

Requires Python 3.

```sh
pip install -r requirements.txt
python build.py
```

`build.py` downloads the upstream OTF files into `sources/`, checks their
SHA-256, and writes the woff2 files and `SHA256SUMS` to `fonts/`.
The build is reproducible: running it again gives byte-identical files,
so `git status` should show no changes in `fonts/` after a rebuild.

## Test

Open [`test/index.html`](test/index.html) through a web server
(browsers block webfonts on `file://` pages):

```sh
python -m http.server 8765
```

Then visit <http://localhost:8765/test/>. Each case shows ✓ when every
syllable is one cell wide. The page also has a box for trying your own text.

Tested on Chrome (Windows): all cases compose the same way as the original
fonts. Safari and Firefox have not been tested yet.

## License

- Fonts (`fonts/*.woff2`): [SIL Open Font License 1.1](fonts/OFL.txt),
  the same license as the upstream fonts.
  Noto is a trademark of Google Inc.
- Everything else (script, test page, documentation):
  [CC0 1.0 Universal](LICENSE).

---

## 한국어

[Noto Sans CJK KR / Noto Serif CJK KR](https://github.com/notofonts/noto-cjk)에서
**옛한글** 표시에 필요한 부분만 남겨 만든 woff2 웹폰트입니다.

> Noto CJK를 바탕으로 만든 **비공식** 서브셋이며,
> Google, Adobe, Noto 프로젝트와는 관계가 없습니다.

### 만든 이유

옛한글 음절은 첫가끝 자모를 이어 적는 방식(예: U+1112 U+119E U+11AB)으로만
쓸 수 있고, 이 자모들을 한 덩어리로 모아 주는 글꼴이 있어야 제대로 보입니다.
이런 글꼴이 기본으로 없는 환경이 많고, Safari는 사용자가 설치한 글꼴을
웹페이지에서 쓰지 못하게 막습니다.

[한국어 위키문헌](https://ko.wikisource.org/)에서 미디어위키
[ULS 웹폰트 기능](https://www.mediawiki.org/wiki/Universal_Language_Selector/WebFonts)으로
제공하는 것을 목표로 만들었습니다. 원본 글꼴은 파일 하나가 16~25MB라서
한글 부분만 남겼습니다.

### 완성형 음절을 넣은 이유

미디어위키는 문서를 NFC로 정규화해 저장합니다. 그래서 'ᄀ+ᅡ+ᇫ'는
'가+ᇫ'로 저장됩니다. 두 글자가 같은 글꼴에서 나와야 한 덩어리로 모이므로,
완성형 음절(U+AC00–D7A3)도 함께 넣었습니다.

### 원본과 달라진 점

- 글리프 65,535개 → 13,483개 (남긴 글리프의 모양은 원본 그대로)
- 조합 규칙: 한글 조합에 필요한 7개만 남김
- 힌팅 제거 (Windows에서 작은 글씨가 조금 흐리게 보일 수 있음)
- CFF 서브루틴 풀기 (모양은 같고 압축이 잘 되게 함)
- 이름에 "Old Hangul"을 붙임
- OTF → woff2

### 만들기와 시험

```sh
pip install -r requirements.txt
python build.py
python -m http.server 8765
```

그다음 <http://localhost:8765/test/>를 엽니다. 음절마다 한 칸 폭이면 ✓가 표시됩니다.
다시 만들어도 결과 파일이 한 바이트도 다르지 않으므로, 다시 만든 뒤
`git status`에 `fonts/` 변경이 없으면 공개된 파일이 이 스크립트로 만든 것임을 확인할 수 있습니다.

### 라이선스

- 글꼴(`fonts/*.woff2`): 원본과 같은 [SIL Open Font License 1.1](fonts/OFL.txt)
- 그 밖의 모든 것(스크립트, 시험 페이지, 문서): [CC0 1.0](LICENSE)
