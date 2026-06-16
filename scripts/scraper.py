import requests

def scrape_offers():
    payload = {
        "limit": 100,
        "skip": 0,
        "query": None,
        "specializationsIds": ["24"],
        "missionsTypesIds": ["VIE"],
        "countriesIds": ["CA"],
        "geographicZones": ["2", "5"],
        "entreprisesIds": [0],
        "porteEnv": ["0"],
        "teletravail": ["0"],
        "activitySectorId": [],
        "companiesSizes": [],
        "missionStartDate": None,
        "missionsDurations": [],
        "studiesLevelId": []
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "Origin": "https://mon-vie-via.businessfrance.fr",
        "Referer": "https://mon-vie-via.businessfrance.fr/"
    }
    offers_details = {}

    # Get the product page content and create a sou

    try:
        # Scrape the product details
        response = requests.post("https://civiweb-api-prd.azurewebsites.net/api/Offers/search", headers=headers, json=payload)
        offers = response.json().get('result')
        for offer in offers:
            the_offer={}
            pays = offer.get('countryNameEn')
            if pays not in offers_details:
                offers_details[pays] = []
                
            the_offer['company'] = offer.get('organizationName')
            the_offer['mission'] = offer.get('missionTitle')
            the_offer['location'] = offer.get('cityNameEn')
            the_offer['duration'] = offer.get('missionDuration')
            the_offer['contact'] = offer.get('contactEmail')
            the_offer['link'] = offer.get('contactURL')
            offers_details[pays].append(the_offer)
        return offers_details
    # Return the product details dictionary
    except Exception as e:
        print('Could not fetch product details')
        print(f'Failed with exception: {e}')
        return None