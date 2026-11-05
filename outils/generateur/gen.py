#!/usr/bin/env python3
"""Generates the static HTML pages of site/ from shared partials (keeps them identical)."""
import os
G = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = os.path.normpath(os.path.join(G, '..', '..', 'site')) + '/'
DOMAIN = 'https://www.marina-immo.com/'
part = lambda n: open(G + n).read()

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%231a1a1a'/%3E%3Ctext x='32' y='43' font-family='Georgia,serif' font-size='30' text-anchor='middle' fill='%23c8a96e'%3EMI%3C/text%3E%3C/svg%3E"
FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@500;600;700&display=swap"
WA_SVG = '<svg class="wa-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.3Z"/></svg>'


def wpart(n):
    return part(n).replace('WA_SVG', WA_SVG)


LISTINGS, DEST, MODAL = wpart('listings.part'), wpart('dest.part'), wpart('modal.part')
_wc = wpart('whycontact.part')
WHY, CONTACT = _wc[:_wc.index('<!-- CONTACT -->')], '    ' + _wc[_wc.index('<!-- CONTACT -->'):]
STEPS, YOUTUBE, WAITLIST = wpart('steps.part'), wpart('youtube.part'), wpart('waitlist.part')
CALC = '''<!-- CALCULATOR (filled by widgets.js) -->
    <section id="calculateur" class="section"></section>

    '''
MARCHE = '''<!-- MARKET DATA (filled by widgets.js) -->
    <section id="marche" class="section"></section>

    '''

# FAQ — FR is the default HTML + JSON-LD; EN lives in site/app.js (keys faqNQ / faqNA)
FAQ = [
    ("Un étranger peut-il acheter à Dubaï ?",
     "Oui. Dans les zones dites « freehold », les étrangers peuvent acheter en pleine propriété, sans être résidents aux Émirats. Nous vérifions le statut de chaque bien avant de vous le proposer."),
    ("Et à Bali ?",
     "Un étranger ne peut pas détenir un terrain en pleine propriété en Indonésie. L'achat se fait le plus souvent en bail longue durée (leasehold), ou via une société locale à capitaux étrangers (PT PMA). Permis de construire, zonage et titre du bail doivent être vérifiés avant de signer."),
    ("Sur plan ou prêt à louer : que choisir ?",
     "Un bien sur plan demande souvent un ticket d'entrée plus bas et se paie en plusieurs fois jusqu'à la livraison, mais il faut attendre et accepter un risque de retard. Un bien livré peut être loué tout de suite. Nous comparons les deux options selon votre budget et votre horizon."),
    ("Peut-on acheter à distance ?",
     "Oui, c'est courant. Visite en vidéo, documents envoyés à l'avance, signature électronique ou procuration selon les cas, paiement par virement. Vous pouvez aussi venir sur place : nous organisons les visites."),
    ("Quels frais prévoir en plus du prix ?",
     "À Dubaï : environ 4 % de frais d'enregistrement au Dubai Land Department (DLD), plus les frais d'agence et quelques frais administratifs. À Bali : frais de notaire, de vérification et de bail, qui varient selon le bien. Nous vous donnons une estimation chiffrée avant toute offre."),
    ("Qui s'occupe de la location ?",
     "Nous pouvons vous mettre en relation avec des gestionnaires locatifs sur place, pour de la location longue durée ou saisonnière. Les rendements affichés sur le site sont des estimations brutes, avant frais de gestion et charges, et ne sont pas garantis."),
    ("Et la Géorgie ?",
     'Notre sélection à Tbilissi et Batoumi arrive bientôt. Inscrivez-vous sur la <a href="georgie.html#liste-attente">liste d\'attente</a> pour être prévenu en premier.'),
]


def faq_section():
    items = ''
    for i, (q, a) in enumerate(FAQ, 1):
        attr = 'data-i18n-html' if '<a ' in a else 'data-i18n'
        items += f'''          <details class="faq-item">
            <summary data-i18n="faq{i}Q">{q}</summary>
            <p {attr}="faq{i}A">{a}</p>
          </details>
'''
    return f'''<!-- FAQ -->
    <section class="section" id="faq" aria-labelledby="faq-title">
      <div class="container faq-wrap">
        <header class="section-head">
          <p class="eyebrow" data-i18n="faqEyebrow">Questions fréquentes</p>
          <h2 id="faq-title" data-i18n="faqTitle">Vos questions, nos réponses</h2>
        </header>
        <div class="faq">
{items}        </div>
      </div>
    </section>

    '''


