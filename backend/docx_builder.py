"""
Zero-*external*-dependency .docx (OOXML) writer — ported from the validated
lesson-planner engine (`index.html` lines 2318-2564 as of 2026-08-14):
crc32/u16le/u32le/concatBytes/createZip, escapeXml, docxRuns, docxP,
docxTable, scriptLineRunsXml, scriptToDocxXml, sheetBlockToDocxXml,
sheetToDocxXml, sheetKeyToDocxXml, docxHeaderXml, docxPageBreak,
buildDocxPackage.

Same byte-level ZIP/XML construction, just in Python — CRC32 uses the
stdlib `zlib.crc32` instead of porting the engine's hand-rolled CRC table
(identical result, `zlib` is Python's standard library, not a new
dependency). Returns raw `bytes` where the engine returned a `Blob`.
"""
import re
import zlib
from typing import List, Optional, Tuple

from prompt_builders import strip_leading_md, strip_leading_name_date_line, split_sheet_content


# ---- ZIP construction ----

def _u16le(n: int) -> bytes:
    return (n & 0xFFFF).to_bytes(2, "little")


def _u32le(n: int) -> bytes:
    return (n & 0xFFFFFFFF).to_bytes(4, "little")


def create_zip(files: List[Tuple[str, bytes]]) -> bytes:
    """files: list of (name, data) pairs. Uses stdlib zlib for CRC32."""
    FLAG_UTF8 = 0x0800
    local_parts: List[bytes] = []
    central_parts: List[bytes] = []
    offset = 0

    for name, data in files:
        name_bytes = name.encode("utf-8")
        crc = zlib.crc32(data) & 0xFFFFFFFF
        size = len(data)

        local_header = b"".join([
            _u32le(0x04034B50), _u16le(20), _u16le(FLAG_UTF8), _u16le(0), _u16le(0), _u16le(0),
            _u32le(crc), _u32le(size), _u32le(size), _u16le(len(name_bytes)), _u16le(0), name_bytes,
        ])
        local_parts.append(local_header)
        local_parts.append(data)

        central_header = b"".join([
            _u32le(0x02014B50), _u16le(20), _u16le(20), _u16le(FLAG_UTF8), _u16le(0), _u16le(0), _u16le(0),
            _u32le(crc), _u32le(size), _u32le(size), _u16le(len(name_bytes)), _u16le(0), _u16le(0),
            _u16le(0), _u16le(0), _u32le(0), _u32le(offset), name_bytes,
        ])
        central_parts.append(central_header)
        offset += len(local_header) + len(data)

    central_dir = b"".join(central_parts)
    eocd = b"".join([
        _u32le(0x06054B50), _u16le(0), _u16le(0), _u16le(len(files)), _u16le(len(files)),
        _u32le(len(central_dir)), _u32le(offset), _u16le(0),
    ])

    return b"".join(local_parts) + central_dir + eocd


# ---- OOXML fragments ----

def escape_xml(s) -> str:
    return (
        str(s if s is not None else "")
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;").replace("'", "&apos;")
    )


_BOLD_ITALIC_RE = re.compile(r"\*\*(.+?)\*\*|\*([^*\n]+?)\*")
_ESCAPED_MD_RE = re.compile(r"\\([_*`\[\]])")


def docx_runs(text: str, force_bold: bool = False) -> str:
    unescaped = _ESCAPED_MD_RE.sub(r"\1", str(text or ""))
    tokens = []
    last_index = 0
    for m in _BOLD_ITALIC_RE.finditer(unescaped):
        if m.start() > last_index:
            tokens.append({"t": unescaped[last_index:m.start()]})
        if m.group(1) is not None:
            tokens.append({"t": m.group(1), "b": True})
        else:
            tokens.append({"t": m.group(2), "i": True})
        last_index = m.end()
    if last_index < len(unescaped):
        tokens.append({"t": unescaped[last_index:]})
    if not tokens:
        tokens.append({"t": ""})

    out = []
    for tok in tokens:
        props = []
        if tok.get("b") or force_bold:
            props.append("<w:b/>")
        if tok.get("i"):
            props.append("<w:i/>")
        r_pr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
        out.append(f'<w:r>{r_pr}<w:t xml:space="preserve">{escape_xml(tok["t"])}</w:t></w:r>')
    return "".join(out)


