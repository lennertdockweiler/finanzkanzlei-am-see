/* ==========================================================================
   Finanzkanzlei am See – main.js
   Vanilla JS, ohne Abhängigkeiten. Wird mit `defer` geladen.
   Module: Header · Navigation · Buoyfield (Signature) · Reveal ·
           Budgetrechner · Formulare · Kleinkram
   ========================================================================== */
(() => {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ── Header: Schatten beim Scrollen ───────────────────────────────────── */
  const header = $(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ── Mobile Navigation ────────────────────────────────────────────────── */
  const toggle = $(".nav-toggle");
  const nav = $("#site-nav");
  if (toggle && nav) {
    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.querySelector(".nav-toggle__label").textContent = open ? "Schließen" : "Menü";
      nav.classList.toggle("is-open", open);
      document.body.style.overflow = open ? "hidden" : "";
      if (open) nav.querySelector("a")?.focus();
    };
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    // Beim Wechsel auf Desktop-Breite Menüzustand zurücksetzen
    window.matchMedia("(min-width: 64em)").addEventListener("change", (mq) => {
      if (mq.matches) setOpen(false);
    });
    // Klick auf Anker-Link im Menü schließt es
    nav.addEventListener("click", (e) => {
      if (e.target.closest("a") && nav.classList.contains("is-open")) setOpen(false);
    });
  }

  /* ── Signature: "1 aus 600" – Punktfeld wie Wellen auf dem See ───────── */
  const field = $("[data-buoyfield]");
  if (field) {
    const NS = "http://www.w3.org/2000/svg";
    const COLS = 30, ROWS = 20, GAP = 20, PAD = 10;
    const BUOY = { c: 21, r: 12 };       // Position "Ihrer" Bank
    const svg = field.querySelector("svg");
    const g = document.createElementNS(NS, "g");
    const dots = [];

    // Deterministischer Pseudo-Zufall, damit das Bild bei jedem Laden gleich ist
    let seed = 7;
    const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);

    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        if (r === BUOY.r && c === BUOY.c) continue;
        const el = document.createElementNS(NS, "circle");
        const depth = r / (ROWS - 1);
        el.setAttribute("class", "dot");
        el.setAttribute("cx", PAD + c * GAP);
        el.setAttribute("r", (2.2 + depth * 1.6).toFixed(2));
        el.setAttribute("opacity", (0.14 + depth * 0.5 * (0.65 + rand() * 0.35)).toFixed(2));
        g.appendChild(el);
        dots.push({ el, c, r });
      }
    }
    svg.insertBefore(g, svg.firstChild);

    const buoyGroup = svg.querySelector(".buoy-group");
    const waveY = (c, r, t) => PAD + r * GAP + Math.sin(c * 0.42 + r * 0.55 + t) * 3.2;
    const draw = (t) => {
      for (const d of dots) d.el.setAttribute("cy", waveY(d.c, d.r, t).toFixed(1));
      buoyGroup?.setAttribute("transform", `translate(0 ${(waveY(BUOY.c, BUOY.r, t) - (PAD + BUOY.r * GAP)).toFixed(1)})`);
    };
    draw(0);

    field.classList.add("is-live");

    if (!reduceMotion) {
      // Animation nur, solange das Feld sichtbar ist – spart Akku.
      let raf = 0, visible = false, last = 0;
      const loop = (ts) => {
        if (ts - last > 33) { draw(ts / 1400); last = ts; }  // ~30 fps genügen
        raf = visible ? requestAnimationFrame(loop) : 0;
      };
      new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        if (visible && !raf) raf = requestAnimationFrame(loop);
      }).observe(field);
      document.addEventListener("visibilitychange", () => {
        if (document.hidden) { visible = false; }
        else if (field.getBoundingClientRect().bottom > 0) { visible = true; if (!raf) raf = requestAnimationFrame(loop); }
      });
    }
  }

  /* ── Sanftes Einblenden von Sektionen ─────────────────────────────────── */
  if (!reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px" });
    $$("[data-reveal]").forEach((el) => { el.classList.add("reveal"); io.observe(el); });
  }

  /* ── Budgetrechner ────────────────────────────────────────────────────── */
  const calc = $("[data-calc]");
  if (calc) {
    const eur = new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
    const pct = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 2 });

    // Kaufnebenkosten Baden-Württemberg (Stand: bitte jährlich prüfen)
    const COSTS = {
      grunderwerbsteuer: 0.05,   // 5,0 % in BW
      notarGrundbuch: 0.02,      // ca. 1,5 % Notar + 0,5 % Grundbuch
      makler: 0.0357             // 3,57 % inkl. MwSt., Käuferanteil
    };

    const inputs = {
      rate: $("#calc-rate", calc),
      equity: $("#calc-equity", calc),
      interest: $("#calc-interest", calc),
      repay: $("#calc-repay", calc),
      broker: $("#calc-broker", calc)
    };
    const out = {
      rate: $("[data-out='rate']", calc),
      equity: $("[data-out='equity']", calc),
      interest: $("[data-out='interest']", calc),
      repay: $("[data-out='repay']", calc),
      price: $("[data-out='price']", calc),
      loan: $("[data-out='loan']", calc),
      extra: $("[data-out='extra']", calc),
      hint: $("[data-out='hint']", calc)
    };
    const cta = $("[data-calc-cta]", calc);
    const samePageForm = $("#formular form[data-form]");
    let msg = "";

    /**
     * Rechnet aus Monatsrate, Eigenkapital, Zins und Tilgung den maximalen Kaufpreis.
     * Annuitätendarlehen: Jahresrate = Darlehen × (Sollzins + anfängliche Tilgung)
     * Kaufpreis: (Darlehen + Eigenkapital) muss Kaufpreis + Nebenkosten decken.
     */
    const calcBudget = ({ rate, equity, interest, repay, broker }) => {
      const loan = (rate * 12) / ((interest + repay) / 100);
      const extraQuote = COSTS.grunderwerbsteuer + COSTS.notarGrundbuch + (broker ? COSTS.makler : 0);
      const price = (loan + equity) / (1 + extraQuote);
      return { loan, price, extra: price * extraQuote };
    };

    /**
     * Fachlicher Hinweis unter dem Ergebnis.
     * Banken erwarten meist, dass das Eigenkapital mindestens die Nebenkosten deckt;
     * darunter wird die Finanzierung teurer oder schwieriger.
     */
    const budgetHint = ({ equity }, { extra, price }) => {
      if (equity < extra) {
        return "Ihr Eigenkapital deckt die Nebenkosten noch nicht. Das ist lösbar – aber nicht mit jeder Bank. Genau dafür vergleichen wir.";
      }
      if (equity < extra + 0.1 * price) {
        return "Mit diesem Eigenkapital sind die Nebenkosten gedeckt. Für Top-Konditionen lohnt sich ein Blick auf KfW- und L-Bank-Programme.";
      }
      return "Gute Ausgangslage: Mit viel Eigenkapital verhandeln wir bei den Banken bessere Zinsen für Sie.";
    };

    const setTrack = (el) => {
      const p = ((el.value - el.min) / (el.max - el.min)) * 100;
      el.style.setProperty("--pct", `${p}%`);
    };

    const update = () => {
      const v = {
        rate: +inputs.rate.value,
        equity: +inputs.equity.value,
        interest: +inputs.interest.value,
        repay: +inputs.repay.value,
        broker: inputs.broker.checked
      };
      Object.values(inputs).forEach((el) => el.type === "range" && setTrack(el));
      out.rate.textContent = eur.format(v.rate);
      out.equity.textContent = eur.format(v.equity);
      out.interest.textContent = `${pct.format(v.interest)} %`;
      out.repay.textContent = `${pct.format(v.repay)} %`;
      // Screenreader lesen sonst "60000" statt "60.000 €"
      ["rate", "equity", "interest", "repay"].forEach((k) => inputs[k].setAttribute("aria-valuetext", out[k].textContent));

      const res = calcBudget(v);
      out.price.textContent = eur.format(Math.round(res.price / 1000) * 1000);
      out.loan.textContent = eur.format(res.loan);
      out.extra.textContent = eur.format(res.extra);
      out.hint.textContent = budgetHint(v, res);

      // Ergebnis an das Kontaktformular übergeben
      if (cta) {
        msg = `Budgetrechner: Monatsrate ${eur.format(v.rate)}, Eigenkapital ${eur.format(v.equity)}, ` +
          `Zins ${pct.format(v.interest)} %, Tilgung ${pct.format(v.repay)} % → Kaufpreis ca. ${out.price.textContent}.`;
        cta.href = samePageForm ? "#formular" : `kontakt.html?anliegen=kauf&nachricht=${encodeURIComponent(msg)}#formular`;
      }
    };

    // Steht das Formular auf derselben Seite (Startseite), wird es direkt vorbefüllt statt neu zu laden.
    cta?.addEventListener("click", () => {
      if (!samePageForm) return;
      samePageForm.querySelector("[name='anliegen'][value='kauf']")?.click();
      const field = samePageForm.querySelector("[name='nachricht']");
      if (field) field.value = msg;
    });

    calc.addEventListener("input", update);
    update();
  }

  /* ── Formulare: Validierung, Honeypot, Versand ───────────────────────── */
  const MESSAGES = {
    valueMissing: {
      name: "Bitte nennen Sie uns Ihren Namen.",
      contact: "Bitte geben Sie eine Telefonnummer oder E-Mail-Adresse an, damit wir Sie erreichen.",
      anliegen: "Bitte wählen Sie, worum es geht.",
      default: "Bitte füllen Sie dieses Feld aus."
    },
    typeMismatch: "Diese E-Mail-Adresse sieht unvollständig aus – bitte prüfen Sie z. B. das @.",
    patternMismatch: "Bitte geben Sie eine gültige Telefonnummer ein (nur Ziffern, Leerzeichen, +, /, -)."
  };

  const fieldOf = (input) => input.closest(".field, .choice-group");

  const validateInput = (input) => {
    const wrap = fieldOf(input);
    if (!wrap) return true;
    const errorEl = wrap.querySelector(".field__error");
    let msg = "";
    const v = input.validity;
    if (v.valueMissing) msg = MESSAGES.valueMissing[input.dataset.msg] || MESSAGES.valueMissing.default;
    else if (v.typeMismatch) msg = MESSAGES.typeMismatch;
    else if (v.patternMismatch) msg = input.type === "email" ? MESSAGES.typeMismatch : MESSAGES.patternMismatch;

    const group = wrap.matches(".choice-group") ? $$("input", wrap) : [input];
    group.forEach((el) => el.setAttribute("aria-invalid", msg ? "true" : "false"));
    // "Telefon oder E-Mail" nur einmal (am Telefonfeld) erklären – E-Mail-Feld wird nur rot markiert
    const quiet = v.valueMissing && input.name === "email";
    wrap.classList.toggle("has-error", Boolean(msg) && !quiet);
    if (errorEl) errorEl.textContent = quiet ? "" : msg;
    return !msg;
  };

  // Telefon ODER E-Mail ist Pflicht – nicht beides.
  const syncContactRequired = (form) => {
    const phone = form.querySelector("[name='telefon']");
    const mail = form.querySelector("[name='email']");
    if (!phone || !mail) return;
    const either = phone.value.trim() || mail.value.trim();
    phone.required = !either;
    mail.required = !either;
  };

  const encode = (data) => new URLSearchParams(data).toString();

  $$("form[data-form]").forEach((form) => {
    const status = form.querySelector(".form-status");
    const submit = form.querySelector("[type='submit']");
    const submitLabel = submit?.textContent.trim();

    // Vorbelegung aus der URL (z. B. vom Budgetrechner oder einer Leistungsseite)
    const params = new URLSearchParams(location.search);
    const anliegen = params.get("anliegen");
    if (anliegen) form.querySelector(`[name='anliegen'][value='${CSS.escape(anliegen)}']`)?.click();
    const standort = params.get("standort");
    const select = form.querySelector("[name='standort']");
    if (standort && select && [...select.options].some((o) => o.value === standort)) select.value = standort;
    const nachricht = params.get("nachricht");
    const msgField = form.querySelector("[name='nachricht']");
    if (nachricht && msgField && !msgField.value) msgField.value = nachricht.slice(0, 600);

    form.addEventListener("input", (e) => {
      if (e.target.name === "telefon" || e.target.name === "email") syncContactRequired(form);
      if (fieldOf(e.target)?.classList.contains("has-error")) validateInput(e.target);
    });
    form.addEventListener("focusout", (e) => {
      if (e.target.matches("input:not([type='radio']):not([type='checkbox']), textarea, select") && e.target.value) {
        validateInput(e.target);
      }
    });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      syncContactRequired(form);

      const controls = $$("input:not([type='hidden']):not([tabindex='-1']), select, textarea", form);
      const results = controls.map(validateInput);
      const firstInvalid = controls[results.indexOf(false)];
      if (firstInvalid) {
        showStatus("error", "Da fehlt noch etwas.", "Bitte prüfen Sie die markierten Felder.");
        firstInvalid.focus();
        return;
      }

      // Honeypot: Bots füllen das unsichtbare Feld aus → still "erfolgreich" beenden
      if (form.querySelector(".hp-field input")?.value) {
        showSuccess();
        return;
      }

      setLoading(true);
      try {
        const res = await fetch(form.getAttribute("action") || "/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: encode(new FormData(form))
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        form.reset();
        showSuccess();
      } catch (err) {
        console.warn("Formularversand fehlgeschlagen:", err.message);
        showStatus(
          "error",
          "Ihre Anfrage konnte gerade nicht gesendet werden.",
          "Bitte rufen Sie uns an unter 07551 93771-0 oder schreiben Sie an info@fksee.de – wir melden uns trotzdem schnell."
        );
      } finally {
        setLoading(false);
      }
    });

    function setLoading(on) {
      if (!submit) return;
      submit.disabled = on;
      submit.classList.toggle("is-loading", on);
      submit.textContent = on ? "Wird gesendet …" : submitLabel;
      form.setAttribute("aria-busy", String(on));
    }
    function showSuccess() {
      showStatus("success", "Danke – Ihre Anfrage ist bei uns.", "Wir melden uns bei Ihnen, um einen Termin zu vereinbaren – vor Ort, am Telefon oder per Video, wie Sie es angegeben haben.");
    }
    function showStatus(type, title, text) {
      if (!status) return;
      const strong = document.createElement("strong");
      const p = document.createElement("p");
      strong.textContent = title;
      p.textContent = text;
      status.className = `form-status form-status--${type} is-visible`;
      status.replaceChildren(strong, p);
      if (type === "success") status.focus();
    }
  });

  /* ── Kleinkram ────────────────────────────────────────────────────────── */
  $$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
