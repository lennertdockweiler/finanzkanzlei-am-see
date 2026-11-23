"""Gemeinsame Bausteine (Head, Header, Footer, Formular, Icons)."""

import os

DOMAIN = "https://finanzkanzlei-am-see.de"
# PREVIEW=1 → noindex für die Vorschau (z. B. GitHub Pages). Live-Build ohne PREVIEW erzeugen!
PREVIEW = os.environ.get("PREVIEW") == "1"
# THEME=blau → Farbvariante in Unterordner variante-<theme>/ mit zusätzlichem Stylesheet
THEME = os.environ.get("THEME", "").strip()
VARIANTS = [("", "Sand"), ("blau", "Blau")]
PHONE = "07551 93771-0"
PHONE_HREF = "+497551937710"
MAIL = "info@fksee.de"

ICON_CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M6 10.5l2.6 2.6L14 7.6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5h3l1.5 4-2 1.3a11 11 0 0 0 6.1 6.1l1.3-2 4 1.5v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# Bildmarke: Boje auf der Wasserlinie (Platzhalter für das Kompass-Signet)
LOGO_MARK = '''<svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">
  <circle cx="20" cy="20" r="19" fill="#163c3e"/>
  <path d="M5 24c3 0 3-1.6 6-1.6s3 1.6 6 1.6 3-1.6 6-1.6 3 1.6 6 1.6 3-1.6 6-1.6" fill="none" stroke="#f3eee4" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M5 29c3 0 3-1.6 6-1.6s3 1.6 6 1.6 3-1.6 6-1.6 3 1.6 6 1.6" fill="none" stroke="#b9ccc6" stroke-width="1.2" stroke-linecap="round" opacity=".7"/>
  <circle cx="20" cy="15" r="5" fill="#ec7a45"/>
</svg>'''

NAV = [
    ("baufinanzierung.html", "Baufinanzierung"),
    ("kapitalanlagen.html", "Kapitalanlagen"),
    ("vermoegen.html", "Vermögen"),
    ("standorte.html", "Standorte"),
    ("ueber-uns.html", "Über uns"),
]

LOCATIONS = [
    # slug, Name, Adresse, Ansprechperson, Telefon, Tel-href, E-Mail, Zeiten, HQ
    ("ueberlingen", "Überlingen", "Hägerstraße 1<br>88662 Überlingen", "Zentrale · Achim Niess, Bernd Schatz, Christopher Schreiner u. a.", "07551 93771-0", "+497551937710", "info@fksee.de", "Mo–Fr 9–16 Uhr und nach Vereinbarung", True),
    ("konstanz", "Konstanz", "Line-Eid-Str. 6<br>78467 Konstanz", "Andreas Scholl · Spezialist für Grenzgänger", "07531 58490 96", "+4975315849096", "andreas.scholl@drklein.de", "Termine nach Vereinbarung", False),
    ("radolfzell", "Radolfzell", "Löwengasse 10<br>78315 Radolfzell", "Christoph Wohlfahrt, Julian Herrmann", "07551 93771-15", "+4975519377115", "c.wohlfahrt@fksee.de", "Termine nach Vereinbarung", False),
    ("stockach", "Stockach", "Kirchhalde 3<br>78333 Stockach", "Daniel Matt, Sebastian Blum", "07771 634013 31", "+497771634013 31".replace(" ", ""), "daniel.matt@drklein.de", "Termine nach Vereinbarung", False),
    ("salem", "Salem", "[[ERSETZEN: Adresse Standort Salem]]", "[[ERSETZEN: Ansprechperson Salem]]", "07551 93771-0", "+497551937710", "info@fksee.de", "Termine nach Vereinbarung", False),
    ("meersburg", "Meersburg", "[[ERSETZEN: Adresse Standort Meersburg]]", "Thomas Neumann · Vermögen", "07551 93771-11", "+4975519377111", "t.neumann@fksee.de", "Termine nach Vereinbarung", False),
    ("friedrichshafen", "Friedrichshafen", "Karlstr. 1<br>88045 Friedrichshafen", "Karin Brodbeck", "07541 3979058 55", "+4975413979058 55".replace(" ", ""), "karin.brodbeck@drklein.de", "Termine nach Vereinbarung", False),
    ("ravensburg", "Ravensburg", "Marienplatz 61<br>88212 Ravensburg", "Marco Haase, Marc Wiedenmann", "0751 18527170", "+4975118527170", "marco.haase@drklein.de", "Mo–Fr 9–17 Uhr und nach Vereinbarung", False),
    ("donaueschingen", "Donaueschingen", "Villinger Str. 17<br>78166 Donaueschingen", "Martin Mantel, Niklas Werbig, Ingrid Sayer, Tobias Wild", "0771 229679 28", "+4977122967928", "martin.mantel@drklein.de", "Mo–Fr 8–18 Uhr und nach Vereinbarung", False),
    ("trossingen", "Trossingen", "[[ERSETZEN: Adresse Standort Trossingen]]", "Peter Hirsch", "07425 31613", "+49742531613", "peter.hirsch@drklein.de", "Termine nach Vereinbarung", False),
    ("albstadt", "Albstadt", "[[ERSETZEN: Adresse Standort Albstadt]]", "Achim Traub", "07471 1805412", "+4974711805412", "achim.traub@drklein.de", "Termine nach Vereinbarung", False),
]