def faq_jsonld():
    import json, re
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in FAQ]}
    return '  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/') + '\n  </script>\n'


FAQ_HTML = faq_section()

JSONLD = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "name": "Marina Immo",
    "url": "https://www.marina-immo.com/",
    "email": "contact@marina-immo.com",
    "telephone": "+971500000000",
    "areaServed": [
      {"@type": "Place", "name": "Dubai, United Arab Emirates"},
      {"@type": "Place", "name": "Bali, Indonesia"},
      {"@type": "Place", "name": "Georgia"}
    ],
    "knowsLanguage": ["fr", "en"],
    "description": "Agence d'investissement immobilier à Dubaï, Bali et en Géorgie. Accompagnement en français et en anglais."
  }
  </script>
'''


def head(title, desc, path, robots='index, follow', extra=''):
    url = DOMAIN + path
    return f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Marina Immo">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:locale:alternate" content="en_US">
  <meta name="twitter:card" content="summary">
  <meta name="theme-color" content="#1a1a1a">
  <link rel="icon" href="{FAVICON}">
  <link rel="preload" href="fonts/PlayfairDisplay-latin-48d1e9.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="fonts.css">
  <link rel="stylesheet" href="styles.css">
{extra}</head>
'''


def header(home, sections=True):
    pre = '' if sections else 'index.html'
    return f'''  <a class="skip-link" href="#main" data-i18n="skip">Aller au contenu</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{home}" aria-label="Marina Immo">
        <span class="brand-mark" aria-hidden="true">MI</span>
        <span class="brand-name" data-brand>Marina Immo</span>
      </a>
      <nav class="main-nav" aria-label="Navigation principale" data-i18n-aria="navLabel">
        <a href="{pre}#biens" data-i18n="navListings">Biens</a>
        <a href="{pre}#destinations" data-i18n="navDestinations">Destinations</a>
        <a href="{pre}#contact" data-i18n="navContact">Contact</a>
      </nav>
      <div class="header-actions">
        <div class="lang-switch" role="group" aria-label="Langue" data-i18n-aria="langLabel">
          <button type="button" class="lang-btn" data-lang="fr" aria-pressed="true" lang="fr">FR</button>
          <span aria-hidden="true">|</span>
          <button type="button" class="lang-btn" data-lang="en" aria-pressed="false" lang="en">EN</button>
        </div>
        <a class="btn btn-wa btn-sm" data-wa-link href="https://wa.me/971500000000" target="_blank" rel="noopener">
          {WA_SVG}
          <span class="wa-label">WhatsApp</span>
        </a>
      </div>
    </div>
  </header>
'''


FOOTER = '''  <footer class="site-footer">
    <div class="container footer-inner">
      <div>
        <p class="footer-brand" data-brand>Marina Immo</p>
        <p class="footer-tag" data-i18n="footerTag">Immobilier d'investissement · Dubaï · Bali · Géorgie</p>
      </div>
      <ul class="footer-links">
        <li><a href="mentions-legales.html" data-i18n="legalLink">Mentions légales</a></li>
        <li><a href="confidentialite.html" data-i18n="privacyLink">Confidentialité</a></li>
        <li data-cookie-settings hidden><button type="button" data-i18n="cookieLink">Cookies</button></li>
      </ul>
      <p class="disclaimer" data-i18n="disclaimer">Les biens marqués « Exemple » sont des illustrations. Les prix sont indicatifs et peuvent évoluer. Les rendements affichés sont des estimations brutes, non garanties. Ce site ne constitue pas un conseil en investissement.</p>
      <p class="rera" data-rera hidden></p>
      <p class="copyright">© <span id="year">2026</span> <span data-brand>Marina Immo</span>. <span data-i18n="rights">Tous droits réservés.</span></p>
    </div>
  </footer>
'''


def scripts(listings=True):
    s = '  <script src="config.js"></script>\n'
    if listings:
        s += '  <script src="listings.js"></script>\n'
    return s + '  <script src="app.js"></script>\n</body>\n</html>\n'


