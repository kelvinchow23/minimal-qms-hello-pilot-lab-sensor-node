"""Build the controlled document LSN-A-0001 rev <X> and its appendices into 03_build_package/.

    python build_document.py            -> PDFs, CSV and zips in ../../03_build_package/ (flat)
    python build_document.py --no-pdf   -> HTML previews only (beside this file)

Outputs: <PN>_assembly_instructions_rev_<X>.pdf, <PN>-A01_bom_rev_<X>.csv, -A02_make_files, -A03_test,
-A04_traveller (inspection, in-process and final checks, test procedures, analysis),
_A04_traveller.pdf. Software is not part of the document (a draft in ../software/). Sources, all in 02_design/: steps.json, images/,
bom.csv, inspection_checks.csv, make_files/ (CAD exports), ../test_procedures/,
../software/. Each step's quantities must add up to the BOM and every BOM line must be used.
"""
import base64
import csv
import html
import json
import subprocess
import time
import zipfile

import markdown
import sys
from pathlib import Path

HERE = Path(__file__).parent
ASM = HERE
DESIGN = HERE.parent
OUT = HERE.parent.parent / "03_build_package"
data = json.loads((ASM / "steps.json").read_text(encoding="utf-8"))
bom = list(csv.DictReader(open(HERE / "bom.csv", encoding="utf-8")))
by_id = {r["ref"]: r for r in bom}
RATES = {"CAD": 1.0, "USD": 1.4369}  # Bank of Canada, 2026-11-23 (OTS library rates.csv)
EMBED = "--embed" in sys.argv


def src(rel):
    if not EMBED:
        return rel
    return "data:image/png;base64," + base64.b64encode((ASM / rel).read_bytes()).decode()


def check():
    """A callout marked "again" shows a part fitted in an earlier step; it is not counted."""
    used = {}
    problems = []
    for s in data["steps"]:
        for c in s["callouts"]:
            if c["id"] not in by_id:
                problems.append(f"step {s['n']}: {c['id']} is not on the BOM")
            elif not c.get("again"):
                used[c["id"]] = used.get(c["id"], 0) + c["qty"]
    for ref, r in by_id.items():
        n = used.get(ref, 0)
        if n != int(r["qty"]):
            problems.append(f"{ref} ({r['pn']}): BOM {r['qty']}, steps {n}")
    return problems


def badge(ref):
    colour = data["classes"][ref[0]][1]
    return f'<span class="bdg" style="background:{colour}">{ref}</span>'


def thumb(ref):
    p = ASM / "images" / f"{ref}.png"
    return f'<img src="{src(f"images/{ref}.png")}" alt="">' if p.exists() else '<div class="noimg"></div>'


def e(x):
    return html.escape(str(x))


def lines(x):
    """Escape, and put each "; "-separated item on its own line."""
    return "<br>".join(html.escape(p) for p in str(x).split("; "))


PN, REV = data["assembly"], data["rev"]
BASE = PN  # kept for HTML preview names


def release_tag():
    """'_YYMMDD' (the release date) once the document is released; nothing while it is a draft."""
    d = data["document"]
    if d.get("status", "").lower() != "released":
        return ""
    y, m, day = d["date"].split("-")
    return f"_{y[2:]}{m}{day}"


def fname(which, name, ext):
    """<PN>[-Ann]_<name>_rev_<X>[_YYMMDD].<ext>, e.g. LSN-A-0001-A04_traveller_rev_A_261126.pdf"""
    return f"{PN}{'-' + which if which else ''}_{name}_rev_{REV}{release_tag()}.{ext}"


FILES = {"A01": fname("A01", "bom", "csv"), "A02": fname("A02", "make_files", "zip"),
         "A03": fname("A03", "test", "pdf"), "A04": fname("A04", "traveller", "pdf"),
         "A05": fname("A05", "incoming", "pdf")}
