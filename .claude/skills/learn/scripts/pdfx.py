#!/usr/bin/env python3
"""Stdlib-only, coordinate-aware PDF text extractor.

Why this exists: these sandboxes have no pdftotext, no poppler/pdftoppm and no
pypdf/PyPDF2, and the Read tool cannot render a PDF. This is the only way in.
It decompresses FlateDecode content streams with zlib and parses the text
operators directly, tracking the text matrix so figure content can be rebuilt
in visual order.

WARNING: relational operators inside FIGURES are unreliable. Springer remaps glyphs
onto C0 control codes per font subset, so the same byte is a different character in
different runs. repair() maps \x1e before a digit to U+2264 which is correct for the
"rank <= 2" run but WRONG inside Fig. 5a, where the HUPO-HPP inset really reads >=2
and >=18. Take inequality directions from prose or Methods, never from this output.

Usage:
  python3 pdfx.py FILE.pdf flat          > flat.txt    # stream-order text (prose)
  python3 pdfx.py FILE.pdf placed        > placed.txt  # coordinate-ordered (figures)
  python3 pdfx.py FILE.pdf grep PATTERN [CHARS]        # regex search with context
  python3 pdfx.py FILE.pdf region YMIN YMAX SUBSTR     # one panel, x-coords shown

Typical first pass on a new document:
  python3 pdfx.py doc.pdf flat   > flat.txt
  python3 pdfx.py doc.pdf placed > placed.txt
Read prose from flat.txt. Read anything inside a figure from placed.txt.

'placed' is the trustworthy mode for anything inside a figure. Flat mode returns
figure labels out of visual order and WILL transpose tables if you trust it.
"""
import re, sys, zlib

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    sys.exit(__doc__)
PDF = sys.argv[1]

CP1252 = {0x91:"\u2018",0x92:"\u2019",0x93:"\u201c",0x94:"\u201d",0x95:"\u2022",
          0x96:"\u2013",0x97:"\u2014",0xa9:"\u00a9",0xb0:"\u00b0",0xb1:"\u00b1",
          0xb5:"\u00b5",0xd7:"\u00d7",0xe1:"\u00e1",0xe9:"\u00e9",0xed:"\u00ed",
          0xf3:"\u00f3",0xfc:"\u00fc",0xfd:"\u00fd"}