HOME_HERO = '''    <section class="hero" id="top" aria-labelledby="hero-title">
      <div class="container hero-inner">
        <p class="eyebrow" data-i18n="heroEyebrow">Dubaï · Bali · Géorgie</p>
        <h1 id="hero-title" data-i18n="heroTitle">Investissez à Dubaï, Bali et en Géorgie. Avec des chiffres, pas des promesses.</h1>
        <p class="hero-lead" data-i18n="heroLead">Des biens sélectionnés, prêts ou sur plan. Une analyse claire du prix, du rendement et des risques. Un accompagnement en français, de la recherche à la remise des clés.</p>
        <div class="hero-picks" role="group" aria-label="Choisir une destination" data-i18n-aria="heroPickLabel">
          <button type="button" class="pick" data-pick="dubai"><span data-i18n="country_dubai">Dubaï</span><span class="pick-arrow" aria-hidden="true">→</span></button>
          <button type="button" class="pick" data-pick="bali"><span data-i18n="country_bali">Bali</span><span class="pick-arrow" aria-hidden="true">→</span></button>
          <button type="button" class="pick" data-pick="georgia"><span data-i18n="country_georgia">Géorgie</span><span class="pick-arrow" aria-hidden="true">→</span></button>
        </div>
        <a class="hero-secondary" href="#contact" data-i18n="heroCta">Parler à un conseiller</a>
      </div>
    </section>

'''


def landing_hero(c, eyebrow, h1, lead):
    return f'''    <section class="hero" id="top" aria-labelledby="hero-title">
      <div class="container hero-inner">
        <p class="eyebrow" data-i18n="heroEyebrow_{c}">{eyebrow}</p>
        <h1 id="hero-title" data-i18n="heroTitle_{c}">{h1}</h1>
        <p class="hero-lead" data-i18n="heroLead_{c}">{lead}</p>
        <div class="hero-ctas">
          <a class="btn btn-gold" href="#biens" data-i18n="seeListings">Voir les biens</a>
          <a class="btn btn-wa" data-wa-link href="https://wa.me/971500000000" target="_blank" rel="noopener">{WA_SVG}<span data-i18n="waCta">Écrire sur WhatsApp</span></a>
        </div>
      </div>
    </section>

    <section class="section section-tight" aria-labelledby="focus-title">
      <div class="container">
        <p class="eyebrow" id="focus-title" data-i18n="focusEyebrow">Pourquoi ce marché</p>
        <div id="dest-focus"></div>
      </div>
    </section>

'''


def write(name, s):
    open(OUT + name, 'w').write(s)
    print('wrote', name, len(s))


# ---- index ----
write('index.html',
      head('Marina Immo — Investir à Dubaï, Bali et en Géorgie',
           "Marina Immo : biens immobiliers à Dubaï, Bali et en Géorgie. Prêts ou sur plan, prix analysés, accompagnement en français et en anglais de la recherche à la remise des clés.",
           '', extra=JSONLD)
      + '<body data-page="home" data-title-key="title_home">\n' + header('#top')
      + '\n  <main id="main">\n' + HOME_HERO + '    ' + LISTINGS + DEST + WHYCONTACT + '  </main>\n\n'
      + FOOTER + '\n  ' + MODAL + scripts())

