/* Widgets autonomes : #calculateur (rendement locatif) et #marche (étude Golden Mile).
   Langue : document.documentElement.lang + événement 'langchange' (e.detail.lang). */
(function () {
  'use strict';

  var AED_PER_USD = 3.6725; // parité fixe
  var STORE_KEY = 'w-calc-v1';

  var T = {
    fr: {
      calcEyebrow: 'Outil investisseur',
      calcTitle: 'Calculateur de rendement',
      calcIntro: 'Saisissez vos chiffres. Rendement brut, net et délai de retour se mettent à jour en direct.',
      currency: 'Devise',
      price: 'Prix d’achat',
      rent: 'Loyer annuel attendu',
      service: 'Charges de copropriété annuelles',
      vacancy: 'Vacance locative',
      mgmt: 'Frais de gestion locative',
      mgmtHint: '% du loyer encaissé. Environ 5 % en location longue durée.',
      costs: 'Frais d’acquisition',
      costsHint: 'Dubaï : environ 4 % DLD + 2 % agence = 6 % du prix. Modifiable.',
      vacancyHint: 'Part de l’année sans locataire.',
      results: 'Résultats estimés',
      gross: 'Rendement brut',
      net: 'Rendement net',
      income: 'Revenu net annuel',
      payback: 'Retour sur investissement',
      years: 'ans',
      perYear: '/ an',
      disclaimer: 'Estimation indicative, hors fiscalité personnelle et financement. Non garanti.',
      calcCta: 'Recevoir une analyse personnalisée',
      example: 'Exemple prérempli : 2 chambres à Dubai Marina.',
      mktEyebrow: 'Étude de cas',
      mktTitle: 'Le timing compte',
      mktIntro: 'Golden Mile, Palm Jumeirah : 2 078 ventes enregistrées au Dubai Land Department, de 2004 à septembre 2026. Même adresse, même vue. Le prix au pied carré a pourtant chuté de près de moitié, puis été multiplié par 2,7.',
      chartTitle: 'Prix médian au pied carré (AED), ventes résidentielles',
      chartSub: '2026 : janvier à septembre. Pointillés : prix de lancement 2004 (≈ 810 AED).',
      chartAria: 'Courbe du prix médian au pied carré à Golden Mile, Palm Jumeirah, de 2009 à 2026 : pic à 1 338 AED en 2014, creux à 722 AED en 2020, 1 937 AED en 2026. Prix de lancement 2004 environ 810 AED.',
      launch: '2004 ≈ 810',
      peak: 'Pic',
      low: 'Creux',
      sqft: 'AED / pi²',
      stat2014: 'Achat au pic',
      stat2020: 'Achat au creux',
      stat2025: 'Valeur récente',
      statSame: '2 ch., 1 794 pi², prix médian',
      punch: 'Même appartement. Seul le moment d’achat a changé.',
      source: 'Source : Dubai Land Department, ventes enregistrées. Médianes. Les performances passées ne préjugent pas des performances futures.',
      mktCta: 'Parler à un conseiller',
      million: 'M AED',
      yearSep: ' : '
    },
    en: {
      calcEyebrow: 'Investor tool',
      calcTitle: 'Rental yield calculator',
      calcIntro: 'Enter your numbers. Gross yield, net yield and payback update live.',
      currency: 'Currency',
      price: 'Purchase price',
      rent: 'Expected annual rent',
      service: 'Annual service charges',
      vacancy: 'Vacancy',
      mgmt: 'Property management fee',
      mgmtHint: '% of rent collected. About 5% for long-term lets.',
      costs: 'One-off purchase costs',
      costsHint: 'Dubai: about 4% DLD + 2% agency = 6% of price. Editable.',
      vacancyHint: 'Share of the year without a tenant.',
      results: 'Estimated results',
      gross: 'Gross yield',
      net: 'Net yield',
      income: 'Annual net income',
      payback: 'Payback period',
      years: 'years',
      perYear: '/ yr',
      disclaimer: 'Indicative estimate, excluding personal taxation and financing. Not guaranteed.',
      calcCta: 'Get a personalised analysis',
      example: 'Prefilled example: 2-bed in Dubai Marina.',
      mktEyebrow: 'Case study',
      mktTitle: 'Timing matters',
      mktIntro: 'Golden Mile, Palm Jumeirah: 2,078 sales registered with the Dubai Land Department, 2004 to September 2026. Same address, same view. Yet the price per sq ft fell by almost half, then rose 2.7-fold.',
      chartTitle: 'Median price per sq ft (AED), residential sales',
      chartSub: '2026: January to September. Dashed: 2004 launch price (≈ 810 AED).',
      chartAria: 'Line chart of median price per sq ft at Golden Mile, Palm Jumeirah, 2009 to 2026: peak of 1,338 AED in 2014, low of 722 AED in 2020, 1,937 AED in 2026. 2004 launch price about 810 AED.',
      launch: '2004 ≈ 810',
      peak: 'Peak',
      low: 'Low',
      sqft: 'AED / sq ft',
      stat2014: 'Bought at the peak',
      stat2020: 'Bought at the low',
      stat2025: 'Recent value',
      statSame: '2-bed, 1,794 sq ft, median price',
      punch: 'Same apartment. Only the timing changed.',
      source: 'Source: Dubai Land Department, registered sales. Medians. Past performance is not indicative of future results.',
      mktCta: 'Talk to an advisor',
      million: 'M AED',
      yearSep: ': '
    }
  };

  var lang = normLang(document.documentElement.lang);
  function normLang(l) { return (l || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'fr'; }
  function t(k) { return T[lang][k]; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // Formatage manuel (indépendant de l'Intl du navigateur) : FR "2 750 000" / EN "2,750,000"
  function fmt(n, dec) {
    dec = dec || 0;
    if (!isFinite(n)) return '–';
    var neg = n < 0; n = Math.abs(n);
    var s = n.toFixed(dec), parts = s.split('.');
    var thou = lang === 'fr' ? ' ' : ',', decSep = lang === 'fr' ? ',' : '.';
    var int = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thou);
    return (neg ? '−' : '') + int + (parts[1] ? decSep + parts[1] : '');
  }
  function pct(n) { return isFinite(n) ? fmt(n * 100, 2) + (lang === 'fr' ? ' %' : '%') : '–'; }
  function parseNum(str) {
    var s = String(str).replace(/[\s  ]/g, '');
    if (lang === 'en') s = s.replace(/,/g, ''); else s = s.replace(/,/g, '.');
    s = s.replace(/[^0-9.]/g, '');
    var firstDot = s.indexOf('.');
    if (firstDot !== -1) s = s.slice(0, firstDot + 1) + s.slice(firstDot + 1).replace(/\./g, '');
    var v = parseFloat(s);
    return isFinite(v) ? v : 0;
  }

  /* ================= Widget 1 : calculateur ================= */
  var DEFAULTS = { cur: 'AED', price: 2750000, rent: 190000, service: 30000, vacancy: 8, mgmt: 5, costs: 6 };
  var state = load();

  function load() {
    var s = {}; for (var k in DEFAULTS) s[k] = DEFAULTS[k];
    try {
      var raw = window.localStorage && localStorage.getItem(STORE_KEY);
      if (raw) {
        var o = JSON.parse(raw);
        for (var key in DEFAULTS) {
          if (key === 'cur') { if (o.cur === 'AED' || o.cur === 'USD') s.cur = o.cur; }
          else if (typeof o[key] === 'number' && isFinite(o[key]) && o[key] >= 0) s[key] = o[key];
        }
      }
    } catch (e) { /* stockage indisponible : valeurs par défaut */ }
    return s;
  }
  function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* ignore */ } }

  function compute(s) {
    var costs = s.price * s.costs / 100;
    var invested = s.price + costs;
    var collected = s.rent * (1 - s.vacancy / 100);
    var mgmt = collected * s.mgmt / 100;
    var net = collected - mgmt - s.service;
    return {
      gross: s.price > 0 ? s.rent / s.price : NaN,
      net: invested > 0 ? net / invested : NaN,
      income: net,
      payback: net > 0 ? invested / net : NaN,
      invested: invested
    };
  }

  var FIELDS = [
    { k: 'price', money: true, label: 'price' },
    { k: 'rent', money: true, label: 'rent' },
    { k: 'service', money: true, label: 'service' },
    { k: 'vacancy', pct: true, label: 'vacancy', hint: 'vacancyHint' },
    { k: 'mgmt', pct: true, label: 'mgmt', hint: 'mgmtHint' },
    { k: 'costs', pct: true, label: 'costs', hint: 'costsHint', full: true }
  ];

  function fieldValue(f) { return f.pct ? fmt(state[f.k], state[f.k] % 1 ? 1 : 0) : fmt(state[f.k]); }

  function renderCalc(root) {
    var html = '<div class="w-wrap">' +
      '<span class="w-eyebrow">' + esc(t('calcEyebrow')) + '</span>' +
      '<h2 class="w-title" id="w-calc-title">' + esc(t('calcTitle')) + '</h2>' +
      '<p class="w-intro">' + esc(t('calcIntro')) + ' ' + esc(t('example')) + '</p>' +
      '<div class="w-calc-grid">' +
      '<form class="w-card" novalidate onsubmit="return false" aria-labelledby="w-calc-title"><div class="w-fields">' +
      '<div class="w-field w-field-full"><span class="w-label" id="w-cur-l">' + esc(t('currency')) + '</span>' +
      '<div class="w-toggle" role="group" aria-labelledby="w-cur-l">' +
      ['AED', 'USD'].map(function (c) { return '<button type="button" data-cur="' + c + '" aria-pressed="' + (state.cur === c) + '">' + c + '</button>'; }).join('') +
      '</div></div>';
    FIELDS.forEach(function (f) {
      var id = 'w-in-' + f.k;
      html += '<div class="w-field' + (f.full ? ' w-field-full' : '') + '">' +
        '<label class="w-label" for="' + id + '">' + esc(t(f.label)) + '</label>' +
        '<div class="w-input-row"><input class="w-input" id="' + id + '" data-k="' + f.k + '" type="text" inputmode="decimal" autocomplete="off" value="' + esc(fieldValue(f)) + '"' +
        (f.hint ? ' aria-describedby="' + id + '-h"' : '') + '>' +
        '<span class="w-unit" data-unit="' + (f.money ? 'cur' : 'pct') + '">' + (f.money ? state.cur + (f.k === 'price' ? '' : ' ' + esc(t('perYear'))) : '%') + '</span></div>' +
        (f.hint ? '<span class="w-hint" id="' + id + '-h">' + esc(t(f.hint)) + '</span>' : '') +
        '</div>';
    });
    html += '</div></form>' +
      '<div class="w-card w-results"><span class="w-eyebrow">' + esc(t('results')) + '</span>' +
      '<div class="w-res-grid" aria-live="polite">' +
      res('gross', 'gross') + res('net', 'net', true) + res('income', 'income') + res('payback', 'payback') +
      '</div>' +
      '<p class="w-disclaimer">' + esc(t('disclaimer')) + '</p>' +
      '<a class="w-cta" href="#contact">' + esc(t('calcCta')) + '</a>' +
      '</div></div></div>';
    root.innerHTML = html;
    updateResults(root);
  }
  function res(key, label, main) {
    return '<div class="w-res' + (main ? ' w-res-main' : '') + '"><span class="w-res-label">' + esc(t(label)) + '</span><span class="w-res-value" data-out="' + key + '">–</span></div>';
  }
  function updateResults(root) {
    var r = compute(state);
    var set = function (k, v) { var el = root.querySelector('[data-out="' + k + '"]'); if (el) el.textContent = v; };
    set('gross', pct(r.gross));
    set('net', pct(r.net));
    set('income', fmt(r.income) + ' ' + state.cur);
    set('payback', isFinite(r.payback) ? fmt(r.payback, 1) + ' ' + t('years') : '–');
    root.setAttribute('data-w-results', JSON.stringify({ gross: r.gross, net: r.net, income: r.income, payback: r.payback }));
  }

  function bindCalc(root) {
    root.addEventListener('input', function (e) {
      var k = e.target.getAttribute && e.target.getAttribute('data-k');
      if (!k) return;
      state[k] = parseNum(e.target.value);
      updateResults(root); save();
    });
    root.addEventListener('focusout', function (e) {
      var k = e.target.getAttribute && e.target.getAttribute('data-k');
      if (!k) return;
      FIELDS.forEach(function (f) { if (f.k === k) e.target.value = fieldValue(f); });
    });
    root.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('[data-cur]');
      if (!btn) return;
      var cur = btn.getAttribute('data-cur');
      if (cur === state.cur) return;
      var factor = cur === 'USD' ? 1 / AED_PER_USD : AED_PER_USD;
      ['price', 'rent', 'service'].forEach(function (k) { state[k] = Math.round(state[k] * factor); });
      state.cur = cur; save();
      renderCalc(root);
      var again = root.querySelector('[data-cur="' + cur + '"]'); if (again) again.focus();
    });
  }

  /* ================= Widget 2 : marché ================= */
  var DATA = [[2009, 843], [2010, 796], [2011, 771], [2012, 824], [2013, 938], [2014, 1338], [2015, 1259], [2016, 1003], [2017, 1189], [2018, 996], [2019, 848], [2020, 722], [2021, 848], [2022, 1110], [2023, 1363], [2024, 1584], [2025, 1829], [2026, 1937]];
  var LAUNCH = 810;

  function chartSVG(cw) {
    // viewBox à la largeur réelle du conteneur : textes à taille lisible (1 unité ≈ 1 px)
    var W = Math.max(280, Math.min(1100, Math.round(cw || 640))), narrow = W < 560;
    var H = narrow ? Math.round(W * 0.78) : Math.round(Math.max(320, W * 0.42));
    var m = { l: narrow ? 44 : 52, r: narrow ? 22 : 34, t: 28, b: 30 };
    var fs = narrow ? 12 : 13;
    var x0 = 2009, x1 = 2026, yMax = 2000;
    var X = function (yr) { return m.l + (yr - x0) / (x1 - x0) * (W - m.l - m.r); };
    var Y = function (v) { return m.t + (1 - v / yMax) * (H - m.t - m.b); };
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" role="img" aria-label="' + esc(t('chartAria')) + '" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">';
    // grille
    [0, 500, 1000, 1500, 2000].forEach(function (v) {
      s += '<line x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="' + (v === 0 ? '#8c8578' : '#e6e1d6') + '" stroke-width="1"/>' +
        '<text x="' + (m.l - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end" font-size="' + fs + '" fill="#5b564e">' + esc(fmt(v)) + '</text>';
    });
    // étiquettes x (une année sur deux)
    DATA.forEach(function (d) {
      if ((d[0] - x0) % 2 === 0) s += '<text x="' + X(d[0]) + '" y="' + (H - m.b + 18) + '" text-anchor="middle" font-size="' + fs + '" fill="#5b564e">' + (W < 480 ? '\u2019' + String(d[0]).slice(2) : d[0]) + '</text>';
    });
    // référence lancement 2004
    s += '<line x1="' + m.l + '" x2="' + (W - m.r) + '" y1="' + Y(LAUNCH) + '" y2="' + Y(LAUNCH) + '" stroke="#8a6a2e" stroke-width="1.25" stroke-dasharray="5 4"/>' +
      '<text x="' + X(2014.6) + '" y="' + (Y(LAUNCH) + fs + 4) + '" text-anchor="start" font-size="' + (fs - 1) + '" fill="#8a6a2e">' + esc(t('launch')) + '</text>';
    // aire + ligne
    var pts = DATA.map(function (d) { return X(d[0]).toFixed(1) + ',' + Y(d[1]).toFixed(1); });
    s += '<polygon points="' + X(x0) + ',' + Y(0) + ' ' + pts.join(' ') + ' ' + X(x1) + ',' + Y(0) + '" fill="#c8a96e" fill-opacity=".12"/>';
    s += '<polyline points="' + pts.join(' ') + '" fill="none" stroke="#1a1a1a" stroke-width="2.25" stroke-linejoin="round" stroke-linecap="round"/>';
    // points
    var key = { 2014: 'peak', 2020: 'low', 2026: 'last' };
    DATA.forEach(function (d) {
      var k = key[d[0]];
      s += '<circle cx="' + X(d[0]) + '" cy="' + Y(d[1]) + '" r="' + (k ? 5 : 3.5) + '" fill="' + (k ? '#c8a96e' : '#fff') + '" stroke="#1a1a1a" stroke-width="1.5"><title>' +
        d[0] + (d[0] === 2026 ? (lang === 'fr' ? ' (janv.–sept.)' : ' (Jan–Sept)') : '') + t('yearSep') + fmt(d[1]) + ' ' + esc(t('sqft')) + '</title></circle>';
    });
    // étiquettes clés
    var lab = function (yr, v, txt, pos, anchor) {
      var y = pos === 'below' ? Y(v) + fs + 10 : Y(v) - 11;
      return '<text x="' + X(yr) + '" y="' + y + '" text-anchor="' + (anchor || 'middle') + '" font-size="' + fs + '" font-weight="600" fill="#1a1a1a">' + esc(txt) + '</text>';
    };
    s += lab(2014, 1338, t('peak') + ' ' + fmt(1338), 'above');
    s += lab(2020, 722, t('low') + ' ' + fmt(722), 'below');
    s += lab(2026, 1937, '2026' + t('yearSep') + fmt(1937), 'above', 'end');
    s += '</svg>';
    return s;
  }

  var mktRoot = null, chartW = 0;
  function chartWidth(root) {
    var box = root.querySelector('.w-chart');
    if (box && box.clientWidth) return box.clientWidth;
    var w = (root.clientWidth || window.innerWidth) - 32 - (window.innerWidth >= 600 ? 48 : 24) - 2;
    return Math.min(w, 1120 - 32 - 50);
  }

  function renderMarket(root) {
    chartW = chartWidth(root);
    var M = function (v) { return fmt(v, 2) + ' ' + t('million'); };
    var tile = function (yr, v, note, cls) {
      return '<li class="w-stat' + (cls ? ' ' + cls : '') + '"><span class="w-stat-year">' + yr + ' · ' + esc(t(note)) + '</span>' +
        '<span class="w-stat-value">' + esc(M(v)) + '</span><span class="w-stat-note">' + esc(t('statSame')) + '</span></li>';
    };
    root.innerHTML = '<div class="w-wrap">' +
      '<span class="w-eyebrow">' + esc(t('mktEyebrow')) + '</span>' +
      '<h2 class="w-title">' + esc(t('mktTitle')) + '</h2>' +
      '<p class="w-intro">' + esc(t('mktIntro')) + '</p>' +
      '<figure class="w-card w-chart-card" style="margin:0">' +
      '<p class="w-chart-title">' + esc(t('chartTitle')) + '</p>' +
      '<p class="w-chart-sub">' + esc(t('chartSub')) + '</p>' +
      '<div class="w-chart">' + chartSVG(chartW) + '</div></figure>' +
      '<ul class="w-stats">' + tile(2014, 2.75, 'stat2014') + tile(2020, 1.40, 'stat2020', 'w-stat-low') + tile(2025, 4.00, 'stat2025') + '</ul>' +
      '<p class="w-punch">' + esc(t('punch')) + '</p>' +
      '<p class="w-source">' + esc(t('source')) + '</p>' +
      '<a class="w-cta w-cta-dark" href="#contact">' + esc(t('mktCta')) + '</a>' +
      '</div>';
    var box = root.querySelector('.w-chart');
    if (box && box.clientWidth && Math.abs(box.clientWidth - chartW) > 2) { chartW = box.clientWidth; box.innerHTML = chartSVG(chartW); }
  }

  /* ================= Initialisation ================= */
  var calcRoot = null;
  function init() {
    calcRoot = document.getElementById('calculateur');
    mktRoot = document.getElementById('marche');
    if (calcRoot) { renderCalc(calcRoot); bindCalc(calcRoot); }
    if (mktRoot) {
      renderMarket(mktRoot);
      var timer;
      window.addEventListener('resize', function () {
        clearTimeout(timer);
        timer = setTimeout(function () { var box = mktRoot.querySelector('.w-chart');
          if (box && Math.abs(box.clientWidth - chartW) > 24) { chartW = box.clientWidth; box.innerHTML = chartSVG(chartW); } }, 150);
      });
    }
    document.addEventListener('langchange', function (e) {
      var l = normLang((e && e.detail && e.detail.lang) || document.documentElement.lang);
      if (l === lang) return;
      lang = l;
      if (calcRoot) renderCalc(calcRoot);
      if (mktRoot) renderMarket(mktRoot);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
