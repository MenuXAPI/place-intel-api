from flask import Flask, request, jsonify
from flask_cors import CORS
from extract_business import get_business_details
from groq_filter import enrich_business_data

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "place-intel-api"}), 200


@app.route("/business", methods=["POST"])
def get_business():
    data = request.get_json()

    if not data or "place_id" not in data:
        return jsonify({"error": "Missing required field: place_id"}), 400

    place_id = data["place_id"].strip()
    if not place_id:
        return jsonify({"error": "place_id cannot be empty"}), 400

    try:
        business = get_business_details(place_id)
        enriched = enrich_business_data(business)
        return jsonify({
            "place_id": place_id,
            "business": business,
            "ai": enriched,
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