# Kartenkoordinaten (aus Längen-/Breitengrad projiziert, viewBox 40 30 720 600)
MAP_POS = {
    "ueberlingen": (408, 397, "l"), "salem": (469, 394, "r"), "meersburg": (464, 454, "r"),
    "friedrichshafen": (570, 484, "r"), "ravensburg": (635, 390, "l"), "konstanz": (413, 480, "b"),
    "radolfzell": (312, 420, "l"), "stockach": (333, 337, "l"), "donaueschingen": (76, 262, "r"),
    "trossingen": (141, 172, "r"), "albstadt": (338, 67, "r"),
}
LAKE_OBER = "M690 596 L670 566 L630 544 L600 525 L564 489 L514 478 L479 465 L461 455 L441 433 L408 403 L378 379 L358 361 L345 366 L365 386 L388 411 L406 433 L423 457 L418 474 L416 484 L444 502 L479 525 L519 551 L544 585 L575 616 L610 611 L640 604 Z"
LAKE_UNTER = "M398 474 L363 471 L328 474 L292 480 L260 478 L267 465 L297 450 L305 439 L315 421 L328 425 L343 441 L368 457 L388 465 Z"


def head(title, desc, path, extra_head=""):
    canonical = f"{DOMAIN}/{'' if path == 'index.html' else path}"
    font_preload = ('  <link rel="preload" href="assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>\n'
                    if THEME == "blau" else
                    '  <link rel="preload" href="assets/fonts/fraunces-var.woff2" as="font" type="font/woff2" crossorigin>\n'
                    '  <link rel="preload" href="assets/fonts/instrument-sans-var.woff2" as="font" type="font/woff2" crossorigin>\n')
    theme_css = f'  <link rel="stylesheet" href="assets/css/theme-{THEME}.css">\n' if THEME else ""
    robots = '  <meta name="robots" content="noindex, nofollow">\n' if PREVIEW and "robots" not in extra_head else ""
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#f3eee4">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Finanzkanzlei am See">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og-image.png">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">

{font_preload}  <link rel="stylesheet" href="assets/css/style.css">
{theme_css}  <script src="assets/js/main.js" defer></script>
{robots}{extra_head}</head>
'''


CUR = ' aria-current="page"'


def preview_bar(active):
    """Nur in der Vorschau: Hinweis + Umschalter zwischen den Farbvarianten derselben Seite."""
    if not PREVIEW or not active:
        return ""
    links = []
    for theme, label in VARIANTS:
        here = "variante-" + THEME + "/" if THEME else ""
        target = "variante-" + theme + "/" if theme else ""
        href = ("../" if here else "") + target + active
        cur = ' aria-current="true"' if theme == THEME else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return ('  <div class="preview-bar" role="note"><span><span class="preview-bar__long">Entwurf zur Abstimmung · </span>Farbvariante:</span> '
            + " ".join(links) + "</div>\n")


def header(active):
    cta = "#formular" if active == "index.html" else "kontakt.html#formular"
    items = "\n".join(
        f'          <li><a href="{href}"{CUR if href == active else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f'''<body>
  <a class="skip-link" href="#inhalt">Zum Inhalt springen</a>
{preview_bar(active)}
  <header class="site-header">
    <div class="container site-header__inner">
      <a class="brand" href="index.html" aria-label="Finanzkanzlei am See – zur Startseite">
        {LOGO_MARK}
        <span class="brand__name">Finanzkanzlei am See<small>Finanzierung · Anlage · Vermögen</small></span>
      </a>

      <a class="header-call" href="tel:{PHONE_HREF}" aria-label="Anrufen: {PHONE}">{ICON_PHONE}</a>

      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
        <span class="nav-toggle__icon" aria-hidden="true"></span>
        <span class="nav-toggle__label">Menü</span>
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Hauptnavigation">
        <ul>
{items}
        </ul>
        <div class="site-nav__cta">
          <a class="btn btn--accent btn--lg" href="{cta}">Kostenloses Erstgespräch anfragen</a>
          <a class="btn btn--ghost" href="tel:{PHONE_HREF}">{ICON_PHONE} {PHONE}</a>
        </div>
      </nav>

      <a class="header-phone" href="tel:{PHONE_HREF}"><span>Mo–Fr 9–16 Uhr</span><strong>{PHONE}</strong></a>
      <a class="btn btn--accent header-cta" href="{cta}"{CUR if active == "kontakt.html" else ""}>Erstgespräch anfragen</a>
    </div>
  </header>
