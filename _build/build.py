"""Erzeugt die statischen HTML-Seiten der Finanzkanzlei am See."""
import json
from urllib.parse import quote
import sys
from pathlib import Path
from partials import *  # noqa: F401,F403

OUT = Path(sys.argv[1])

def ticks(items):
    return "<ul class=\"ticks\">" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def breadcrumb(name):
    return f'''<nav class="breadcrumb" aria-label="Brotkrumen"><ol><li><a href="index.html">Start</a></li><li aria-current="page">{name}</li></ol></nav>'''

def faq(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><div class="faq__body"><p>{a}</p></div></details>' for q, a in items) + "</div>"

def faq_ld(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

def ld(*objs):
    return "".join(f'  <script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in objs)

ORG_LD = {
    "@context": "https://schema.org",
    "@type": "FinancialService",
    "@id": f"{DOMAIN}/#org",
    "name": "Finanzkanzlei am See GmbH",
    "slogan": "Bei Geld fängt die Freundschaft an",
    "url": DOMAIN + "/",
    "logo": f"{DOMAIN}/favicon.svg",
    "telephone": "+49 7551 93771-0",
    "email": MAIL,
    "foundingDate": "2012",
    "address": {"@type": "PostalAddress", "streetAddress": "Hägerstraße 1", "postalCode": "88662", "addressLocality": "Überlingen", "addressRegion": "Baden-Württemberg", "addressCountry": "DE"},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "16:00"}],
    "areaServed": ["Bodensee", "Oberschwaben", "Südbaden"],
    "knowsAbout": ["Baufinanzierung", "Anschlussfinanzierung", "Forward-Darlehen", "Kapitalanlage-Immobilien", "Vermögensverwaltung"],
}

FAQ_MAIN = [
    ("Was kostet mich die Beratung?",
     "Nichts. Kein Honorar, keine Bearbeitungsgebühr. Unsere Arbeit wird von dem Kreditinstitut vergütet, für das Sie sich am Ende entscheiden. Entscheiden Sie sich gegen alle Angebote, kostet Sie das ebenfalls nichts."),
    ("Warum nicht einfach zu meiner Hausbank?",
     "Ihre Hausbank kann Ihnen nur ihre eigenen Konditionen anbieten. Wir vergleichen über 600 Banken und Bausparkassen – und kooperieren mit nahezu allen regionalen Instituten. Gut möglich, dass Ihre Hausbank also auch in unserem Vergleich auftaucht. Dann wissen Sie wenigstens, dass sie wirklich die beste ist."),
    ("Wann sollte ich mich um die Anschlussfinanzierung kümmern?",
     "Früher, als die meisten denken: Mit einem Forward-Darlehen sichern Sie sich den Zins bis zu 60 Monate vor Ablauf Ihrer Zinsbindung. Ein Blick in Ihren Darlehensvertrag genügt – bringen Sie ihn einfach zum Erstgespräch mit."),
    ("Welche Unterlagen brauche ich?",
     "Zum Erstgespräch: keine. Danach bekommen Sie von uns eine Liste, abgestimmt auf Ihr Vorhaben – meist Einkommensnachweise, eine Selbstauskunft und Angaben zur Immobilie. Wir prüfen alles, bevor es an eine Bank geht."),
    ("Ich arbeite in der Schweiz. Geht das trotzdem?",
     "Ja. In Konstanz berät Sie Andreas Scholl, der sich seit 2017 auf Finanzierungen für Grenzgänger mit Franken-Einkommen und auf Kapitalanleger aus der Schweiz spezialisiert hat."),
    ("Muss ich dafür ins Büro kommen?",
     "Nein. Sie können uns in einem unserer 11 Büros besuchen, wir telefonieren oder sprechen per Video. Sie können das auch kombinieren: erstes Gespräch per Video, Unterschrift vor Ort."),
    ("Bin ich nach dem Erstgespräch an Sie gebunden?",
     "Nein. Sie bekommen eine ehrliche Einschätzung und entscheiden dann in Ruhe, ob und wie es weitergeht."),
]

# ───────────────────────────── Startseite ─────────────────────────────
def page_index():
    trust = f'''<ul class="trust-line">
              <li>{ICON_CHECK} Für Sie kostenlos</li>
              <li>{ICON_CHECK} Über 600 Banken im Vergleich</li>
              <li>{ICON_CHECK} Seit 2012 am Bodensee</li>
            </ul>'''
    locs = "".join(f'<li><a href="standorte.html#{s}">{n}</a></li>' for s, n, *_ in LOCATIONS)
    body = f'''
  <main id="inhalt">
    <!-- HERO ─ Signature-Element "1 aus 600" -->
    <section class="hero" aria-labelledby="hero-title">
      <div class="container hero__grid">
        <div>
          <p class="eyebrow">Baufinanzierung am Bodensee · 11 Standorte</p>
          <h1 id="hero-title">Ihre Baufinanzierung – aus über 600 Banken <em>die eine,</em> die passt.</h1>
          <p class="lead">Wir sind Ex-Banker und keiner Bank verpflichtet. Wir vergleichen, verhandeln und bereiten Ihre Unterlagen so vor, dass die Bank kaum Rückfragen hat. Sie zahlen dafür nichts.</p>
          <div class="hero__actions">
            <a class="btn btn--accent btn--lg" href="#formular">Kostenloses Erstgespräch anfragen</a>
            <a class="btn btn--ghost btn--lg" href="tel:{PHONE_HREF}">{ICON_PHONE} {PHONE}</a>
          </div>
          {trust}
        </div>

        <figure class="buoyfield" data-buoyfield>
          <svg class="buoyfield__svg" viewBox="0 -80 600 484" aria-hidden="true">
            <g class="buoy-group">
              <line class="buoy-line" x1="430" y1="-20" x2="430" y2="240"/>
              <circle class="buoy-ring" cx="430" cy="250" r="8"/>
              <circle class="buoy-ring buoy-ring--2" cx="430" cy="250" r="8"/>
              <circle class="buoy" cx="430" cy="250" r="8"/>
            </g>
            <text class="buoyfield__label" x="418" y="-48" text-anchor="end">Ihre Bank</text>
            <text class="buoyfield__label-soft" x="418" y="-28" text-anchor="end">1 von über 600 – passend zu Ihnen</text>
          </svg>
          <figcaption>
            <span><strong>Jeder Punkt</strong> steht für eine Bank oder Bausparkasse, die wir für Sie vergleichen.</span>
          </figcaption>
        </figure>
      </div>
    </section>

    <!-- KENNZAHLEN -->
    <!-- [[ERSETZEN: Kennzahlen prüfen – Werte stammen von der bisherigen Website (Stand Nov. 2026)]] -->
    <section class="section--tight" aria-label="Die Finanzkanzlei in Zahlen">
      <div class="container">
        <dl class="stats" data-reveal>
          <div class="stat"><dt>Banken und Bausparkassen im Vergleich</dt><dd>600<small>+</small></dd></div>
          <div class="stat"><dt>Finanzierungsvolumen pro Jahr</dt><dd>500<small>Mio. €</small></dd></div>
          <div class="stat"><dt>Finanzierungs-, Anlage- und Immobilien­spezialisten</dt><dd>40</dd></div>
          <div class="stat"><dt>Standorte zwischen Albstadt und Friedrichshafen</dt><dd>11</dd></div>
          <div class="stat"><dt>Vermittler und Kooperations­partner</dt><dd>350</dd></div>
        </dl>
      </div>
    </section>

    <!-- SITUATIONEN -->
    <section class="section" aria-labelledby="sit-title">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow">Wobei wir helfen</p>
          <h2 id="sit-title">Vier Situationen, in denen sich ein Vergleich besonders lohnt.</h2>
        </div>
        <ol class="situations">
          <li class="situation" data-reveal>
            <div>
              <h3>Sie kaufen oder bauen.</h3>
              <p>Wir rechnen mit Ihnen durch, was realistisch ist, binden KfW- und L-Bank-Förderung ein und holen Angebote von über 600 Instituten. Neubau, Bestand oder Eigentumswohnung.</p>
              <a class="arrow-link mt-4" href="baufinanzierung.html#kauf">Zum Hauskredit</a>
            </div>
            <p class="situation__fact"><strong>bis 30 Jahre</strong>Zinsbindung möglich – Planungssicherheit bis zur letzten Rate.</p>
          </li>
          <li class="situation" data-reveal>
            <div>
              <h3>Ihre Zinsbindung läuft aus.</h3>
              <p>Die Hausbank schickt ein Verlängerungsangebot und hofft, dass Sie unterschreiben. Wir zeigen Ihnen, was andere Banken bieten – Prolongation, Umschuldung oder Forward-Darlehen.</p>
              <a class="arrow-link mt-4" href="baufinanzierung.html#anschluss">Zur Anschlussfinanzierung</a>
            </div>
            <p class="situation__fact"><strong>60 Monate</strong>vorher können Sie sich den Zins per Forward-Darlehen sichern.</p>
          </li>
          <li class="situation" data-reveal>
            <div>
              <h3>Sie verdienen in Franken.</h3>
              <p>Viele deutsche Banken tun sich mit Schweizer Einkommen schwer. In Konstanz sitzt unser Spezialist für Grenzgänger und Kapitalanleger mit Wohnsitz in der Schweiz.</p>
              <a class="arrow-link mt-4" href="baufinanzierung.html#grenzgaenger">Zur Grenzgänger-Finanzierung</a>
            </div>
            <p class="situation__fact"><strong>seit 2017</strong>spezialisiert auf Finanzierungen Deutschland / Schweiz.</p>
          </li>
          <li class="situation" data-reveal>
            <div>
              <h3>Sie modernisieren oder sanieren.</h3>
              <p>Heizung, Dach, Dämmung: Im Dschungel der Förderprogramme wissen wir, wo es was und wie viel gibt – und wie man es mit dem Bankdarlehen kombiniert.</p>
              <a class="arrow-link mt-4" href="baufinanzierung.html#modernisierung">Zur Modernisierung</a>
            </div>
            <p class="situation__fact"><strong>KfW + L-Bank</strong>Förderprogramme direkt in Ihre Finanzierung eingebunden.</p>
          </li>
        </ol>
      </div>
    </section>

    <!-- KOSTEN – Einwand Nr. 1 -->
    <section class="section section--lake on-lake" aria-labelledby="cost-title">
      <div class="container cost">
        <div data-reveal>
          <p class="eyebrow">Die Frage, die jeder stellt</p>
          <h2 id="cost-title">Was kostet Sie unsere Beratung?</h2>
          <p class="cost__mega" aria-hidden="true">0&nbsp;€</p>
          <p class="lead">Kein Honorar, keine Bearbeitungsgebühr. Bezahlt werden wir von der Bank, für die Sie sich entscheiden. Wir sind keiner Bank verpflichtet und haben keine eigenen Produkte – wir verdienen nur, wenn Sie ein Angebot überzeugt.</p>
          <a class="btn btn--accent btn--lg mt-4" href="#formular">Kostenloses Erstgespräch anfragen</a>
        </div>
        <ol class="flow" data-reveal aria-label="So fließt das Geld">
          <li><span class="flow__node" aria-hidden="true">1</span><div><h3>Sie</h3><p>schildern uns Ihr Vorhaben – im Büro, am Telefon oder per Video. Kostenlos und unverbindlich.</p></div></li>
          <li><span class="flow__node" aria-hidden="true">2</span><div><h3>Wir</h3><p>vergleichen über 600 Banken und Bausparkassen, inklusive KfW- und L-Bank-Förderung, und verhandeln für Sie.</p></div></li>
          <li class="is-key"><span class="flow__node" aria-hidden="true">3</span><div><h3>Ihre Bank</h3><p>bekommt Ihren Vertrag – und zahlt uns die Vermittlungs­provision. Nicht Sie.</p></div></li>
        </ol>
      </div>
    </section>

    <!-- ABLAUF – Einwand Nr. 3 -->
    <section class="section" aria-labelledby="steps-title">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow">So läuft es ab</p>
          <h2 id="steps-title">Vom ersten Gespräch bis zur Auszahlung – in vier Schritten.</h2>
          <p>Sie müssen kein Finanzprofi sein. Wir sprechen Deutsch, nicht Bankisch.</p>
        </div>
        <ol class="steps" data-reveal>
          <li class="step"><h3>Erstgespräch</h3><p>In einem unserer 11 Büros, am Telefon oder per Video. Wir klären, was Sie vorhaben und was realistisch ist.</p><span class="step__meta">kostenlos &amp; unverbindlich</span></li>
          <li class="step"><h3>Unterlagen</h3><p>Sie bekommen eine Liste, was Ihre künftige Bank sehen will. Wir prüfen alles vorab, damit die Bank keine Rückfragen hat.</p><span class="step__meta">wir prüfen vorab</span></li>
          <li class="step"><h3>Vergleich</h3><p>Angebote aus über 600 Instituten, nebeneinander gelegt und in klaren Worten erklärt – mit Fördermitteln.</p><span class="step__meta">über 600 Institute</span></li>
          <li class="step"><h3>Zusage</h3><p>Sie entscheiden. Wir reichen ein, verhandeln nach und bleiben an Ihrer Seite bis zur Auszahlung – und darüber hinaus.</p><span class="step__meta">bis zur Auszahlung</span></li>
        </ol>
      </div>
    </section>

    <!-- BUDGETRECHNER -->
    <section class="section section--mist" id="rechner" aria-labelledby="calc-title">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow">Budgetrechner</p>
          <h2 id="calc-title">Wie viel Haus ist drin? Rechnen Sie es in 30&nbsp;Sekunden aus.</h2>
          <p>Ohne Anmeldung, ohne Cookies. Ihre Eingaben bleiben in Ihrem Browser.</p>
        </div>
        <div class="calc" data-calc data-reveal>
          <div class="calc__inputs">
            <div class="range-field">
              <div class="range-field__top"><label for="calc-rate">Monatliche Rate, die Sie tragen können</label><output for="calc-rate" data-out="rate">1.500 €</output></div>
              <input class="range" id="calc-rate" type="range" min="500" max="4000" step="50" value="1500">
            </div>
            <div class="range-field">
              <div class="range-field__top"><label for="calc-equity">Eigenkapital</label><output for="calc-equity" data-out="equity">60.000 €</output></div>
              <input class="range" id="calc-equity" type="range" min="0" max="300000" step="5000" value="60000">
            </div>
            <div class="range-field">
              <div class="range-field__top"><label for="calc-interest">Sollzins (Annahme)</label><output for="calc-interest" data-out="interest">3,5 %</output></div>
              <!-- [[ERSETZEN: Standard-Sollzins regelmäßig an das aktuelle Zinsniveau anpassen (value="3.5")]] -->
              <input class="range" id="calc-interest" type="range" min="1.5" max="6" step="0.1" value="3.5" aria-describedby="calc-interest-hint">
              <span class="hint small text-soft" id="calc-interest-hint">Ihren tagesaktuellen Zins nennen wir Ihnen im Gespräch.</span>
            </div>
            <div class="range-field">
              <div class="range-field__top"><label for="calc-repay">Anfängliche Tilgung</label><output for="calc-repay" data-out="repay">2,0 %</output></div>
              <input class="range" id="calc-repay" type="range" min="1" max="4" step="0.25" value="2">
            </div>
            <label class="check"><input id="calc-broker" type="checkbox"> Mit Maklerprovision rechnen (3,57&nbsp;%)</label>
          </div>

          <div class="calc__result on-lake" aria-live="polite">
            <p class="label">Möglicher Kaufpreis, ca.</p>
            <p class="calc__big" data-out="price">–</p>
            <dl class="calc__breakdown">
              <div><dt>Darlehen</dt><dd data-out="loan">–</dd></div>
              <div><dt>Kaufnebenkosten</dt><dd data-out="extra">–</dd></div>
            </dl>
            <p class="small mb-0" data-out="hint"></p>
            <a class="btn btn--accent" href="kontakt.html?anliegen=kauf#formular" data-calc-cta>Ergebnis mit einem Berater prüfen</a>
            <p class="calc__note">Orientierung, keine Finanzierungszusage. Nebenkosten für Baden-Württemberg: 5&nbsp;% Grunderwerbsteuer, ca. 2&nbsp;% Notar und Grundbuch.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- WEITERE FELDER -->
    <section class="section" aria-labelledby="more-title">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow">Wenn die Finanzierung steht</p>
          <h2 id="more-title">Und danach? Vermögen aufbauen – mit denselben Menschen.</h2>
        </div>
        <div class="fields">
          <a class="field-panel field-panel--sand" href="kapitalanlagen.html" data-reveal>
            <p class="eyebrow mb-0">Kapitalanlagen</p>
            <h3>Immobilien, die Miete bringen statt Arbeit machen.</h3>
            <p>Denkmal, Pflegeimmobilie oder Mikroappartement: Wir prüfen Objekt und Betreiber, finanzieren und begleiten – auch mit allen Risiken, die dazugehören.</p>
            <ul class="tags"><li>Denkmal-AfA</li><li>Pflegeimmobilien</li><li>Mikroappartements</li></ul>
            <span class="arrow-link mt-4">Kapitalanlagen ansehen</span>
          </a>
          <a class="field-panel field-panel--mist" href="vermoegen.html" data-reveal>
            <p class="eyebrow mb-0">Vermögen</p>
            <h3>Ihr Depot, unabhängig geprüft – kostenlos.</h3>
            <p>Vermögensberatung ab 50&nbsp;€ Sparrate im Monat, Vermögensverwaltung mit der Fürst Fugger Privatbank, Nachfolgeplanung für Familien.</p>
            <span class="arrow-link mt-4">Zum Vermögensmanagement</span>
          </a>
        </div>
      </div>
    </section>

    <!-- STANDORTE -->
    <section class="section section--lake on-lake" aria-labelledby="map-title">
      <div class="container map-wrap">
        <div data-reveal>
          {map_svg("standorte.html")}
        </div>
        <div data-reveal>
          <p class="eyebrow">Vor Ort</p>
          <h2 id="map-title">11 Büros zwischen Alb und See – eines davon in <em>Ihrer</em> Nähe.</h2>
          <p class="lead">Rund um den See, in Oberschwaben und bis Südbaden – mit Menschen, die die Region und ihre Banken kennen.</p>
          <ul class="loc-list mt-4">{locs}</ul>
          <a class="btn btn--ghost mt-4" href="standorte.html">Alle Standorte mit Adresse</a>
        </div>
      </div>
    </section>

    <!-- HALTUNG -->
    <section class="section" aria-labelledby="values-title">
      <div class="container values">
        <div class="ph ph--portrait ph--organic" role="img" aria-label="Platzhalter: Gründerfoto auf der Insel Reichenau">
          <span>[[ERSETZEN: Foto – Gründer Achim Niess, Thomas Neumann und Christopher Schreiner auf der Insel Reichenau 2012, Hochformat 4:5]]</span>
        </div>
        <div>
          <p class="eyebrow">Seit 2012 · gegründet auf der Reichenau</p>
          <h2 id="values-title">Ex-Banker, die keine Bank mehr vertreten.</h2>
          <p class="lead">Wir kennen die Kreditinstitute von innen. Deshalb wissen wir, wie sie „ticken“ – und arbeiten heute für die andere Seite des Tisches: Ihre.</p>
          <ul class="values__list mt-5">
            <li data-reveal><h3>Unabhängig.</h3><p>Keine Bank, keine Versicherung, keine eigenen Produkte. Wir empfehlen, was zu Ihnen passt – nicht, was eine Vertriebsvorgabe erfüllt.</p></li>
            <li data-reveal><h3>Persönlich.</h3><p>Sie haben einen persönlichen Ansprechpartner vor Ort – kein wechselndes Callcenter, keine Hotline-Warteschleife.</p></li>
            <li data-reveal><h3>Fair.</h3><p>Offene Karten, klare Worte. „Abgehobenes Fachkauderwelsch ist nicht unser Ding.“</p></li>
          </ul>
          <a class="arrow-link mt-4" href="ueber-uns.html">Wer wir sind</a>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section section--surface" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow">Ehrliche Antworten</p>
          <h2 id="faq-title">Was Sie wissen sollten, bevor Sie uns anrufen.</h2>
        </div>
        {faq(FAQ_MAIN)}
      </div>
    </section>

    <!-- KONTAKT -->
    <section class="section" id="formular" aria-labelledby="contact-title">
      <div class="container contact">
        <div class="contact__aside">
          <div>
            <p class="eyebrow">Erstgespräch</p>
            <h2 id="contact-title">Erzählen Sie uns, was Sie vorhaben.</h2>
            <p class="text-soft">Wir melden uns, vereinbaren einen Termin und sagen Ihnen ehrlich, was möglich ist. Unverbindlich und kostenlos.</p>
          </div>
          <div class="contact__card">
            <h3>Lieber direkt sprechen?</h3>
            <a class="contact__phone" href="tel:{PHONE_HREF}">{PHONE}</a>
            <p class="mb-0">Mo–Fr 9–16 Uhr und nach Vereinbarung<br><a href="mailto:{MAIL}">{MAIL}</a></p>
          </div>
          <div class="contact__card">
            <h3>Zentrale Überlingen</h3>
            <address>Hägerstraße 1<br>88662 Überlingen</address>
          </div>
        </div>
        <div class="contact__form">
{contact_form("home")}
        </div>
      </div>
    </section>
  </main>
'''
    return (head("Baufinanzierung am Bodensee – über 600 Banken im Vergleich | Finanzkanzlei am See",
                 "Unabhängige Baufinanzierung aus Überlingen: Ex-Banker vergleichen über 600 Banken für Sie – kostenlos, an 11 Standorten oder per Video. Jetzt Erstgespräch anfragen.",
                 "index.html", ld(ORG_LD, faq_ld(FAQ_MAIN)))
            + header("index.html") + body + footer())


# ───────────────────────────── Baufinanzierung ─────────────────────────────
def page_bau():
    faqs = FAQ_MAIN[:4]
    body = f'''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container">
        {breadcrumb("Baufinanzierung")}
        <p class="eyebrow">Finanzierung &amp; Kapitalbedarf</p>
        <h1>Baufinanzierung vom Bodensee: verglichen unter 600 Banken, erklärt in <em>normalem</em> Deutsch.</h1>
        <p class="lead">Eine Finanzierung „von der Stange“ gibt es bei uns nicht. Unsere Spezialisten sind durchgehend ehemalige Banker – sie wissen, was eine Bank sehen will, und holen das Beste für Sie heraus.</p>
        <div class="hero__actions mt-4">
          <a class="btn btn--accent btn--lg" href="kontakt.html?anliegen=kauf#formular">Kostenloses Erstgespräch anfragen</a>
          <a class="btn btn--ghost btn--lg" href="index.html#rechner">Budget berechnen</a>
        </div>
        <ul class="trust-line"><li>{ICON_CHECK} Für Sie kostenlos</li><li>{ICON_CHECK} Zertifizierter Beratungspartner der Dr. Klein Privatkunden AG</li></ul>
      </div>
    </section>
    {WATERLINE}

    <div class="container">
      <section class="feature" id="kauf" aria-labelledby="kauf-t">
        <div>
          <h2 id="kauf-t">Hauskredit für Neubau oder Bestand – mit dem Angebot, das Ihre Hausbank Ihnen nicht zeigt.</h2>
          <p>Gemeinsam entwickeln wir ein Finanzierungskonzept, das zu Ihren Zielen passt: Wie hoch soll die Rate sein? Wie lange wollen Sie Zinssicherheit? Wie viel Sondertilgung brauchen Sie? Dann vergleichen wir Angebote von über 600 Kreditinstituten.</p>
          <p>Günstige Zinsen sind das eine. Das Drumherum – Unterlagen, Bewertung, Fristen – ist das andere. Wir bereiten alles so auf, dass die angefragten Banken ohne größere Nachfragen entscheiden können.</p>
        </div>
        <aside class="feature__aside" aria-label="Auf einen Blick">
          <h3>Auf einen Blick</h3>
          {ticks(["Kauf, Neubau, Eigentumswohnung", "Zinsbindung bis zu 30 Jahre", "Vielfältige Sondertilgungsoptionen und Tilgungssatzwechsel", "Für Angestellte, Selbstständige und Beamte"])}
        </aside>
      </section>

      <section class="feature feature--flip" id="anschluss" aria-labelledby="ansch-t">
        <div>
          <h2 id="ansch-t">Zinsbindung läuft aus? Unterschreiben Sie nicht das erste Angebot Ihrer Bank.</h2>
          <p>Wenn die Zinsbindung Ihrer ersten Baufinanzierung endet, haben Sie drei Wege: Prolongation bei Ihrer Bank, Umschuldung zu einer anderen – oder ein Forward-Darlehen, mit dem Sie sich heute schon den Zins für später sichern.</p>
          <p>Wir prüfen alle drei und zeigen Ihnen schwarz auf weiß, was der Unterschied für Ihre Rate bedeutet.</p>
          <a class="arrow-link" href="kontakt.html?anliegen=anschluss#formular">Anschlussfinanzierung prüfen lassen</a>
        </div>
        <aside class="feature__aside" aria-label="Fristen">
          <h3>Gut zu wissen</h3>
          {ticks(["Forward-Darlehen bis zu 60 Monate im Voraus", "Umschuldung ohne Vorfälligkeitsentschädigung zum Ende der Zinsbindung", "Bringen Sie einfach Ihren Darlehensvertrag mit"])}
        </aside>
      </section>

      <section class="feature" id="grenzgaenger" aria-labelledby="gg-t">
        <div>
          <h2 id="gg-t">Grenzgänger: Finanzierung mit Schweizer Einkommen.</h2>
          <p>Wer in der Schweiz arbeitet und in Deutschland kauft, erlebt bei vielen Banken Zurückhaltung. In Konstanz berät Sie Andreas Scholl, Bankbetriebswirt und seit 1995 in der Beratung vermögender Kundschaft. Seit 2017 ist er bei uns auf Finanzierungen für Grenzgänger und Kapitalanleger mit Wohnsitz in der Schweiz spezialisiert.</p>
          <a class="arrow-link" href="standorte.html#konstanz">Zum Standort Konstanz</a>
        </div>
        <aside class="feature__aside" aria-label="Schwerpunkte Konstanz">
          <h3>Schwerpunkte in Konstanz</h3>
          {ticks(["Grenzgänger-Finanzierungen", "Kapitalanleger mit Wohnsitz in der Schweiz", "Existenzgründung für Heil- und Freiberufler"])}
        </aside>
      </section>

      <section class="feature feature--flip" id="modernisierung" aria-labelledby="mod-t">
        <div>
          <h2 id="mod-t">Modernisieren mit Fördergeld: Wir wissen, wo es was und wie viel gibt.</h2>
          <p>Ob neue Heizung, Dämmung oder altersgerechter Umbau: KfW und L-Bank Baden-Württemberg fördern viel – wenn man die Programme kennt und richtig kombiniert. Wir binden die passenden Programme direkt in Ihre Finanzierung ein.</p>
        </div>
        <aside class="feature__aside" aria-label="Förderung">
          <h3>Eingebunden</h3>
          {ticks(["Alle KfW-Förderprogramme", "Alle L-Bank-Förderprogramme", "Kombination mit Bankdarlehen"])}
        </aside>
      </section>

      <section class="feature" id="ratenkredit" aria-labelledby="rk-t">
        <div>
          <h2 id="rk-t">Ratenkredit: schnell entschieden, fair verglichen.</h2>
          <p>Auto, Umschuldung teurer Kredite, Energie- oder Beamtendarlehen: Wir vergleichen die Zinsen der relevanten Anbieter. Über unser System erfolgt die Prüfung sofort, das Geld ist innerhalb weniger Tage auf dem Konto. Ihre Bonität bestimmt den Zins – wir sagen Ihnen vorher, womit Sie rechnen können.</p>
          <a class="arrow-link" href="kontakt.html?anliegen=sonstiges#formular">Ratenkredit anfragen</a>
        </div>
        <aside class="feature__aside" aria-label="Ratenkredit">
          <h3>Eckdaten</h3>
          {ticks(["Laufzeiten bis 120 Monate", "Beratung vor Ort, am Telefon oder per Video", "Kostenlos – wir erhalten eine Provision vom Produktpartner"])}
        </aside>
      </section>

      <section class="feature feature--flip" id="gewerbe" aria-labelledby="gw-t">
        <div>
          <h2 id="gw-t">Gewerbliche Finanzierung: für Unternehmen, Bauträger und Investoren.</h2>
          <p>Maschinen, Neubau, Erweiterung, Firmenübergabe: Gemeinsam mit unserem Partner FinMatch AG machen wir gewerbliche Finanzierungen transparent und vergleichbar. Förderprogramme und der Zugang zur Bürgschaftsbank sind direkt eingebunden.</p>
          <p>Bauträgerfinanzierungen gehören zu den anspruchsvollsten Finanzierungen überhaupt – nicht jede Bank begleitet sie. Grundlage ist eine professionelle Vorbereitung mit Projektkalkulation und vollständigen Unterlagen.</p>
          <a class="arrow-link" href="kontakt.html?anliegen=gewerbe#formular">Gewerbliches Vorhaben besprechen</a>
        </div>
        <aside class="feature__aside" aria-label="Gewerbe">
          <h3>Für wen</h3>
          {ticks(["Unternehmen in Gründungs- und Wachstumsphase", "Bauträger, Aufteiler, Projektentwickler", "Immobilieninvestoren", "Betriebserweiterung, Nachfolge"])}
        </aside>
      </section>
    </div>

    <section class="section section--surface" aria-labelledby="docs-t">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Unterlagen</p>
          <h2 id="docs-t">Schon mal vorbereiten? Diese Formulare brauchen die meisten Banken.</h2>
          <p>Kein Muss für das Erstgespräch – aber wer sie dabeihat, ist schneller am Ziel.</p>
        </div>
        <!-- [[ERSETZEN: PDFs von der bisherigen Website übernommen – Aktualität prüfen]] -->
        {ticks(['<a href="assets/docs/selbstauskunft.pdf">Finanzierungsantrag &amp; Selbstauskunft (PDF)</a>', '<a href="assets/docs/objektbeschreibung.pdf">Objektbeschreibung (PDF)</a>', '<a href="assets/docs/wohnflaechenberechnung.pdf">Wohnflächenberechnung, ausfüllbar (PDF)</a>'])}
      </div>
    </section>

    <section class="section" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head"><h2 id="faq-title">Häufige Fragen zur Baufinanzierung</h2></div>
        {faq(faqs)}
      </div>
    </section>
{cta_band("Ein Gespräch – und Sie wissen, was <em>wirklich</em> drin ist.", "Bringen Sie mit, was Sie haben: Exposé, Darlehensvertrag oder nur eine Idee. Den Rest machen wir.", "kauf")}
  </main>
'''
    return (head("Baufinanzierung, Anschlussfinanzierung & Hauskredit | Finanzkanzlei am See",
                 "Hauskredit, Anschlussfinanzierung, Forward-Darlehen, Grenzgänger- und Gewerbefinanzierung: Ex-Banker vergleichen über 600 Banken für Sie. Kostenlos, am Bodensee.",
                 "baufinanzierung.html", ld(faq_ld(faqs)))
            + header("baufinanzierung.html") + body + footer())


# ───────────────────────────── Kapitalanlagen ─────────────────────────────
def page_kapital():
    body = f'''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container">
        {breadcrumb("Kapitalanlagen")}
        <p class="eyebrow">Suche, Vermittlung &amp; Betreuung</p>
        <h1>Immobilien als Kapitalanlage – <em>geprüft,</em> finanziert und begleitet aus einer Hand.</h1>
        <p class="lead">Immobilien sind oft der größte Baustein eines Vermögens – und werden in der Vermögensberatung trotzdem gern übersehen. Wir verbinden Objektauswahl, Bewertung, Finanzierung und Verwaltung.</p>
        <a class="btn btn--accent btn--lg mt-4" href="kontakt.html?anliegen=kapitalanlage#formular">Passende Anlage besprechen</a>
      </div>
    </section>
    {WATERLINE}

    <section class="section" aria-label="Drei Anlageformen im Vergleich">
      <div class="container compare">
        <article id="denkmal" data-reveal>
          <p class="eyebrow mb-0">Für hohe Steuerlast</p>
          <h2>Denkmal­immobilien</h2>
          <p>Aufwendig sanierte Altbauten und Industriedenkmäler, deren Sanierung der Staat mit Sonderabschreibungen fördert.</p>
          <dl>
            <div><dt>Der Vorteil</dt><dd>Steuervorteile, die die Gesamtrendite deutlich verbessern; hohe Mietnachfrage nach sanierten Altbauwohnungen.</dd></div>
            <div><dt>Ehrlich gesagt</dt><dd>Umkämpfter Markt, Fertigstellungsrisiko wie beim Neubau, und die Steuervorteile laufen nach einigen Jahren aus.</dd></div>
          </dl>
        </article>
        <article id="pflege" data-reveal>
          <p class="eyebrow mb-0">Für wenig Aufwand</p>
          <h2>Pflege­immobilien &amp; betreutes Wohnen</h2>
          <p>Sie kaufen ein Apartment in einer Pflegeeinrichtung, die komplett an einen Betreiber verpachtet ist.</p>
          <dl>
            <div><dt>Der Vorteil</dt><dd>Pachtverträge meist über 20–30 Jahre, keine Mietersuche, oft ein Vorbelegungsrecht bei eigenem Pflegebedarf.</dd></div>
            <div><dt>Ehrlich gesagt</dt><dd>Alles steht und fällt mit dem Betreiber. Wir nehmen nur Objekte renommierter nationaler oder internationaler Betreiber auf.</dd></div>
          </dl>
        </article>
        <article id="mikro" class="on-lake" data-reveal>
          <p class="eyebrow mb-0">Für kleinere Budgets</p>
          <h2>Mikro­appartements</h2>
          <p>Möblierte 1–2-Zimmer-Wohnungen für Pendler, Studierende und Forschende in Uni- und Großstädten.</p>
          <dl>
            <div><dt>Der Vorteil</dt><dd>Einstieg je nach Lage ab etwa 150.000–300.000 €, überdurchschnittliche Mieten, Full-Service-Modelle halten den Aufwand gering.</dd></div>
            <div><dt>Ehrlich gesagt</dt><dd>Hohe Quadratmeterpreise und mehr Mieterwechsel als bei klassischen Wohnungen.</dd></div>
          </dl>
        </article>
      </div>
    </section>

    <section class="section section--surface" aria-labelledby="nk-t">
      <div class="container feature">
        <div>
          <p class="eyebrow">Bevor Sie rechnen</p>
          <h2 id="nk-t">Der Kaufpreis ist nie der ganze Preis.</h2>
          <p>Bei jedem Immobilienkauf kommen Erwerbsnebenkosten hinzu. Wir rechnen sie von Anfang an mit ein – auch in Ihre Finanzierung.</p>
          <a class="arrow-link" href="index.html#rechner">Zum Budgetrechner</a>
        </div>
        <aside class="feature__aside" aria-label="Kaufnebenkosten">
          <h3>Kaufnebenkosten</h3>
          {ticks(["Grunderwerbsteuer: je Bundesland 3,5–6,5 % (Baden-Württemberg: 5 %)", "Notar: ca. 1–1,5 %", "Grundbuch: ca. 0,5 %"])}
        </aside>
      </div>
    </section>

    <section class="section" aria-labelledby="fb-t">
      <div class="container">
        <div class="section-head">
          <h2 id="fb-t">Nicht sicher, welche Anlage zu Ihnen passt?</h2>
          <p>Unser Fragebogen hilft Ihnen, Ihre Ziele zu sortieren – Steuerlast, Budget, Zeithorizont. Füllen Sie ihn aus und bringen Sie ihn mit, oder wir gehen ihn gemeinsam durch.</p>
          <!-- [[ERSETZEN: Fragebogen-PDF (Kundenanforderungsprofil) auf Aktualität prüfen]] -->
          <a class="btn btn--ghost" href="assets/docs/fragebogen-kapitalanlage.pdf">Fragebogen herunterladen (PDF)</a>
        </div>
        <p class="small text-soft">Hinweis: Immobilien als Kapitalanlage sind mit Risiken verbunden, z. B. Leerstand, Wertentwicklung, Betreiberausfall und Änderungen steuerlicher Rahmenbedingungen. Eine steuerliche Beratung ersetzen wir nicht – auf Wunsch binden wir Ihren Steuerberater ein.</p>
      </div>
    </section>
{cta_band("Welche Immobilie zu Ihrer <em>Steuerlast</em> passt, klären wir in einem Gespräch.", "Wir zeigen Ihnen aktuelle Objekte, rechnen die Finanzierung durch und sagen offen, wo die Haken liegen.", "kapitalanlage")}
  </main>
'''
    return (head("Kapitalanlage-Immobilien: Denkmal, Pflege, Mikroappartement | Finanzkanzlei am See",
                 "Denkmalimmobilien, Pflegeimmobilien und Mikroappartements als Kapitalanlage – mit Vorteilen und Risiken ehrlich erklärt. Auswahl, Finanzierung und Begleitung aus Überlingen.",
                 "kapitalanlagen.html")
            + header("kapitalanlagen.html") + body + footer())


# ───────────────────────────── Vermögen ─────────────────────────────
def page_vermoegen():
    body = f'''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container">
        {breadcrumb("Vermögen")}
        <p class="eyebrow">Vermögensmanagement &amp; Investment</p>
        <h1>Vermögen, das niemandem verpflichtet ist – <em>außer Ihnen.</em></h1>
        <p class="lead">Wir bieten keine eigenen Produkte an. Deshalb wählen wir in offener Architektur aus Einzeltiteln, ETFs, Fonds, Gold und Immobilien – passend zu Ihrer Renditeerwartung und Ihrer Risikoneigung.</p>
        <a class="btn btn--accent btn--lg mt-4" href="kontakt.html?anliegen=vermoegen#formular">Kostenlose Depotanalyse anfragen</a>
      </div>
    </section>
    {WATERLINE}

    <div class="container">
      <section class="feature" id="depotanalyse" aria-labelledby="da-t">
        <div>
          <h2 id="da-t">Depotanalyse: eine neutrale zweite Meinung zu Ihrem Depot – kostenlos.</h2>
          <p>Wie ist Ihr Wertpapierdepot wirklich aufgestellt? Wir sind keinem Produktpartner verpflichtet und sagen Ihnen unvoreingenommen, was wir sehen. Was Sie mit dem Ergebnis machen, entscheiden Sie.</p>
        </div>
        <aside class="feature__aside" aria-label="Ziele der Analyse">
          <h3>Drei Ziele</h3>
          <ol class="mb-0"><li>Chancen erhöhen</li><li>Risiken senken</li><li>Kosten optimieren</li></ol>
        </aside>
      </section>

      <section class="feature feature--flip" id="beratung" aria-labelledby="vb-t">
        <div>
          <h2 id="vb-t">Vermögensberatung: Wir holen Sie da ab, wo Sie stehen.</h2>
          <p>Es spielt keine Rolle, wie gut Sie sich an den Finanzmärkten auskennen. Wir lernen Sie kennen, klären Ihre Anlegerpersönlichkeit, entwickeln eine Strategie, setzen sie um – und überprüfen sie laufend.</p>
          <p>Klassische Anlageberatung mit Service-Fee: ohne Ausgabeaufschläge und ohne teure Kaufspesen.</p>
        </div>
        <aside class="feature__aside" aria-label="Eckdaten">
          <h3>Eckdaten</h3>
          {ticks(["Schon ab 50 € Sparrate im Monat", "Fonds- und ETF-Sparpläne", "Nachhaltige Anlagen auf Wunsch", "Depotführung in Deutschland und der Schweiz"])}
        </aside>
      </section>

      <section class="feature" id="verwaltung" aria-labelledby="vv-t">
        <div>
          <h2 id="vv-t">Vermögensverwaltung: Sie legen die Richtung fest, wir kümmern uns um den Rest.</h2>
          <p>Gemeinsam mit der Fürst Fugger Privatbank verwalten wir Ihr Vermögen strategieorientiert. Sie wählen eine Anlagerichtlinie – von konservativ bis chancenorientiert – und müssen nicht bei jedem Kauf oder Verkauf mitwirken. Beraten werden Sie trotzdem vor Ort.</p>
          <p>Zur Wahl stehen eine klassische Vermögensverwaltung mit fünf Strategien und eine substanzorientierte, risikoadjustierte Variante.</p>
        </div>
        <aside class="feature__aside" aria-label="Depotbanken">
          <h3>Depotführung u. a. bei</h3>
          {ticks(["Fürst Fugger Privatbank", "St. Galler Kantonalbank", "comdirect", "ebase", "FIL Fondsbank"])}
        </aside>
      </section>

      <section class="feature feature--flip" id="nachfolge" aria-labelledby="nf-t">
        <div>
          <h2 id="nf-t">Nachfolgeplanung: damit Familienvermögen Familienvermögen bleibt.</h2>
          <p>Generationsübergreifende Vermögens- und Liquiditätsplanung – bei Bedarf gemeinsam mit Ihren Juristen und Steuerberatern. Für große Familienvermögen bieten wir Family-Office-Leistungen.</p>
        </div>
        <aside class="feature__aside" aria-label="Ansprechpartner">
          <h3>Ihr Ansprechpartner</h3>
          <p class="mb-0">Thomas Neumann und das Team Vermögensberatung<br><a href="tel:+4975519377111">07551 93771-11</a></p>
        </aside>
      </section>
    </div>

    <section class="section--tight">
      <div class="container">
        <p class="placeholder-note"><strong>Pflichthinweis:</strong> Die Anlageberatung und die Anlagevermittlung im Sinne des Kreditwesengesetzes (KWG) bieten wir Ihnen als vertraglich gebundener Vermittler im Sinne des KWG im Auftrag, im Namen und für Rechnung der Fürst Fugger Privatbank Aktiengesellschaft, Maximilianstr. 38, 86150 Augsburg an. Weitere Informationen im <a href="impressum.html#erstinformation">Impressum</a>. Kapitalanlagen unterliegen Wertschwankungen; Verluste sind möglich.</p>
      </div>
    </section>
{cta_band("Ihr Depot verdient eine <em>ehrliche</em> zweite Meinung.", "Bringen Sie Ihren Depotauszug mit – wir sagen Ihnen kostenlos, was wir sehen.", "vermoegen")}
  </main>
'''
    return (head("Vermögensberatung, Vermögensverwaltung & Depotanalyse | Finanzkanzlei am See",
                 "Unabhängige Vermögensberatung ab 50 € Sparrate, Vermögensverwaltung mit der Fürst Fugger Privatbank und kostenlose Depotanalyse – persönlich am Bodensee.",
                 "vermoegen.html")
            + header("vermoegen.html") + body + footer())


# ───────────────────────────── Standorte ─────────────────────────────
def page_standorte():
    cards = []
    lds = []
    for slug, name, addr, person, tel, telh, mail, hours, hq in LOCATIONS:
        badge = '<span class="location__badge">Zentrale</span>' if hq else ""
        cards.append(f'''          <li class="location{" location--hq" if hq else ""}" id="{slug}">
            <h3>{name} {badge}</h3>
            <p class="location__person mb-0">{person}</p>
            <address>{addr}</address>
            <p class="mb-0"><a href="tel:{telh}">{tel}</a> · <a href="mailto:{mail}">{mail}</a></p>
            <p class="mb-0 small">{hours}</p>
            <a class="arrow-link location__cta" href="kontakt.html?standort={quote(name)}#formular">Termin in {name} anfragen</a>
          </li>''')
    body = f'''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container">
        {breadcrumb("Standorte")}
        <p class="eyebrow">Persönlich vor Ort</p>
        <h1>11 Büros rund um den See – und eines per <em>Video.</em></h1>
        <p class="lead">Von Albstadt bis Friedrichshafen, von Donaueschingen bis Konstanz: Wählen Sie das Büro in Ihrer Nähe oder sprechen Sie per Video mit uns.</p>
      </div>
    </section>

    <section class="section section--lake on-lake" aria-label="Karte der Standorte">
      <div class="container">
        {map_svg("")}
        <p class="small text-soft mb-0">Schematische Darstellung. Bewusst ohne eingebettete Online-Karte – so werden beim Aufruf keine Daten an Dritte übertragen.</p>
      </div>
    </section>

    <section class="section" aria-labelledby="loc-t">
      <div class="container">
        <h2 id="loc-t" class="visually-hidden">Alle Standorte</h2>
        <ul class="locations">
{chr(10).join(cards)}
        </ul>
      </div>
    </section>
{cta_band("Welches Büro? Egal – Hauptsache, wir <em>sprechen.</em>", "Im Formular können Sie Ihren Wunschstandort angeben oder ein Videogespräch wählen.")}
  </main>
'''
    return (head("Standorte: Überlingen, Konstanz, Ravensburg & mehr | Finanzkanzlei am See",
                 "11 Standorte der Finanzkanzlei am See zwischen Albstadt, Donaueschingen, Konstanz und Friedrichshafen – mit Adressen, Ansprechpartnern und Öffnungszeiten.",
                 "standorte.html")
            + header("standorte.html") + body + footer())


# ───────────────────────────── Über uns ─────────────────────────────
def page_ueber():
    team = [
        ("Achim Niess", "Geschäftsführender Gesellschafter, Vertrieb", "Dipl.-Betriebswirt (FH) Banking und Finance"),
        ("Thomas Neumann", "Geschäftsführer, Vermögen", "[[ERSETZEN: Qualifikation Thomas Neumann]]"),
        ("Christopher Schreiner", "Geschäftsführer", "[[ERSETZEN: Rolle und Qualifikation Christopher Schreiner]]"),
        ("Bernd Schatz", "Kaufmännische Geschäftsführung", "Dipl.-Betriebswirt (BA), Dipl.-Immobiliensachverständiger (DIA)"),
    ]
    team_html = "\n".join(f'''          <li data-reveal>
            <div class="ph ph--portrait{" ph--organic" if i % 2 else ""}" role="img" aria-label="Platzhalter: Porträt {n}"><span>[[ERSETZEN: Porträt {n}, Hochformat 4:5, natürliches Licht, gern am See]]</span></div>
            <h3>{n}</h3><p>{r}</p><p>{q}</p>
          </li>''' for i, (n, r, q) in enumerate(team))
    body = f'''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container">
        {breadcrumb("Über uns")}
        <p class="eyebrow">Seit 2012</p>
        <h1>Bei Geld fängt die <em>Freundschaft</em> an.</h1>
        <p class="lead">2012 auf der Insel Reichenau gegründet, heute inhabergeführt mit rund 40 Spezialistinnen und Spezialisten an 11 Standorten. Was uns verbindet: Wir haben bei Banken gearbeitet – und wollten es anders machen.</p>
      </div>
    </section>
    {WATERLINE}

    <section class="section" aria-labelledby="phil-t">
      <div class="container values">
        <div class="ph ph--wide" role="img" aria-label="Platzhalter: Die Geschäftsführung"><span>[[ERSETZEN: Foto – Geschäftsführung Bernd Schatz, Achim Niess, Thomas Neumann, Christopher Schreiner, Querformat 3:2]]</span></div>
        <div>
          <h2 id="phil-t">Unabhängig. Persönlich. Fair.</h2>
          <p>Wir sind keiner Bank, keiner Versicherung und keinem Finanzinstitut verpflichtet. Das ist keine Floskel, sondern unser Geschäftsmodell: Für Sie vergleichen wir über 600 Geldinstitute und Netzwerkpartner – und empfehlen das, was zu Ihnen passt.</p>
          <p>Finanzberatung ist ein Geschäft unter Menschen. Unsere Anlageentscheidungen richten sich nach Ihrer Risikomentalität, nicht nach unserer Selbstverwirklichung. Und wir spielen mit offenen Karten – ohne Fachkauderwelsch.</p>
          <p>Intern nennen wir uns manchmal „Bankpunks“: Wir haben das Handwerk bei Banken gelernt und machen es heute auf unsere Art.</p>
        </div>
      </div>
    </section>

    <section class="section section--surface" aria-labelledby="team-t">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Geschäftsführung</p>
          <h2 id="team-t">Die Menschen, die dafür geradestehen.</h2>
        </div>
        <ul class="team">
{team_html}
        </ul>
      </div>
    </section>

    <section class="section" aria-labelledby="partner-t">
      <div class="container feature">
        <div>
          <p class="eyebrow">Partner</p>
          <h2 id="partner-t">Starke Partner, freie Wahl.</h2>
          <p>Unsere Partner geben uns Zugang zu Plattformen, Banken und Produkten. Welches Angebot Sie bekommen, entscheidet trotzdem allein der Vergleich.</p>
        </div>
        <aside class="feature__aside" aria-label="Partner">
          <h3>Wir arbeiten u. a. mit</h3>
          {ticks(["Dr. Klein Privatkunden AG – Baufinanzierung", "Fürst Fugger Privatbank – Vermögen", "FinMatch AG – Gewerbefinanzierung", "Immoheld – Kapitalanlage-Immobilien"])}
        </aside>
      </div>
    </section>

    <section class="section section--mist" id="stiftung" aria-labelledby="st-t">
      <div class="container feature">
        <div>
          <p class="eyebrow">Etwas zurückgeben</p>
          <h2 id="st-t">Die FKSee Kinder- und Jugendstiftung.</h2>
          <p>Kinderarmut ist eine Tatsache, die wir nicht hinnehmen wollen. Mit Unterstützung vieler unserer Kundinnen und Kunden setzt sich unsere Stiftung für Kinder und Jugendliche ein, die nicht auf der sonnigen Seite des Lebens geboren wurden.</p>
          <p class="small">Spendenkonto: Bezirkssparkasse Reichenau · IBAN DE27 6905 1410 0007 0915 31</p>
        </div>
        <aside class="feature__aside" aria-label="Vorstand">
          <h3>Vorstand der Stiftung</h3>
          {ticks(["Stefan Keller", "Achim Niess", "Thomas Neumann"])}
        </aside>
      </div>
    </section>

    <section class="section" id="karriere" aria-labelledby="kar-t">
      <div class="container feature">
        <div>
          <p class="eyebrow">Karriere</p>
          <h2 id="kar-t">Bankerfahrung, aber keine Lust mehr auf Produktvorgaben?</h2>
          <p>Wir erwarten viel und bieten viel: flexible, freiheitliche Arbeitsmodelle, Zugriff auf rund 600 Produktpartner über die Plattform Europace und ein Team rund um den Bodensee. „Nur angestellt“ zu sein, passt nicht zu uns.</p>
          <a class="btn btn--ghost" href="mailto:b.schatz@fksee.de?subject=Bewerbung">Bei Bernd Schatz bewerben</a>
        </div>
        <aside class="feature__aside" aria-label="Offene Stellen">
          <h3>Wir suchen</h3>
          {ticks(["Spezialist/in für Baufinanzierung (m/w/d)", "Initiativbewerbungen – zeigen Sie uns, was fehlt"])}
          <!-- [[ERSETZEN: Offene Stellen aktuell halten]] -->
        </aside>
      </div>
    </section>

    <section class="section section--surface" id="kooperation" aria-labelledby="koop-t">
      <div class="container feature">
        <div>
          <p class="eyebrow">Für Makler, Bauträger, Versicherungsbüros</p>
          <h2 id="koop-t">Sie verkaufen die Immobilie. Wir finanzieren sie.</h2>
          <p>Als Kooperationspartner bekommen Ihre Kundinnen und Kunden Zugang zu nahezu allen Banken und Förderprogrammen – und Sie behalten Ihre Kundschaft: Wir übernehmen ausschließlich die Finanzierung.</p>
          <a class="arrow-link" href="kontakt.html?anliegen=sonstiges&amp;nachricht=Kooperationsanfrage#formular">Kooperation anfragen</a>
        </div>
        <aside class="feature__aside" aria-label="Vorteile">
          <h3>Ihre Vorteile</h3>
          {ticks(["100 % Kundenschutz", "Stornofreie Tippgeberprovision", "Erfahrene Finanzierungsspezialisten"])}
        </aside>
      </div>
    </section>
{cta_band("Lernen Sie uns kennen – am besten bei einem <em>Kaffee.</em>", "Oder per Video, wenn der Weg zu weit ist.")}
  </main>
'''
    return (head("Über uns: Ex-Banker vom Bodensee seit 2012 | Finanzkanzlei am See",
                 "Die Finanzkanzlei am See: 2012 auf der Reichenau gegründet, inhabergeführt, unabhängig. Geschäftsführung, Partner, Stiftung, Karriere und Kooperationen.",
                 "ueber-uns.html")
            + header("ueber-uns.html") + body + footer())


# ───────────────────────────── Kontakt ─────────────────────────────
def page_kontakt():
    body = f'''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container">
        {breadcrumb("Kontakt")}
        <h1>Ein Gespräch, <em>kostenlos</em> und unverbindlich.</h1>
        <p class="lead">Schreiben Sie uns kurz, worum es geht. Wir melden uns, vereinbaren einen Termin – vor Ort, am Telefon oder per Video.</p>
      </div>
    </section>
    <section class="section" id="formular" aria-label="Kontaktformular">
      <div class="container contact">
        <div class="contact__aside">
          <div class="contact__card">
            <h2 class="h4">Direkt anrufen</h2>
            <a class="contact__phone" href="tel:{PHONE_HREF}">{PHONE}</a>
            <p class="mb-0">Mo–Fr 9–16 Uhr und nach Vereinbarung</p>
          </div>
          <div class="contact__card">
            <h2 class="h4">E-Mail</h2>
            <p class="mb-0"><a href="mailto:{MAIL}">{MAIL}</a></p>
          </div>
          <div class="contact__card">
            <h2 class="h4">Zentrale</h2>
            <address>Finanzkanzlei am See GmbH<br>Hägerstraße 1<br>88662 Überlingen</address>
            <a class="arrow-link mt-4" href="standorte.html">Alle 11 Standorte</a>
          </div>
          <ul class="trust-line">
            <li>{ICON_CHECK} Für Sie kostenlos</li>
            <li>{ICON_CHECK} Über 600 Banken</li>
            <li>{ICON_CHECK} Seit 2012</li>
          </ul>
        </div>
        <div class="contact__form">
          <h2>Ihre Anfrage</h2>
{contact_form("kontakt")}
        </div>
      </div>
    </section>
  </main>
'''
    return (head("Kontakt & Erstgespräch | Finanzkanzlei am See, Überlingen",
                 "Kostenloses Erstgespräch zur Baufinanzierung, Kapitalanlage oder Vermögen anfragen. Telefon 07551 93771-0, Hägerstraße 1, 88662 Überlingen.",
                 "kontakt.html")
            + header("kontakt.html") + body + footer())


# ───────────────────────────── Impressum ─────────────────────────────
def page_impressum():
    body = '''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container prose">
        <nav class="breadcrumb" aria-label="Brotkrumen"><ol><li><a href="index.html">Start</a></li><li aria-current="page">Impressum</li></ol></nav>
        <h1>Impressum</h1>
        <p class="placeholder-note">[[ERSETZEN: Angaben wurden von der bisherigen Website übernommen – vor Veröffentlichung vollständig rechtlich prüfen lassen.]]</p>

        <h2>Angaben gemäß § 5 DDG</h2>
        <p>Finanzkanzlei am See GmbH<br>Hägerstraße 1<br>88662 Überlingen</p>
        <p>Handelsregister: HRB 709481<br>Registergericht: Amtsgericht Freiburg i. Br.</p>
        <p>Vertreten durch die Geschäftsführer:<br>Thomas Neumann, Achim Niess, Christopher Schreiner, Bernd Schatz</p>

        <h2>Kontakt</h2>
        <p>Telefon: <a href="tel:+497551937710">+49 7551 93771-0</a><br>E-Mail: <a href="mailto:info@fksee.de">info@fksee.de</a></p>

        <h2>Umsatzsteuer-ID</h2>
        <p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a UStG: DE286038569</p>

        <h2 id="erstinformation">Erlaubnisse und Registereintragungen</h2>
        <p>Versicherungsmakler gemäß § 34d Abs. 1 GewO, IHK Bodensee-Oberschwaben, Reg.-Nr. D-8BAD-8MXN5-98</p>
        <p>Immobiliardarlehensvermittler gemäß § 34i Abs. 1 S. 1 GewO, IHK Bodensee-Oberschwaben, Reg.-Nr. D-W-165-DT4Q-25</p>
        <p>Erlaubnis nach § 34c GewO, Landratsamt Bodenseekreis</p>
        <p>Das Vermittlerregister kann eingesehen werden unter <a href="https://www.vermittlerregister.info">www.vermittlerregister.info</a>.</p>
        <p>Aufsichtsbehörden: Landratsamt Bodenseekreis und Bundesanstalt für Finanzdienstleistungsaufsicht (BaFin)</p>

        <h3>Hinweise zu Anlageberatung und Anlagevermittlung</h3>
        <p>Die Anlageberatung und die Anlagevermittlung im Sinne des Kreditwesengesetzes (KWG) bieten wir Ihnen als vertraglich gebundene Vermittlerin im Sinne des KWG im Auftrag, im Namen und für Rechnung der Fürst Fugger Privatbank Aktiengesellschaft, Maximilianstr. 38, 86150 Augsburg an. Sie erreichen die Fürst Fugger Privatbank telefonisch unter (0821) 3201111 und per E-Mail unter vertriebsbetreuung@fuggerbank.de. Die Fürst Fugger Privatbank Aktiengesellschaft ist ein Kreditinstitut und Finanzdienstleistungsinstitut im Sinne des KWG und verfügt über die erforderlichen Erlaubnisse der Aufsichtsbehörden. Die BaFin führt ein öffentliches Register der vertraglich gebundenen Vermittler, einsehbar unter <a href="https://www.bafin.de">www.bafin.de</a>.</p>

        <h2>Redaktionell verantwortlich</h2>
        <p>Achim Niess, Finanzkanzlei am See GmbH, Hägerstraße 1, 88662 Überlingen</p>

        <h2>Verbraucherstreitbeilegung</h2>
        <p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
        <p>[[ERSETZEN: Prüfen, ob für Versicherungs- und Darlehensvermittlung Angaben zu Schlichtungsstellen (z. B. Versicherungsombudsmann) verpflichtend sind]]</p>

        <h2>Gestaltung und Umsetzung</h2>
        <p>[[ERSETZEN: Agentur / Umsetzung der neuen Website]]</p>
      </div>
    </section>
  </main>
'''
    return (head("Impressum | Finanzkanzlei am See", "Impressum der Finanzkanzlei am See GmbH, Hägerstraße 1, 88662 Überlingen – Registereintragungen, Erlaubnisse und Aufsichtsbehörden.", "impressum.html")
            + header("impressum.html") + body + footer())


def page_datenschutz():
    body = '''
  <main id="inhalt">
    <section class="page-hero">
      <div class="container prose">
        <nav class="breadcrumb" aria-label="Brotkrumen"><ol><li><a href="index.html">Start</a></li><li aria-current="page">Datenschutz</li></ol></nav>
        <h1>Datenschutzerklärung</h1>
        <p class="placeholder-note">[[ERSETZEN: Vollständige Datenschutzerklärung durch Datenschutzbeauftragte/n oder Anwalt erstellen lassen. Die folgenden Punkte beschreiben nur, was die Website technisch tut – sie sind keine Rechtsberatung.]]</p>

        <h2>Verantwortliche Stelle</h2>
        <p>Finanzkanzlei am See GmbH, Hägerstraße 1, 88662 Überlingen, Telefon +49 7551 93771-0, E-Mail info@fksee.de</p>
        <p>[[ERSETZEN: Kontaktdaten des/der Datenschutzbeauftragten]]</p>

        <h2>Was diese Website technisch tut</h2>
        <h3>Hosting</h3>
        <p>[[ERSETZEN: Angaben zum Hoster, z. B. Netlify, Inc. – Server-Logfiles, Auftragsverarbeitungsvertrag, Drittlandübermittlung]]</p>
        <h3>Kontaktformular</h3>
        <p>[[ERSETZEN: Verarbeitung der Formulardaten (Name, Telefon, E-Mail, Anliegen, Standort, Nachricht), Rechtsgrundlage, Speicherdauer, Empfänger, z. B. Netlify Forms]]</p>
        <h3>Schriften</h3>
        <p>Die Schriften „Fraunces“ und „Instrument Sans“ werden lokal von diesem Server geladen. Es findet keine Verbindung zu Google oder anderen Schriftanbietern statt.</p>
        <h3>Cookies, Tracking, externe Inhalte</h3>
        <p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Tracking-Dienste und bindet keine externen Karten, Videos oder Social-Media-Inhalte ein. Der Budgetrechner läuft vollständig in Ihrem Browser; Eingaben werden nicht übertragen.</p>

        <h2>Ihre Rechte</h2>
        <p>[[ERSETZEN: Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit, Widerspruch und Beschwerde bei der Aufsichtsbehörde]]</p>
      </div>
    </section>
  </main>
'''
    return (head("Datenschutzerklärung | Finanzkanzlei am See", "Datenschutzerklärung der Finanzkanzlei am See GmbH: welche Daten diese Website verarbeitet – ohne Cookies, ohne Tracking, mit lokal gehosteten Schriften.", "datenschutz.html")
            + header("datenschutz.html") + body + footer())


def page_404():
    body = f'''
  <main id="inhalt">
    <section class="section">
      <div class="container notfound">
        <p class="notfound__num" aria-hidden="true">404</p>
        <h1>Diese Seite ist leider abgetaucht.</h1>
        <p class="lead">Vielleicht wurde sie verschoben – oder der Link war nicht ganz richtig. Hier geht es weiter:</p>
        <div class="hero__actions mt-4">
          <a class="btn btn--accent" href="index.html">Zur Startseite</a>
          <a class="btn btn--ghost" href="baufinanzierung.html">Baufinanzierung</a>
          <a class="btn btn--ghost" href="kontakt.html">Kontakt</a>
        </div>
      </div>
    </section>
  </main>
'''
    h = head("Seite nicht gefunden | Finanzkanzlei am See", "Diese Seite gibt es nicht (mehr). Hier geht es zurück zur Finanzkanzlei am See.", "404.html",
             '  <meta name="robots" content="noindex">\n')
    # 404 wird unter beliebigen Pfaden ausgeliefert → absolute Asset-Pfade
    h = h if PREVIEW else h.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="favicon', 'href="/favicon').replace('href="apple-touch', 'href="/apple-touch').replace('href="site.webmanifest', 'href="/site.webmanifest')
    import re
    page = h + header("") + body + footer()
    if PREVIEW:
        return page
    return re.sub(r'href="(?!https?:|mailto:|tel:|#|/)', 'href="/', page)


PAGES = {
    "index.html": page_index, "baufinanzierung.html": page_bau, "kapitalanlagen.html": page_kapital,
    "vermoegen.html": page_vermoegen, "standorte.html": page_standorte, "ueber-uns.html": page_ueber,
    "kontakt.html": page_kontakt, "impressum.html": page_impressum, "datenschutz.html": page_datenschutz,
    "404.html": page_404,
}

def rebase(html):
    """Variante liegt einen Ordner tiefer: gemeinsame Assets über ../ laden."""
    import re
    html = re.sub(r'(href|src)="(assets/|favicon|apple-touch|site\.webmanifest)', r'\1="../\2', html)
    return html.replace('<meta name="theme-color" content="#f3eee4">', '<meta name="theme-color" content="#ffffff">')


if __name__ == "__main__":
    out = OUT / f"variante-{THEME}" if THEME else OUT
    out.mkdir(exist_ok=True)
    for name, fn in PAGES.items():
        if THEME and name == "404.html":
            continue  # Server liefert nur die 404 im Wurzelordner aus
        html = fn()
        (out / name).write_text(rebase(html) if THEME else html, encoding="utf-8")
        print("✓", out.name + "/" + name)
