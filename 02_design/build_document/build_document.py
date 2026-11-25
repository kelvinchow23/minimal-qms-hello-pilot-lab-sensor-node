"""Build the controlled document LSN-A-0001 rev <X> and its appendices into 03_build_package/.

    python build_document.py            -> PDFs, CSV and zips in ../../03_build_package/ (flat)
    python build_document.py --no-pdf   -> HTML previews only (beside this file)

Outputs: <PN>_rev<X>.pdf (assembly instruction), _A01_bom.csv, _A02_make-files.zip,
_A03_inspection-test.pdf (inspection, in-process and final checks, test procedures, analysis),
_A04_traveller.pdf. Software is not part of the document (a draft in ../software/). Sources, all in 02_design/: steps.json, images/,
bom.csv, inspection_checks.csv, make_files/ (CAD exports), ../test_procedures/,
../software/. Each step's quantities must add up to the BOM and every BOM line must be used.
"""
import base64
import csv
import html
import json
import subprocess
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


BASE = f"{data['assembly']}_rev{data['rev']}"
FILES = {"A01": f"{BASE}_A01_bom.csv", "A02": f"{BASE}_A02_make-files.zip",
         "A03": f"{BASE}_A03_inspection-test.pdf", "A04": f"{BASE}_A04_traveller.pdf"}
NAMES = {"A01": "Bill of materials (for ordering)", "A02": "Make files (STL for printing)",
         "A03": "Inspection and test", "A04": "Build traveller (one per unit)"}