# ---- landing pages ----
LP = [
    ('dubai', 'dubai.html', 'Investir à Dubaï — Biens prêts et sur plan | Marina Immo',
     "Investir à Dubaï : appartements, villas et biens sur plan, prix comparés aux transactions du Dubai Land Department. Pas d'impôt sur le revenu aux Émirats. Conseil en français.",
     'Immobilier à Dubaï', "Investir à Dubaï : pas d'impôt sur le revenu aux Émirats, des prix comparés aux ventes réelles.",
     "Appartements, villas et biens sur plan dans les meilleurs quartiers. Chaque prix est comparé aux transactions du Dubai Land Department avant de vous être proposé."),
    ('bali', 'bali.html', 'Investir à Bali — Villas | Marina Immo',
     "Investir à Bali : villas sélectionnées pour la location saisonnière à Canggu, Uluwatu et Ubud. Cadre juridique expliqué, accompagnement en français.",
     'Immobilier à Bali', "Investir à Bali : des villas tropicales pensées pour la location saisonnière.",
     "Canggu, Uluwatu, Ubud… Des villas sélectionnées pour la location saisonnière, avec un cadre juridique expliqué clairement."),
    ('georgia', 'georgie.html', 'Investir en Géorgie — Appartements à Tbilissi et Batoumi | Marina Immo',
     "Investir en Géorgie : appartements à Tbilissi et Batoumi, ticket d'entrée accessible, pleine propriété pour les étrangers. Accompagnement en français et en anglais.",
     'Immobilier en Géorgie', "Investir en Géorgie : un ticket d'entrée bas, en pleine propriété.",
     "Tbilissi et Batoumi : des appartements à prix d'entrée accessible, achetables en pleine propriété par les étrangers."),
]
for c, f, title, desc, eb, h1, lead in LP:
    write(f, head(title, desc, f)
          + f'<body data-page="landing" data-country="{c}" data-title-key="title_{c}">\n' + header('index.html')
          + '\n  <main id="main">\n' + landing_hero(c, eb, h1, lead) + '    ' + LISTINGS + WHYCONTACT + DEST.replace('<!-- DESTINATIONS -->', '<!-- OTHER DESTINATIONS -->') + '  </main>\n\n'
          + FOOTER + '\n  ' + MODAL + scripts())

# ---- merci ----
write('merci.html',
      head('Merci — Marina Immo', "Votre demande a bien été envoyée à Marina Immo.", 'merci.html', robots='noindex, follow')
      + '<body data-page="merci" data-title-key="title_merci">\n' + header('index.html', sections=False)
      + f'''
  <main id="main" class="page-simple">
    <div class="container merci-box">
      <p class="eyebrow" data-i18n="merciEyebrow">Demande envoyée</p>
      <h1 data-i18n="merciTitle">Merci, votre demande est bien reçue.</h1>
      <p data-i18n="merciText">Un conseiller vous répond sous 24 h ouvrées. Pour aller plus vite, écrivez-nous directement sur WhatsApp.</p>
      <div class="btns">
        <a class="btn btn-wa" data-wa-link href="https://wa.me/971500000000" target="_blank" rel="noopener">{WA_SVG}<span data-i18n="waCta">Écrire sur WhatsApp</span></a>
        <a class="btn btn-ghost" href="index.html" data-i18n="backHome">Retour à l'accueil</a>
      </div>
    </div>
  </main>

''' + FOOTER + scripts(listings=False))

# ---- legal pages ----
TODO = lambda s: f'<span class="todo">[À COMPLÉTER : {s}]</span>'
TODO_EN = lambda s: f'<span class="todo">[TO COMPLETE: {s}]</span>'