def docx_p(
    text: Optional[str] = None,
    runs_xml: Optional[str] = None,
    bold: bool = False,
    before: int = 0,
    after: int = 160,
    border_left: Optional[str] = None,
    border_bottom: Optional[str] = None,
    border_box: Optional[str] = None,
    shade: Optional[str] = None,
) -> str:
    p_pr_parts = [f'<w:spacing w:before="{before}" w:after="{after}"/>']
    p_bdr = []
    if border_left:
        p_bdr.append(f'<w:left w:val="single" w:sz="24" w:space="8" w:color="{border_left}"/>')
    if border_bottom:
        p_bdr.append(f'<w:bottom w:val="single" w:sz="16" w:space="4" w:color="{border_bottom}"/>')
    if border_box:
        for side in ("top", "left", "bottom", "right"):
            p_bdr.append(f'<w:{side} w:val="single" w:sz="8" w:space="6" w:color="{border_box}"/>')
    if p_bdr:
        p_pr_parts.append(f'<w:pBdr>{"".join(p_bdr)}</w:pBdr>')
    if shade:
        p_pr_parts.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>')
    p_pr = f'<w:pPr>{"".join(p_pr_parts)}</w:pPr>'
    runs = runs_xml if runs_xml is not None else docx_runs(text, bold)
    return f"<w:p>{p_pr}{runs}</w:p>"


def docx_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    b = 'w:val="single" w:sz="4" w:space="0" w:color="999999"'
    tbl_pr = (
        f'<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
        f"<w:top {b}/><w:left {b}/><w:bottom {b}/><w:right {b}/><w:insideH {b}/><w:insideV {b}/>"
        f"</w:tblBorders></w:tblPr>"
    )

    header_shade = '<w:shd w:val="clear" w:color="auto" w:fill="EEEEEC"/>'

    def row_xml(cells: List[str], header: bool) -> str:
        cells_xml = "".join(
            f'<w:tc><w:tcPr>{header_shade if header else ""}</w:tcPr>'
            f'<w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{docx_runs(c, header)}</w:p></w:tc>'
            for c in cells
        )
        return f"<w:tr>{cells_xml}</w:tr>"

    return f"<w:tbl>{tbl_pr}{row_xml(head, True)}{''.join(row_xml(r, False) for r in body)}</w:tbl>"


# ---- markdown-lite line classification (mirrors the engine's parser) ----

def is_rule(line: str) -> bool:
    return bool(re.match(r"^(-{3,}|\*{3,}|_{3,})$", line.strip()))


def is_table_row(line: str) -> bool:
    return bool(re.match(r"^\|.*\|$", line.strip()))


def is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$", line.strip()))


def parse_table_row(line: str) -> List[str]:
    stripped = line.strip()
    stripped = re.sub(r"^\|", "", stripped)
    stripped = re.sub(r"\|$", "", stripped)
    return [c.strip() for c in stripped.split("|")]


_SCRIPT_MARKERS = [
    ("teacher", re.compile(r"^▶\s*Teacher:", re.IGNORECASE)),
    ("students", re.compile(r"^👥\s*Students?:", re.IGNORECASE)),
    ("board", re.compile(r"^📋\s*Board:", re.IGNORECASE)),
    ("materials", re.compile(r"^📦\s*Materials?:", re.IGNORECASE)),
]


def classify_script_line(line: str) -> Optional[dict]:
    clean = strip_leading_md(line)
    for_match = clean.replace("**", "").strip()
    if re.match(r"^STAGE\s+\d", for_match, re.IGNORECASE):
        return {"type": "stage", "clean": for_match}
    for type_name, regex in _SCRIPT_MARKERS:
        if regex.match(for_match):
            return {"type": type_name, "clean": clean}
    return None


def script_line_runs_xml(text: str) -> str:
    m = re.match(r"^([▶👥📋📦]\s*[A-Za-z\']+:)\s*(.*)$", text)
    if m:
        return docx_runs(m.group(1), True) + (docx_runs(" " + m.group(2)) if m.group(2) else "")
    return docx_runs(text)


