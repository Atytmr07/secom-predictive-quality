"""Akademik biçim: siyah metin, Times New Roman, siyah çizgili tablolar, sayfa numarası."""
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches

BLACK = RGBColor(0, 0, 0)


def _font(style, name="Times New Roman", size=None, bold=None, italic=None):
    f = style.font; f.name = name; f.color.rgb = BLACK
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts"); rpr.append(fonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if fonts.get(qn(a)) is not None:
            del fonts.attrib[qn(a)]
    col = rpr.find(qn("w:color"))
    if col is not None:  # tema renk özniteliklerini temizle
        for a in ("w:themeColor", "w:themeShade", "w:themeTint"):
            if col.get(qn(a)) is not None:
                del col.attrib[qn(a)]
    if size: f.size = Pt(size)
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic


def _borders(table):
    tbl = table._tbl; tblPr = tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None: tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000"); b.append(e)
    tblPr.append(b)


def _page_number(section):
    p = section.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        r = p.add_run()
        if t:
            fc = OxmlElement("w:fldChar"); fc.set(qn("w:fldCharType"), t); r._r.append(fc)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt; r._r.append(it)
        r.font.name = "Times New Roman"; r.font.size = Pt(10)


def restyle(doc, body_size=12, line_spacing=1.5):
    s = doc.styles
    _font(s["Normal"], size=body_size)
    s["Normal"].paragraph_format.line_spacing = line_spacing; s["Normal"].paragraph_format.space_after = Pt(6)
    for name, size, bold, italic in (("Title", 16, True, False), ("Heading 1", 13, True, False), ("Heading 2", 12, True, False), ("Heading 3", 12, True, True)):
        if name in [x.name for x in s]:
            _font(s[name], size=size, bold=bold, italic=italic)
            s[name].paragraph_format.space_before = Pt(12); s[name].paragraph_format.space_after = Pt(6)
            s[name].paragraph_format.line_spacing = 1.15
    if "List Bullet" in [x.name for x in s]:
        _font(s["List Bullet"], size=body_size)
    if "Title" in [x.name for x in s]:  # başlık altındaki mavi çizgiyi kaldır
        ppr = s["Title"].element.get_or_add_pPr(); bd = ppr.find(qn("w:pBdr"))
        if bd is not None: ppr.remove(bd)
    for p in doc.paragraphs:
        if p.style.name == "Title":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.color.rgb = BLACK
    for t in doc.tables:
        t.style = s["Table Grid"]; _borders(t)
        for i, row in enumerate(t.rows):
            for c in row.cells:
                for p in c.paragraphs:
                    p.paragraph_format.line_spacing = 1.0; p.paragraph_format.space_after = Pt(1)
                    for r in p.runs:
                        r.font.color.rgb = BLACK; r.font.name = "Times New Roman"
                        if i == 0: r.bold = True
    W = {2: [0.28, 0.72], 3: [0.2, 0.3, 0.5], 4: [0.07, 0.3, 0.43, 0.2], 5: [0.2, 0.3, 0.14, 0.12, 0.24]}
    for t in doc.tables:
        n = len(t.columns); fr = W.get(n)
        total = 6.3 if doc.sections[0].orientation == 0 else 6.3
        if n >= 6 or fr is None: continue
        t.autofit = False
        for row in t.rows:
            for c, f in zip(row.cells, fr):
                c.width = Inches(total * f)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2.54) if sec.orientation == 0 else Cm(1.8)
        sec.top_margin = sec.bottom_margin = Cm(2.54)
        _page_number(sec)
