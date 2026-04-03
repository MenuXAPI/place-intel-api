import requests
from config import GOOGLE_PLACES_API_KEY

PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PLACES_PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo"

FIELDS = [
    "name",
    "formatted_address",
    "formatted_phone_number",
    "website",
    "opening_hours",
    "rating",
    "price_level",
    "types",
    "photos",
    "editorial_summary",
]


def get_business_details(place_id: str) -> dict:
    params = {
        "place_id": place_id,
        "fields": ",".join(FIELDS),
        "key": GOOGLE_PLACES_API_KEY,
    }
    response = requests.get(PLACES_DETAILS_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        raise ValueError(f"Places API error: {data.get('status')} - {data.get('error_message', '')}")

    result = data["result"]

    photos = []
    for photo in result.get("photos", [])[:10]:
        photo_ref = photo.get("photo_reference")
        if photo_ref:
            photo_url = (
                f"{PLACES_PHOTO_URL}"
                f"?maxwidth=1200&photo_reference={photo_ref}&key={GOOGLE_PLACES_API_KEY}"
            )
            photos.append(photo_url)

    hours = None
    if result.get("opening_hours"):
        hours = result["opening_hours"].get("weekday_text", [])

    return {
        "name": result.get("name"),
        "address": result.get("formatted_address"),
        "phone": result.get("formatted_phone_number"),
        "website": result.get("website"),
        "hours": hours,
        "rating": result.get("rating"),
        "price_level": result.get("price_level"),
        "types": result.get("types", []),
        "editorial_summary": result.get("editorial_summary", {}).get("overview"),
        "photos": photos,
    }
