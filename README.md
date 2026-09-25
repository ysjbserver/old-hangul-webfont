# old-hangul-webfont

Small woff2 webfonts for displaying **Old Hangul** (옛한글), made by subsetting
[Noto Sans CJK KR / Noto Serif CJK KR](https://github.com/notofonts/noto-cjk).

> This is an unofficial subset based on Noto CJK.
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
| `fonts/NotoSansCJKKROldHangul-Regular.woff2` | 598 KB |
| `fonts/NotoSansCJKKROldHangul-Bold.woff2` | 622 KB |
| `fonts/NotoSerifCJKKROldHangul-Regular.woff2` | 1095 KB |
| `fonts/NotoSerifCJKKROldHangul-Bold.woff2` | 1190 KB |

SHA-256 checksums are in [`fonts/SHA256SUMS`](fonts/SHA256SUMS).

### Character coverage (11,626 characters, 13,485 glyphs)

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
| Glyphs | 65,535 | 13,485 (outlines unchanged) |
| OpenType features | all | `ccmp`, `ljmo`, `vjmo`, `tjmo`, `vert`, `vrt2` (see below) |
| Scripts in GSUB/GPOS | all | `DFLT`, `hang` |
| Hinting | yes | removed |
| CFF subroutines | yes | flattened (better woff2 compression) |
| Family name | Noto Sans/Serif CJK KR | Noto Sans/Serif CJK KR Old Hangul |
| Format | OTF | woff2 |

Removing hinting may make small text look slightly softer on Windows.

### OpenType features kept

Only features that have rules for the kept glyphs remain.
The numbers are the same in all four fonts.

| Feature | What it does | Size |
|---|---|---|
| `ccmp` | Replaces a jamo sequence with one pre-drawn glyph: 500 frequent Old Hangul syllables (134 initial+medial, 366 initial+medial+final) and 121 compound jamo written as 2–3 jamo (34 initials, 28 medials, 59 finals; e.g. U+1100 U+1103) | 621 ligatures |
| `ljmo` | Picks the initial consonant shape that fits the following vowel and final | 744 glyphs |
| `vjmo` | Picks the vowel shape (zero width, drawn over the initial's cell) | 189 glyphs |
| `tjmo` | Picks the final consonant shape (zero width) | 548 glyphs |
| `vert`, `vrt2` | Vertical forms of the two tone marks (U+302E, U+302F), plus their vertical positioning (GPOS `vert`). Without them, a tone mark takes a cell of its own in vertical text | 2 glyphs |

`ccmp` is applied first. When there is no pre-drawn glyph, `ljmo`, `vjmo` and
`tjmo` pick a piece for each jamo and draw them in one cell.

`locl`, `calt`, `liga` and the other GPOS features (kerning etc.) apply only
to non-Hangul glyphs in the upstream fonts, so nothing of them remains.

Note: compound initials written as two jamo (e.g. U+1102 U+1109) do not
compose in Chrome even with the upstream font. Use the dedicated code point instead (U+115B).

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
syllable is one cell wide. The vertical writing section shows ✓ when a
syllable with a tone mark is one cell tall. The page also has a box for
trying your own text.

Tested on Chrome (Windows): all cases, including vertical writing, lay out the
same way as the original fonts. Safari and Firefox have not been tested yet.

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

> Noto CJK를 바탕으로 만든 비공식 서브셋이며,
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

미디어위키는 문서를 유니코드 정규화 형태 C(NFC)로 정규화해 저장합니다.
예를 들어, 'ᄀ+ᅡ+ᇫ'는 '가+ᇫ'로 저장됩니다.
두 글자가 같은 글꼴에서 나와야 한 덩어리로 모이므로 (서로 글꼴이 다르면 합쳐지지 않음), 완성형 음절(U+AC00–D7A3)도 함께 넣었습니다.

### 원본과 달라진 점

- 글리프 65,535개 → 13,485개 (남긴 글리프의 모양은 원본 그대로)
- 조합 규칙: 남긴 글자에 쓰이는 6개만 남김 (아래 참고)
- 힌팅 제거 (Windows에서 작은 글씨가 조금 흐리게 보일 수 있음)
- CFF 서브루틴 풀기 (모양은 같고 압축이 잘 되게 함)
- 이름에 "Old Hangul" 추가
- OTF → woff2

### 남긴 조합 규칙

남긴 글자에 적용되는 규칙만 남았습니다. 네 글꼴 모두 숫자가 같습니다.

| 규칙 | 하는 일 | 규모 |
|---|---|---|
| `ccmp` | 자모 여러 개를 미리 그려 둔 모양 하나로 통째로 바꿈. ① 자주 쓰는 옛한글 음절 500개 (첫+가운뎃소리 134개, 첫+가운데+끝소리 366개) ② 자모 2~3개로 적은 겹자모 121개 (겹초성 34, 겹중성 28, 겹종성 59. 예: ᄀ+ᄃ) | 합자 621개 |
| `ljmo` | 뒤에 오는 가운뎃소리와 끝소리에 맞는 첫소리 모양을 고름 | 글리프 744개 |
| `vjmo` | 가운뎃소리 모양을 고름 (폭 0, 첫소리 칸 위에 겹쳐 그림) | 글리프 189개 |
| `tjmo` | 끝소리 모양을 고름 (폭 0) | 글리프 548개 |
| `vert`, `vrt2` | 방점 2개(〮 〯)의 세로쓰기용 모양과 위치 (GPOS `vert` 포함). 없으면 세로쓰기에서 방점이 따로 한 칸을 차지함 | 글리프 2개 |

`ccmp`가 먼저 적용되고, 미리 그려 둔 모양이 없으면 `ljmo`·`vjmo`·`tjmo`가
자모마다 알맞은 조각을 골라 한 칸에 겹쳐 그립니다.

원본의 `locl`, `calt`, `liga`와 그 밖의 위치 조정 규칙(GPOS, 자간 조정 등)은 한글 이외 글자에만 사용되어 삭제하였습니다.

참고: ᄂ+ᄉ처럼 겹초성을 자모 두 개로 나눠 적으면, 원본 글꼴에서도 Chrome에서
조합되지 않습니다. 표준에 따로 있는 글자(ᅛ, U+115B)로 적어야 합니다.

### 제작 및 시험

```sh
pip install -r requirements.txt
python build.py
python -m http.server 8765
```

그다음 <http://localhost:8765/test/>를 엽니다. 음절마다 한 칸 폭이면 ✓가 표시됩니다.
세로쓰기 칸에서는 방점이 붙은 음절의 세로 길이가 한 칸이면 ✓가 표시됩니다.
Windows의 Chrome에서는 세로쓰기를 포함한 모든 사례가 원본과 같게 나왔고, Safari와 Firefox는 아직 확인하지 않았습니다.
다시 만들어도 결과 파일이 한 바이트도 다르지 않으므로, 다시 만든 뒤
`git status`에 `fonts/` 변경이 없으면 공개된 파일이 이 스크립트로 만든 것임을 확인할 수 있습니다.

### 라이선스

- 글꼴(`fonts/*.woff2`): 원본과 같은 [SIL Open Font License 1.1](fonts/OFL.txt)
- 그 밖의 모든 것(스크립트, 시험 페이지, 문서): [CC0 1.0](LICENSE)