def script_to_docx_xml(text: str) -> str:
    """The teacher's script export is deliberately plain — no colored boxes,
    no tables, just text with the ▶/👥/📋/📦 marker bolded so lines are
    still easy to scan without any Word borders/shading."""
    lines = [line.strip() for line in re.split(r"\r?\n", text)]
    n = len(lines)
    xml = ""
    i = 0
    while i < n:
        raw = lines[i]
        if not raw:
            i += 1
            continue
        if is_rule(raw):
            i += 1
            continue
        if is_table_row(raw):
            # No real Word tables in the script export -- flatten to plain lines.
            while i < n and is_table_row(lines[i]):
                if not is_table_separator(lines[i]):
                    xml += docx_p(text="  —  ".join(parse_table_row(lines[i])), after=80)
                i += 1
            continue
        cls = classify_script_line(raw)
        if cls and cls["type"] == "stage":
            xml += docx_p(text=cls["clean"], bold=True, before=240, after=120)
            i += 1
            continue
        if cls:
            parts = [cls["clean"]]
            i += 1
            while i < n and lines[i] and not classify_script_line(lines[i]) and not is_rule(lines[i]) and not is_table_row(lines[i]):
                parts.append(strip_leading_md(lines[i]))
                i += 1
            xml += docx_p(runs_xml=script_line_runs_xml("  ".join(parts)), after=120)
            continue
        clean = strip_leading_md(raw)
        xml += docx_p(text=clean, bold=True, after=120) if re.match(r"^#{1,6}\s", raw) else docx_p(text=clean, after=120)
        i += 1
    return xml


def sheet_block_to_docx_xml(lines: List[str]) -> str:
    n = len(lines)
    xml = ""
    i = 0
    while i < n:
        raw = lines[i]
        if not raw:
            i += 1
            continue
        if is_rule(raw):
            i += 1
            continue
        if is_table_row(raw):
            rows = []
            while i < n and is_table_row(lines[i]):
                if not is_table_separator(lines[i]):
                    rows.append(parse_table_row(lines[i]))
                i += 1
            xml += docx_table(rows)
            continue
        clean = strip_leading_md(raw)
        xml += docx_p(text=clean, bold=True, after=100) if re.match(r"^#{1,6}\s", raw) else docx_p(text=clean, after=100)
        i += 1
    return xml


def sheet_to_docx_xml(content: str) -> str:
    """Student copy — only the content before the answer-key/teacher-notes
    boundary. No injected "Sheet X — Title" heading (each sheet already
    carries its own descriptive title as its first line) and no per-sheet
    Name/Date line — the combined document shows Name/Date once, at the top."""
    main_lines, _ = split_sheet_content(content)
    main_lines = strip_leading_name_date_line(main_lines)
    return sheet_block_to_docx_xml(main_lines)


def sheet_key_to_docx_xml(content: str, letter_or_key: str, sheet_title: str) -> str:
    """Teacher's copy — only the answer-key/teacher-notes part, if any."""
    _, key_lines = split_sheet_content(content)
    if not key_lines:
        return ""
    xml = docx_p(text=f"Sheet {letter_or_key} — {sheet_title}", bold=True, before=200, after=120, border_bottom="22242A")
    xml += sheet_block_to_docx_xml(key_lines)
    return xml


def docx_header_xml(level_label: str, week: int, week_start: str, week_end: str) -> str:
    return docx_p(text=f"theteachkit.com — {level_label} — Week {week} of 32 — {week_start} to {week_end}", after=200)


def docx_page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def build_docx_package(title: str, body_xml: str) -> bytes:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>{escape_xml(title)}</dc:title>
<dc:creator>theteachkit.com</dc:creator>
</cp:coreProperties>"""

    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
{body_xml}
<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr>
</w:body>
</w:document>"""

    return create_zip([
        ("[Content_Types].xml", content_types.encode("utf-8")),
        ("_rels/.rels", rels.encode("utf-8")),
        ("docProps/core.xml", core.encode("utf-8")),
        ("word/document.xml", document.encode("utf-8")),
    ])
