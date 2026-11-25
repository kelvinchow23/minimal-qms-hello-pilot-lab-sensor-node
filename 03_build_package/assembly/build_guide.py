"""Build the picture-led assembly guide from steps.json and bom.csv.

    python build_guide.py            -> LSN-A-0001_guide.html beside this file
    python build_guide.py --embed    -> the same, with the pictures inside the file (one file to share)

Callouts come from the refdes column of bom.csv; quantities in each step must add up to the
BOM, and every BOM line must be used (the script stops if not). Step pictures are CAD renders
in images/; a callout may carry "pts" (pixel positions in its step picture) for leader lines.
Print the page to PDF from a browser for the paper copy.
"""
import base64
import csv
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
data = json.loads((HERE / "steps.json").read_text(encoding="utf-8"))
bom = [r for r in csv.DictReader(open(HERE.parent / "bom.csv", encoding="utf-8"))
       if r["parent_pn"] == data["assembly"]]
by_id = {r["refdes"]: r for r in bom}
EMBED = "--embed" in sys.argv


def src(rel):
    if not EMBED:
        return rel
    return "data:image/png;base64," + base64.b64encode((HERE / rel).read_bytes()).decode()


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
    p = HERE / "images" / f"{ref}.png"
    return f'<img src="{src(f"images/{ref}.png")}" alt="">' if p.exists() else '<div class="noimg"></div>'


def page():
    out = [f"<h1>{html.escape(data['assembly'])} {html.escape(data['title'])}</h1>",
           f"<p class='sub'>Rev {data['rev']} · from {html.escape(data['source'])}</p>",
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
        img = HERE / s["img"]
        if img.exists():
            out.append(f"<div class='fig'><img src='{src(s["img"])}' alt='Step {s['n']}'>")
            w, h = s.get("w"), s.get("h")
            if w and h:
                out.append(f"<svg viewBox='0 0 {w} {h}' class='ov'>")
                for c in s["callouts"]:
                    colour = data["classes"][c["id"][0]][1]
                    for (x, y) in c.get("pts", []):
                        out.append(f"<circle cx='{x}' cy='{y}' r='7' fill='none' stroke='{colour}' stroke-width='3'/>")
                    if c.get("label_at"):
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
        out.append("</section>")
    out.append("<h2>Final checks</h2><ul class='checks'>" + "".join(f"<li>☐ {html.escape(c)}</li>" for c in data["final_checks"]) + "</ul>")
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
@media print{main{max-width:none}}
"""

if __name__ == "__main__":
    problems = check()
    if problems:
        print("Steps do not match bom.csv:\n  " + "\n  ".join(problems))
        sys.exit(1)
    out = HERE / f"{data['assembly']}_guide.html"
    out.write_text(f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                   f"<title>{data['assembly']} assembly guide</title><style>{CSS}</style></head><body><main>{page()}</main></body></html>",
                   encoding="utf-8")
    print(f"wrote {out.name}: {len(data['steps'])} steps, every BOM line used once")
