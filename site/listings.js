/*
 * =====================================================================
 *  MARINA IMMO — FICHIER DES ANNONCES (contenu du site)
 * =====================================================================
 *
 *  Ce fichier contient toutes les annonces affichées sur le site,
 *  ainsi que la présentation des trois pays (Dubaï, Bali, Géorgie).
 *  Vous pouvez le modifier avec n'importe quel éditeur de texte.
 *
 *  POUR AJOUTER UNE ANNONCE
 *  1. Copiez un bloc complet, depuis l'accolade ouvrante « { »
 *     jusqu'à l'accolade fermante « }, » (virgule comprise).
 *  2. Collez-le juste en dessous du dernier bloc de la liste.
 *  3. Changez les valeurs : identifiant (id), ville, prix, surface,
 *     titre, description, etc. Chaque id doit être unique
 *     (ex. : DXB-005, BAL-005, GEO-005).
 *  4. Gardez bien les virgules entre les blocs et entre les lignes,
 *     ainsi que les guillemets autour des textes.
 *
 *  POUR MODIFIER UNE ANNONCE
 *  Changez seulement le texte entre guillemets ou les nombres.
 *  Ne supprimez pas les noms de champs (price:, city:, etc.).
 *
 *  RÈGLES DES CHAMPS
 *  - country : "dubai", "bali" ou "georgia"
 *  - type    : "apartment", "villa", "penthouse" ou "townhouse"
 *  - status  : "ready" (livré) ou "offplan" (sur plan)
 *  - bedrooms : nombre de chambres (0 = studio)
 *  - price   : prix dans la devise indiquée (currency : "AED" ou "USD"),
 *              écrit sans espaces ni points (ex. : 1950000)
 *  - price_usd : le même prix converti en dollars US
 *              (Dubaï : prix en AED divisé par 3,6725)
 *  - handover : date de livraison pour un bien sur plan (ex. : "T4 2027"),
 *              ou null si le bien est déjà livré
 *  - est_yield_pct : rendement locatif brut estimé en %, ou null
 *  - permit  : (facultatif) numéro de permis publicitaire Trakheesi / DLD,
 *              OBLIGATOIRE pour toute vraie annonce à Dubaï
 *              (ex. permit: "1234567890") — affiché dans la fiche du bien
 *
 *  IMPORTANT — LES EXEMPLES
 *  Les 12 annonces ci-dessous sont des EXEMPLES ILLUSTRATIFS, pas de
 *  vrais biens. La ligne « sample: true » affiche un badge « Exemple »
 *  sur l'annonce. Pour une vraie annonce, mettez « sample: false »
 *  (ou supprimez simplement le bloc d'exemple).
 * =====================================================================
 */