MENTIONS_FR = f'''
      <div data-lang-block="fr" lang="fr">
        <h1>Mentions légales</h1>
        <p>Dernière mise à jour : {TODO("date")}</p>
        <h2>Éditeur du site</h2>
        <p>Raison sociale : {TODO("nom de la société")}<br>
        Forme juridique et capital : {TODO("forme juridique, capital")}<br>
        Adresse du siège : {TODO("adresse complète")}<br>
        Numéro d'immatriculation / licence commerciale : {TODO("numéro de registre ou de licence")}<br>
        E-mail : <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a><br>
        Directeur de la publication : {TODO("nom du responsable")}</p>
        <h2>Activité réglementée (Dubaï)</h2>
        <p>Courtier enregistré auprès de la RERA / Dubai Land Department — numéro ORN : {TODO("numéro ORN")}<br>
        Numéro BRN du ou des agents : {TODO("numéro(s) BRN")}<br>
        Les annonces de biens situés à Dubaï affichent, lorsqu'il existe, le numéro de permis publicitaire (Trakheesi / DLD).</p>
        <h2>Hébergement</h2>
        <p>Netlify, Inc. — 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis — netlify.com</p>
        <h2>Propriété intellectuelle</h2>
        <p>Les textes, visuels et la mise en page de ce site appartiennent à {TODO("nom de la société")}. Toute reproduction sans autorisation est interdite.</p>
        <h2>Informations sur les biens</h2>
        <p>Les biens marqués « Exemple » sont des illustrations et ne constituent pas une offre. Les prix, surfaces, dates de livraison et rendements sont indicatifs et peuvent évoluer. Les montants convertis en dollars US sont approximatifs. Les rendements affichés sont des estimations brutes, sans garantie.</p>
        <h2>Absence de conseil en investissement</h2>
        <p>Les informations de ce site sont fournies à titre informatif. Elles ne constituent ni un conseil en investissement, ni un conseil fiscal ou juridique. Tout investissement immobilier comporte des risques, y compris de perte en capital et de change. Consultez un professionnel qualifié avant toute décision.</p>
        <h2>Contact</h2>
        <p>Pour toute question : <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a></p>
      </div>
'''
MENTIONS_EN = f'''
      <div data-lang-block="en" lang="en" hidden>
        <h1>Legal notice</h1>
        <p>Last updated: {TODO_EN("date")}</p>
        <h2>Website publisher</h2>
        <p>Company name: {TODO_EN("company name")}<br>
        Legal form and share capital: {TODO_EN("legal form, capital")}<br>
        Registered address: {TODO_EN("full address")}<br>
        Registration / trade licence number: {TODO_EN("registry or licence number")}<br>
        Email: <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a><br>
        Publication director: {TODO_EN("name of the person responsible")}</p>
        <h2>Regulated activity (Dubai)</h2>
        <p>Broker registered with RERA / Dubai Land Department — ORN: {TODO_EN("ORN number")}<br>
        Agent BRN number(s): {TODO_EN("BRN number(s)")}<br>
        Listings for properties in Dubai show the advertising permit number (Trakheesi / DLD) where one exists.</p>
        <h2>Hosting</h2>
        <p>Netlify, Inc. — 512 2nd Street, Suite 200, San Francisco, CA 94107, USA — netlify.com</p>
        <h2>Intellectual property</h2>
        <p>The texts, visuals and layout of this website belong to {TODO_EN("company name")}. Any reproduction without permission is prohibited.</p>
        <h2>Property information</h2>
        <p>Listings marked "Sample" are illustrations and do not constitute an offer. Prices, sizes, handover dates and yields are indicative and may change. Amounts converted to US dollars are approximate. Yields shown are gross estimates and are not guaranteed.</p>
        <h2>No investment advice</h2>
        <p>The information on this website is provided for information purposes only. It does not constitute investment, tax or legal advice. Any property investment carries risks, including loss of capital and currency risk. Consult a qualified professional before making any decision.</p>
        <h2>Contact</h2>
        <p>For any question: <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a></p>
      </div>
'''

