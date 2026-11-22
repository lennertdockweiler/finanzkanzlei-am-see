# Finanzkanzlei am See – Website-Relaunch (Entwurf)

**Vorschau – zwei Farbvarianten** (oben auf jeder Seite umschaltbar):

- **Sand:** https://lennertdockweiler.github.io/finanzkanzlei-am-see/
- **Blau:** https://lennertdockweiler.github.io/finanzkanzlei-am-see/variante-blau/

Variante Blau: mehr Weiß, Bodensee-Blau als Arbeitsfarbe (Buttons, Links, Akzente). Orange markiert nur noch „Ihres“ – die Boje „Ihre Bank“, den berechneten Kaufpreis, „0 €“ und die Zentrale auf der Karte. Layout, Texte und Funktionen sind identisch; die Variante überschreibt nur Farben (`assets/css/theme-blau.css`).

> ⚠️ Das ist ein **Entwurf zur internen Abstimmung**, nicht die offizielle Website der Finanzkanzlei am See GmbH.
> Alle Seiten sind auf `noindex` gesetzt. Stellen mit `[[ERSETZEN: …]]` sind bewusst markierte Platzhalter
> (fehlende Adressen, Fotos, Rechtstexte).

## Was drin ist

- 10 Seiten: Start, Baufinanzierung, Kapitalanlagen, Vermögen, Standorte, Über uns, Kontakt, Impressum, Datenschutz, 404
- Signature-Element „1 aus 600“: Punktfeld, in dem eine einzelne Boje für die passende Bank steht
- Budgetrechner (läuft komplett im Browser), schematische Standortkarte als SVG – **ohne Cookies, Tracking oder externe Dienste**
- Beratungsformular für Netlify Forms (auf GitHub Pages wird nicht gesendet – dort erscheint die Fehlermeldung mit Telefonnummer)
- Schriften Fraunces + Instrument Sans, selbst gehostet

## Lokal ansehen

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

## Seiten neu erzeugen

Header, Navigation und Footer kommen aus `_build/partials.py`, die Seiteninhalte aus `_build/build.py`.

```bash
cd _build
PREVIEW=1 python3 build.py ..   # Vorschau: mit noindex, relative Pfade auf der 404-Seite
PREVIEW=1 THEME=blau python3 build.py ..   # Variante Blau → ./variante-blau/
python3 build.py ..             # LIVE-Build: ohne noindex – vor dem Livegang verwenden!
python3 qa.py ..                # prüft Links, Anker, h1, Meta, Platzhalter
```

## Livegang (Netlify)

1. Live-Build erzeugen (ohne `PREVIEW`), alle `[[ERSETZEN]]`-Stellen erledigen.
2. Ordner auf Netlify deployen – `netlify.toml` setzt Sicherheits-Header und die 404-Seite.
3. Netlify Forms aktiviert sich automatisch; Auftragsverarbeitungsvertrag abschließen und in der Datenschutzerklärung nennen.