window.LISTINGS = [
  /* ============================ DUBAÏ ============================ */
  {
    id: "DXB-001",
    country: "dubai",
    city: "Dubai Marina",
    type: "apartment",
    status: "ready",
    bedrooms: 2,
    bathrooms: 2,
    size_sqm: 120,
    price: 2750000,
    currency: "AED",
    price_usd: 748809,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: null,
    est_yield_pct: 6.2,
    title: {
      fr: "Appartement 2 chambres avec vue sur la marina",
      en: "2-bedroom apartment with marina views"
    },
    description: {
      fr: "Appartement lumineux situé dans une tour résidentielle de Dubai Marina, à quelques minutes à pied de la promenade et du tramway. Les pièces de vie s'ouvrent sur un balcon orienté vers la marina. Bien livré, disponible pour une occupation personnelle ou la location.",
      en: "A bright apartment in a residential tower in Dubai Marina, a short walk from the promenade and the tram. The living areas open onto a balcony facing the marina. Completed and available for personal use or rental."
    },
    features: {
      fr: ["Vue sur la marina", "Balcon", "Piscine et salle de sport", "Parking privé", "Proche tramway et métro"],
      en: ["Marina views", "Balcony", "Pool and gym", "Private parking", "Near tram and metro"]
    },
    sample: true
  },
  {
    id: "DXB-002",
    country: "dubai",
    city: "Jumeirah Village Circle",
    type: "apartment",
    status: "offplan",
    bedrooms: 1,
    bathrooms: 1,
    size_sqm: 72,
    price: 1180000,
    currency: "AED",
    price_usd: 321307,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: "T4 2027",
    est_yield_pct: 7,
    title: {
      fr: "Appartement 1 chambre sur plan à JVC",
      en: "Off-plan 1-bedroom apartment in JVC"
    },
    description: {
      fr: "Appartement d'une chambre dans une résidence en construction au cœur de Jumeirah Village Circle, quartier familial bien relié aux grands axes. Plan de paiement échelonné jusqu'à la livraison. Un point d'entrée accessible sur le marché de Dubaï.",
      en: "A one-bedroom apartment in a residence under construction at the heart of Jumeirah Village Circle, a family-oriented community with good road access. Staged payment plan until handover. An accessible entry point into the Dubai market."
    },
    features: {
      fr: ["Plan de paiement échelonné", "Cuisine équipée", "Piscine sur le toit", "Salle de sport", "Parking inclus"],
      en: ["Staged payment plan", "Fitted kitchen", "Rooftop pool", "Gym", "Parking included"]
    },
    sample: true
  },
  {
    id: "DXB-003",
    country: "dubai",
    city: "Dubai Hills Estate",
    type: "townhouse",
    status: "ready",
    bedrooms: 4,
    bathrooms: 4,
    size_sqm: 260,
    price: 5600000,
    currency: "AED",
    price_usd: 1524847,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: null,
    est_yield_pct: 5.2,
    title: {
      fr: "Maison de ville 4 chambres à Dubai Hills",
      en: "4-bedroom townhouse in Dubai Hills"
    },
    description: {
      fr: "Maison de ville sur trois niveaux dans une communauté arborée de Dubai Hills Estate, proche du parc central, des écoles et du centre commercial. Jardin privatif et terrasse sur le toit. Un cadre de vie pensé pour les familles.",
      en: "A three-level townhouse in a leafy community of Dubai Hills Estate, close to the central park, schools and the mall. Private garden and roof terrace. A setting designed for family living."
    },
    features: {
      fr: ["Jardin privatif", "Terrasse sur le toit", "Chambre de service", "Garage 2 places", "Proche écoles et parc"],
      en: ["Private garden", "Roof terrace", "Maid's room", "2-car garage", "Near schools and park"]
    },
    sample: true
  },
  {
    id: "DXB-004",
    country: "dubai",
    city: "Palm Jumeirah",
    type: "apartment",
    status: "ready",
    bedrooms: 2,
    bathrooms: 3,
    size_sqm: 150,
    price: 4100000,
    currency: "AED",
    price_usd: 1116406,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: null,
    est_yield_pct: 5.5,
    title: {
      fr: "Appartement 2 chambres avec accès plage, Palm Jumeirah",
      en: "2-bedroom beach-access apartment, Palm Jumeirah"
    },
    description: {
      fr: "Appartement sur l'une des branches de Palm Jumeirah, avec accès direct à une plage privée de la résidence. Grandes baies vitrées et terrasse donnant sur la mer. Adresse recherchée pour la résidence principale comme pour la location saisonnière.",
      en: "An apartment on one of the fronds of Palm Jumeirah, with direct access to the residence's private beach. Floor-to-ceiling windows and a terrace overlooking the sea. A sought-after address for both primary residence and holiday rental."
    },
    features: {
      fr: ["Accès plage privée", "Vue mer", "Terrasse", "Piscine et spa", "Conciergerie"],
      en: ["Private beach access", "Sea views", "Terrace", "Pool and spa", "Concierge"]
    },
    sample: true
  },

  /* ============================ BALI ============================ */
  {
    id: "BAL-001",
    country: "bali",
    city: "Canggu",
    type: "villa",
    status: "ready",
    bedrooms: 2,
    bathrooms: 2,
    size_sqm: 140,
    price: 380000,
    currency: "USD",
    price_usd: 380000,
    tenure: { fr: "Bail de 25 ans (leasehold)", en: "25-year leasehold" },
    handover: null,
    est_yield_pct: 9,
    title: {
      fr: "Villa 2 chambres avec piscine à Canggu",
      en: "2-bedroom pool villa in Canggu"
    },
    description: {
      fr: "Villa de style tropical moderne à Canggu, à quelques minutes des plages et des cafés du quartier. Salon ouvert sur une piscine privée et un jardin. Livrée meublée, adaptée à la location de courte durée.",
      en: "A modern tropical villa in Canggu, a few minutes from the beaches and the area's cafés. Open living area facing a private pool and garden. Delivered furnished and suited to short-term rental."
    },
    features: {
      fr: ["Piscine privée", "Entièrement meublée", "Salon ouvert", "Jardin tropical", "Proche plages"],
      en: ["Private pool", "Fully furnished", "Open-plan living", "Tropical garden", "Near the beaches"]
    },
    sample: true
  },
  {
    id: "BAL-002",
    country: "bali",
    city: "Uluwatu (Bingin)",
    type: "villa",
    status: "offplan",
    bedrooms: 3,
    bathrooms: 3,
    size_sqm: 210,
    price: 520000,
    currency: "USD",
    price_usd: 520000,
    tenure: { fr: "Bail de 30 ans (leasehold)", en: "30-year leasehold" },
    handover: "T3 2027",
    est_yield_pct: 8.5,
    title: {
      fr: "Villa 3 chambres sur plan près de Bingin",
      en: "Off-plan 3-bedroom villa near Bingin"
    },
    description: {
      fr: "Villa en construction sur les hauteurs de Bingin, dans la péninsule d'Uluwatu, à proximité des spots de surf et des falaises. Architecture contemporaine en matériaux naturels, avec piscine à débordement. Paiement échelonné selon l'avancement des travaux.",
      en: "A villa under construction on the hillside of Bingin, on the Uluwatu peninsula, close to surf breaks and the cliffs. Contemporary architecture in natural materials, with an infinity pool. Payments staged with construction progress."
    },
    features: {
      fr: ["Piscine à débordement", "Vue sur l'océan partielle", "Matériaux naturels", "Paiement échelonné", "Proche spots de surf"],
      en: ["Infinity pool", "Partial ocean views", "Natural materials", "Staged payments", "Near surf breaks"]
    },
    sample: true
  },
  {
    id: "BAL-003",
    country: "bali",
    city: "Ubud",
    type: "villa",
    status: "ready",
    bedrooms: 1,
    bathrooms: 1,
    size_sqm: 85,
    price: 215000,
    currency: "USD",
    price_usd: 215000,
    tenure: { fr: "Bail de 25 ans (leasehold)", en: "25-year leasehold" },
    handover: null,
    est_yield_pct: 8,
    title: {
      fr: "Villa 1 chambre face aux rizières à Ubud",
      en: "1-bedroom villa overlooking rice fields in Ubud"
    },
    description: {
      fr: "Petite villa au calme dans les environs d'Ubud, avec vue dégagée sur les rizières. Piscine privée et pièces de vie ouvertes sur la nature. Un format compact, recherché par les voyageurs en quête de sérénité.",
      en: "A small, quiet villa on the outskirts of Ubud, with open views over the rice fields. Private pool and living spaces that open onto nature. A compact format popular with travellers seeking calm."
    },
    features: {
      fr: ["Vue sur les rizières", "Piscine privée", "Meublée", "Environnement calme", "Proche centre d'Ubud"],
      en: ["Rice field views", "Private pool", "Furnished", "Quiet setting", "Near Ubud centre"]
    },
    sample: true
  },
  {
    id: "BAL-004",
    country: "bali",
    city: "Pererenan",
    type: "villa",
    status: "offplan",
    bedrooms: 2,
    bathrooms: 2,
    size_sqm: 130,
    price: 340000,
    currency: "USD",
    price_usd: 340000,
    tenure: { fr: "Bail de 25 ans (leasehold)", en: "25-year leasehold" },
    handover: "T2 2027",
    est_yield_pct: null,
    title: {
      fr: "Villa 2 chambres sur plan à Pererenan",
      en: "Off-plan 2-bedroom villa in Pererenan"
    },
    description: {
      fr: "Villa en construction à Pererenan, village voisin de Canggu, plus résidentiel et proche de la plage. Plans ouverts, piscine privée et toit-terrasse. Livraison prévue meublée.",
      en: "A villa under construction in Pererenan, a quieter, more residential village next to Canggu and close to the beach. Open-plan layout, private pool and roof terrace. Planned to be delivered furnished."
    },
    features: {
      fr: ["Piscine privée", "Toit-terrasse", "Livrée meublée", "Paiement échelonné", "Proche plage"],
      en: ["Private pool", "Roof terrace", "Delivered furnished", "Staged payments", "Near the beach"]
    },
    sample: true
  },

  /* =========================== GÉORGIE =========================== */
  {
    id: "GEO-001",
    country: "georgia",
    city: "Batumi",
    type: "apartment",
    status: "offplan",
    bedrooms: 1,
    bathrooms: 1,
    size_sqm: 48,
    price: 78000,
    currency: "USD",
    price_usd: 78000,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: "T2 2027",
    est_yield_pct: 8,
    title: {
      fr: "Appartement 1 chambre sur plan, front de mer de Batumi",
      en: "Off-plan 1-bedroom seafront apartment, Batumi"
    },
    description: {
      fr: "Appartement d'une chambre dans une résidence neuve en construction, à proximité du boulevard de Batumi et de la mer Noire. Livraison en finition blanche ou meublée selon option. Un ticket d'entrée modéré sur le littoral géorgien.",
      en: "A one-bedroom apartment in a new residence under construction, close to Batumi Boulevard and the Black Sea. Delivered white-box or furnished, depending on the option chosen. A moderate entry ticket on the Georgian coast."
    },
    features: {
      fr: ["Vue mer partielle", "Proche boulevard", "Option meublée", "Paiement échelonné", "Résidence avec piscine"],
      en: ["Partial sea views", "Near the boulevard", "Furnished option", "Staged payments", "Residence with pool"]
    },
    sample: true
  },
  {
    id: "GEO-002",
    country: "georgia",
    city: "Batumi",
    type: "apartment",
    status: "ready",
    bedrooms: 2,
    bathrooms: 1,
    size_sqm: 68,
    price: 105000,
    currency: "USD",
    price_usd: 105000,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: null,
    est_yield_pct: 7.5,
    title: {
      fr: "Appartement 2 chambres meublé à Batumi",
      en: "Furnished 2-bedroom apartment in Batumi"
    },
    description: {
      fr: "Appartement livré et meublé dans le nouveau Batumi, à quelques minutes à pied de la plage. Séjour avec balcon et cuisine équipée. Prêt à être occupé ou mis en location.",
      en: "A completed, furnished apartment in New Batumi, a few minutes' walk from the beach. Living room with balcony and fitted kitchen. Ready to move in or to rent out."
    },
    features: {
      fr: ["Meublé", "Balcon", "Cuisine équipée", "Proche plage", "Prêt à louer"],
      en: ["Furnished", "Balcony", "Fitted kitchen", "Near the beach", "Rental-ready"]
    },
    sample: true
  },
  {
    id: "GEO-003",
    country: "georgia",
    city: "Tbilisi — Vake",
    type: "apartment",
    status: "ready",
    bedrooms: 2,
    bathrooms: 2,
    size_sqm: 95,
    price: 210000,
    currency: "USD",
    price_usd: 210000,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: null,
    est_yield_pct: 7,
    title: {
      fr: "Appartement 2 chambres dans le quartier de Vake",
      en: "2-bedroom apartment in the Vake district"
    },
    description: {
      fr: "Appartement rénové à Vake, quartier résidentiel prisé de Tbilissi, proche du parc Vake et des avenues commerçantes. Pièces lumineuses, deux salles de bains et balcon. Adapté à la location longue durée.",
      en: "A renovated apartment in Vake, a sought-after residential district of Tbilisi, close to Vake Park and the main shopping avenues. Bright rooms, two bathrooms and a balcony. Suited to long-term rental."
    },
    features: {
      fr: ["Rénové", "Deux salles de bains", "Balcon", "Proche parc Vake", "Chauffage central"],
      en: ["Renovated", "Two bathrooms", "Balcony", "Near Vake Park", "Central heating"]
    },
    sample: true
  },
  {
    id: "GEO-004",
    country: "georgia",
    city: "Tbilisi — Old Town",
    type: "penthouse",
    status: "ready",
    bedrooms: 3,
    bathrooms: 2,
    size_sqm: 140,
    price: 295000,
    currency: "USD",
    price_usd: 295000,
    tenure: { fr: "Pleine propriété", en: "Freehold" },
    handover: null,
    est_yield_pct: null,
    title: {
      fr: "Penthouse 3 chambres avec terrasse, vieille ville de Tbilissi",
      en: "3-bedroom penthouse with terrace, Old Tbilisi"
    },
    description: {
      fr: "Dernier étage d'un immeuble restauré de la vieille ville de Tbilissi, avec terrasse ouverte sur les toits et la forteresse de Narikala. Volumes généreux et cachet préservé. Proche des bains de soufre et des rues piétonnes.",
      en: "The top floor of a restored building in Old Tbilisi, with a terrace overlooking the rooftops and Narikala Fortress. Generous volumes and preserved character. Close to the sulphur baths and pedestrian streets."
    },
    features: {
      fr: ["Terrasse sur les toits", "Vue sur Narikala", "Immeuble restauré", "Hauts plafonds", "Quartier historique"],
      en: ["Rooftop terrace", "Narikala views", "Restored building", "High ceilings", "Historic district"]
    },
    sample: true
  }
];

