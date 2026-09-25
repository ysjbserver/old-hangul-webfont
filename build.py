"""Build Old Hangul webfonts (woff2) by subsetting Noto Sans/Serif CJK KR.

Usage:
    pip install -r requirements.txt
    python build.py

The upstream OTF files are downloaded into sources/ (verified by SHA-256),
and the subset woff2 files are written to fonts/ together with SHA256SUMS.
Running the script again should produce byte-identical files, so after a
rebuild `git status` showing no changes in fonts/ means the published files
match this script.
"""

import hashlib
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

BASE = Path(__file__).parent
SRC = BASE / "sources"
OUT = BASE / "fonts"

UPSTREAM = "https://raw.githubusercontent.com/notofonts/noto-cjk"

# (upstream tag, path in upstream repo, SHA-256, new family name, style)
FONTS = [
    ("Sans2.004", "Sans/OTF/Korean/NotoSansCJKkr-Regular.otf",
     "6bcb2a0703aa137e874fc2dffa85f6c21ba9a67fa329e81b8c801663af7e992a",
     "Noto Sans CJK KR Old Hangul", "Regular"),
    ("Sans2.004", "Sans/OTF/Korean/NotoSansCJKkr-Bold.otf",
     "26d0c6748500a0444844280b308f5b62c7ae92ac6c6ac88148e502dd211eb52a",
     "Noto Sans CJK KR Old Hangul", "Bold"),
    ("Serif2.003", "Serif/OTF/Korean/NotoSerifCJKkr-Regular.otf",
     "77b4b741f864d27f15e90f275b17106dde90b2ad28f82bab72dc95805db5fb42",
     "Noto Serif CJK KR Old Hangul", "Regular"),
    ("Serif2.003", "Serif/OTF/Korean/NotoSerifCJKkr-Bold.otf",
     "10cc03741178ad6d2747df8497d911e34b167d0474a826fb9d866c402cbe3d8f",
     "Noto Serif CJK KR Old Hangul", "Bold"),
]

RANGES = [
    (0x1100, 0x11FF),  # Hangul Jamo (conjoining jamo)
    (0x302E, 0x302F),  # Hangul tone marks (bangjeom)
    (0x3131, 0x318E),  # Hangul Compatibility Jamo
    (0xA960, 0xA97F),  # Hangul Jamo Extended-A
    # Precomposed syllables are needed because MediaWiki stores text in NFC:
    # U+1100 U+1161 U+11EB becomes U+AC00 U+11EB, and both parts must come
    # from the same font to compose.
    (0xAC00, 0xD7A3),  # Hangul Syllables
    (0xD7B0, 0xD7FF),  # Hangul Jamo Extended-B
    (0x25CC, 0x25CC),  # Dotted circle, used as a base for isolated jamo
]

# Features that have rules for the kept glyphs. Other upstream features
# (locl, calt, liga, kern, ...) apply only to non-Hangul glyphs.
LAYOUT_FEATURES = [
    "ccmp",          # pre-drawn syllables and compound jamo
    "ljmo",          # initial consonant forms
    "vjmo",          # vowel forms
    "tjmo",          # final consonant forms
    "vert", "vrt2",  # vertical forms of the tone marks
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(tag, path, digest):
    local = SRC / Path(path).name
    if not local.exists():
        SRC.mkdir(exist_ok=True)
        url = f"{UPSTREAM}/{tag}/{path}"
        print(f"downloading {url}")
        urllib.request.urlretrieve(url, local)
    if sha256(local) != digest:
        raise SystemExit(f"checksum mismatch: {local} (delete it and run again)")
    return local


def rename(font, family, style):
    """Give the subset its own name so it is not mistaken for the original."""
    ps_family = family.replace(" ", "")
    names = {
        1: family,
        2: style,
        3: f"{ps_family}-{style};subset",
        4: f"{family} {style}" if style != "Regular" else family,
        6: f"{ps_family}-{style}",
        16: family,
        17: style,
    }
    table = font["name"]
    for name_id in list(names) + [18, 21, 22]:
        table.removeNames(nameID=name_id)
    for name_id, value in names.items():
        table.setName(value, name_id, 3, 1, 0x409)
    version = (table.getDebugName(5) or "").split(";")[0]
    table.setName(f"{version}; Old Hangul subset", 5, 3, 1, 0x409)
    if "CFF " in font:
        cff = font["CFF "].cff
        cff.fontNames = [f"{ps_family}-{style}"]
        top = cff.topDictIndex[0]
        top.FamilyName = family
        top.FullName = names[4]


def build(src, family, style):
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = LAYOUT_FEATURES
    options.layout_scripts = ["DFLT", "hang"]
    options.hinting = False
    options.desubroutinize = True
    options.name_IDs = ["*"]
    options.name_languages = ["*"]
    options.notdef_outline = True

    font = subset.load_font(str(src), options)
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=[c for a, b in RANGES for c in range(a, b + 1)])
    subsetter.subset(font)
    rename(font, family, style)

    OUT.mkdir(exist_ok=True)
    out = OUT / f"{family.replace(' ', '')}-{style}.woff2"
    subset.save_font(font, str(out), options)
    result = TTFont(str(out))
    print(f"{out.name:<42} {out.stat().st_size / 1024:6.0f} KB"
          f"  {len(result.getBestCmap()):6} chars  {result['maxp'].numGlyphs:6} glyphs")
    return out


if __name__ == "__main__":
    outputs = [build(fetch(tag, path, digest), family, style)
               for tag, path, digest, family, style in FONTS]
    sums = "".join(f"{sha256(p)}  {p.name}\n" for p in outputs)
    (OUT / "SHA256SUMS").write_text(sums, encoding="utf-8", newline="\n")
