#!/usr/bin/env python3
"""Genera index.html, el-proyecto.html y aplicaciones.html desde data/*.json.
Uso: python3 tools/build.py"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
esc = html.escape
BASE = "https://www.proyectodane.org"  # dominio de producción
OG_IMAGE = f"{BASE}/assets/img/foto-nene-tablet.jpg"
JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "NGO",
    "name": "Proyecto Dane",
    "alternateName": "Proyecto DANE",
    "url": BASE + "/",
    "logo": f"{BASE}/assets/img/logo-proyecto-dane.jpg",
    "description": "Aplicaciones gratuitas para el aprendizaje de niños y jóvenes con discapacidad.",
    "address": {"@type": "PostalAddress", "streetAddress": "Rivadavia 717, 8º piso", "postalCode": "1002", "addressLocality": "Ciudad de Buenos Aires", "addressCountry": "AR"},
    "telephone": "+54 11 4342-8034",
    "sameAs": [
        "https://www.youtube.com/channel/UCLE1R-akE4t1lhw_TMGbY2Q",
        "https://x.com/proyectodane",
        "https://www.facebook.com/ProyectoDANE/",
        "https://www.linkedin.com/company/proyecto-dane",
        "https://www.instagram.com/proyectodane/",
    ],
}, ensure_ascii=False)
apps = json.loads((ROOT / "data/apps.json").read_text())
premios = json.loads((ROOT / "data/premios.json").read_text())
equipo = json.loads((ROOT / "data/equipo.json").read_text())["integrantes"]

CATS = {  # categoría: (fondo, texto)
    "Académicas-funcionales": ("#F6E6F1", "#7A2E69"),
    "Comunicación": ("#DDF1FB", "#1F4FB5"),
    "Destrezas auditivas y visuales": ("#FDF0D0", "#6B4A00"),
    "Habilidades sociales y emocionales": ("#FDE3E4", "#A3121B"),
}
PALETA = ["#B5509E", "#D992C3", "#EE9C44", "#ED2530", "#93D9F7", "#4169E1"]
STRIP = '<div class="brand-strip" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span></div>'
LINKEDIN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>'

def svg(inner):
    return f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

SOCIAL = [
    ("YouTube", svg('<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/>')),
    ("X", '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'),
    ("Facebook", svg('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>')),
    ("LinkedIn", svg('<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>')),
    ("Instagram", svg('<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>')),
]
SOCIAL_URL = {
    "YouTube": "https://www.youtube.com/channel/UCLE1R-akE4t1lhw_TMGbY2Q",
    "X": "https://x.com/proyectodane",
    "Facebook": "https://www.facebook.com/ProyectoDANE/",
    "LinkedIn": "https://www.linkedin.com/company/proyecto-dane?_l=en_US",
    "Instagram": "https://www.instagram.com/proyectodane/",
}


def page(*, file, title, desc, body, active=None, scripts=()):
    home = "index.html" if file != "index.html" else ""
    def nav_a(label, href, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    nav = "".join([
        nav_a("El proyecto", "el-proyecto.html", "proyecto"),
        nav_a("Aplicaciones", "aplicaciones.html", "apps"),
        nav_a("Contacto", f"{home}#contacto", None),
    ])
    social = "".join(f'<a href="{SOCIAL_URL[n]}" target="_blank" rel="noopener noreferrer" aria-label="{n}">{i}</a>' for n, i in SOCIAL)
    jsonld = f'<script type="application/ld+json">{JSONLD}</script>' if file == "index.html" else ""
    js = "".join(f'<script src="assets/js/{s}" defer></script>' for s in ("menu.js", *scripts))
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}/{"" if file == "index.html" else file}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Proyecto Dane">
<meta property="og:locale" content="es_AR">
<meta property="og:url" content="{BASE}/{"" if file == "index.html" else file}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:alt" content="Niño usando una app en una tablet">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@proyectodane">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="theme-color" content="#B5509E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/styles.css">
{jsonld}
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
{STRIP}
<header class="site-header container">
<a class="logo" href="index.html"><img src="assets/img/logo-proyecto-dane.jpg" width="198" height="53" alt="Proyecto Dane, tecnología para la inclusión"></a>
<button class="menu-btn" type="button" aria-label="Menú" aria-expanded="false" aria-controls="nav-principal"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
<nav id="nav-principal" class="nav" aria-label="Principal">{nav}</nav>
</header>
<main id="contenido">
{body}
</main>
<footer class="footer">
<div class="footer-main container">
<div class="footer-brand"><span class="pill"><img src="assets/img/logo-proyecto-dane.jpg" width="198" height="53" alt="Proyecto Dane, tecnología para la inclusión"></span><span>Aplicaciones para el aprendizaje de niños y jóvenes con discapacidad.</span></div>
<nav class="footer-col" aria-label="Pie"><span class="eyebrow">Navegá</span><a href="el-proyecto.html">El proyecto</a><a href="aplicaciones.html">Aplicaciones</a><a href="{home}#contacto">Contacto</a></nav>
<div class="footer-col"><span class="eyebrow">Contacto</span><span>Rivadavia 717, 8º piso</span><span>(1002) Ciudad de Buenos Aires</span><span>República Argentina</span><a class="tel" href="tel:+541143428034">Tel.: (54 11) 4342-8034</a></div>
<div class="footer-col"><span class="eyebrow">Seguinos</span><div class="social">{social}</div></div>
</div>
<div class="footer-bar container"><div><span>© Proyecto Dane. Todos los derechos reservados.</span><span class="hosted">Hosteado por <a href="https://donweb.com/es-ar/" target="_blank" rel="noopener" aria-label="Donweb (se abre en una pestaña nueva)"><img src="assets/img/logo-donweb.png" width="73" height="32" alt="Donweb"></a></span></div></div>
{STRIP}
</footer>
{js}
</body>
</html>
'''


def app_card(a):
    cats = a["categorias"]
    color = PALETA[sum(map(ord, a["slug"])) % 6]
    tags = "".join(f'<span class="tag" style="background:{CATS[c][0]};color:{CATS[c][1]}">{esc(c)}</span>' for c in cats)
    et = ""
    if a.get("etiqueta") == "Nueva app":
        et = '<span class="tag nueva">Nueva app</span>'
    elif a.get("etiqueta"):
        et = f'<span class="tag reco">{esc(a["etiqueta"])}</span>'
    et = f'<div class="tags">{et}</div>' if et else ""
    play = f'<a class="text-link" href="{esc(a["play"])}" target="_blank" rel="noopener">Descargar en Google Play<span class="sr-only"> (se abre en una pestaña nueva)</span></a>' if a.get("play") else ""
    return f'''<article class="app" data-categorias="{esc("|".join(cats))}">
<div class="app-top"><div class="app-icon" style="--c:{color}"><span aria-hidden="true">{esc(a["nombre"][0])}</span><img src="{a["icono_local"]}" alt="" loading="lazy" width="72" height="72"></div><div class="app-title">{et}<h3>{esc(a["nombre"])}</h3></div></div>
<p>{esc(a["descripcion"])}</p>
<div class="tags">{tags}</div>{play}
</article>'''


# ---------------- INICIO ----------------
destacadas = [("como-pago", "#EE9C44"), ("emocionalmente", "#D992C3"), ("aplicacionlsaenfamilia", "#93D9F7")]
by_slug = {a["slug"]: a for a in apps}
by_slug["aplicacionlsaenfamilia"] = next(a for a in apps if a["nombre"] == "LSA en Familia")
feat = ""
for slug, col in destacadas:
    a = by_slug[slug]
    full = {"como-pago": "assets/img/apps/como-pago-home.png", "emocionalmente": a["icono_local"], "aplicacionlsaenfamilia": "assets/img/apps/lsa-home.png"}
    if slug in full:
        cover = f'<div class="cover full"><img src="{full[slug]}" alt="" loading="lazy"></div>'
    else:
        cover = f'<div class="cover" style="background:{col}"><img src="{a["icono_local"]}" alt="" width="112" height="112"></div>'
    feat += f'''<article class="feature-card">{cover}<div class="body"><h3>{esc(a["nombre"])}</h3><p>{esc(a["descripcion"])}</p></div></article>'''

IMPACTO = [("20", "aplicaciones"), ("+300 mil", "descargas"), ("150", "instituciones que las usan"), ("13", "años de trabajo")]
metrics = "".join(f'<div class="metric"><strong>{n}</strong><span>{l}</span></div>' for n, l in IMPACTO)
ALIADOS = [("Q Services", "qservices.jpg"), ("GlobeMind", "globemind.png"), ("intive", "intive.svg"), ("Globant", "globant.svg"), ("GlobalLogic", "globallogic.png"), ("Nybble Group", "nybble.png"), ("ReservIT", "reservit.png")]
allies = "".join(f'<div class="ally"><img src="assets/img/aliados/{f}" alt="{esc(n)}" loading="lazy" height="48"></div>' for n, f in ALIADOS)

form = '''<form class="form" id="form-contacto" novalidate>
<label>Nombre<input type="text" name="nombre" autocomplete="name" required></label>
<label>Email<input type="email" name="email" autocomplete="email" required></label>
<label>Mensaje<textarea name="mensaje" rows="4" required></textarea></label>
<label class="hp" aria-hidden="true">No completar<input type="text" name="website" tabindex="-1" autocomplete="off"></label>
<button class="btn btn-primary" type="submit">Enviar mensaje</button>
<p class="form-msg" id="form-msg" role="status"></p>
</form>'''

index_body = f'''<section id="inicio" class="hero container">
<div class="hero-text">
<div class="badges"><span class="badge rosa">Organización sin fines de lucro</span><span class="badge amarillo"><svg width="16" height="16" viewBox="0 0 24 24" fill="#6B4A00" aria-hidden="true"><polygon points="12 2 15.1 8.6 22 9.3 16.8 14 18.2 21 12 17.5 5.8 21 7.2 14 2 9.3 8.9 8.6"/></svg>Proyecto de Interés Social</span></div>
<h1>Tecnología para la inclusión</h1>
<p class="lead">Desarrollamos aplicaciones para el aprendizaje de niños y jóvenes con discapacidad, junto a especialistas en educación y programadores.</p>
<div class="actions"><a class="btn btn-primary" href="aplicaciones.html">Conocé las aplicaciones</a><a class="btn btn-outline" href="el-proyecto.html">Conocé el proyecto</a></div>
</div>
<div class="video-wrap"><div class="video">
<video id="video-hero" controls autoplay muted playsinline preload="metadata" aria-label="Charla TED sobre el Proyecto Dane"><source src="https://www.proyectodane.org/wp-content/uploads/2016/03/Charla-TED-edicion480.mp4" type="video/mp4">Tu navegador no puede reproducir este video.</video>
{STRIP.replace('class="brand-strip"', 'class="brand-strip thin"')}
</div></div>
</section>

<section id="reconocimiento" class="container reco">
<div class="head" style="max-width:900px"><span class="eyebrow">Reconocimiento</span><h2>La Legislatura porteña nos reconoció como <span>Proyecto de Interés Social</span></h2></div>
<img src="assets/img/banner-legislatura-interes-social.png" width="1553" height="236" alt="Legislatura de la Ciudad Autónoma de Buenos Aires y Proyecto Dane: la Legislatura porteña nos reconoció como Proyecto de Interés Social">
</section>

<section id="el-proyecto" class="section alt"><div class="container split">
<div class="hero-art" role="img" aria-label="Tablet con la aplicación Dibugrama rodeada de íconos de las aplicaciones del Proyecto Dane">
<span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span>
<img class="tablet" src="assets/img/foto-tablet-dibugrama.jpg" width="599" height="409" alt="" loading="lazy">
<img class="ico i1" src="assets/img/apps/sonigrama.jpg" width="150" height="150" alt="" loading="lazy">
<img class="ico i2" src="assets/img/apps/emocionalmente.jpg" width="150" height="150" alt="" loading="lazy">
<img class="ico i3" src="assets/img/apps/grupolandia.jpg" width="150" height="150" alt="" loading="lazy">
<img class="ico i4" src="assets/img/apps/superapp.jpg" width="150" height="150" alt="" loading="lazy">
<span class="chip c1">100% gratuitas</span><span class="chip c2">+300 mil descargas</span>
</div>
<div class="split-text"><span class="eyebrow">El proyecto</span><h2>Educación y tecnología, trabajando juntas</h2>
<p>Especialistas en educación y programadores trabajan en conjunto para crear aplicaciones adaptadas a las necesidades concretas de quienes las usan. Integramos el software a la educación para innovar en la manera de enseñar contenidos.</p>
<a class="text-link" href="el-proyecto.html" style="align-self:flex-start">Conocé nuestra historia</a></div>
</div></section>

<section id="aplicaciones" class="section container stack" style="gap:48px">
<div class="head-row"><div class="head" style="max-width:640px"><span class="eyebrow">Aplicaciones destacadas</span><h2>Apps pensadas para aprender</h2></div><a class="text-link" href="aplicaciones.html">Ver todas</a></div>
<div class="cards-3">{feat}</div>
</section>

<section id="impacto" class="impact"><div class="container"><h2 style="max-width:640px">Nuestro impacto en números</h2><div class="metrics">{metrics}</div></div></section>

<section class="allies" aria-label="Aliados"><div class="container"><span class="allies-title">Nos acompañan</span><div class="allies-grid">{allies}</div></div></section>

<section id="contacto" class="section container contact">
<div class="contact-text"><span class="eyebrow">Contacto</span><h2>Escribinos, te respondemos</h2><p>Rivadavia 717, 8º piso, (1002) Ciudad de Buenos Aires, República Argentina · Tel.: <a href="tel:+541143428034">(54 11) 4342-8034</a></p></div>
{form}
</section>'''

# ---------------- EL PROYECTO ----------------
def ico(c, inner):
    return f'<span class="ico"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg></span>'
define = [
    ("#F6E6F1", "#7A2E69", '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>', "Inéditas", "Nuestras aplicaciones son inéditas en el mercado argentino y latinoamericano."),
    ("#FDF0D0", "#6B4A00", '<polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>', "Gratuitas", "Todas se descargan sin costo, para que lleguen a quienes las necesitan."),
    ("#DDF1FB", "#1F4FB5", '<rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/>', "En tu dispositivo", "Se instalan en cualquier dispositivo móvil de última generación."),
]
define_html = "".join(f'<div class="define-card" style="background:{bg}">{ico(c, i)}<h2>{t}</h2><p>{p}</p></div>' for bg, c, i, t, p in define)
steps = [("01", "Facilitamos el aprendizaje", "Desarrollamos proyectos tecnológicos innovadores que tienen en cuenta lo que necesitan las personas con discapacidad para aprender."),
         ("02", "Mejoramos la calidad de vida", "Usamos la tecnología para resolver situaciones de la vida cotidiana y promover una mejor calidad de vida, para ellos y para su familia."),
         ("03", "Capacitamos y difundimos", "Implementamos capacitación y difusión sobre las TIC en el ámbito de la discapacidad.")]
steps_html = "".join(f'<div class="step"><span class="num">{n}</span><h3>{t}</h3><p>{p}</p></div>' for n, t, p in steps)
awards_html = ""
for i, p in enumerate(premios):
    dest = " destacado" if p["titulo"] == "Interés Social" else ""
    awards_html += f'<article class="award{dest}" style="--c:{PALETA[i % 6]}"><span class="year">{p["anio"]}</span><h3>{esc(p["titulo"])}</h3><p>{esc(p["institucion"])}</p></article>'

team_section = ""
if equipo:
    cards = ""
    for m in equipo:
        n = esc(m["nombre"].strip() or "[Nombre y apellido]")
        m = dict(m, puesto=m["puesto"].strip() or "[Puesto en el equipo]")
        foto = f'<img src="{esc(m["foto"])}" alt="" loading="lazy">' if m.get("foto") else '<svg width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="#B5509E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>'
        li = f'<a class="linkedin" href="{esc(m["linkedin"])}" target="_blank" rel="noopener noreferrer" aria-label="Perfil de LinkedIn de {n}">{LINKEDIN}LinkedIn</a>' if m.get("linkedin") else ""
        cards += f'<article class="member"><div class="photo">{foto}</div><div><h3>{n}</h3><span class="puesto">{esc(m["puesto"])}</span></div>{li}</article>'
    team_section = f'''<section id="equipo" class="section alt"><div class="container stack" style="gap:48px"><div class="head"><span class="eyebrow">Equipo de trabajo</span><h2>Las personas detrás de Dane</h2><p class="lead">Somos un grupo de profesionales de distintas áreas que trabaja en conjunto para integrar la tecnología informática a la educación de niños y jóvenes con discapacidad. Nuestra energía está puesta en lograr que la tecnología sea una herramienta de inclusión.</p></div><div class="team">{cards}</div></div></section>'''

proyecto_body = f'''<section class="page-head container">
<div class="page-head-text">
<nav class="crumbs" aria-label="Ruta de navegación"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><span>El proyecto</span></nav>
<h1>El proyecto</h1>
<p class="subhead">Desarrollo de aplicaciones para niños y jóvenes con discapacidad.</p>
<p class="lead">Nuestro objetivo es ofrecer tecnología para la inclusión. Desarrollamos proyectos tecnológicos innovadores que facilitan el aprendizaje de las personas, contemplando los aspectos necesarios para quienes tienen alguna discapacidad.</p>
</div>
<div class="page-head-photo"><img src="assets/img/foto-nene-tablet.jpg" width="1014" height="653" alt="Niño concentrado usando una app en una tablet"></div>
</section>

<section class="container define">{define_html}</section>

<section class="section alt"><div class="container stack" style="gap:48px"><div class="head"><span class="eyebrow">Qué hacemos</span><h2>Tecnología al servicio de la vida cotidiana</h2></div><div class="steps">{steps_html}</div></div></section>

<section id="reconocimientos" class="section container stack" style="gap:48px"><div class="head" style="max-width:760px"><span class="eyebrow">Reconocimientos y premios</span><h2>Un camino acompañado por muchos</h2><p class="lead">Desde que empezamos, muchas empresas, ONG, instituciones académicas y voluntarios nos ayudaron a desarrollar las aplicaciones, y seguimos trabajando juntos a diario. Estos son los premios y reconocimientos que recibimos en estos años.</p></div><div class="awards">{awards_html}</div></section>

{team_section}

<section class="section container tech">
<div class="tech-main"><span class="eyebrow">Tecnología aplicada</span><h2>Pensada para el aula y para la familia</h2><p>La tecnología informática evoluciona con los años, pero muchos desarrolladores no tienen en cuenta los matices que enfrentan los docentes cuando trabajan en el aula con chicos que tienen una discapacidad puntual.</p><img src="assets/img/foto-tablet-dibugrama.jpg" width="1058" height="728" loading="lazy" alt="Tablet con la aplicación Dibugrama, de Proyecto Dane"></div>
<div class="tech-list">
<div><h3>Intuitiva</h3><p>A diferencia de una computadora con mouse, la tablet es un dispositivo muy intuitivo de usar. Esa es una de las principales ventajas de llevar las aplicaciones a la enseñanza.</p></div>
<div><h3>Amigable</h3><p>Las herramientas son muy amigables y permiten a los chicos desarrollar habilidades a la par de sus compañeros, y convertirse en nativos digitales, algo imprescindible en el mundo de hoy.</p></div>
<div><h3>Cotidiana y en familia</h3><p>Desde muy temprana edad, los chicos se conectan con situaciones de la vida cotidiana, reales y simuladas, que desarrollan habilidades cognitivas, sociales, de comunicación y de autoabastecimiento. Las actividades también integran a la familia.</p></div>
</div>
</section>

<section class="cta"><div class="container"><h2>Conocé las aplicaciones del Proyecto Dane</h2><a class="btn btn-accent" href="aplicaciones.html">Ver las aplicaciones</a></div></section>'''

# ---------------- APLICACIONES ----------------
skills = ["Funciones ejecutivas", "Memoria", "Atención", "Lenguaje", "Lectura y escritura", "Orientación espaciotemporal", "Psicomotricidad"]
skills_html = "".join(f'<span style="--c:{PALETA[i % 6]}">{s}</span>' for i, s in enumerate(skills))
chips = '<button class="chip" type="button" data-cat="" aria-pressed="true">Todas</button>' + "".join(
    f'<button class="chip" type="button" data-cat="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in CATS)
# Apps visibles en aplicaciones.html (el resto sigue en data/apps.json pero queda oculto)
VISIBLES = {"como-pago", "emocionalmente", "lsa-familia-lengua-senas-argentina-apple-store", "aplicacionlsaenfamilia", "comunicat", "sonigrama"}
apps_vis = [a for a in apps if a["slug"] in VISIBLES]
cards_html = "\n".join(app_card(a) for a in apps_vis)

apps_body = f'''<section class="page-head simple container">
<nav class="crumbs" aria-label="Ruta de navegación"><a href="index.html">Inicio</a><span aria-hidden="true">/</span><span>Aplicaciones</span></nav>
<h1>Aplicaciones</h1>
<p class="subhead">Apps inclusivas para que las usen quienes tienen alguna discapacidad.</p>
<p class="lead">Están pensadas para niños, jóvenes y, en algunos casos, personas adultas. Las de enfoque académico cubren desde el nivel inicial hasta el secundario. Hoy tenemos más de 15 aplicaciones desarrolladas, y además sugerimos otras que probamos nosotros.</p>
</section>

<section class="container info-grid">
<div class="info-card"><h2>Qué habilidad desarrolla cada app</h2><p>En cada aplicación se detalla el objetivo de la actividad y la habilidad cognitiva que trabaja:</p><div class="skills">{skills_html}</div></div>
<div class="info-card"><h2>Dónde se pueden usar</h2><p>De forma individual o grupal, en el aula, en un espacio terapéutico, fuera de la escuela y también en el hogar. Cada grupo de apps tiene distintos niveles de complejidad y características que las hacen únicas frente a las que se encuentran en las tiendas.</p></div>
</section>

<section class="notice"><div class="container">
<div class="notice-text"><h2>Descargá las apps, es gratis</h2><p>Todas las aplicaciones del Proyecto Dane son gratuitas. Encontralas en Google Play y en el App Store.</p></div>
<div class="stores"><a href="https://play.google.com/store/apps/developer?id=Proyecto+DANE" target="_blank" rel="noopener" aria-label="Disponible en Google Play"><img src="assets/img/badge-google-play.png" alt="Disponible en Google Play"></a><a href="https://apps.apple.com/us/developer/fundaci%C3%B3n-tinc/id1552917309" target="_blank" rel="noopener" aria-label="Descargar en el App Store (se abre en una pestaña nueva)"><img src="assets/img/badge-app-store.png" alt="Descargar en el App Store"></a></div>
</div></section>

<section id="listado" class="section container stack" style="gap:32px">
<div class="head"><span class="eyebrow">Todas las aplicaciones</span><h2>Elegí por categoría</h2></div>
<div class="filters" role="group" aria-label="Filtrar por categoría">{chips}</div>
<p class="lead" id="apps-count" role="status" aria-live="polite" style="font-size:16px">{len(apps_vis)} aplicaciones</p>
<div class="apps">
{cards_html}
</div>
</section>'''

pages = [
    ("index.html", "Proyecto Dane | Tecnología para la inclusión", "Aplicaciones gratuitas para el aprendizaje de niños y jóvenes con discapacidad. Proyecto de Interés Social, Legislatura porteña.", index_body, None, ("contacto.js", "video.js")),
    ("el-proyecto.html", "El proyecto | Proyecto Dane", "Desarrollo de aplicaciones para niños y jóvenes con discapacidad: qué hacemos, premios, equipo y tecnología aplicada.", proyecto_body, "proyecto", ()),
    ("aplicaciones.html", "Aplicaciones | Proyecto Dane", "Apps inclusivas, gratuitas e inéditas para quienes tienen alguna discapacidad. Filtrá por categoría.", apps_body, "apps", ("filtros-apps.js",)),
]
for f, t, d, b, act, sc in pages:
    (ROOT / f).write_text(page(file=f, title=t, desc=d, body=b, active=act, scripts=sc))
    print("ok", f)

(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
urls = "".join(f"  <url><loc>{BASE}/{'' if f == 'index.html' else f}</loc></url>\n" for f, *_ in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