window.COUNTRIES = {
  dubai: {
    name: { fr: "Dubaï", en: "Dubai" },
    tagline: {
      fr: "Un marché international, liquide et sans impôt sur le revenu.",
      en: "An international, liquid market with no personal income tax."
    },
    highlights: {
      fr: [
        "0 % d'impôt sur le revenu des personnes physiques.",
        "Pleine propriété (freehold) ouverte aux étrangers dans les zones désignées.",
        "Golden Visa possible via l'investissement immobilier, à partir d'environ 2 M AED, sous conditions.",
        "Biens sur plan avec paiements échelonnés jusqu'à la livraison.",
        "Frais d'enregistrement d'environ 4 % auprès du Dubai Land Department (DLD)."
      ],
      en: [
        "0% personal income tax.",
        "Freehold ownership open to foreigners in designated areas.",
        "Golden Visa possible through property investment, from around AED 2M, subject to conditions.",
        "Off-plan properties with staged payment plans until handover.",
        "Registration fee of around 4% with the Dubai Land Department (DLD)."
      ]
    }
  },
  bali: {
    name: { fr: "Bali", en: "Bali" },
    tagline: {
      fr: "Des villas tropicales accessibles, portées par le tourisme.",
      en: "Accessible tropical villas, driven by tourism."
    },
    highlights: {
      fr: [
        "Les étrangers achètent en bail longue durée (leasehold) : la pleine propriété du terrain leur est fermée.",
        "Forte demande en location saisonnière, liée au tourisme international.",
        "Tickets d'entrée plus bas que sur d'autres destinations balnéaires.",
        "Vérifications indispensables avant achat : permis de construire, zonage et titre du bail.",
        "Option possible : détenir le bien via une société locale à capitaux étrangers (PT PMA)."
      ],
      en: [
        "Foreigners buy on long-term leasehold: freehold land ownership is not open to them.",
        "Strong holiday-rental demand, driven by international tourism.",
        "Lower entry prices than many other seaside destinations.",
        "Due diligence is essential before buying: building permits, zoning and lease title.",
        "Possible option: holding the property through a foreign-owned local company (PT PMA)."
      ]
    }
  },
  georgia: {
    name: { fr: "Géorgie", en: "Georgia" },
    tagline: {
      fr: "Des prix d'entrée bas, entre mer Noire et capitale.",
      en: "Low entry prices, between the Black Sea and the capital."
    },
    highlights: {
      fr: [
        "Les étrangers peuvent acheter des appartements en pleine propriété (les terres agricoles font l'objet de restrictions).",
        "Enregistrement simple et rapide auprès du Public Service Hall.",
        "Prix d'entrée bas par rapport aux marchés d'Europe de l'Ouest.",
        "Deux marchés complémentaires : Batumi au bord de la mer Noire, Tbilissi la capitale.",
        "Permis de séjour possible via un investissement immobilier au-delà d'un certain seuil, sous conditions."
      ],
      en: [
        "Foreigners can buy apartments freehold (agricultural land is subject to restrictions).",
        "Simple, fast registration at the Public Service Hall.",
        "Low entry prices compared with Western European markets.",
        "Two complementary markets: seaside Batumi on the Black Sea and the capital, Tbilisi.",
        "Residence permit possible through property investment above a certain threshold, subject to conditions."
      ]
    }
  }
};
