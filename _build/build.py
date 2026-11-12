"""Genera index.html (web móvil) y carta.pdf (mismas pantallas, una página por sección).
Uso: python build.py <carpeta-del-repo>"""
import html, pathlib, sys
from weasyprint import HTML

here = pathlib.Path(__file__).parent
repo = pathlib.Path(sys.argv[1])

# Datos de la carta: se reutilizan de gen.bak (lista S)
src = (here / "gen.bak").read_text(encoding="utf-8")
ns = {}
exec(src[src.index("S = ["):src.index("\ne = html.escape")], ns)
DATA = {s[0]: s[4] for s in ns["S"]}

MAP = ("https://www.google.com/maps/place/Pizza+Loco/@37.1681584,-3.6095901,17z/data=!3m2!4b1"
       "!5s0xd71fc90a5211197:0x7edf0a3a55f35c3c!4m6!3m5!1s0xd71fc90ae47c753:0xa0e72d3e5dff9bd8"
       "!8m2!3d37.1681584!4d-3.6070152!16s%2Fg%2F11fx8hhqfs")

# id, etiqueta corta, título, frase gancho, foto, tipo de cabecera
SECS = [
 ("entrantes", "Entrantes", "Entrantes", "Para abrir boca", "piadina.jpg", "photo"),
 ("ensaladas", "Ensaladas", "Ensaladas", "Frescas y con color", "caprese.jpg", "photo"),
 ("burguer", "Burguer", "Burguer<br>&amp; Food", "Para hambre de la buena", "", "plain"),
 ("pastas", "Pastas", "Pastas", "Cremosas, al horno, con parmesano", "pasta.jpg", "photo"),
 ("clasicas", "Clásicas", "Pizzas<br>clásicas", "Las de toda la vida", "pizza.jpg", "circle"),
 ("especiales", "Especiales", "Pizzas<br>especiales", "Cuando ya lo has probado todo", "", "plain"),
 ("panouzzo", "Panouzzo", "Panouzzo", "Nuestra masa, rellena hasta arriba", "panouzzo.jpg", "photo"),
 ("postres", "Postres", "Postres", "Guarda un hueco", "", "plain"),
]
FEAT = {  # plato destacado por sección -> etiqueta
 ("entrantes", "Patatas locas"): "Para compartir",
 ("burguer", "Burguer Pica Loco"): "Con nombre propio",
 ("pastas", "Tortiglioni horno"): "Al horno",
 ("clasicas", "Pizza Loco"): "La de la casa",
 ("especiales", "Mortalla"): "Con burrata y pistacho",
 ("postres", "Calzone de Nutella"): "¿Te atreves?",
}
HOT = {("entrantes", "Patatas bravas"), ("burguer", "Burguer Pica Loco"),
       ("clasicas", "Venta"), ("especiales", "Mexicana")}
ASK = {  # gancho de curiosidad que aparece justo antes de ese plato
 ("especiales", "Antonia"): ("¿Manzana y morcilla en una pizza?", "Pide la Antonia y nos cuentas."),
 ("especiales", "Granola"): ("Queso de cabra, nueces y miel.", "Dulce y salado en el mismo bocado: la Granola."),
 ("panouzzo", "Romana"): ("¿Calamares a la romana dentro de nuestra masa?", "Eso es el Panouzzo Romana."),
}
e = html.escape


def items(sec):
    out = []
    for name, price, desc in DATA[sec]:
        if (sec, name) in ASK:
            q, a = ASK[(sec, name)]
            out.append(f'<li class="ask">{e(q)}<small>{e(a)}</small></li>')
        badge = FEAT.get((sec, name))
        hot = '<span class="hot">Picante</span>' if (sec, name) in HOT else ''
        out.append(
            f'<li class="{"feat" if badge else ""}">'
            + (f'<span class="badge">{e(badge)}</span>' if badge else '')
            + f'<div class="top"><h3>{e(name)}{hot}</h3><b>{price}</b></div>'
            + (f'<p>{e(desc)}</p>' if desc else '') + '</li>')
    return "".join(out)