'''


WATERLINE = '''<svg class="waterline" viewBox="0 0 1200 24" preserveAspectRatio="none" aria-hidden="true"><path d="M0 12 Q 25 4 50 12 T 100 12 T 150 12 T 200 12 T 250 12 T 300 12 T 350 12 T 400 12 T 450 12 T 500 12 T 550 12 T 600 12 T 650 12 T 700 12 T 750 12 T 800 12 T 850 12 T 900 12 T 950 12 T 1000 12 T 1050 12 T 1100 12 T 1150 12 T 1200 12" fill="none" stroke="currentColor" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg>'''


def footer():
    locs = "\n".join(
        f'            <li><a href="standorte.html#{slug}">{name}</a></li>' for slug, name, *_ in LOCATIONS
    )
    return f'''
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <p class="footer-claim">Bei Geld fängt die <em>Freundschaft</em> an.</p>
          <address>
            Finanzkanzlei am See GmbH<br>
            Hägerstraße 1, 88662 Überlingen<br>
            <a href="tel:{PHONE_HREF}">{PHONE}</a> · <a href="mailto:{MAIL}">{MAIL}</a>
          </address>
        </div>
        <nav aria-label="Leistungen">
          <h2>Leistungen</h2>
          <ul>
            <li><a href="baufinanzierung.html">Baufinanzierung</a></li>
            <li><a href="baufinanzierung.html#anschluss">Anschlussfinanzierung</a></li>
            <li><a href="baufinanzierung.html#gewerbe">Gewerbliche Finanzierung</a></li>
            <li><a href="kapitalanlagen.html">Kapitalanlagen</a></li>
            <li><a href="vermoegen.html">Vermögen</a></li>
          </ul>
        </nav>
        <nav aria-label="Standorte">
          <h2>11 Standorte</h2>
          <ul class="loc-list">
{locs}
          </ul>
        </nav>
        <nav aria-label="Unternehmen">
          <h2>Kanzlei</h2>
          <ul>
            <li><a href="ueber-uns.html">Über uns</a></li>
            <li><a href="ueber-uns.html#karriere">Karriere</a></li>
            <li><a href="ueber-uns.html#stiftung">Kinder- und Jugendstiftung</a></li>
            <li><a href="kontakt.html">Kontakt</a></li>
          </ul>
        </nav>
      </div>
      <div class="footer-legal">
        <p class="mb-0">© <span data-year>2026</span> Finanzkanzlei am See GmbH</p>
        <ul>
          <li><a href="impressum.html">Impressum</a></li>
          <li><a href="datenschutz.html">Datenschutz</a></li>
          <li><a href="impressum.html#erstinformation">Erstinformation &amp; Erlaubnisse</a></li>
        </ul>
      </div>
    </div>
  </footer>
</body>
</html>
'''


def cta_band(title, text, anliegen=""):
    q = f"?anliegen={anliegen}" if anliegen else ""
    return f'''
    <section class="section section--tight" aria-labelledby="cta-title">
      <div class="container">
        <div class="cta-band on-lake" data-reveal>
          <div>
            <h2 id="cta-title">{title}</h2>
            <p class="mt-4">{text}</p>
          </div>
          <div>
            <div class="cta-band__actions">
              <a class="btn btn--accent btn--lg" href="kontakt.html{q}#formular">Kostenloses Erstgespräch anfragen</a>
              <a class="btn btn--ghost" href="tel:{PHONE_HREF}">{ICON_PHONE} {PHONE}</a>
            </div>
            <ul class="trust-line">
              <li>{ICON_CHECK} Für Sie kostenlos</li>
              <li>{ICON_CHECK} Unverbindlich</li>
              <li>{ICON_CHECK} Vor Ort oder per Video</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