# Springer subsets these fonts and remaps glyphs onto C0 control codes. The same
# code means different things in different font runs, so resolve by context.
def repair(t):
    t = "".join(CP1252.get(ord(c), c) for c in t)
    # running header/footer noise: "Nature | Vol <ctl> | <ctl> June <ctl>"
    t = re.sub(r"Nature \| Vol[^|]*\|[\x18-\x1f\s]*June[\x18-\x1f\s]*", "", t)
    t = re.sub(r"[\x18-\x1f]*\s*\|\s*8[12]\d", "", t)
    # named diacritics that got subset-mapped
    t = t.replace("Micha\x1f I. \x1ewirski", "Micha\u0142 I. \u015awirski")
    # ligatures: only between letters
    t = re.sub(r"(?<=[A-Za-z])\x1f(?=[a-z])", "fi", t)
    t = re.sub(r"(?<=[A-Za-z])\x1e(?=[a-z])", "ff", t)
    t = re.sub(r"(?<=[A-Za-z])\x1d(?=[a-z])", "fi", t)
    # relational operators
    t = t.replace("\x19", "\u2265").replace("\x1b", "\u2264")
    t = re.sub(r"\x1e(?=\s*\d)", "\u2264", t)
    # superscript minus, e.g. 10<ctl>9  ->  10-9
    t = re.sub(r"(?<=\d)\x1a(?=\d)", "-", t)
    t = re.sub(r"\x1a(?=[\d.])", "-", t)
    # primes: 5'-UTR, 3' Gene Expression
    t = re.sub(r"(?<=[35])\x18", "\u2032", t)
    # everything else in this band was a thin/no-break space
    t = re.sub(r"[\x18-\x1f]", " ", t)
    # soft hyphen across a line break, and Springer's mid-word hyphen artefacts
    t = re.sub(r"([a-z])-\n([a-z])", r"\1\2", t)
    t = re.sub(r"([a-z])-\s(?=[a-z]{2})", r"\1", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t

def unesc(b):
    out = bytearray(); i = 0
    while i < len(b):
        c = b[i]
        if c == 0x5c and i+1 < len(b):
            n = b[i+1]
            m = {0x6e:10,0x72:13,0x74:9,0x62:8,0x66:12,0x28:40,0x29:41,0x5c:92}
            if n in m: out.append(m[n]); i += 2; continue
            if 48 <= n <= 55:
                j = i+1; o = ""
                while j < len(b) and 48 <= b[j] <= 55 and len(o) < 3:
                    o += chr(b[j]); j += 1
                out.append(int(o, 8) & 0xFF); i = j; continue
            i += 2; continue
        out.append(c); i += 1
    return bytes(out)

def streams():
    data = open(PDF, "rb").read()
    for s in re.findall(rb"stream\r?\n(.*?)endstream", data, re.S):
        try: d = zlib.decompress(s)
        except Exception: continue
        if b"Tj" in d or b"TJ" in d: yield d

TOK = re.compile(
    rb"BT|ET"
    rb"|([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm"
    rb"|([-\d.]+)\s+([-\d.]+)\s+Td|([-\d.]+)\s+([-\d.]+)\s+TD|T\*"
    rb"|(\((?:\\.|[^()\\])*\))\s*Tj|(\[(?:[^\[\]]|\\.)*\])\s*TJ", re.S)

def _str(raw):
    if raw.startswith(b"("):
        return unesc(raw[1:-1]).decode("latin-1")
    s = ""
    for sm in re.finditer(rb"\((?:\\.|[^()\\])*\)|(-?[\d.]+)", raw[1:-1], re.S):
        g = sm.group(0)
        if g.startswith(b"("): s += unesc(g[1:-1]).decode("latin-1")
        else:
            try:
                if float(g) < -180: s += " "
            except ValueError: pass
    return s

def placed(d):
    """-> [(y, x, text)] using the text matrix."""
    items = []; tm = [1,0,0,1,0,0]; tlm = tm[:]
    for m in TOK.finditer(d):
        t = m.group(0)
        if t == b"BT": tm = [1,0,0,1,0,0]; tlm = tm[:]
        elif t.endswith(b"Tm"): tm = [float(m.group(i)) for i in range(1,7)]; tlm = tm[:]
        elif t.endswith(b"Td") or t.endswith(b"TD"):
            g = (7,8) if t.endswith(b"Td") else (9,10)
            dx, dy = float(m.group(g[0])), float(m.group(g[1]))
            tlm = [tlm[0],tlm[1],tlm[2],tlm[3],
                   tlm[4]+dx*tlm[0]+dy*tlm[2], tlm[5]+dx*tlm[1]+dy*tlm[3]]
            tm = tlm[:]
        elif t == b"T*":
            tlm = [tlm[0],tlm[1],tlm[2],tlm[3],tlm[4],tlm[5]-10*tlm[3]]; tm = tlm[:]
        else:
            raw = m.group(11) or m.group(12)
            if raw is None: continue
            s = _str(raw)
            if s.strip(): items.append((round(tm[5],1), round(tm[4],1), s))
    return items

def flat(d):
    parts = []
    for m in TOK.finditer(d):
        t = m.group(0)
        if t.endswith(b"Tj") or t.endswith(b"TJ"):
            raw = m.group(11) or m.group(12)
            if raw is not None: parts.append(_str(raw))
        elif t == b"T*": parts.append("\n")
    return "".join(parts)

def rows(items, tol=3.0):
    g = {}
    for y, x, t in items: g.setdefault(round(y/tol), []).append((x, t))
    return [(k*tol, sorted(v)) for k, v in sorted(g.items(), reverse=True)]

cmd = sys.argv[2] if len(sys.argv) > 2 else "flat"

if cmd == "flat":
    for i, d in enumerate(streams()):
        t = flat(d)
        if len(t.strip()) > 200:
            print(f"\n===== STREAM {i} =====")
            print(repair(re.sub(r"\n{3,}", "\n\n", t)))
elif cmd == "placed":
    for i, d in enumerate(streams()):
        it = placed(d)
        if not it: continue
        print(f"\n===== STREAM {i} =====")
        for y, cells in rows(it):
            line = "".join(t for _, t in cells)
            if line.strip(): print(f"y{y:7.1f} | {repair(line)}")
elif cmd == "grep":
    pat = sys.argv[3]; span = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    # repair() BEFORE collapsing whitespace: Python's \s matches the C0 separators
    # (\x1c-\x1f) that carry the ligature glyphs, so collapsing first destroys them.
    blob = re.sub(r"[ \t]+", " ", repair(" ".join(flat(d) for d in streams())))
    blob = re.sub(r"\s*\n\s*", " ", blob)
    n = 0
    for m in re.finditer(pat, blob, re.I):
        a, b = max(0, m.start()-span), min(len(blob), m.end()+span)
        print(f"--- match {n} ---\n...{blob[a:b]}...\n"); n += 1
    if not n: print("no match")
elif cmd == "region":
    ymin, ymax, sub = float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    for i, d in enumerate(streams()):
        if sub.encode() not in d: continue
        it = [(y,x,t) for y,x,t in placed(d) if ymin <= y <= ymax]
        if not it: continue
        print(f"===== STREAM {i} =====")
        for y, cells in rows(it, 5.0):
            print(f"y{y:7.1f} | " + "  ".join(f"[{x:.0f}]{repair(t)}" for x, t in cells))