def section(sid, _short, title, kicker, img, kind):
    if kind == "photo":
        head = (f'<div class="sh photo"><img src="img/{img}" alt=""><div class="ov"></div>'
                f'<p class="k">{e(kicker)}</p><h2>{title}</h2></div>')
    else:
        circ = f'<img class="circ" src="img/{img}" alt="">' if kind == "circle" else ''
        extra = ('<p class="trio">Masa napolitana · Tomate San Marzano · Fior di latte</p>'
                 if sid == "clasicas" else '')
        head = (f'<div class="sh plain">{circ}<span class="flag s"></span>'
                f'<p class="k">{e(kicker)}</p><h2>{title}</h2>{extra}</div>')
    return f'<section class="pg" id="{sid}">{head}<ul>{items(sid)}</ul></section>'


pills = "".join(f'<a href="#{s[0]}">{e(s[1])}</a>' for s in SECS)

CSS = """
@font-face{font-family:Bebas;src:url(fonts/BebasNeue-Regular.woff2) format("woff2");font-display:swap}
@font-face{font-family:Kaushan;src:url(fonts/KaushanScript-Regular.woff2) format("woff2");font-display:swap}
@font-face{font-family:Barlow;font-weight:400;src:url(fonts/Barlow-Regular.woff2) format("woff2");font-display:swap}
@font-face{font-family:Barlow;font-weight:500;src:url(fonts/Barlow-Medium.woff2) format("woff2");font-display:swap}
@font-face{font-family:Barlow;font-weight:700;src:url(fonts/Barlow-Bold.woff2) format("woff2");font-display:swap}
:root{--bg:#15100d;--s:#221a14;--line:rgba(247,239,226,.1);--cream:#f7efe2;--mute:#b9ab9a;--red:#e23b24;--gold:#f5b942;--green:#2f9e55}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html{background:#0b0806;scroll-behavior:smooth}
body{margin:0 auto;max-width:480px;background:var(--bg);color:var(--cream);font:400 16px/1.45 Barlow,system-ui,sans-serif;-webkit-text-size-adjust:100%}
a{color:inherit}
.flag{display:block;height:5px;background:linear-gradient(90deg,#2f9e55 33.3%,#f7efe2 33.3%,#f7efe2 66.6%,#e23b24 66.6%)}
.flag.s{width:66px;height:4px;border-radius:2px;margin-bottom:14px}

.cover{text-align:center;padding-bottom:30px}
.plate{background:#fff;border-radius:0 0 50% 50%/0 0 20% 20%;padding:22px 16px 40px}
.plate img{width:88%;height:auto;display:block;margin:0 auto}
.tag{margin:26px 0 10px;font-weight:500;font-size:12.5px;letter-spacing:.32em;text-transform:uppercase;color:var(--gold)}
.hook{margin:0 16px;font:400 58px/.92 Bebas,Impact,sans-serif;letter-spacing:.01em}
.hook em{display:block;margin-top:6px;font:400 38px/1.05 Kaushan,cursive;color:var(--red);letter-spacing:0}
.lead{margin:16px 34px 0;color:var(--mute);font-size:15.5px}
.cta{display:flex;gap:10px;padding:24px 16px 0}
.btn{flex:1;display:flex;align-items:center;justify-content:center;min-height:52px;padding:0 16px;border-radius:14px;font-weight:700;font-size:16px;letter-spacing:.02em;text-decoration:none;background:var(--red);color:#fff}
.btn.ghost{background:transparent;border:1.5px solid rgba(247,239,226,.35);color:var(--cream)}
.index{display:none;flex-wrap:wrap;justify-content:center;gap:8px;padding:26px 20px 0}
.index a,.bar a{flex:none;text-decoration:none;font-weight:500;font-size:14.5px;padding:8px 15px;border-radius:999px;border:1px solid rgba(247,239,226,.22)}
.bar{position:sticky;top:0;z-index:9;display:flex;gap:8px;overflow-x:auto;padding:10px 12px;background:rgba(21,16,13,.97);border-bottom:1px solid var(--line);scrollbar-width:none}
.bar a.on{background:var(--gold);border-color:var(--gold);color:var(--bg);font-weight:700}

.promo{background:var(--red);padding:30px 20px 28px;display:flex;align-items:center;gap:12px}
.promo .t{flex:1}
.promo .k{color:#fff;font-size:24px}
.promo h2{font-size:50px;color:#fff}
.promo p.d{margin:8px 0 0;font-size:15px;color:#ffe3dc;line-height:1.35}
.promo .price{margin-top:8px;font:400 104px/.85 Bebas,Impact,sans-serif;color:var(--gold)}
.promo .price span{font-size:60px}
.promo img{flex:none;width:158px;height:158px;border-radius:50%;object-fit:cover;border:5px solid var(--cream)}

section{scroll-margin-top:58px}
.sh{position:relative}
.sh.photo{height:290px;display:flex;flex-direction:column;justify-content:flex-end;padding:0 18px 10px;overflow:hidden}
.sh.photo img,.sh .ov{position:absolute;top:0;left:0;width:100%;height:100%}
.sh.photo img{object-fit:cover}
.sh .ov{background:linear-gradient(180deg,rgba(21,16,13,0) 30%,rgba(21,16,13,.72) 68%,#15100d 100%)}
.sh.photo .k,.sh.photo h2{position:relative}
.sh.plain{padding:46px 18px 4px}
.circ{position:absolute;right:18px;top:34px;width:132px;height:132px;border-radius:50%;object-fit:cover;border:4px solid var(--gold)}
.k{margin:0;font:400 23px/1.1 Kaushan,cursive;color:var(--gold)}
h2{margin:4px 0 0;font:400 68px/.9 Bebas,Impact,sans-serif;letter-spacing:.01em}
.trio{margin:14px 0 0;font-weight:500;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}

ul{list-style:none;margin:0;padding:6px 18px 22px}
li{padding:15px 0;border-bottom:1px solid var(--line)}
li:last-child{border-bottom:0}
.top{display:flex;justify-content:space-between;align-items:baseline;gap:14px}
h3{margin:0;font:700 17px/1.22 Barlow,system-ui,sans-serif;letter-spacing:.035em;text-transform:uppercase}
.top b{flex:none;font:400 25px/1 Bebas,Impact,sans-serif;letter-spacing:.02em;color:var(--gold)}
li p{margin:5px 0 0;max-width:86%;color:var(--mute);font-size:14.5px;line-height:1.42}
.hot{display:inline-block;margin-left:8px;padding:2px 8px;border-radius:999px;background:var(--red);color:#fff;font-size:10px;letter-spacing:.12em;vertical-align:middle}
li.feat{margin:12px -8px;padding:14px 16px 16px;border:1.5px solid rgba(245,185,66,.6);border-radius:18px;background:var(--s)}
.badge{display:inline-block;margin-bottom:9px;padding:3px 10px;border-radius:999px;background:var(--gold);color:var(--bg);font-weight:700;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase}
li.feat h3{font-size:19px}
li.ask{margin:12px 0 4px;padding:16px 18px;border:0;border-left:4px solid var(--red);border-radius:0 16px 16px 0;background:var(--s);font:400 23px/1.2 Kaushan,cursive}
li.ask small{display:block;margin-top:7px;font:400 14.5px/1.35 Barlow,system-ui,sans-serif;color:var(--mute)}

.end{text-align:center;padding:50px 22px 44px;border-top:1px solid var(--line)}
.end .flag.s{margin:0 auto 18px}
.end h2{font-size:58px}
.end .btn{display:inline-flex;min-width:240px;margin-top:24px}
.end .n{margin:26px 0 0;color:var(--mute);font-size:12.5px;letter-spacing:.08em}
.end .n a{color:var(--cream)}
@media print{
 @page{margin:0;size:108mm 2000mm}
 html{background:#15100d}
 body{max-width:none}
 .bar,.noprint{display:none}
 .index{display:flex}
}
"""