'''


def contact_form(prefix):
    """Beratungsformular. Netlify Forms; Honeypot 'bot-field'."""
    opts = "\n".join(f'                <option value="{name}">{name}</option>' for _, name, *_ in LOCATIONS)
    chips = [("kauf", "Kauf oder Neubau"), ("anschluss", "Anschlussfinanzierung"), ("modernisierung", "Modernisierung"),
             ("gewerbe", "Gewerbe"), ("kapitalanlage", "Kapitalanlage"), ("vermoegen", "Vermögen"), ("sonstiges", "Etwas anderes")]
    chip_html = "\n".join(
        f'''              <label class="choice"><input type="radio" name="anliegen" value="{v}" required data-msg="anliegen"><span>{l}</span></label>'''
        for v, l in chips)
    p = prefix
    return f'''
          <form class="form" name="beratung" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" data-form novalidate>
            <input type="hidden" name="form-name" value="beratung">
            <p class="hp-field" aria-hidden="true"><label>Bitte leer lassen <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>

            <fieldset class="choice-group">
              <legend>Worum geht es?</legend>
              <div class="choices">
{chip_html}
              </div>
              <p class="field__error" id="{p}-anliegen-error" aria-live="polite"></p>
            </fieldset>

            <div class="field">
              <label for="{p}-name">Ihr Name</label>
              <input class="input" id="{p}-name" name="name" type="text" autocomplete="name" required data-msg="name" aria-describedby="{p}-name-error">
              <p class="field__error" id="{p}-name-error" aria-live="polite"></p>
            </div>

            <div class="form__row form__row--2">
              <div class="field">
                <label for="{p}-tel">Telefon</label>
                <input class="input" id="{p}-tel" name="telefon" type="tel" autocomplete="tel" inputmode="tel" pattern="[0-9 +\\/\\(\\)\\-]{{6,}}" required data-msg="contact" aria-describedby="{p}-tel-hint {p}-tel-error">
                <span class="hint" id="{p}-tel-hint">Telefon oder E-Mail genügt.</span>
                <p class="field__error" id="{p}-tel-error" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="{p}-mail">E-Mail</label>
                <input class="input" id="{p}-mail" name="email" type="email" autocomplete="email" pattern="[^@\\s]+@[^@\\s]+\\.[^@\\s]+" required data-msg="contact" aria-describedby="{p}-mail-error">
                <p class="field__error" id="{p}-mail-error" aria-live="polite"></p>
              </div>
            </div>

            <div class="field">
              <label for="{p}-ort">Wo möchten Sie sich beraten lassen? <span class="optional">(optional)</span></label>
              <select class="select" id="{p}-ort" name="standort">
                <option value="egal">Egal – Hauptsache bald</option>
                <option value="video">Per Video oder Telefon</option>
{opts}
              </select>
            </div>

            <div class="field">
              <label for="{p}-msg">Was sollen wir vorab wissen? <span class="optional">(optional)</span></label>
              <textarea class="textarea" id="{p}-msg" name="nachricht" rows="4" maxlength="2000" placeholder="z. B. Kaufpreis, Zinsbindung läuft aus im …, bevorzugte Rückrufzeit"></textarea>
            </div>

            <div class="form-status" role="status" aria-live="polite" tabindex="-1"></div>

            <div class="form__submit">
              <button class="btn btn--accent btn--lg" type="submit">Kostenloses Erstgespräch anfragen</button>
              <p class="form__privacy">Wir nutzen Ihre Angaben nur, um Ihre Anfrage zu beantworten. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>. Die Beratung ist kostenlos und unverbindlich.</p>
            </div>
          </form>
'''


def map_svg(link_prefix=""):
    locs = []
    for slug, name, *_rest in LOCATIONS:
        x, y, side = MAP_POS[slug]
        hq = slug == "ueberlingen"
        r = 9 if hq else 6.5
        if side == "r":
            tx, ty, anchor = x + 14, y + 5, "start"
        elif side == "l":
            tx, ty, anchor = x - 14, y + 5, "end"
        else:
            tx, ty, anchor = x, y + 26, "middle"
        locs.append(
            f'      <a class="loc{" loc--hq" if hq else ""}" href="{link_prefix}#{slug}"><title>{name}{" – Zentrale" if hq else ""}</title>'
            f'<circle cx="{x}" cy="{y}" r="{r}"/><text x="{tx}" y="{ty}" text-anchor="{anchor}">{name}</text></a>'
        )
    locs_html = "\n".join(locs)
    return f'''<svg class="map" viewBox="20 20 720 620" role="group" aria-label="Schematische Karte: 11 Standorte zwischen Albstadt, Donaueschingen und Friedrichshafen">
      <path class="region" d="M60 230 C 140 80, 300 20, 420 60 S 700 260, 690 420"/>
      <path class="lake" d="{LAKE_OBER}"/>
      <path class="lake" d="{LAKE_UNTER}"/>
      <text class="map__label" x="560" y="575" aria-hidden="true">Bodensee</text>
{locs_html}
    </svg>'''
