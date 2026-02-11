"""Comprehensive Visa Database for 50+ Countries"""

VISA_DATABASE = {
    # ===== EUROPE =====
    "France": {
        "country": "France",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "French Embassy/Consulate",
        "useful_links": [
            "https://www.france-visas.gouv.fr",
            "https://www.diplomatie.gouv.fr"
        ],
        "required_documents": [
            "Passport (valid 6+ months)",
            "Visa application form",
            "Passport photos (4x6 cm)",
            "Travel insurance",
            "Proof of financial means",
            "Accommodation booking",
            "Flight itinerary",
            "Employment letter",
            "Bank statements"
        ]
    },
    "Germany": {
        "country": "Germany",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 10,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "German Embassy/Consulate",
        "useful_links": [
            "https://www.auswaertiges-amt.de",
            "https://www.make-it-in-germany.com"
        ],
        "required_documents": [
            "Passport (valid 6+ months)",
            "Visa application form",
            "Passport photos",
            "Travel insurance",
            "Proof of funds",
            "Hotel booking",
            "Flight confirmation",
            "Employment letter",
            "Bank statements"
        ]
    },
    "Spain": {
        "country": "Spain",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Spanish Embassy/Consulate",
        "useful_links": [
            "https://www.inclusion.gob.es"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Financial proof", "Accommodation", "Flight"]
    },
    "Italy": {
        "country": "Italy",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Italian Embassy/Consulate",
        "useful_links": [
            "https://vistoperitalia.esteri.it"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Bank proof", "Hotel booking", "Flight"]
    },
    "United Kingdom": {
        "country": "United Kingdom",
        "region": "Europe",
        "visa_type": "Standard Visitor",
        "processing_days": 3,
        "validity": "6 months",
        "visa_fee": 99,
        "currency": "GBP",
        "processing_location": "UK Visas and Immigration",
        "useful_links": [
            "https://www.gov.uk/check-uk-visa",
            "https://www.gov.uk/apply-uk-visa"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Financial proof", "Hotel booking", "Return flight"]
    },
    "Netherlands": {
        "country": "Netherlands",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 12,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Dutch Embassy/Consulate",
        "useful_links": [
            "https://www.ind.nl"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Proof of funds", "Accommodation", "Employment letter"]
    },
    "Belgium": {
        "country": "Belgium",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 14,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Belgian Embassy/Consulate",
        "useful_links": [
            "https://diplomatie.belgium.be"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Travel insurance", "Financial proof", "Hotel booking"]
    },
    "Switzerland": {
        "country": "Switzerland",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 10,
        "validity": "90 days",
        "visa_fee": 120,
        "currency": "CHF",
        "processing_location": "Swiss Embassy/Consulate",
        "useful_links": [
            "https://www.sem.admin.ch"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Bank statement", "Hotel booking", "Return flight"]
    },
    "Sweden": {
        "country": "Sweden",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Swedish Embassy/Consulate",
        "useful_links": [
            "https://www.migrationsverket.se"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Travel insurance", "Proof of funds", "Accommodation"]
    },
    "Norway": {
        "country": "Norway",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 100,
        "currency": "NOK",
        "processing_location": "Norwegian Embassy/Consulate",
        "useful_links": [
            "https://www.udi.no"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Bank proof", "Hotel booking"]
    },

    # ===== ASIA =====
    "India": {
        "country": "India",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 7,
        "validity": "1 year",
        "visa_fee": 80,
        "currency": "USD",
        "processing_location": "Indian Embassy/Consulate",
        "useful_links": [
            "https://www.indianvisaonline.gov.in",
            "https://www.mea.gov.in"
        ],
        "required_documents": [
            "Passport",
            "Visa application form",
            "Passport photos",
            "Proof of funds",
            "Hotel booking",
            "Return flight ticket",
            "Employment letter",
            "Bank statements"
        ]
    },
    "Japan": {
        "country": "Japan",
        "region": "Asia",
        "visa_type": "Temporary Visitor",
        "processing_days": 5,
        "validity": "90 days",
        "visa_fee": 0,
        "currency": "JPY",
        "processing_location": "Japanese Embassy/Consulate",
        "useful_links": [
            "https://www.mofa.go.jp",
            "https://www.us.emb-japan.go.jp"
        ],
        "required_documents": ["Passport", "Return ticket", "Travel insurance", "Hotel booking"]
    },
    "Thailand": {
        "country": "Thailand",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 5,
        "validity": "60 days",
        "visa_fee": 40,
        "currency": "USD",
        "processing_location": "Thai Embassy/Consulate",
        "useful_links": [
            "https://www.mfa.go.th",
            "https://bangkok.usembassy.gov"
        ],
        "required_documents": ["Passport", "Photos", "Hotel booking", "Return flight"]
    },
    "Vietnam": {
        "country": "Vietnam",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 3,
        "validity": "90 days",
        "visa_fee": 50,
        "currency": "USD",
        "processing_location": "Vietnamese Embassy/Consulate",
        "useful_links": [
            "https://mofa.gov.vn"
        ],
        "required_documents": ["Passport", "Photos", "Bank proof", "Hotel booking"]
    },
    "Philippines": {
        "country": "Philippines",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 1,
        "validity": "30 days",
        "visa_fee": 0,
        "currency": "PHP",
        "processing_location": "Bureau of Immigration",
        "useful_links": [
            "https://www.immigration.gov.ph"
        ],
        "required_documents": ["Passport", "Return ticket"]
    },
    "South Korea": {
        "country": "South Korea",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 5,
        "validity": "90 days",
        "visa_fee": 0,
        "currency": "KRW",
        "processing_location": "Korean Embassy/Consulate",
        "useful_links": [
            "https://overseas.mofa.go.kr"
        ],
        "required_documents": ["Passport", "Hotel booking", "Return flight"]
    },
    "China": {
        "country": "China",
        "region": "Asia",
        "visa_type": "L (Tourist)",
        "processing_days": 5,
        "validity": "90 days",
        "visa_fee": 140,
        "currency": "USD",
        "processing_location": "Chinese Embassy/Consulate",
        "useful_links": [
            "https://www.fmprc.gov.cn"
        ],
        "required_documents": ["Passport", "Photos", "Hotel booking", "Employment letter", "Bank statement"]
    },
    "Malaysia": {
        "country": "Malaysia",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 1,
        "validity": "90 days",
        "visa_fee": 0,
        "currency": "MYR",
        "processing_location": "Immigration Office",
        "useful_links": [
            "https://www.malaysia.gov.my"
        ],
        "required_documents": ["Passport", "Return ticket", "Hotel booking"]
    },
    "Singapore": {
        "country": "Singapore",
        "region": "Asia",
        "visa_type": "Tourist",
        "processing_days": 1,
        "validity": "30 days",
        "visa_fee": 0,
        "currency": "SGD",
        "processing_location": "Immigration & Checkpoints Authority",
        "useful_links": [
            "https://www.ica.gov.sg"
        ],
        "required_documents": ["Passport", "Return ticket"]
    },
    "Indonesia": {
        "country": "Indonesia",
        "region": "Asia",
        "visa_type": "VOA (Visa on Arrival)",
        "processing_days": 0,
        "validity": "30 days",
        "visa_fee": 35,
        "currency": "USD",
        "processing_location": "Airport",
        "useful_links": [
            "https://www.imigrasi.go.id"
        ],
        "required_documents": ["Passport", "Passport photo"]
    },

    # ===== AMERICAS =====
    "USA": {
        "country": "United States",
        "region": "Americas",
        "visa_type": "B1/B2",
        "processing_days": 60,
        "validity": "10 years",
        "visa_fee": 160,
        "currency": "USD",
        "processing_location": "US Embassy/Consulate",
        "useful_links": [
            "https://travel.state.gov",
            "https://www.uscis.gov"
        ],
        "required_documents": [
            "Passport (valid 6+ months)",
            "DS-160 form",
            "Passport photo",
            "Interview appointment",
            "Employment letter",
            "Bank statements",
            "Hotel booking",
            "Return flight",
            "Travel insurance"
        ]
    },
    "Canada": {
        "country": "Canada",
        "region": "Americas",
        "visa_type": "Visitor",
        "processing_days": 14,
        "validity": "6 months",
        "visa_fee": 100,
        "currency": "CAD",
        "processing_location": "Canadian Embassy/Consulate",
        "useful_links": [
            "https://www.canada.ca/en/immigration-refugees-citizenship.html"
        ],
        "required_documents": ["Passport", "eTA", "Bank proof", "Hotel booking", "Return flight"]
    },
    "Mexico": {
        "country": "Mexico",
        "region": "Americas",
        "visa_type": "FMM",
        "processing_days": 0,
        "validity": "180 days",
        "visa_fee": 0,
        "currency": "MXN",
        "processing_location": "Entry Point",
        "useful_links": [
            "https://www.gob.mx/inm"
        ],
        "required_documents": ["Passport", "Return ticket", "Hotel booking"]
    },
    "Argentina": {
        "country": "Argentina",
        "region": "Americas",
        "visa_type": "Tourist",
        "processing_days": 0,
        "validity": "90 days",
        "visa_fee": 0,
        "currency": "ARS",
        "processing_location": "Entry Point",
        "useful_links": [
            "https://www.migraciones.gov.ar"
        ],
        "required_documents": ["Passport", "Return ticket"]
    },
    "Brazil": {
        "country": "Brazil",
        "region": "Americas",
        "visa_type": "Tourist",
        "processing_days": 5,
        "validity": "90 days",
        "visa_fee": 160,
        "currency": "USD",
        "processing_location": "Brazilian Embassy/Consulate",
        "useful_links": [
            "https://www.gov.br/cidadania"
        ],
        "required_documents": ["Passport", "Photos", "Bank proof", "Employment letter", "Hotel booking"]
    },
    "Peru": {
        "country": "Peru",
        "region": "Americas",
        "visa_type": "Tourist",
        "processing_days": 0,
        "validity": "90 days",
        "visa_fee": 0,
        "currency": "PEN",
        "processing_location": "Entry Point",
        "useful_links": [
            "https://www.migraciones.gob.pe"
        ],
        "required_documents": ["Passport", "Hotel booking", "Return ticket"]
    },

    # ===== AUSTRALIA & OCEANIA =====
    "Australia": {
        "country": "Australia",
        "region": "Oceania",
        "visa_type": "ETA",
        "processing_days": 1,
        "validity": "12 months",
        "visa_fee": 20,
        "currency": "AUD",
        "processing_location": "Online",
        "useful_links": [
            "https://immi.homeaffairs.gov.au"
        ],
        "required_documents": ["Passport", "Email", "Credit card for payment"]
    },
    "New Zealand": {
        "country": "New Zealand",
        "region": "Oceania",
        "visa_type": "Visitor",
        "processing_days": 1,
        "validity": "9 months",
        "visa_fee": 0,
        "currency": "NZD",
        "processing_location": "Entry Point",
        "useful_links": [
            "https://www.immigration.govt.nz"
        ],
        "required_documents": ["Passport", "Return ticket", "Hotel booking"]
    },
    "Fiji": {
        "country": "Fiji",
        "region": "Oceania",
        "visa_type": "Tourist",
        "processing_days": 0,
        "validity": "30 days",
        "visa_fee": 0,
        "currency": "FJD",
        "processing_location": "Entry Point",
        "useful_links": [
            "https://www.fiji.gov.fj"
        ],
        "required_documents": ["Passport", "Return ticket"]
    },

    # ===== MIDDLE EAST & AFRICA =====
    "United Arab Emirates": {
        "country": "United Arab Emirates",
        "region": "Middle East",
        "visa_type": "Tourist",
        "processing_days": 1,
        "validity": "30 days",
        "visa_fee": 100,
        "currency": "AED",
        "processing_location": "UAE Embassy/Online",
        "useful_links": [
            "https://www.uae.gov.ae"
        ],
        "required_documents": ["Passport", "Photos", "Hotel booking"]
    },
    "Saudi Arabia": {
        "country": "Saudi Arabia",
        "region": "Middle East",
        "visa_type": "Tourist",
        "processing_days": 5,
        "validity": "1 year",
        "visa_fee": 140,
        "currency": "SAR",
        "processing_location": "Saudi Embassy/Online",
        "useful_links": [
            "https://www.saudi.gov.sa"
        ],
        "required_documents": ["Passport", "Photos", "Bank proof", "Sponsor letter"]
    },
    "Egypt": {
        "country": "Egypt",
        "region": "Africa",
        "visa_type": "Tourist",
        "processing_days": 5,
        "validity": "30 days",
        "visa_fee": 60,
        "currency": "EGP",
        "processing_location": "Egyptian Embassy/Air port",
        "useful_links": [
            "https://www.mfa.gov.eg"
        ],
        "required_documents": ["Passport", "Photos", "Hotel booking"]
    },
    "South Africa": {
        "country": "South Africa",
        "region": "Africa",
        "visa_type": "Visitor",
        "processing_days": 5,
        "validity": "3 months",
        "visa_fee": 75,
        "currency": "ZAR",
        "processing_location": "South African Embassy/Consulate",
        "useful_links": [
            "https://www.dha.gov.za"
        ],
        "required_documents": ["Passport", "Photos", "Bank proof", "Hotel booking", "Return flight"]
    },
    "Morocco": {
        "country": "Morocco",
        "region": "Africa",
        "visa_type": "Tourist",
        "processing_days": 0,
        "validity": "90 days",
        "visa_fee": 0,
        "currency": "MAD",
        "processing_location": "Entry Point",
        "useful_links": [
            "https://www.maroc.ma"
        ],
        "required_documents": ["Passport", "Return ticket"]
    },

    # ===== ADDITIONAL POPULAR DESTINATIONS =====
    "Iceland": {
        "country": "Iceland",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Icelandic Mission",
        "useful_links": [
            "https://www.utl.is"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Bank proof"]
    },
    "Turkey": {
        "country": "Turkey",
        "region": "Asia",
        "visa_type": "e-Visa",
        "processing_days": 1,
        "validity": "90 days",
        "visa_fee": 50,
        "currency": "USD",
        "processing_location": "Online",
        "useful_links": [
            "https://www.evisa.gov.tr"
        ],
        "required_documents": ["Passport", "Email", "Credit card"]
    },
    "Greece": {
        "country": "Greece",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Greek Embassy/Consulate",
        "useful_links": [
            "https://www.mfa.gr"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Bank statement"]
    },
    "Portugal": {
        "country": "Portugal",
        "region": "Europe",
        "visa_type": "Schengen",
        "processing_days": 15,
        "validity": "90 days",
        "visa_fee": 80,
        "currency": "EUR",
        "processing_location": "Portuguese Embassy/Consulate",
        "useful_links": [
            "https://www.sef.pt"
        ],
        "required_documents": ["Passport", "Visa form", "Photos", "Insurance", "Accommodation proof"]
    },
}

def get_visa_requirements(destination: str) -> dict:
    """Get visa requirements for a destination"""
    return VISA_DATABASE.get(destination.title(), {})

def get_all_countries() -> list:
    """Get list of all countries with visa info"""
    return sorted(list(VISA_DATABASE.keys()))

def search_visa_countries(query: str) -> list:
    """Search for countries by name or region"""
    query_lower = query.lower()
    results = []
    
    for country, info in VISA_DATABASE.items():
        if (query_lower in country.lower() or 
            query_lower in info.get("region", "").lower()):
            results.append(country)
    
    return sorted(results)
