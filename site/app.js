/* Marina Immo — front-end (vanilla JS, no dependencies) */
(function () {
  "use strict";

  var CFG = window.SITE_CONFIG || {};
  var LISTINGS = Array.isArray(window.LISTINGS) ? window.LISTINGS : [];
  var COUNTRIES = window.COUNTRIES || {};
  var COUNTRY_KEYS = ["dubai", "bali", "georgia"];
  var LANDING = { dubai: "dubai.html", bali: "bali.html", georgia: "georgie.html" };
  var BRAND = CFG.brand || "Marina Immo";
  var WA_NUMBER = String(CFG.whatsapp || "").replace(/\D/g, "");
  var EMAIL = CFG.email || "";
  var body = document.body;
  var PAGE_COUNTRY = body.getAttribute("data-country") || "";
  var PAGE = body.getAttribute("data-page") || "home";

  /* ---------- Safe storage ---------- */
  function store(type, key, val) {
    try {
      var s = window[type];
      if (val === undefined) return s.getItem(key);
      if (val === null) s.removeItem(key); else s.setItem(key, val);
    } catch (e) { return null; }
    return null;
  }

  /* ---------- Dictionary ---------- */
  var DICT = {
    fr: {
      skip: "Aller au contenu",
      navLabel: "Navigation principale", langLabel: "Langue",
      navListings: "Biens", navDestinations: "Destinations", navContact: "Contact",
      title_home: "Marina Immo — Investir à Dubaï, Bali et en Géorgie",
      title_dubai: "Investir à Dubaï — Biens prêts et sur plan | Marina Immo",
      title_bali: "Investir à Bali — Villas | Marina Immo",
      title_georgia: "Investir en Géorgie — Appartements à Tbilissi et Batoumi | Marina Immo",
      title_merci: "Merci — Marina Immo",
      title_legal: "Mentions légales — Marina Immo",
      title_privacy: "Politique de confidentialité — Marina Immo",
      heroEyebrow: "Dubaï · Bali · Géorgie",
      heroTitle: "Investissez à Dubaï, Bali et en Géorgie. Avec des chiffres, pas des promesses.",
      heroLead: "Des biens sélectionnés, prêts ou sur plan. Une analyse claire du prix, du rendement et des risques. Un accompagnement en français, de la recherche à la remise des clés.",
      heroPickLabel: "Choisir une destination",
      heroCta: "Parler à un conseiller",
      heroEyebrow_dubai: "Immobilier à Dubaï",
      heroTitle_dubai: "Investir à Dubaï : pas d'impôt sur le revenu aux Émirats, des prix comparés aux ventes réelles.",
      heroLead_dubai: "Appartements, villas et biens sur plan dans les meilleurs quartiers. Chaque prix est comparé aux transactions du Dubai Land Department avant de vous être proposé.",
      heroEyebrow_bali: "Immobilier à Bali",
      heroTitle_bali: "Investir à Bali : des villas tropicales pensées pour la location saisonnière.",
      heroLead_bali: "Canggu, Uluwatu, Ubud… Des villas sélectionnées pour la location saisonnière, avec un cadre juridique expliqué clairement.",
      heroEyebrow_georgia: "Immobilier en Géorgie",
      heroTitle_georgia: "Investir en Géorgie : un ticket d'entrée bas, en pleine propriété.",
      heroLead_georgia: "Tbilissi et Batoumi : des appartements à prix d'entrée accessible, achetables en pleine propriété par les étrangers.",
      seeListings: "Voir les biens",
      seeListingsIn: "Voir les biens · {country}",
      landingPage: "Page dédiée",
      country_dubai: "Dubaï", country_bali: "Bali", country_georgia: "Géorgie",
      listingsEyebrow: "Sélection", listingsTitle: "Nos biens",
      filtersLabel: "Filtrer les biens",
      fCountry: "Pays", fType: "Type", fStatus: "Statut", fBeds: "Chambres min.", fBudget: "Budget max (USD)", fReset: "Réinitialiser",
      optAll: "Tous", optAny: "Indifférent", optChoose: "Choisir…",
      type_apartment: "Appartement", type_villa: "Villa", type_penthouse: "Penthouse", type_townhouse: "Maison de ville",
      status_ready: "Prêt à emménager", status_offplan: "Sur plan",
      count0: "Aucun bien", count1: "1 bien", countN: "{n} biens",
      emptyText: "Aucun bien ne correspond à ces critères.",
      sample: "Exemple", photoSoon: "Photo à venir",
      studio: "Studio", beds: "{n} ch.", baths: "{n} sdb",
      viewDetail: "Voir le détail",
      dType: "Type", dStatus: "Statut", dBeds: "Chambres", dBaths: "Salles de bain", dSize: "Surface",
      dTenure: "Régime de propriété", dHandover: "Livraison", dYield: "Rendement locatif brut estimé",
      dPermit: "Permis / Permit", dRef: "Référence", dFeatures: "Points forts", dPrice: "Prix",
      sampleNote: "Annonce d'exemple, à titre d'illustration. Contactez-nous pour les biens réellement disponibles.",
      interested: "Je suis intéressé", close: "Fermer",
      waListing: "Bonjour {brand}, je suis intéressé(e) par le bien {id} — {title}. Pouvez-vous m'en dire plus ?",
      waDefault: "Bonjour {brand}, je souhaite des informations sur l'investissement immobilier.",
      waDefaultCountry: "Bonjour {brand}, je souhaite des informations sur l'investissement immobilier à {country}.",
      destEyebrow: "Trois marchés", destTitle: "Destinations",
      focusEyebrow: "Pourquoi ce marché",
      whyEyebrow: "Notre méthode", whyTitle: "Pourquoi Marina Immo",
      why1Title: "Expertise locale", why1Text: "Nous connaissons chaque quartier, chaque promoteur et les pièges à éviter sur place.",
      why2Title: "Analyse chiffrée", why2Text: "Prix comparés aux transactions réelles, notamment les données du Dubai Land Department. Pas d'estimation au doigt mouillé.",
      why3Title: "De la recherche aux clés", why3Text: "Sélection, visite, négociation, démarches, remise des clés : un seul interlocuteur du début à la fin.",
      why4Title: "Français & anglais", why4Text: "Tout est expliqué dans votre langue. Les documents, les chiffres, les étapes.",
      contactEyebrow: "Contact", contactTitle: "Parlons de votre projet",
      contactLead: "Dites-nous ce que vous cherchez. Réponse sous 24 h ouvrées, avec une première sélection adaptée à votre budget.",
      waCta: "Écrire sur WhatsApp", orEmail: "Ou par e-mail :",
      lName: "Nom complet", lEmail: "E-mail", lPhone: "WhatsApp / téléphone", lCountry: "Pays d'intérêt",
      lBudget: "Budget (USD)", lRef: "Référence du bien", lMessage: "Message",
      lConsent: "J'accepte que {brand} utilise ces informations pour me recontacter au sujet de mon projet. Elles ne sont ni vendues ni partagées. Voir la <a href=\"confidentialite.html\">politique de confidentialité</a> et les <a href=\"mentions-legales.html\">mentions légales</a>.",
      phName: "Prénom Nom", phEmail: "vous@exemple.com", phPhone: "+33 6 12 34 56 78", phRef: "ex. DXB-001", phMessage: "Votre projet, vos délais, vos questions…",
      undecided: "Je ne sais pas encore",
      budget1: "Moins de 250 000 $", budget2: "250 000 – 500 000 $", budget3: "500 000 – 1 000 000 $", budget4: "1 – 2 millions $", budget5: "Plus de 2 millions $",
      budgetMax: "≤ {n} USD",
      submit: "Envoyer ma demande", requiredNote: "* Champs obligatoires",
      footerTag: "Immobilier d'investissement · Dubaï · Bali · Géorgie",
      disclaimer: "Les biens marqués « Exemple » sont des illustrations. Les prix sont indicatifs et peuvent évoluer. Les rendements affichés sont des estimations brutes, non garanties. Ce site ne constitue pas un conseil en investissement.",
      rights: "Tous droits réservés.",
      legalLink: "Mentions légales", privacyLink: "Confidentialité", cookieLink: "Cookies",
      backHome: "Retour à l'accueil",
      merciEyebrow: "Demande envoyée",
      merciTitle: "Merci, votre demande est bien reçue.",
      merciText: "Un conseiller vous répond sous 24 h ouvrées. Pour aller plus vite, écrivez-nous directement sur WhatsApp.",
      cookieTitle: "Cookies",
      cookieText: "Nous utilisons des cookies de mesure d'audience et publicitaires (Google, Meta, TikTok) uniquement si vous les acceptez. Le site fonctionne normalement si vous refusez.",
      cookieMore: "En savoir plus",
      cookieAccept: "Accepter", cookieRefuse: "Refuser"
    },
    en: {
      skip: "Skip to content",
      navLabel: "Main navigation", langLabel: "Language",
      navListings: "Properties", navDestinations: "Destinations", navContact: "Contact",
      title_home: "Marina Immo — Invest in Dubai, Bali and Georgia",
      title_dubai: "Invest in Dubai — Ready and off-plan properties | Marina Immo",
      title_bali: "Invest in Bali — Villas | Marina Immo",
      title_georgia: "Invest in Georgia — Apartments in Tbilisi and Batumi | Marina Immo",
      title_merci: "Thank you — Marina Immo",
      title_legal: "Legal notice — Marina Immo",
      title_privacy: "Privacy policy — Marina Immo",
      heroEyebrow: "Dubai · Bali · Georgia",
      heroTitle: "Invest in Dubai, Bali and Georgia. Backed by numbers, not promises.",
      heroLead: "Hand-picked properties, ready or off-plan. A clear analysis of price, yield and risk. Guidance in English and French, from search to handover.",
      heroPickLabel: "Choose a destination",
      heroCta: "Talk to an advisor",
      heroEyebrow_dubai: "Dubai real estate",
      heroTitle_dubai: "Invest in Dubai: no personal income tax in the UAE, prices compared with real sales.",
      heroLead_dubai: "Apartments, villas and off-plan homes in the best communities. Every price is compared with Dubai Land Department transactions before we show it to you.",
      heroEyebrow_bali: "Bali real estate",
      heroTitle_bali: "Invest in Bali: tropical villas designed for holiday rental.",
      heroLead_bali: "Canggu, Uluwatu, Ubud… Villas selected for short-term rental, with the legal framework explained clearly.",
      heroEyebrow_georgia: "Georgia real estate",
      heroTitle_georgia: "Invest in Georgia: low entry price, full freehold ownership.",
      heroLead_georgia: "Tbilisi and Batumi: apartments at an accessible entry price that foreigners can buy freehold.",
      seeListings: "See properties",
      seeListingsIn: "See properties · {country}",
      landingPage: "Dedicated page",
      country_dubai: "Dubai", country_bali: "Bali", country_georgia: "Georgia",
      listingsEyebrow: "Selection", listingsTitle: "Our properties",
      filtersLabel: "Filter properties",
      fCountry: "Country", fType: "Type", fStatus: "Status", fBeds: "Min. bedrooms", fBudget: "Max budget (USD)", fReset: "Reset",
      optAll: "All", optAny: "Any", optChoose: "Choose…",
      type_apartment: "Apartment", type_villa: "Villa", type_penthouse: "Penthouse", type_townhouse: "Townhouse",
      status_ready: "Ready", status_offplan: "Off-plan",
      count0: "No properties", count1: "1 property", countN: "{n} properties",
      emptyText: "No property matches these filters.",
      sample: "Sample", photoSoon: "Photo coming soon",
      studio: "Studio", beds: "{n} bd", baths: "{n} ba",
      viewDetail: "View details",
      dType: "Type", dStatus: "Status", dBeds: "Bedrooms", dBaths: "Bathrooms", dSize: "Size",
      dTenure: "Tenure", dHandover: "Handover", dYield: "Estimated gross rental yield",
      dPermit: "Permis / Permit", dRef: "Reference", dFeatures: "Highlights", dPrice: "Price",
      sampleNote: "Sample listing, for illustration only. Contact us for properties actually available.",
      interested: "I'm interested", close: "Close",
      waListing: "Hello {brand}, I'm interested in listing {id} — {title}. Could you tell me more?",
      waDefault: "Hello {brand}, I'd like information about property investment.",
      waDefaultCountry: "Hello {brand}, I'd like information about property investment in {country}.",
      destEyebrow: "Three markets", destTitle: "Destinations",
      focusEyebrow: "Why this market",
      whyEyebrow: "Our approach", whyTitle: "Why Marina Immo",
      why1Title: "Local expertise", why1Text: "We know every community, every developer and the pitfalls to avoid on the ground.",
      why2Title: "Data-driven analysis", why2Text: "Prices compared with real transactions, including Dubai Land Department data. No guesswork.",
      why3Title: "From search to handover", why3Text: "Selection, viewings, negotiation, paperwork, handover: one point of contact from start to finish.",
      why4Title: "French & English", why4Text: "Everything explained in your language. The documents, the numbers, the steps.",
      contactEyebrow: "Contact", contactTitle: "Let's talk about your project",
      contactLead: "Tell us what you are looking for. Reply within one business day, with a first shortlist that fits your budget.",
      waCta: "Message us on WhatsApp", orEmail: "Or by email:",
      lName: "Full name", lEmail: "Email", lPhone: "WhatsApp / phone", lCountry: "Country of interest",
      lBudget: "Budget (USD)", lRef: "Property reference", lMessage: "Message",
      lConsent: "I agree that {brand} may use this information to contact me about my project. It is never sold or shared. See the <a href=\"confidentialite.html\">privacy policy</a> and <a href=\"mentions-legales.html\">legal notice</a>.",
      phName: "First Last", phEmail: "you@example.com", phPhone: "+44 7700 900123", phRef: "e.g. DXB-001", phMessage: "Your project, timing, questions…",
      undecided: "Not sure yet",
      budget1: "Under $250,000", budget2: "$250,000 – $500,000", budget3: "$500,000 – $1,000,000", budget4: "$1M – $2M", budget5: "Over $2M",
      budgetMax: "≤ {n} USD",
      submit: "Send my request", requiredNote: "* Required fields",
      footerTag: "Investment real estate · Dubai · Bali · Georgia",
      disclaimer: "Listings marked \"Sample\" are illustrations. Prices are indicative and may change. Yields shown are gross estimates and are not guaranteed. This website does not constitute investment advice.",
      rights: "All rights reserved.",
      legalLink: "Legal notice", privacyLink: "Privacy", cookieLink: "Cookies",
      backHome: "Back to home",
      merciEyebrow: "Request sent",
      merciTitle: "Thank you, we have received your request.",
      merciText: "An advisor will reply within one business day. For a faster answer, message us directly on WhatsApp.",
      cookieTitle: "Cookies",
      cookieText: "We use analytics and advertising cookies (Google, Meta, TikTok) only if you accept them. The site works normally if you decline.",
      cookieMore: "Learn more",
      cookieAccept: "Accept", cookieRefuse: "Decline"
    }
  };

  /* ---------- Language ---------- */
  var LANG = store("localStorage", "mi_lang");
  if (LANG !== "fr" && LANG !== "en") LANG = CFG.defaultLang === "en" ? "en" : "fr";

  function t(key, vars) {
    var s = (DICT[LANG] && DICT[LANG][key]) || DICT.fr[key] || key;
    vars = vars || {};
    vars.brand = vars.brand || BRAND;
    return s.replace(/\{(\w+)\}/g, function (m, k) { return vars[k] != null ? vars[k] : m; });
  }
  function L(obj) { // pick localized value from {fr,en}
    if (obj == null) return "";
    if (typeof obj !== "object" || Array.isArray(obj)) return obj;
    return obj[LANG] != null ? obj[LANG] : (obj.fr != null ? obj.fr : obj.en);
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function num(n) {
    return Math.round(Number(n) || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, LANG === "fr" ? " " : ",");
  }
  function countryName(c) {
    return (COUNTRIES[c] && L(COUNTRIES[c].name)) || t("country_" + c);
  }
  function handoverText(h) {
    return LANG === "en" ? String(h).replace(/^T([1-4])\b/, "Q$1") : String(h);
  }
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  function waUrl(text) {
    return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(text);
  }
  function defaultWaText() {
    return PAGE_COUNTRY ? t("waDefaultCountry", { country: countryName(PAGE_COUNTRY) }) : t("waDefault");
  }

  function applyI18n() {
    document.documentElement.lang = LANG;
    $$("[data-i18n]").forEach(function (el) { el.textContent = t(el.getAttribute("data-i18n")); });
    $$("[data-i18n-html]").forEach(function (el) { el.innerHTML = t(el.getAttribute("data-i18n-html")); });
    $$("[data-i18n-ph]").forEach(function (el) { el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph"))); });
    $$("[data-i18n-aria]").forEach(function (el) { el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria"))); });
    $$("[data-num]").forEach(function (el) { el.textContent = t("budgetMax", { n: num(el.getAttribute("data-num")) }); });
    $$("[data-lang-block]").forEach(function (el) { el.hidden = el.getAttribute("data-lang-block") !== LANG; });
    $$("[data-brand]").forEach(function (el) { el.textContent = BRAND; });
    var tk = body.getAttribute("data-title-key");
    if (tk) document.title = t(tk);
    $$(".lang-btn").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === LANG)); });
    $$("[data-wa-link]").forEach(function (a) { a.href = waUrl(defaultWaText()); });
    $$("[data-email-link]").forEach(function (a) { a.href = "mailto:" + EMAIL; a.textContent = EMAIL; });
  }

  function setLang(l) {
    if (l === LANG) return;
    LANG = l;
    store("localStorage", "mi_lang", l);
    applyI18n();
    renderAll();
    if (openId) renderModal(openId);
    renderBanner();
  }
  $$(".lang-btn").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
  });

  /* ---------- Footer extras ---------- */
  var yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
  $$("[data-rera]").forEach(function (el) {
    if (CFG.reraOrn) { el.textContent = "RERA ORN: " + CFG.reraOrn; el.hidden = false; }
  });

  /* ---------- Listings ---------- */
  var grid = $("#grid");
  var F = {
    country: $("#f-country"), type: $("#f-type"), status: $("#f-status"),
    beds: $("#f-beds"), budget: $("#f-budget")
  };

  function placeholder(l, cls) {
    var label = countryName(l.country);
    return '<div class="ph ph-' + esc(l.country) + " " + (cls || "") + '" role="img" aria-label="' +
      esc(t("photoSoon") + " — " + label + ", " + l.city) + '">' +
      '<span class="ph-country">' + esc(label) + "</span>" +
      '<span class="ph-note">' + esc(t("photoSoon")) + "</span></div>";
  }
  function badges(l) {
    var b = '<span class="badge badge-status badge-' + esc(l.status) + '">' + esc(t("status_" + l.status)) + "</span>";
    if (l.sample) b += '<span class="badge badge-sample">' + esc(t("sample")) + "</span>";
    return '<div class="badges">' + b + "</div>";
  }
  function bedText(n) { return Number(n) === 0 ? t("studio") : t("beds", { n: n }); }
  function priceHtml(l) {
    var h = '<p class="price">' + esc(num(l.price)) + " " + esc(l.currency) + "</p>";
    if (l.currency !== "USD" && l.price_usd) h += '<p class="price-usd">≈ ' + esc(num(l.price_usd)) + " USD</p>";
    return h;
  }

  function card(l) {
    return '<article class="card">' +
      '<div class="card-media">' + placeholder(l) + badges(l) + "</div>" +
      '<div class="card-body">' +
      '<p class="card-city">' + esc(l.city) + " · " + esc(countryName(l.country)) + "</p>" +
      '<h3 class="card-title"><button type="button" class="card-link" data-open="' + esc(l.id) + '">' + esc(L(l.title)) + "</button></h3>" +
      priceHtml(l) +
      '<ul class="specs">' +
      "<li>" + esc(bedText(l.bedrooms)) + "</li>" +
      "<li>" + esc(t("baths", { n: l.bathrooms })) + "</li>" +
      "<li>" + esc(num(l.size_sqm)) + " m²</li>" +
      "</ul>" +
      '<p class="card-foot"><span class="ref">' + esc(l.id) + '</span><span class="more" aria-hidden="true">' + esc(t("viewDetail")) + " →</span></p>" +
      "</div></article>";
  }

  function filtered() {
    var c = F.country.value, ty = F.type.value, st = F.status.value,
      b = parseInt(F.beds.value, 10) || 0, max = parseInt(F.budget.value, 10) || 0;
    return LISTINGS.filter(function (l) {
      return (!c || l.country === c) && (!ty || l.type === ty) && (!st || l.status === st) &&
        (Number(l.bedrooms) || 0) >= b && (!max || Number(l.price_usd) <= max);
    });
  }

  function renderListings() {
    if (!grid) return;
    var list = filtered();
    grid.innerHTML = list.map(card).join("");
    var n = list.length;
    $("#result-count").textContent = n === 0 ? t("count0") : n === 1 ? t("count1") : t("countN", { n: n });
    $("#empty").hidden = n !== 0;
  }

  function resetFilters() {
    Object.keys(F).forEach(function (k) { F[k].value = ""; });
    if (PAGE_COUNTRY) F.country.value = PAGE_COUNTRY;
    renderListings();
  }

  function pickCountry(c) {
    if (!F.country) return;
    F.country.value = c;
    renderListings();
    var target = $("#biens");
    if (target) target.scrollIntoView({ behavior: prefersReduced() ? "auto" : "smooth", block: "start" });
  }
  function prefersReduced() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  if (grid) {
    Object.keys(F).forEach(function (k) { F[k].addEventListener("change", renderListings); });
    $$("#f-reset, [data-reset]").forEach(function (b) { b.addEventListener("click", resetFilters); });
    // Initial country: ?pays= param, else page country
    var qp = "";
    try { qp = (new URLSearchParams(location.search).get("pays") || "").toLowerCase(); } catch (e) { /* old browser */ }
    if (qp === "georgie") qp = "georgia";
    if (qp === "dubai" || qp === "dubaï") qp = "dubai";
    F.country.value = COUNTRY_KEYS.indexOf(qp) > -1 ? qp : (PAGE_COUNTRY || "");
    grid.addEventListener("click", function (e) {
      var art = e.target.closest(".card");
      if (!art) return;
      var btn = $(".card-link", art);
      if (btn) openModal(btn.getAttribute("data-open"), btn);
    });
  }
  document.addEventListener("click", function (e) {
    var p = e.target.closest("[data-pick]");
    if (p) { e.preventDefault(); pickCountry(p.getAttribute("data-pick")); }
  });

  /* ---------- Destinations ---------- */
  function destBlock(c, big) {
    var d = COUNTRIES[c];
    if (!d) return "";
    var hl = L(d.highlights) || [];
    var actions = '<div class="dest-actions"><button type="button" class="btn ' + (big ? "btn-primary" : "btn-outline-gold") + '" data-pick="' + c + '">' +
      esc(t("seeListingsIn", { country: countryName(c) })) + "</button>";
    if (!big && PAGE_COUNTRY !== c) actions += '<a class="dest-link" href="' + LANDING[c] + '">' + esc(t("landingPage")) + " →</a>";
    actions += "</div>";
    return '<article class="dest dest-' + c + (big ? " dest-big" : "") + '">' +
      '<div class="dest-band" aria-hidden="true"></div>' +
      "<h3>" + esc(L(d.name)) + "</h3>" +
      '<p class="dest-tagline">' + esc(L(d.tagline)) + "</p>" +
      '<ul class="dest-list">' + hl.map(function (h) { return "<li>" + esc(h) + "</li>"; }).join("") + "</ul>" +
      actions + "</article>";
  }
  function renderDestinations() {
    var g = $("#dest-grid");
    if (g) g.innerHTML = COUNTRY_KEYS.map(function (c) { return destBlock(c, false); }).join("");
    var f = $("#dest-focus");
    if (f && PAGE_COUNTRY) f.innerHTML = destBlock(PAGE_COUNTRY, true);
  }

  function renderAll() { renderListings(); renderDestinations(); }

  /* ---------- Modal ---------- */
  var modal = $("#modal");
  var openId = null, lastFocus = null;
  var outside = $$("body > header, body > main, body > footer, .skip-link");

  function findListing(id) {
    id = String(id || "").toUpperCase();
    for (var i = 0; i < LISTINGS.length; i++) if (String(LISTINGS[i].id).toUpperCase() === id) return LISTINGS[i];
    return null;
  }
  function row(label, value) {
    return value == null || value === "" ? "" : "<div><dt>" + esc(label) + "</dt><dd>" + esc(value) + "</dd></div>";
  }
  function renderModal(id) {
    var l = findListing(id);
    if (!l) return false;
    var feats = L(l.features) || [];
    var title = L(l.title);
    var html =
      '<div class="modal-media">' + placeholder(l, "ph-lg") + badges(l) + "</div>" +
      '<div class="modal-content">' +
      '<p class="card-city">' + esc(l.city) + " · " + esc(countryName(l.country)) + " · " + esc(l.id) + "</p>" +
      '<h2 id="modal-title">' + esc(title) + "</h2>" +
      '<div class="modal-price">' + priceHtml(l) + "</div>" +
      (l.sample ? '<p class="sample-note">' + esc(t("sampleNote")) + "</p>" : "") +
      '<p class="modal-desc">' + esc(L(l.description)) + "</p>" +
      '<dl class="facts">' +
      row(t("dRef"), l.id) +
      row(t("dType"), t("type_" + l.type)) +
      row(t("dStatus"), t("status_" + l.status)) +
      row(t("dBeds"), Number(l.bedrooms) === 0 ? t("studio") : l.bedrooms) +
      row(t("dBaths"), l.bathrooms) +
      row(t("dSize"), num(l.size_sqm) + " m²") +
      row(t("dTenure"), L(l.tenure)) +
      (l.handover ? row(t("dHandover"), handoverText(l.handover)) : "") +
      (l.est_yield_pct != null ? row(t("dYield"), String(l.est_yield_pct).replace(".", LANG === "fr" ? "," : ".") + (LANG === "fr" ? "\u00a0%" : "%")) : "") +
      (l.permit ? row(t("dPermit"), l.permit) : "") +
      "</dl>" +
      (feats.length ? "<h3>" + esc(t("dFeatures")) + '</h3><ul class="features">' +
        feats.map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("") + "</ul>" : "") +
      '<div class="modal-actions">' +
      '<a class="btn btn-wa" target="_blank" rel="noopener" href="' + esc(waUrl(t("waListing", { id: l.id, title: title }))) + '">WhatsApp</a>' +
      '<button type="button" class="btn btn-primary" data-interested="' + esc(l.id) + '">' + esc(t("interested")) + "</button>" +
      "</div></div>";
    $("#modal-body").innerHTML = html;
    return true;
  }
  function focusables() {
    return $$('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])', modal)
      .filter(function (el) { return el.offsetParent !== null; });
  }
  function openModal(id, trigger) {
    if (!modal || !renderModal(id)) return;
    openId = findListing(id).id;
    lastFocus = trigger || document.activeElement;
    modal.hidden = false;
    document.documentElement.classList.add("modal-open");
    outside.forEach(function (el) { el.setAttribute("inert", ""); el.setAttribute("aria-hidden", "true"); });
    $(".modal-dialog", modal).focus();
    try { history.replaceState(null, "", "#bien-" + openId); } catch (e) { /* file:// edge cases */ }
  }
  function closeModal() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    openId = null;
    document.documentElement.classList.remove("modal-open");
    outside.forEach(function (el) { el.removeAttribute("inert"); el.removeAttribute("aria-hidden"); });
    try { history.replaceState(null, "", location.pathname + location.search); } catch (e) { /* ignore */ }
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
  }
  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target.closest("[data-close]")) closeModal();
      var it = e.target.closest("[data-interested]");
      if (it) {
        var id = it.getAttribute("data-interested");
        lastFocus = null;
        closeModal();
        var ref = $("#c-ref"), l = findListing(id);
        if (ref) ref.value = id;
        var cs = $("#c-country");
        if (cs && l) cs.value = l.country;
        var c = $("#contact");
        if (c) c.scrollIntoView({ behavior: prefersReduced() ? "auto" : "smooth", block: "start" });
        var nm = $("#c-name");
        if (nm) setTimeout(function () { nm.focus({ preventScroll: true }); }, prefersReduced() ? 0 : 400);
      }
    });
    document.addEventListener("keydown", function (e) {
      if (modal.hidden) return;
      if (e.key === "Escape") { e.preventDefault(); closeModal(); return; }
      if (e.key === "Tab") {
        var f = focusables();
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && (document.activeElement === first || document.activeElement === $(".modal-dialog", modal))) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
  function openFromHash() {
    var m = /^#bien-(.+)$/i.exec(location.hash || "");
    if (m && findListing(decodeURIComponent(m[1]))) openModal(decodeURIComponent(m[1]));
  }
  window.addEventListener("hashchange", openFromHash);

  /* ---------- Consent + tracking ---------- */
  var TR = CFG.tracking || {};
  var hasTracking = !!(TR.ga4 || TR.metaPixel || TR.tiktokPixel);
  var loaded = false;
  function consent() { return store("localStorage", "mi_consent"); }

  function addScript(src) {
    var s = document.createElement("script");
    s.async = true; s.src = src;
    document.head.appendChild(s);
  }
  function loadTracking() {
    if (loaded || !hasTracking) return;
    loaded = true;
    if (TR.ga4) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", TR.ga4);
      addScript("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(TR.ga4));
    }
    if (TR.metaPixel) {
      /* Meta Pixel base code */
      (function (f, b, e, v, n) {
        if (f.fbq) return;
        n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n;
        n.push = n; n.loaded = true; n.version = "2.0"; n.queue = [];
        addScript(v);
      })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
      window.fbq("init", TR.metaPixel);
      window.fbq("track", "PageView");
    }
    if (TR.tiktokPixel) {
      /* TikTok Pixel base code */
      (function (w, t) {
        w.TiktokAnalyticsObject = t;
        var ttq = w[t] = w[t] || [];
        ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie"];
        ttq.setAndDefer = function (o, m) { o[m] = function () { o.push([m].concat(Array.prototype.slice.call(arguments, 0))); }; };
        for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
        ttq.instance = function (id) { for (var e = ttq._i[id] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e; };
        ttq.load = function (id, opts) {
          var u = "https://analytics.tiktok.com/i18n/pixel/events.js";
          ttq._i = ttq._i || {}; ttq._i[id] = []; ttq._i[id]._u = u;
          ttq._t = ttq._t || {}; ttq._t[id] = +new Date();
          ttq._o = ttq._o || {}; ttq._o[id] = opts || {};
          addScript(u + "?sdkid=" + encodeURIComponent(id) + "&lib=" + t);
        };
        ttq.load(TR.tiktokPixel);
        ttq.page();
      })(window, "ttq");
    }
  }
  // kind: "form" | "whatsapp"
  function trackLead(kind) {
    if (consent() !== "granted") return;
    try {
      if (window.gtag) window.gtag("event", "generate_lead", { method: kind });
      if (window.fbq) window.fbq("track", "Lead", { content_name: kind });
      if (window.ttq) window.ttq.track(kind === "form" ? "SubmitForm" : "Contact");
    } catch (e) { /* never break the page */ }
  }

  var banner = null;
  function renderBanner(force) {
    if (!hasTracking) return;
    var c = consent();
    if (!force && !banner && (c === "granted" || c === "denied")) return;
    if (!banner) {
      banner = document.createElement("div");
      banner.className = "cookie";
      banner.setAttribute("role", "region");
      document.body.appendChild(banner);
    }
    banner.setAttribute("aria-label", t("cookieTitle"));
    banner.innerHTML = '<p class="cookie-text"><strong>' + esc(t("cookieTitle")) + ".</strong> " + esc(t("cookieText")) +
      ' <a href="confidentialite.html#cookies' + (LANG === "en" ? "-en" : "") + '">' + esc(t("cookieMore")) + "</a></p>" +
      '<div class="cookie-actions"><button type="button" class="btn btn-ghost-light" data-consent="denied">' + esc(t("cookieRefuse")) +
      '</button><button type="button" class="btn btn-gold" data-consent="granted">' + esc(t("cookieAccept")) + "</button></div>";
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-consent]");
    if (b) {
      var v = b.getAttribute("data-consent");
      store("localStorage", "mi_consent", v);
      if (banner) { banner.remove(); banner = null; }
      if (v === "granted") loadTracking();
      else if (loaded) location.reload(); // stop already-loaded trackers
      return;
    }
    if (e.target.closest("[data-cookie-settings]")) { e.preventDefault(); renderBanner(true); return; }
    var a = e.target.closest('a[href^="https://wa.me/"]');
    if (a) trackLead("whatsapp");
  });
  $$("[data-cookie-settings]").forEach(function (el) { el.hidden = !hasTracking; });
  if (consent() === "granted") loadTracking();

  // Lead form: mark submission; conversion fires on merci.html (reliable after redirect)
  var form = $('form[name="contact"]');
  if (form) form.addEventListener("submit", function () { store("sessionStorage", "mi_lead", "1"); });
  if (PAGE === "merci" && store("sessionStorage", "mi_lead") === "1") {
    store("sessionStorage", "mi_lead", null);
    trackLead("form");
  }

  /* ---------- Init ---------- */
  applyI18n();
  renderAll();
  renderBanner();
  openFromHash();
})();
