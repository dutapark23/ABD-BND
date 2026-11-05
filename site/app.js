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
  document.documentElement.classList.add("js");
  function isSoon(c) { return !!(COUNTRIES[c] && COUNTRIES[c].comingSoon); }
  // Countries that can be filtered (not "coming soon")
  var LIVE_KEYS = COUNTRY_KEYS.filter(function (c) { return !isSoon(c); });

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
      menuLabel: "Menu",
      waDefault_georgia: "Bonjour {brand}, je souhaite être prévenu(e) de l'ouverture de vos biens en Géorgie.",
      waBar: "Une question ? WhatsApp",
      sortLabel: "Trier", sortReco: "Recommandés", sortPriceAsc: "Prix croissant", sortPriceDesc: "Prix décroissant", sortYield: "Rendement",
      soonPill: "Bientôt", soonBadge: "Bientôt disponible", waitCta: "Être prévenu en premier",
      photoOf: "Photo {n} sur {total}", galleryLabel: "Photos du bien",
      stepsEyebrow: "Comment ça marche", stepsTitle: "De votre premier message à la remise des clés",
      step1Title: "Appel découverte", step1Text: "Un échange par WhatsApp ou en visio pour cerner votre budget, vos objectifs et votre calendrier. Sans engagement.",
      step2Title: "Sélection de biens et analyse chiffrée", step2Text: "Une courte liste de biens adaptés, avec pour chacun : prix comparé au marché, frais à prévoir, rendement estimé et points de vigilance.",
      step3Title: "Visite (sur place ou vidéo) et réservation", step3Text: "Vous visitez sur place ou en vidéo, en direct. Une fois le bien choisi, nous vous guidons pour l'offre et la réservation.",
      step4Title: "Accompagnement jusqu'aux clés", step4Text: "Démarches, signature et remise des clés. Si vous le souhaitez, mise en relation avec un gestionnaire pour la location.",
      stepsCta: "Réserver mon appel découverte",
      ytEyebrow: "Vu sur YouTube", ytTitle: "Visites de biens et analyses de marché, en vidéo.", ytCta: "Voir la chaîne",
      faqEyebrow: "Questions fréquentes", faqTitle: "Vos questions, nos réponses",
      faq1Q: "Un étranger peut-il acheter à Dubaï ?",
      faq1A: "Oui. Dans les zones dites « freehold », les étrangers peuvent acheter en pleine propriété, sans être résidents aux Émirats. Nous vérifions le statut de chaque bien avant de vous le proposer.",
      faq2Q: "Et à Bali ?",
      faq2A: "Un étranger ne peut pas détenir un terrain en pleine propriété en Indonésie. L'achat se fait le plus souvent en bail longue durée (leasehold), ou via une société locale à capitaux étrangers (PT PMA). Permis de construire, zonage et titre du bail doivent être vérifiés avant de signer.",
      faq3Q: "Sur plan ou prêt à louer : que choisir ?",
      faq3A: "Un bien sur plan demande souvent un ticket d'entrée plus bas et se paie en plusieurs fois jusqu'à la livraison, mais il faut attendre et accepter un risque de retard. Un bien livré peut être loué tout de suite. Nous comparons les deux options selon votre budget et votre horizon.",
      faq4Q: "Peut-on acheter à distance ?",
      faq4A: "Oui, c'est courant. Visite en vidéo, documents envoyés à l'avance, signature électronique ou procuration selon les cas, paiement par virement. Vous pouvez aussi venir sur place : nous organisons les visites.",
      faq5Q: "Quels frais prévoir en plus du prix ?",
      faq5A: "À Dubaï : environ 4 % de frais d'enregistrement au Dubai Land Department (DLD), plus les frais d'agence et quelques frais administratifs. À Bali : frais de notaire, de vérification et de bail, qui varient selon le bien. Nous vous donnons une estimation chiffrée avant toute offre.",
      faq6Q: "Qui s'occupe de la location ?",
      faq6A: "Nous pouvons vous mettre en relation avec des gestionnaires locatifs sur place, pour de la location longue durée ou saisonnière. Les rendements affichés sur le site sont des estimations brutes, avant frais de gestion et charges, et ne sont pas garantis.",
      faq7Q: "Et la Géorgie ?",
      faq7A: "Notre sélection à Tbilissi et Batoumi arrive bientôt. Inscrivez-vous sur la <a href=\"georgie.html#liste-attente\">liste d'attente</a> pour être prévenu en premier.",
      waitEyebrow: "Liste d'attente", waitTitle: "Soyez prévenu en premier",
      waitLead: "Nous préparons une sélection d'appartements à Tbilissi et Batoumi. Inscrivez-vous : vous recevrez les premiers biens et leur analyse chiffrée avant leur mise en ligne.",
      waitPoint1: "Accès anticipé aux premiers biens", waitPoint2: "Analyse chiffrée : prix, frais, rendement estimé", waitPoint3: "Aucun engagement, désinscription en un message",
      wBudget1: "Moins de 100 000 $", wBudget2: "100 000 – 250 000 $", wBudget4: "Plus de 500 000 $",
      lConsentWait: "J'accepte que {brand} utilise ces informations pour me prévenir de l'ouverture de la Géorgie et me recontacter. Elles ne sont ni vendues ni partagées. Voir la <a href=\"confidentialite.html\">politique de confidentialité</a>.",
      waitSubmit: "Rejoindre la liste d'attente",
      navLabel: "Navigation principale", langLabel: "Langue",
      navListings: "Biens", navCalc: "Calculateur", navDestinations: "Destinations", navContact: "Contact",
      title_home: "Marina Immo — Investir à Dubaï et Bali, Géorgie bientôt",
      title_dubai: "Investir à Dubaï — Biens prêts et sur plan | Marina Immo",
      title_bali: "Investir à Bali — Villas | Marina Immo",
      title_georgia: "Géorgie — Bientôt disponible | Marina Immo",
      title_merci: "Merci — Marina Immo",
      title_legal: "Mentions légales — Marina Immo",
      title_privacy: "Politique de confidentialité — Marina Immo",
      heroEyebrow: "Dubaï · Bali · Géorgie (bientôt)",
      heroTitle: "Investissez à Dubaï et à Bali. Avec des chiffres, pas des promesses.",
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
      heroTitle_georgia: "Géorgie — bientôt disponible",
      heroLead_georgia: "Tbilissi et Batoumi : nous préparons une sélection d'appartements analysés et chiffrés. Inscrivez-vous pour la recevoir en premier.",
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
      emptyHelp: "Élargissez vos filtres, ou décrivez-nous votre recherche : nous vous envoyons une sélection sur mesure.",
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
      menuLabel: "Menu",
      waDefault_georgia: "Hello {brand}, I'd like to be notified when your Georgia properties launch.",
      waBar: "Questions? WhatsApp us",
      sortLabel: "Sort", sortReco: "Recommended", sortPriceAsc: "Price: low to high", sortPriceDesc: "Price: high to low", sortYield: "Yield",
      soonPill: "Soon", soonBadge: "Coming soon", waitCta: "Get early access",
      photoOf: "Photo {n} of {total}", galleryLabel: "Property photos",
      stepsEyebrow: "How it works", stepsTitle: "From your first message to handover",
      step1Title: "Discovery call", step1Text: "A WhatsApp or video call to understand your budget, goals and timing. No commitment.",
      step2Title: "Property shortlist and numbers", step2Text: "A short list of suitable properties, each with its price compared with the market, expected fees, estimated yield and points to watch.",
      step3Title: "Viewing (on site or video) and reservation", step3Text: "View on site or by live video. Once you have chosen, we guide you through the offer and reservation.",
      step4Title: "Support through to handover", step4Text: "Paperwork, signing and key handover. If you wish, an introduction to a rental management company.",
      stepsCta: "Book my discovery call",
      ytEyebrow: "As seen on YouTube", ytTitle: "Property tours and market analysis, on video.", ytCta: "Watch the channel",
      faqEyebrow: "FAQ", faqTitle: "Your questions, answered",
      faq1Q: "Can foreigners buy in Dubai?",
      faq1A: "Yes. In designated freehold areas, foreigners can buy with full ownership without being UAE residents. We check the status of every property before showing it to you.",
      faq2Q: "And in Bali?",
      faq2A: "Foreigners cannot own land freehold in Indonesia. Purchases are usually made on a long-term leasehold, or through a foreign-owned local company (PT PMA). Building permits, zoning and lease title must be checked before signing.",
      faq3Q: "Off-plan or ready: which one?",
      faq3A: "Off-plan often means a lower entry ticket and staged payments until handover, but you have to wait and accept a risk of delay. A ready property can be rented out straight away. We compare both options against your budget and time horizon.",
      faq4Q: "Can I buy remotely?",
      faq4A: "Yes, it is common. Video viewings, documents sent in advance, e-signature or power of attorney depending on the case, payment by bank transfer. You can also come in person: we organise the viewings.",
      faq5Q: "What fees should I expect on top of the price?",
      faq5A: "In Dubai: around 4% registration fee to the Dubai Land Department (DLD), plus the agency fee and some admin fees. In Bali: notary, due-diligence and lease costs, which vary by property. We give you a costed estimate before any offer.",
      faq6Q: "Who manages the rental?",
      faq6A: "We can introduce you to local rental management companies, for long-term or holiday letting. Yields shown on this website are gross estimates, before management fees and charges, and are not guaranteed.",
      faq7Q: "What about Georgia?",
      faq7A: "Our selection in Tbilisi and Batumi is coming soon. Join the <a href=\"georgie.html#liste-attente\">waitlist</a> to be the first to know.",
      waitEyebrow: "Waitlist", waitTitle: "Be the first to know",
      waitLead: "We are preparing a selection of apartments in Tbilisi and Batumi. Sign up to receive the first properties and their costed analysis before they go online.",
      waitPoint1: "Early access to the first properties", waitPoint2: "Costed analysis: price, fees, estimated yield", waitPoint3: "No commitment, unsubscribe with one message",
      wBudget1: "Under $100,000", wBudget2: "$100,000 – $250,000", wBudget4: "Over $500,000",
      lConsentWait: "I agree that {brand} may use this information to notify me when Georgia launches and to contact me. It is never sold or shared. See the <a href=\"confidentialite.html\">privacy policy</a>.",
      waitSubmit: "Join the waitlist",
      navLabel: "Main navigation", langLabel: "Language",
      navListings: "Properties", navCalc: "Calculator", navDestinations: "Destinations", navContact: "Contact",
      title_home: "Marina Immo — Invest in Dubai and Bali, Georgia soon",
      title_dubai: "Invest in Dubai — Ready and off-plan properties | Marina Immo",
      title_bali: "Invest in Bali — Villas | Marina Immo",
      title_georgia: "Georgia — Coming soon | Marina Immo",
      title_merci: "Thank you — Marina Immo",
      title_legal: "Legal notice — Marina Immo",
      title_privacy: "Privacy policy — Marina Immo",
      heroEyebrow: "Dubai · Bali · Georgia (soon)",
      heroTitle: "Invest in Dubai and Bali. Backed by numbers, not promises.",
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
      heroTitle_georgia: "Georgia — coming soon",
      heroLead_georgia: "Tbilisi and Batumi: we are preparing a selection of analysed, fully costed apartments. Sign up to get it first.",
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
      emptyHelp: "Widen your filters, or tell us what you are looking for and we will send you a tailored shortlist.",
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
    if (!PAGE_COUNTRY) return t("waDefault");
    if (DICT.fr["waDefault_" + PAGE_COUNTRY]) return t("waDefault_" + PAGE_COUNTRY);
    return t("waDefaultCountry", { country: countryName(PAGE_COUNTRY) });
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
    // Contract for widgets.js: fired on initial load AND on every language change
    var ev;
    try { ev = new CustomEvent("langchange", { detail: { lang: LANG } }); }
    catch (e) { ev = document.createEvent("CustomEvent"); ev.initCustomEvent("langchange", false, false, { lang: LANG }); }
    document.dispatchEvent(ev);
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

  /* ---------- YouTube strip (only if SITE_CONFIG.youtube is set) ---------- */
  var YT = /^https?:\/\//i.test(String(CFG.youtube || "")) ? String(CFG.youtube) : "";
  $$("[data-youtube]").forEach(function (el) { el.hidden = !YT; });
  if (YT) $$("[data-youtube-link]").forEach(function (a) { a.href = YT; });

  /* ---------- Mobile menu ---------- */
  var navToggle = $(".nav-toggle"), header = $(".site-header");
  function setNav(open) {
    if (!navToggle) return;
    navToggle.setAttribute("aria-expanded", String(open));
    header.classList.toggle("nav-open", open);
  }
  if (navToggle) {
    navToggle.addEventListener("click", function () { setNav(navToggle.getAttribute("aria-expanded") !== "true"); });
    $$(".main-nav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("nav-open")) { setNav(false); navToggle.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (header.classList.contains("nav-open") && !e.target.closest(".site-header")) setNav(false);
    });
  }

  /* ---------- Line-art illustrations (gold strokes, no photos needed) ---------- */
  var ART = {
    dubai:
      // water
      '<path d="M0 182h320M14 190h60M110 190h90M232 190h70M40 197h40M150 197h50M250 197h30" opacity=".5"/>' +
      // sun
      '<circle cx="262" cy="46" r="16" opacity=".6"/>' +
      // skyline
      '<path d="M0 182v-38h18v-14h16v52"/>' +
      '<path d="M34 182v-74l12-10 12 10v74M40 118h12M40 132h12M40 146h12M40 160h12"/>' +
      '<path d="M64 182v-56h22v56M70 140h10M70 154h10M70 168h10"/>' +
      '<path d="M92 182V92q11-16 22 0v90M103 80v-6M98 108h10M98 124h10M98 140h10M98 156h10"/>' +
      '<path d="M122 182v-60h14v-10h12v70"/>' +
      '<path d="M152 182V78l5-6V50l3-4V26l2-18 2 18v20l3 4v22l5 6v104M158 96h10M158 116h10M158 136h10M158 156h10"/>' +
      '<path d="M184 182v-84l16-12 16 12v84M192 106h16M192 122h16M192 138h16M192 154h16M192 170h16"/>' +
      '<path d="M222 182v-46c8-18 18-18 26 0v46"/>' +
      '<path d="M254 182v-64h20v64M259 130h10M259 146h10M259 162h10"/>' +
      '<path d="M280 182v-30h16v-12h10v42M296 182v-20h24"/>',
    bali:
      // sun + birds
      '<circle cx="258" cy="44" r="15" opacity=".6"/><path d="M96 40q5-4 10 0q5-4 10 0M122 30q4-3 8 0q4-3 8 0" opacity=".6"/>' +
      // palm left
      '<path d="M56 160q-8-50 10-96"/><path d="M66 64q-24-6-40 10M66 64q-12-20-34-20M66 64q6-24 28-30M66 64q22-6 38 8M66 64q8 14 4 34M66 64q-14 10-18 30"/>' +
      // palm right
      '<path d="M276 158q6-40-6-80"/><path d="M270 78q20-10 38 2M270 78q10-18 30-18M270 78q-8-18-28-20M270 78q-20 0-32 14M270 78q-4 14 2 30"/>' +
      // villa: two-tier roof, walls, columns, steps
      '<path d="M112 116l48-44 48 44zM128 116l32-28 32 28M160 72v-10"/>' +
      '<path d="M120 116v40h80v-40M134 156v-28h18v28M168 128h22v14h-22zM179 128v14"/>' +
      '<path d="M108 156h104M112 162h96"/>' +
      // rice terraces
      '<path d="M0 168q60-12 120-2t120 2 80-6"/><path d="M0 178q70-10 140 0t180-4"/><path d="M0 188q80-8 160 0t160-2"/><path d="M0 197q90-6 180 0t140-2"/>' +
      '<path d="M20 170v-6M30 168v-6M40 167v-6M200 172v-6M212 172v-6M224 171v-6M60 182v-5M72 181v-5M250 180v-5M262 179v-5" opacity=".7"/>',
    georgia:
      // mountains + snow caps
      '<path d="M0 118l44-46 30 28 46-64 40 52 26-22 46 40 34-30 54 46"/>' +
      '<path d="M108 50l12-14 12 16-6-2-6 6-6-4zM44 72l-8 8 6-1 4 4 4-5 6 2" opacity=".7"/>' +
      '<circle cx="270" cy="34" r="12" opacity=".6"/>' +
      // fortress wall on the hill
      '<path d="M200 122v-10h6v4h6v-4h6v4h6v-4h6v10" opacity=".8"/>' +
      // old-town rooftops
      '<path d="M0 182v-26l18-14 18 14v26M8 182v-12h8v12M24 160h6v8h-6z"/>' +
      '<path d="M36 182v-34h34v34M32 148l21-16 21 16M42 160h8v8h-8zM56 160h8v8h-8zM40 172h26"/>' +
      '<path d="M74 182v-22l16-12 16 12v22M84 182v-10h12v10"/>' +
      // church with conical dome
      '<path d="M112 182v-40h36v40M120 142v-14h20v14M122 128v-10l8-14 8 14v10M130 104v-8M126 100h8M126 160a4 4 0 0 1 8 0v10h-8z"/>' +
      '<path d="M154 182v-30l14-10 14 10v30M162 160h12M160 168h16" />' +
      '<path d="M186 182v-38h40v38M182 144l24-18 24 18M192 154h8v8h-8zM212 154h8v8h-8zM190 170h32"/>' +
      '<path d="M230 182v-24l16-12 16 12v24M240 182v-12h12v12"/>' +
      '<path d="M266 182v-36h30v36M262 146l19-14 19 14M272 156h6v8h-6zM284 156h6v8h-6zM300 182v-22l20-14"/>' +
      '<path d="M0 182h320M0 190h320" opacity=".5"/>'
  };
  function flip(id) { // mirror every other listing's illustration so cards don't look identical
    var h = 0; String(id).replace(/\d/g, function (d) { h += Number(d); });
    return h % 2 === 0;
  }
  function artSvg(c, fit, flipped) {
    if (!ART[c]) return "";
    return '<svg class="art' + (flipped ? " art-flip" : "") + '" viewBox="0 0 320 200" preserveAspectRatio="xMidYMax ' + (fit || "slice") + '" aria-hidden="true" focusable="false">' +
      '<g fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke">' +
      ART[c] + "</g></svg>";
  }
  $$("[data-art]").forEach(function (el) {
    el.innerHTML = el.getAttribute("data-art").split(/\s+/).map(function (c) {
      return '<div class="hero-art-item hero-art-' + c + '">' + artSvg(c, "meet") + "</div>";
    }).join("");
  });

  /* ---------- Listings ---------- */
  var grid = $("#grid");
  var F = {
    country: $("#f-country"), type: $("#f-type"), status: $("#f-status"),
    beds: $("#f-beds"), budget: $("#f-budget")
  };
  var SORT = $("#f-sort");

  function images(l) {
    return Array.isArray(l.images) ? l.images.filter(function (src) { return typeof src === "string" && src; }) : [];
  }
  function placeholder(l, cls) {
    var label = countryName(l.country);
    return '<div class="ph ph-' + esc(l.country) + " " + (cls || "") + '" role="img" aria-label="' +
      esc(t("photoSoon") + " — " + label + ", " + l.city) + '">' + artSvg(l.country, "slice", flip(l.id)) +
      '<span class="ph-country">' + esc(label) + "</span>" +
      '<span class="ph-note">' + esc(t("photoSoon")) + "</span></div>";
  }
  function media(l, cls) {
    var im = images(l);
    if (!im.length) return placeholder(l, cls);
    return '<img class="media-img ' + (cls || "") + '" src="' + esc(im[0]) + '" alt="' + esc(L(l.title) + " — " + l.city) +
      '" loading="lazy" decoding="async">';
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
      '<div class="card-media">' + media(l) + badges(l) + "</div>" +
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

  function sorted(list) {
    var mode = SORT ? SORT.value : "reco";
    var idx = list.map(function (l, i) { return { l: l, i: i }; });
    var price = function (x) { return Number(x.l.price_usd) || 0; };
    var yld = function (x) { var y = x.l.est_yield_pct; return y == null || isNaN(Number(y)) ? null : Number(y); };
    idx.sort(function (a, b) {
      var d = 0;
      if (mode === "price-asc") d = price(a) - price(b);
      else if (mode === "price-desc") d = price(b) - price(a);
      else if (mode === "yield") {
        var ya = yld(a), yb = yld(b);
        if (ya == null && yb == null) d = 0;
        else if (ya == null) d = 1; // nulls last
        else if (yb == null) d = -1;
        else d = yb - ya;
      }
      return d || a.i - b.i; // stable: keep recommended order on ties
    });
    return idx.map(function (x) { return x.l; });
  }

  function renderListings() {
    if (!grid) return;
    var list = sorted(filtered());
    grid.innerHTML = list.map(card).join("");
    var n = list.length;
    $("#result-count").textContent = n === 0 ? t("count0") : n === 1 ? t("count1") : t("countN", { n: n });
    $("#empty").hidden = n !== 0;
  }

  function resetFilters() {
    Object.keys(F).forEach(function (k) { F[k].value = ""; });
    if (LIVE_KEYS.indexOf(PAGE_COUNTRY) > -1) F.country.value = PAGE_COUNTRY;
    renderListings();
  }

  function scrollToEl(el) {
    if (el) el.scrollIntoView({ behavior: prefersReduced() ? "auto" : "smooth", block: "start" });
  }
  function pickCountry(c) {
    if (isSoon(c)) { // coming soon: show its destination block (waitlist CTA) instead of filtering
      var d = $("#dest-" + c);
      if (d) scrollToEl(d); else location.href = LANDING[c];
      return;
    }
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
    if (SORT) SORT.addEventListener("change", renderListings);
    $$("#f-reset, [data-reset]").forEach(function (b) { b.addEventListener("click", resetFilters); });
    // Initial country: ?pays= param, else page country
    var qp = "";
    try { qp = (new URLSearchParams(location.search).get("pays") || "").toLowerCase(); } catch (e) { /* old browser */ }
    if (qp === "georgie") qp = "georgia";
    if (qp === "dubai" || qp === "dubaï") qp = "dubai";
    F.country.value = LIVE_KEYS.indexOf(qp) > -1 ? qp : (LIVE_KEYS.indexOf(PAGE_COUNTRY) > -1 ? PAGE_COUNTRY : "");
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
    var soon = isSoon(c), actions;
    if (soon) {
      actions = '<div class="dest-actions"><a class="btn ' + (big ? "btn-primary" : "btn-gold") + '" href="' +
        (PAGE_COUNTRY === c ? "#liste-attente" : LANDING[c] + "#liste-attente") + '">' + esc(t("waitCta")) + " →</a></div>";
    } else {
      actions = '<div class="dest-actions"><button type="button" class="btn ' + (big ? "btn-primary" : "btn-outline-gold") + '" data-pick="' + c + '">' +
        esc(t("seeListingsIn", { country: countryName(c) })) + "</button>";
      if (!big && PAGE_COUNTRY !== c) actions += '<a class="dest-link" href="' + LANDING[c] + '">' + esc(t("landingPage")) + " →</a>";
      actions += "</div>";
    }
    return '<article class="dest dest-' + c + (big ? " dest-big" : "") + (soon ? " dest-soon" : "") + '"' + (big ? "" : ' id="dest-' + c + '"') + ">" +
      '<div class="dest-band" aria-hidden="true"></div>' +
      (soon && !big ? '<p class="soon-badge">' + esc(t("soonBadge")) + "</p>" : "") +
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
  function gallery(l) {
    var im = images(l);
    if (!im.length) return placeholder(l, "ph-lg");
    var alt = L(l.title) + " — " + l.city;
    var h = '<img class="gallery-main" id="gallery-main" src="' + esc(im[0]) + '" alt="' + esc(alt) + '">';
    if (im.length > 1) {
      h += '<div class="gallery-thumbs" role="group" aria-label="' + esc(t("galleryLabel")) + '">' + im.map(function (src, i) {
        return '<button type="button" class="gallery-thumb" data-gal="' + i + '" aria-pressed="' + (i === 0) + '" aria-label="' +
          esc(t("photoOf", { n: i + 1, total: im.length })) + '"><img src="' + esc(src) + '" alt="" loading="lazy"></button>';
      }).join("") + "</div>";
    }
    return h;
  }
  function renderModal(id) {
    var l = findListing(id);
    if (!l) return false;
    var feats = L(l.features) || [];
    var title = L(l.title);
    var html =
      '<div class="modal-media">' + gallery(l) + badges(l) + "</div>" +
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
      var g = e.target.closest("[data-gal]");
      if (g) {
        var l0 = findListing(openId), im = l0 ? images(l0) : [], i0 = Number(g.getAttribute("data-gal"));
        var main = $("#gallery-main");
        if (main && im[i0]) main.src = im[i0];
        $$("[data-gal]", modal).forEach(function (b) { b.setAttribute("aria-pressed", String(b === g)); });
      }
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
  $$('form[name="contact"], form[name="georgie-liste-attente"]').forEach(function (form) {
    form.addEventListener("submit", function () { store("sessionStorage", "mi_lead", "1"); });
  });
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