NAMES = {"A01": "Bill of materials (for ordering)", "A02": "Make files (STL for printing)",
         "A03": "Inspection and test procedures", "A04": "Build traveller (one per unit)",
         "A05": "Incoming inspection record (one per delivery)"}


def tb_fields(which=None):
    """The title block fields, the same on every document and form (also used for the CSV forms)."""
    d = data["document"]
    return [("Document no.", data["assembly"] + (f"-{which}" if which else "")), ("Rev", data["rev"]),
            ("Assembly name", data["name"]), ("Assembly no.", data["assembly"]),
            ("Status", d["status"]), ("Date", d["date"]), ("Approval", d["approval"]),
            ("Design source", data["source_top"])]


def title_block(which=None):
    title = NAMES[which] if which else "Assembly instructions"
    f = dict(tb_fields(which))
    cell = lambda k: f"<th>{e(k)}</th><td>{e(f[k])}</td>"
    out = (f"<table class='tblock'><tr><td class='tt' colspan='4'>{e(title)}</td></tr>"
           f"<tr>{cell('Document no.')}{cell('Rev')}</tr><tr>{cell('Assembly name')}{cell('Assembly no.')}</tr>"
           f"<tr>{cell('Status')}{cell('Date')}</tr>"
           f"<tr>{cell('Approval')}{cell('Design source')}</tr></table>")
    if not which:
        out += ("<table class='tb'><tr><th>Appendices</th><td>"
                + "<br>".join(f"{data['assembly']}-{k} {e(NAMES[k])}" for k in FILES) + "</td></tr></table>")
    return out


def source_rule(r):
    """Where a part may be bought, from its class (SOP-002): A from an approved supplier, B/C anywhere."""
    if r["category"].startswith("Custom"):
        return "Custom"
    if r.get("class") == "A":
        return "Approved supplier, exact part"
    if r.get("exact_part") == "yes":
        return "Any supplier, exact part"
    return "Any supplier, any matching part"