def title_block(which=None):
    d = data["document"]
    doc = f"{data['assembly']} rev {data['rev']}" + (f", appendix {which}" if which else "")
    title = f"{data['title']}: " + (NAMES[which].lower() if which else "assembly instruction")
    rows = [("Document", doc), ("Title", title), ("Status", d["status"]), ("Approval", d["approval"]),
            ("Design source", data["source"])]
    if not which:
        rows.append(("Appendices", " · ".join(f"{k} {NAMES[k]}: {FILES[k]}" for k in FILES)))
    return (f"<h1>{e(data['assembly'])} {e(data['title'])}" + (f" · {which}" if which else "") + "</h1><table class='tb'>"
            + "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in rows) + "</table>")


def write_appendix_a():
    cols = ["ref", "pn", "rev", "description", "category", "qty", "unit", "manufacturer", "mpn", "supplier", "supplier_pn",
            "link", "unit_price", "pack_qty", "currency", "each_cad", "line_cad", "price_date", "notes"]
    with open(OUT / FILES["A01"], "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in bom:
            p = price_cad(r)
            row = dict(r, each_cad="" if p is None else f"{p:.2f}", line_cad="" if p is None else f"{p * int(r['qty']):.2f}")
            w.writerow([row.get(c, "") for c in cols])


def price_cad(r):
    if not r.get("unit_price"):
        return None
    return float(r["unit_price"]) * RATES[r["currency"]]


def appendix_c():
    names = {r["pn"]: (r["ref"], data["labels"].get(r["ref"], r["description"])) for r in bom}
    out = ["<section class='app'><h2>A03 · Inspection and test</h2>",
           "<h3>1 Incoming inspection</h3><p>Check each part when it arrives, before it goes into a build. "
           "Record the result on the build traveller (A04).</p>",
           "<table class='insp'><tr><th>Part</th><th>Check</th><th>How</th><th>Pass if</th><th>How many</th></tr>"]
    for r in csv.DictReader(open(HERE / "inspection_checks.csv", encoding="utf-8")):
        if r["pn"] == data["assembly"]:
            continue
        ref, name = names.get(r["pn"], ("", r["pn"]))
        out.append(f"<tr><td>{badge(ref) if ref else ''} {e(name)}<div class='small'>{e(r['pn'])}</div></td><td>{e(r['characteristic'])}</td>"
                   f"<td>{e(r['method'])}</td><td>{e(r['criterion'])}</td><td>{e(r['sample'])}</td></tr>")
    out.append("</table><h3>2 In-process checks</h3><table class='insp'><tr><th>Step</th><th>Check before moving on</th></tr>")
    for s in data["steps"]:
        out.append(f"<tr><td>{s['n']} {e(s['title'])}</td><td>{e(s.get('check', ''))}</td></tr>")
    out.append("</table><h3>3 Final checks and tests</h3><ul>"
               + "".join(f"<li>{e(c)}</li>" for c in data["final_checks"]) + "</ul><table class='insp'><tr><th>Test</th><th>What it shows</th></tr>")
    for tp in sorted((DESIGN / "test_procedures").glob("*.md")):
        meta = {}
        for line in tp.read_text(encoding="utf-8").split("---")[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        out.append(f"<tr><td>{e(meta.get('id', tp.stem))}</td><td>{e(meta.get('title', ''))}</td></tr>")
    out.append("</table><p>The full procedures and the analysis follow.</p>")
    for tp in sorted((DESIGN / "test_procedures").glob("*.md")):
        body = tp.read_text(encoding="utf-8").split("---", 2)[2]
        out.append("<div class='tp'>" + markdown.markdown(body, extensions=["tables"]) + "</div>")
    out.append("</section>")
    return out


def appendix_d():
    line = "<span class='blank'></span>"
    out = ["<section class='app'><h2>A04 · Build traveller (one per unit)</h2>",
           "<p>Print one per unit. It goes with the unit through the build; a copy or photo is kept in <code>builds/B00n/</code>.</p>",
           f"<table class='tb'><tr><th>Serial number</th><td>{data['assembly']}-YYMMDD + letter: {line}</td></tr>"
           f"<tr><th>Build</th><td>B00n {line}</td></tr><tr><th>Assembled by</th><td>{line}</td></tr><tr><th>Date</th><td>{line}</td></tr></table>",
           "<table class='trav'><tr><th>Stage</th><th>Item</th><th>Pass</th><th>Initials</th><th>Date</th></tr>"]
    names = {r["pn"]: (r["ref"], data["labels"].get(r["ref"], r["description"])) for r in bom}
    for r in csv.DictReader(open(HERE / "inspection_checks.csv", encoding="utf-8")):
        if r["pn"] == data["assembly"] or r["sample"] not in ("all",):
            continue
        ref, name = names.get(r["pn"], ("", r["pn"]))
        out.append(f"<tr><td>Incoming</td><td>{ref} {e(name)}: {e(r['characteristic'])}</td><td>☐</td><td></td><td></td></tr>")
    for s in data["steps"]:
        out.append(f"<tr><td>Step {s['n']}</td><td>{e(s.get('check', s['title']))}</td><td>☐</td><td></td><td></td></tr>")
    for c in data["final_checks"]:
        out.append(f"<tr><td>Final</td><td>{e(c)}</td><td>☐</td><td></td><td></td></tr>")
    for tp in sorted((DESIGN / "test_procedures").glob("TP-*.md")):
        out.append(f"<tr><td>Test</td><td>{e(tp.stem)} (results in test_results.csv)</td><td>☐</td><td></td><td></td></tr>")
    out.append("</table><table class='tb'><tr><th>Build complete, all items pass</th><td>Signature " + line + " Date " + line + "</td></tr>"
               "<tr><th>Released (SOP-007)</th><td>Recorded in release.yaml after the tests</td></tr></table></section>")
    return out


def page():
    out = [title_block(), f"<p class='prep'><b>Printing A1 and A2:</b> {e(data['document']['print_note'])} STL files are in A02.</p>",
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
            out.append(f"<p class='chk'>☑ <b>Check:</b> {html.escape(s['check'])}</p>")
        out.append("</section>")
    out.append("<h2>Final checks</h2><ul class='checks'>" + "".join(f"<li>☐ {html.escape(c)}</li>" for c in data["final_checks"]) + "</ul>")
    out.append("<p class='prep'>Record the serial number and sign off each unit on its build traveller (A04).</p>")
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
.tb{border-collapse:collapse;margin:8px 0 16px;font-size:14px}.tb th{text-align:left;background:#f2f2f2;padding:5px 10px;border:1px solid #ccc;white-space:nowrap}.tb td{padding:5px 10px;border:1px solid #ccc;min-width:260px}
.app{page-break-before:always;margin-top:32px}.bom,.insp,.trav{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0}.bom th,.bom td,.insp th,.insp td,.trav th,.trav td{border:1px solid #ccc;padding:4px 6px;text-align:left;vertical-align:top}
.bom th,.insp th,.trav th{background:#f2f2f2}.n{text-align:right}.tot td{font-weight:700}.small{font-size:12px;color:#555}.chk{margin:6px 0;font-size:15px}
.trav td:nth-child(3),.trav td:nth-child(4),.trav td:nth-child(5){width:70px}.blank{display:inline-block;min-width:180px;border-bottom:1px solid #333;height:1em}
@media print{main{max-width:none}}
"""

if __name__ == "__main__":
    problems = check()
    if problems:
        print("Steps do not match bom.csv:\n  " + "\n  ".join(problems))
        sys.exit(1)
    def write(name, title, body):
        out = HERE / name
        out.write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                       f"<title>{title}</title><style>{CSS}</style></head><body><main>{body}</main></body></html>", encoding="utf-8")
        edge = Path(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
        pdf = OUT / out.with_suffix(".pdf").name
        if edge.exists() and "--no-pdf" not in sys.argv:
            subprocess.run([str(edge), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", out.resolve().as_uri()], capture_output=True, timeout=120)
        return pdf.name

    def zip_dir(name, folder, readme):
        with zipfile.ZipFile(OUT / name, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(folder.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    z.write(f, f.relative_to(folder))
            z.writestr("README.txt", readme)
        return name

    OUT.mkdir(exist_ok=True)
    made = [write(f"{BASE}.html", f"{data['assembly']} rev {data['rev']}", page())]
    write_appendix_a(); made.append(FILES["A01"])
    made.append(zip_dir(FILES["A02"], HERE / "make_files", data["document"]["make_readme"]))
    made.append(write(f"{BASE}_A03_inspection-test.html", f"{BASE} A03", title_block("A03") + "\n".join(appendix_c()[1:])))
    made.append(write(f"{BASE}_A04_traveller.html", f"{BASE} A04", title_block("A04") + "\n".join(appendix_d()[1:])))
    print("wrote " + ", ".join(made))