PRIV_FR = f'''
      <div data-lang-block="fr" lang="fr">
        <h1>Politique de confidentialité</h1>
        <p>Dernière mise à jour : {TODO("date")}</p>
        <h2>Responsable du traitement</h2>
        <p>{TODO("nom de la société")}, {TODO("adresse complète")}. Contact : <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a></p>
        <h2>Données du formulaire de contact</h2>
        <p>Quand vous remplissez le formulaire, nous recevons : nom, e-mail, numéro WhatsApp / téléphone (facultatif), pays d'intérêt, budget, référence du bien et message.</p>
        <ul>
          <li><strong>Pourquoi :</strong> répondre à votre demande et vous proposer des biens adaptés.</li>
          <li><strong>Base légale :</strong> votre consentement (case à cocher) et les mesures précontractuelles prises à votre demande.</li>
          <li><strong>Qui y accède :</strong> l'équipe {TODO("nom de la société")} uniquement. Les données sont transmises via Netlify (hébergeur du site et du formulaire). Elles ne sont ni vendues ni louées.</li>
        </ul>
        <h2>WhatsApp</h2>
        <p>Si vous nous écrivez sur WhatsApp, votre numéro et vos messages sont traités par WhatsApp (Meta Platforms) selon sa propre politique de confidentialité. Nous utilisons ces échanges uniquement pour suivre votre projet.</p>
        <h2 id="cookies">Cookies et pixels publicitaires</h2>
        <p>Le site fonctionne sans cookie de suivi. Avec votre accord uniquement (bandeau « Accepter / Refuser »), nous pouvons activer :</p>
        <ul>
          <li>Google Analytics 4 (mesure d'audience, Google) ;</li>
          <li>Pixel Meta (publicités Facebook / Instagram) ;</li>
          <li>Pixel TikTok (publicités TikTok).</li>
        </ul>
        <p>Ils mesurent les visites et les demandes de contact, pour savoir quelles publicités fonctionnent. Si vous refusez, aucun de ces outils n'est chargé. Votre choix (ainsi que votre langue préférée) est mémorisé dans votre navigateur. Vous pouvez le changer à tout moment avec le lien « Cookies » en bas de page.</p>
        <h2>Durée de conservation</h2>
        <p>Demandes de contact : {TODO("ex. 3 ans après le dernier échange")}. Données de mesure d'audience : selon les réglages de chaque outil, {TODO("ex. 14 mois pour Google Analytics")}.</p>
        <h2>Transferts hors de votre pays</h2>
        <p>Netlify, Google, Meta et TikTok peuvent traiter des données hors de l'Union européenne, avec les garanties prévues par leurs contrats (clauses contractuelles types).</p>
        <h2>Vos droits</h2>
        <p>Vous pouvez demander l'accès, la correction ou la suppression de vos données, ou retirer votre consentement, en écrivant à <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a>. Réponse sous 30 jours. Si vous résidez dans l'Union européenne, vous pouvez aussi saisir l'autorité de protection des données de votre pays (en France : la CNIL).</p>
      </div>
'''
PRIV_EN = f'''
      <div data-lang-block="en" lang="en" hidden>
        <h1>Privacy policy</h1>
        <p>Last updated: {TODO_EN("date")}</p>
        <h2>Data controller</h2>
        <p>{TODO_EN("company name")}, {TODO_EN("full address")}. Contact: <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a></p>
        <h2>Contact form data</h2>
        <p>When you fill in the form, we receive: name, email, WhatsApp / phone number (optional), country of interest, budget, property reference and message.</p>
        <ul>
          <li><strong>Why:</strong> to answer your request and suggest suitable properties.</li>
          <li><strong>Legal basis:</strong> your consent (checkbox) and pre-contractual steps taken at your request.</li>
          <li><strong>Who has access:</strong> the {TODO_EN("company name")} team only. Data is transmitted through Netlify (host of the website and form). It is never sold or rented.</li>
        </ul>
        <h2>WhatsApp</h2>
        <p>If you message us on WhatsApp, your number and messages are processed by WhatsApp (Meta Platforms) under its own privacy policy. We use these conversations only to follow up on your project.</p>
        <h2 id="cookies-en">Cookies and advertising pixels</h2>
        <p>The website works without tracking cookies. Only with your consent (the "Accept / Decline" banner) may we enable:</p>
        <ul>
          <li>Google Analytics 4 (audience measurement, Google);</li>
          <li>Meta Pixel (Facebook / Instagram ads);</li>
          <li>TikTok Pixel (TikTok ads).</li>
        </ul>
        <p>They measure visits and contact requests, so we know which ads work. If you decline, none of these tools is loaded. Your choice (and your preferred language) is stored in your browser. You can change it at any time with the "Cookies" link at the bottom of the page.</p>
        <h2>Retention</h2>
        <p>Contact requests: {TODO_EN("e.g. 3 years after the last exchange")}. Analytics data: according to each tool's settings, {TODO_EN("e.g. 14 months for Google Analytics")}.</p>
        <h2>Transfers outside your country</h2>
        <p>Netlify, Google, Meta and TikTok may process data outside the European Union, with the safeguards provided in their contracts (standard contractual clauses).</p>
        <h2>Your rights</h2>
        <p>You can request access to, correction or deletion of your data, or withdraw your consent, by writing to <a data-email-link href="mailto:contact@marina-immo.com">contact@marina-immo.com</a>. Reply within 30 days. If you live in the European Union, you can also contact your national data protection authority (in France: the CNIL).</p>
      </div>
'''

for f, title, desc, key, fr, en in [
    ('mentions-legales.html', 'Mentions légales — Marina Immo', "Mentions légales du site Marina Immo.", 'title_legal', MENTIONS_FR, MENTIONS_EN),
    ('confidentialite.html', 'Politique de confidentialité — Marina Immo', "Politique de confidentialité et cookies du site Marina Immo.", 'title_privacy', PRIV_FR, PRIV_EN),
]:
    write(f, head(title, desc, f)
          + f'<body data-page="legal" data-title-key="{key}">\n' + header('index.html', sections=False)
          + '\n  <main id="main" class="page-simple">\n    <article class="container legal">' + fr + en
          + '    </article>\n  </main>\n\n' + FOOTER + scripts(listings=False))