def write_appendix_a():
    cols = ["ref", "internal_pn", "rev", "description", "category", "purchasing", "qty", "unit", "manufacturer",
            "manufacturer_pn", "supplier", "supplier_pn", "link", "unit_price", "pack_qty", "currency",
            "unit_cost_cad", "line_cost_cad", "price_date", "notes"]
    with open(OUT / FILES["A01"], "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in bom:
            p = price_cad(r)
            row = dict(r, internal_pn=r["pn"], manufacturer_pn=r["mpn"], purchasing=source_rule(r),
                       unit_cost_cad="" if p is None else f"{p:.2f}",
                       line_cost_cad="" if p is None else f"{p * int(r['qty']):.2f}")
            w.writerow([row.get(c) or "-" for c in cols])  # no blank cells: "-" means not applicable


def price_cad(r):
    if not r.get("unit_price"):
        return None
    return float(r["unit_price"]) * RATES[r["currency"]]


def part_names():
    return {r["pn"]: (r["ref"], data["labels"].get(r["ref"], r["description"])) for r in bom}


def incoming_rows():
    names = part_names()
    for r in csv.DictReader(open(HERE / "inspection_checks.csv", encoding="utf-8")):
        if r["pn"] == data["assembly"]:
            continue
        ref, name = names.get(r["pn"], ("", r["pn"]))
        yield ref, name, r


def tests():
    out = []
    for tp in sorted((DESIGN / "test_procedures").glob("TP-*.md")):
        meta = {}
        for line in tp.read_text(encoding="utf-8").split("---")[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        out.append((tp.stem, meta.get("title", ""), data["document"]["tp_briefs"].get(tp.stem, "")))
    return out


FAIL_NOTE = "Fail: mark F, describe it in Comments, stop, tell the quality lead (they raise an NC)."


def appendix_c():
    out = ["<section class='app'>", "<h3>1 Incoming inspection</h3>"]
    if list(incoming_rows()):
        out.append("<p>Critical parts only. Record on A05, one per delivery.</p>"
                   "<table class='insp'><tr><th>Part</th><th>Check</th><th>How</th><th>Pass if</th><th>How many</th></tr>")
        for ref, name, r in incoming_rows():
            out.append(f"<tr><td>{badge(ref) if ref else ''} {e(name)}<div class='small'>{e(r['pn'])}</div></td>"
                       f"<td>{e(r['characteristic'])}</td><td>{e(r['method'])}</td><td>{lines(r['criterion'])}</td>"
                       f"<td>{e(r['sample'])}</td></tr>")
        out.append("</table>")
    else:
        out.append(f"<p>None. {e(data['document']['no_incoming'])}</p>")
    out.append("<h3>2 In-process checks</h3><table class='insp'><tr><th>Step</th><th>Check before moving on</th></tr>")
    for s in data["steps"]:
        out.append(f"<tr><td>{s['n']} {e(s['title'])}</td><td>{lines(s.get('check', ''))}</td></tr>")
    out.append("</table><h3>3 Final checks and tests</h3><ul>"
               + "".join(f"<li>{e(c)}</li>" for c in data["final_checks"]) + "</ul>")
    out.append("<table class='insp'><tr><th>Test</th><th>Title</th><th>In short</th></tr>"
               + "".join(f"<tr><td>{e(i)}</td><td>{e(ti)}</td><td>{lines(b)}</td></tr>" for i, ti, b in tests())
               + "</table>")
    for tp in sorted((DESIGN / "test_procedures").glob("*.md")):
        body = tp.read_text(encoding="utf-8").split("---", 2)[2]
        out.append("<div class='tp'>" + markdown.markdown(body, extensions=["tables"]) + "</div>")
    out.append("</section>")
    return out


BLANK = "<span class='blank'></span>"
REC_COLS = ["P / F", "Initials", "Date", "Comments", "NC"]


def record_table(head, rows):
    cols = head + REC_COLS
    cells = "<td>☐ P ☐ F</td><td></td><td></td><td class='cm'></td><td></td>"
    return ("<table class='trav'><tr>" + "".join(f"<th>{e(c)}</th>" for c in cols) + "</tr>"
            + "".join("<tr>" + "".join(f"<td>{lines(x)}</td>" for x in r) + cells + "</tr>" for r in rows)
            + "</table>")


def traveller_rows():
    rows = [("Step " + str(s["n"]), s.get("check", s["title"])) for s in data["steps"]]
    rows += [("Final", c) for c in data["final_checks"]]
    rows += [("First unit only", c) for c in data.get("first_unit_checks", [])]
    rows += [(i, f"{ti}; {b}; Full procedure in A03") for i, ti, b in tests()]
    return rows


def appendix_d():
    return ["<section class='app'>",
            "<p>One per unit. Keep the filled copy in <code>builds/B001/</code> (first build).</p>",
            f"<table class='tb'><tr><th>Serial number</th><td>{e(data['assembly'])}-{BLANK}</td></tr>"
            f"<tr><th>Build number</th><td>B{BLANK} (B001 = first build)</td></tr>"
            f"<tr><th>Assembled by</th><td>{BLANK}</td></tr><tr><th>Date</th><td>{BLANK}</td></tr></table>",
            f"<p class='prep'>{e(FAIL_NOTE)}</p>",
            record_table(["Stage", "Check: pass if"], traveller_rows()),
            f"<table class='tb'><tr><th>Build complete, all pass</th><td>Signature {BLANK} Date {BLANK}</td></tr>"
            "<tr><th>Released</th><td>Decided separately after the tests (SOP-007)</td></tr></table>",
            "</section>"]


def incoming_record_rows():
    return [(f"{ref} {name} ({r['pn']})", f"{r['characteristic']}: {r['criterion']}", r["sample"], "")
            for ref, name, r in incoming_rows()]


def appendix_e():
    return ["<section class='app'>",
            "<p>One record per delivery: check every part in the box in one go. Strike out rows for parts that "
            "are not in this delivery.</p>",
            f"<table class='tb'><tr><th>Received</th><td>{BLANK}</td></tr><tr><th>Order / supplier</th><td>{BLANK}</td></tr>"
            f"<tr><th>Inspected by</th><td>{BLANK}</td></tr></table>",
            f"<p class='prep'>{e(FAIL_NOTE)}</p>",
            record_table(["Part", "Check: pass if", "How many", "Qty received"], incoming_record_rows()),
            "</section>"]


def write_record_csv(name, top, head, rows, which):
    """The same form as CSV, for an agent or a spreadsheet to fill; a filled copy goes in builds/B00n/."""
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Title", NAMES[which]])
        for k, v in tb_fields(which):
            w.writerow([k, v])
        w.writerow([])
        for k in top:
            w.writerow([k, ""])
        w.writerow([])
        w.writerow(head + ["pass_fail", "initials", "date", "comments", "nc"])
        for r in rows:
            w.writerow(list(r) + ["", "", "", "", ""])


def page():
    out = [title_block(), f"<div class='cover'><img src='{src('images/finished.png')}' alt='Finished unit'></div>",
           "<div class='pb'></div>",
           f"<p class='prep'>Print A1, A2: {e(data['document']['print_note'])} STL files in A02.</p>",
           "<h2>Parts</h2>"]
    for letter, (name, _) in data["classes"].items():
        refs = [r for r in by_id if r[0] == letter]
        if not refs:
            continue
        out.append(f"<h3>{name}</h3><div class='grid'>")
        for ref in sorted(refs, key=lambda x: int(x[1:])):
            r = by_id[ref]
            out.append(f"<div class='card'>{thumb(ref)}<div>{badge(ref)}<span class='cq'>×{r['qty']}</span></div>"
                       f"<div class='cap'>{html.escape(data['labels'][ref])}</div><div class='pn'>{r['pn']}</div></div>")
        out.append("</div>")
    b = data["before"]
    out.append("<h2>Before you start</h2><div class='before'>")
    out.append("<div><b>Tools</b><ul>" + "".join(f"<li>{html.escape(t)}</li>" for t in b["tools"]) + "</ul></div>")
    out.append("<div><b>Consumables</b><ul>" + "".join(f"<li>{html.escape(t)}</li>" for t in b["consumables"]) + "</ul></div>")
    out.append("<div><b>Safety</b><ul>" + "".join(f"<li>{html.escape(t)}</li>" for t in b["safety"]) + "</ul></div></div>")
    out.append(f"<p class='prep'>{html.escape(b['prep'])}</p>")
    wires = data.get("wires")
    if wires:
        # Wires are built first, from their own BOM, then used as W parts in the steps.
        out.append("<h2>W · Wires: build these first</h2>")
        if wires.get("note"):
            out.append(f"<p>{html.escape(wires['note'])}</p>")
        if wires.get("bom"):
            out.append("<table class='wbom'><tr><th>Item</th><th>Qty</th><th>What</th></tr>" + "".join(
                f"<tr><td>{html.escape(i['item'])}</td><td>{html.escape(str(i['qty']))}</td><td>{html.escape(i['what'])}</td></tr>"
                for i in wires["bom"]) + "</table>")
        for w in wires.get("build", []):
            out.append(f"<div class='har'><div>{badge(w['id'])}<span class='q'> ×{by_id[w['id']]['qty']}</span><div class='cap'>{html.escape(w['length'])}</div></div>"
                       f"<div><b>{html.escape(w['what'])}</b><div class='ends'><div><b>End A:</b> {html.escape(w['end_a'])}</div><div><b>End B:</b> {html.escape(w['end_b'])}</div></div>"
                       "<ol>" + "".join(f"<li>{html.escape(x)}</li>" for x in w["steps"]) + "</ol></div></div>")
    for s in data["steps"]:
        out.append(f"<section class='step'><div class='head'><div class='num'>{s['n']}</div><div class='title'>{html.escape(s['title'])}</div></div>")
        out.append("<div class='box'><div class='parts'>")
        for c in s["callouts"]:
            out.append(f"<div class='pi'>{thumb(c['id'])}<div>{badge(c['id'])}<span class='q'> ×{c['qty']}</span></div></div>")
        out.append("</div>")
        if s.get("tools"):
            out.append(f"<div class='tools'>\U0001F527 {html.escape(s['tools'])}</div>")
        out.append("</div>")
        img = ASM / s["img"]
        if img.exists():
            out.append(f"<div class='fig'><img src='{src(s["img"])}' alt='Step {s['n']}'>")
            w, h = s.get("w"), s.get("h")
            if w and h:
                out.append(f"<svg viewBox='0 0 {w} {h}' class='ov'>")
                for c in s["callouts"]:
                    colour = data["classes"][c["id"][0]][1]
                    for (x, y) in c.get("pts", []):
                        out.append(f"<circle cx='{x}' cy='{y}' r='7' fill='none' stroke='{colour}' stroke-width='3'/>")
                    if c.get("paths"):
                        # A cable route: one line per cable, its callout at the middle of the run.
                        for path in c["paths"]:
                            pts = " ".join(f"{x},{y}" for x, y in path)
                            out.append(f"<polyline points='{pts}' fill='none' stroke='white' stroke-width='9' stroke-linejoin='round' stroke-linecap='round'/>"
                                       f"<polyline points='{pts}' fill='none' stroke='{colour}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'/>")
                            mx, my = path[len(path) // 2]
                            out.append(f"<rect x='{mx-18}' y='{my-13}' width='36' height='26' rx='13' fill='{colour}' stroke='white' stroke-width='2'/>"
                                       f"<text x='{mx}' y='{my+5}' font-size='14' font-weight='800' fill='white' text-anchor='middle'>{c['id']}</text>")
                    elif c.get("label_at"):
                        lx, ly = c["label_at"]
                        for (x, y) in c.get("pts", []):
                            out.append(f"<line x1='{x}' y1='{y}' x2='{lx}' y2='{ly}' stroke='{colour}' stroke-width='1.5'/>")
                        out.append(f"<rect x='{lx-18}' y='{ly-13}' width='36' height='26' rx='13' fill='{colour}' stroke='white' stroke-width='2'/>"
                                   f"<text x='{lx}' y='{ly+5}' font-size='14' font-weight='800' fill='white' text-anchor='middle'>{c['id']}</text>")
                out.append("</svg>")
            out.append("</div>")
        else:
            out.append(f"<div class='fig missing'>Picture to come: {html.escape(s['img'])}</div>")
        out.append("<div class='legend'>" + "".join(
            f"<div>{badge(c['id'])}<span class='q'>{c['qty']}×</span> {html.escape(c['action'])}</div>" for c in s["callouts"]) + "</div>")
        if s.get("notes"):
            out.append("<ul class='notes'>" + "".join(f"<li>{html.escape(n)}</li>" for n in s["notes"]) + "</ul>")
        if s.get("check"):
            out.append(f"<p class='chk'>☑ <b>Check:</b><br>{lines(s['check'])}</p>")
        out.append("</section>")
    out.append("<h2>Final checks</h2><ul class='checks'>" + "".join(f"<li>☐ {html.escape(c)}</li>" for c in data["final_checks"]) + "</ul>")
    out.append("<p class='prep'>Sign off each unit on its traveller (A04).</p>")
    if data.get("credits"):
        out.append("<h2>Picture credits</h2><ul class='credits'>" + "".join(f"<li>{html.escape(c)}</li>" for c in data["credits"]) + "</ul>")
    return "\n".join(out)


CSS = """
body{font-family:Helvetica,Arial,sans-serif;margin:0;color:#222;background:#fff}
main{max-width:1000px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:32px;margin:0}.sub{color:#555;margin:4px 0 16px}h2{font-size:24px;margin:28px 0 8px}h3{font-size:16px;margin:12px 0 6px;color:#444}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
.card{border:1px solid #ddd;border-radius:8px;padding:6px;text-align:center}.card img,.noimg{height:90px;max-width:100%;object-fit:contain;margin:0 auto}
.noimg{background:#f2f2f2;border-radius:4px}.cq{font-weight:800;font-size:17px;margin-left:6px}.cap{font-size:13px;font-weight:700}.pn{font-size:11px;color:#777}
.bdg{display:inline-block;min-width:26px;padding:2px 8px;border-radius:12px;color:#fff;font-weight:800;font-size:13px;text-align:center}
.before{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}.before ul{margin:4px 0 0 18px}.prep{border-left:4px solid #1f77b4;padding:6px 10px;background:#f4f8fc}
.step{page-break-before:always;margin-top:28px}.head{display:flex;align-items:baseline;gap:14px}.num{font-size:60px;font-weight:800;line-height:1}.title{font-size:24px;font-weight:700}
.box{display:flex;gap:12px;flex-wrap:wrap;margin:10px 0}.parts{border:2px solid #222;border-radius:8px;padding:8px 12px;display:flex;flex-wrap:wrap;gap:8px 16px}
.pi{display:flex;flex-direction:column;align-items:center}.pi img,.pi .noimg{height:54px;width:auto;min-width:54px}.q{font-weight:800}
.tools{border:2px dashed #888;border-radius:8px;padding:8px 12px;font-size:14px;align-self:flex-start}
.fig{position:relative;border:1px solid #ddd;border-radius:8px;overflow:hidden}.fig img{display:block;width:100%}.ov{position:absolute;inset:0;width:100%;height:100%}
.missing{padding:60px 16px;text-align:center;color:#888;background:#fafafa}
.legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:6px 20px;margin:8px 0;font-size:15px}
.har{border:2px solid #8c564b;border-radius:10px;padding:10px 14px;margin:10px 0;display:grid;grid-template-columns:110px 1fr;gap:12px}.har .ends{display:grid;grid-template-columns:1fr 1fr;gap:6px 18px;font-size:14px}.har ol{margin:4px 0 0 18px;font-size:14px}.wbom{border-collapse:collapse;font-size:14px}.wbom td,.wbom th{border:1px solid #ccc;padding:4px 8px}.credits{font-size:12px;color:#555}.notes{margin:4px 0 0 18px;font-size:14px;color:#333}.checks{list-style:none;padding:0;font-size:15px;line-height:1.8}
.tp{border-top:2px solid #ccc;margin-top:18px;font-size:14px}.tp table{border-collapse:collapse}.tp td,.tp th{border:1px solid #ccc;padding:3px 6px}
.tblock{border-collapse:collapse;width:100%;margin:0 0 18px;font-size:14px;border:2px solid #222}.tblock th,.tblock td{border:1px solid #888;padding:5px 8px;text-align:left}.tblock th{background:#f2f2f2;white-space:nowrap;width:1%}.tblock .tt{font-size:24px;font-weight:800;padding:10px 8px}
.tb{border-collapse:collapse;margin:8px 0 16px;font-size:14px}.tb th{text-align:left;background:#f2f2f2;padding:5px 10px;border:1px solid #ccc;white-space:nowrap}.tb td{padding:5px 10px;border:1px solid #ccc;min-width:260px}
.app{page-break-before:always;margin-top:32px}.bom,.insp,.trav{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0}.bom th,.bom td,.insp th,.insp td,.trav th,.trav td{border:1px solid #ccc;padding:4px 6px;text-align:left;vertical-align:top}
.bom th,.insp th,.trav th{background:#f2f2f2}.n{text-align:right}.tot td{font-weight:700}.small{font-size:12px;color:#555}.chk{margin:6px 0;font-size:15px}
.trav td:nth-child(3),.trav td:nth-child(4),.trav td:nth-child(5){width:70px}.cm{min-width:140px}.blank{display:inline-block;min-width:180px;border-bottom:1px solid #333;height:1em}
*{font-family:Helvetica,Arial,sans-serif !important}
body,p,li,td,th,.legend,.notes,.chk,.prep,.tools,.cap,.small,.pn,.tp,.tp td,.tp th{font-size:13px !important}
h1,.tblock .tt{font-size:22px !important}h2,.title{font-size:18px !important}h3{font-size:14px !important}
.num{font-size:40px !important}.q,.cq{font-size:13px !important}.bdg{font-size:12px !important}
.cover{text-align:center;margin:24px 0}.cover img{max-width:80%;max-height:520px}.pb{page-break-after:always}
@media print{main{max-width:none}}
"""

if __name__ == "__main__":
    problems = check()
    if problems:
        print("Steps do not match bom.csv:\n  " + "\n  ".join(problems))
        sys.exit(1)
    def write(name, title, body, landscape=False):
        out = HERE / name
        out.write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                       f"<title>{title}</title><style>{CSS}{'@page{size:landscape}' if landscape else ''}</style></head><body><main>{body}</main></body></html>", encoding="utf-8")
        edge = Path(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
        pdf = OUT / out.with_suffix(".pdf").name
        if edge.exists() and "--no-pdf" not in sys.argv:
            started = time.time()
            subprocess.run([str(edge), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", out.resolve().as_uri()], capture_output=True, timeout=120)
            if not pdf.exists() or pdf.stat().st_mtime < started - 1:
                print(f"LOCKED (close it and run again): {pdf.name}")
        return pdf.name

    def zip_dir(name, folder, readme):
        # once released, files named ..._rev_<X>.<ext> inside get the release date too
        dated = lambda s: s.replace(f"_rev_{REV}.", f"_rev_{REV}{release_tag()}.")
        with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(folder.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    z.write(f, dated(str(f.relative_to(folder))))
            z.writestr("README.txt", dated(readme))
        return name

    OUT.mkdir(exist_ok=True)
    if not list(incoming_rows()):  # no critical parts: no incoming inspection record
        FILES.pop("A05"); NAMES.pop("A05")
    made = [write(fname(None, "assembly_instructions", "html"), f"{data['assembly']} rev {data['rev']}", page())]
    try:
        write_appendix_a(); made.append(FILES["A01"])
    except PermissionError:
        print(f"LOCKED (close it and run again): {FILES['A01']}")
    made.append(zip_dir(FILES["A02"], HERE / "make_files", data["document"]["make_readme"]))
    made.append(write(fname("A03", "test", "html"), f"{BASE} A03", title_block("A03") + "\n".join(appendix_c()[1:])))
    made.append(write(fname("A04", "traveller", "html"), f"{BASE} A04", title_block("A04") + "\n".join(appendix_d()[1:])))
    write_record_csv(fname("A04", "traveller", "csv"),
                     ["serial_number", "build_number", "assembled_by", "date", "build_complete_signature"],
                     ["stage", "check_pass_if"], traveller_rows(), "A04")
    made.append(fname("A04", "traveller", "csv"))
    if "A05" in FILES:
        made.append(write(fname("A05", "incoming", "html"), f"{BASE} A05", title_block("A05") + "\n".join(appendix_e()[1:]), landscape=True))
        write_record_csv(fname("A05", "incoming", "csv"), ["received", "order_supplier", "inspected_by"],
                         ["part", "check_pass_if", "how_many", "qty_received"], incoming_record_rows(), "A05")
        made.append(fname("A05", "incoming", "csv"))
    else:
        for old in OUT.glob(f"{PN}-A05_*"):
            try:
                old.unlink()
            except PermissionError:
                print(f"LOCKED, delete by hand: {old.name}")
    print("wrote " + ", ".join(made))
