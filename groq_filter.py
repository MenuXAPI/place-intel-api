import json
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.1-8b-instant"


def enrich_business_data(business: dict) -> dict:
      prompt = f"""You are a business data assistant. Given the following raw business data from Google Places, return a clean JSON object with:
      1. "summary": A 2-3 sentence professional description of the business suitable for a website about section.
      2. "category": A single clean category label (e.g. "Italian Restaurant", "Coffee Shop", "Hair Salon").
      3. "highlights": A list of 3-5 short highlights about the business (e.g. "Family-owned since 1990", "Outdoor seating available").
      4. "photo_count": The number of photos available.

      Business data:
      {json.dumps(business, indent=2)}

      Respond with only valid JSON. No markdown, no explanation."""

    response = client.chat.completions.create(
              model=MODEL,
              messages=[{"role": "user", "content": prompt}],
              temperature=0.3,
              max_tokens=500,
    )

    raw = response.choices[0].message.content.strip()

    try:
              enriched = json.loads(raw)
except json.JSONDecodeError:
          enriched = {
                        "summary": None,
                        "category": None,
                        "highlights": [],
                        "photo_count": len(business.get("photos", [])),
          }

    enriched["photo_count"] = len(business.get("photos", []))
    return enriched
