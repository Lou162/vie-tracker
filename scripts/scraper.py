import requests
from datetime import datetime

def scrape_offers():
    payload = {
        "limit": 100,
        "skip": 0,
        "query": None,
        "specializationsIds": ["24"],
        "missionsTypesIds": ["VIE"],
        "countriesIds": ["CA", "BE"],
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

    # Get the product page content and create a sou

    try:
        # Scrape the product details
        response = requests.post("https://civiweb-api-prd.azurewebsites.net/api/Offers/search", headers=headers, json=payload)
        offers = response.json().get('result')
        offers_details, others_offer = getMostRecentOffers(offers)
        return getOffersByCountry(offers_details, others_offer)
        
    # Return the product details dictionary
    except Exception as e:
        print('Could not fetch product details')
        print(f'Failed with exception: {e}')
        return None
    
def getMostRecentOffers(offers):
    others_offer=[]
    max_date = max(datetime.fromisoformat(offer["creationDate"]).date() for offer in offers)
    offers_details = {}
    for offer in offers:
        the_offer={}
        if datetime.fromisoformat(offer.get('creationDate')).date() == max_date:
            the_offer['company'] = offer.get('organizationName')
            the_offer['mission'] = offer.get('missionTitle')
            the_offer['location'] = offer.get('cityNameEn')
            the_offer['duration'] = offer.get('missionDuration')
            the_offer['contact'] = transformContactEmailToLink(offer.get('contactEmail'), False)
            the_offer['country'] = offer.get('countryNameEn')
            the_offer['link'] = transformContactEmailToLink(offer.get('contactURL'), True)
            if '🏆most Recent 🏆' not in offers_details:
                offers_details['🏆most Recent 🏆'] = []
            offers_details['🏆most Recent 🏆'].append(the_offer)
        else:
            others_offer.append(offer)
    return offers_details, others_offer

def transformContactEmailToLink(link, isLink=False):
    if(link == ""):
        return "N/A"
    elif(isLink):
        return f"[Lien]({link})"
    else:
        return f"[{link}]({link})"

def getOffersByCountry(offers_details, offers):
    for offer in offers:
        the_offer={}
        if offer.get('countryNameEn') not in offers_details:
            offers_details[offer.get('countryNameEn')] = []
            
        the_offer['company'] = offer.get('organizationName')
        the_offer['mission'] = offer.get('missionTitle')
        the_offer['location'] = offer.get('cityNameEn')
        the_offer['duration'] = offer.get('missionDuration')
        the_offer['contact'] = transformContactEmailToLink(offer.get('contactEmail'), False)
        the_offer['link'] = transformContactEmailToLink(offer.get('contactURL'), True)
        offers_details[offer.get('countryNameEn')].append(the_offer)
    return offers_details