JS = """try{var L=[].slice.call(document.querySelectorAll('.bar a')),O=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){L.forEach(function(a){var on=a.getAttribute('href')=='#'+x.target.id;a.classList.toggle('on',on);if(on)a.scrollIntoView({inline:'center',block:'nearest'})})}})},{rootMargin:'-30% 0px -60% 0px'});document.querySelectorAll('section').forEach(function(s){O.observe(s)})}catch(e){}"""

page = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Carta · Pizza Loco</title>
<meta name="description" content="La carta de Pizza Loco, Granada: pizza napolitana, pastas, burguers, panouzzo y postres.">
<meta name="theme-color" content="#15100d">
<style>{CSS}</style>
</head>
<body>
<div class="pg"><div class="cover">
<span class="flag"></span>
<div class="plate"><img src="img/hero.jpg" alt="Pizza Loco"></div>
<p class="tag">Pizza napolitana · Granada</p>
<p class="hook">Aviso:<em>esta carta da hambre</em></p>
<p class="lead">Masa napolitana, tomate San Marzano y Fior di latte. Lo demás, lo eliges tú.</p>
<div class="cta noprint"><a class="btn" href="{MAP}">Cómo llegar</a><a class="btn ghost" href="carta.pdf">Carta en PDF</a></div>
<div class="index">{pills}</div>
</div>
<div class="promo">
<div class="t"><p class="k">¿Ya la has probado?</p><h2>Pizza<br>Portafoglio</h2>
<p class="d">Doblada y lista para comer con la mano.</p><div class="price">5<span>€</span></div></div>
<img src="img/portafoglio.jpg" alt="Pizza Portafoglio">
</div>
</div>
<nav class="bar">{pills}</nav>
{"".join(section(*s) for s in SECS)}
<div class="pg end">
<span class="flag s"></span>
<p class="k">Te esperamos</p>
<h2>¿Ya sabes cuál<br>vas a pedir?</h2>
<a class="btn" href="{MAP}">Cómo llegar a Pizza Loco</a>
<p class="n">Precios en euros<span class="noprint"> · <a href="carta.pdf">Descargar carta en PDF</a></span></p>
</div>
<script>{JS}</script>
</body>
</html>
"""
(repo / "index.html").write_text(page, encoding="utf-8")

# --- PDF: 1ª pasada mide cada bloque .pg; 2ª pasada da a cada uno su propia página a medida
def render(extra_css=""):
    return HTML(string=page.replace("</style>", extra_css + "</style>", 1), base_url=str(repo) + "/").render()

first = render(".pg{break-before:page}")
heights = []
for pg in first.pages:
    for box in pg._page_box.descendants():
        el = getattr(box, "element", None)
        if el is not None and "pg" in (el.get("class") or "").split():
            heights.append(box.margin_height())
            break
rules = "".join(
    f"@page p{i}{{size:108mm {h * 25.4 / 96 + 0.3:.2f}mm;margin:0}}"
    f".pg:nth-of-type({i + 1}){{page:p{i}}}" for i, h in enumerate(heights))
# nth-of-type cuenta por etiqueta (div/section), así que se asigna por atributo en su lugar
out = page
parts = out.split('class="pg')
out = parts[0] + "".join(f'style="page:p{i}" class="pg' + p for i, p in enumerate(parts[1:]))
rules = "".join(f"@page p{i}{{size:108mm {h * 25.4 / 96 + 0.3:.2f}mm;margin:0}}" for i, h in enumerate(heights))
doc = HTML(string=out.replace("</style>", rules + "</style>", 1), base_url=str(repo) + "/").render()
doc.write_pdf(str(repo / "carta.pdf"))
print("bloques:", len(heights), "paginas:", len(doc.pages), "alturas mm:", [round(h * 25.4 / 96) for h in heights])
