import requests
import base64
import pandas as pd
from datetime import datetime

API_KEY = "your_api_key_here"   # paste your key here
API_URL = "https://my-api.plantnet.org/v2/identify/all"

# ── Encode image to base64 ────────────────────────
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()   # plantnet takes raw bytes

# ── Call Pl@ntNet API ─────────────────────────────
def detect_disease(image_path):
    print("\n🌿 Analyzing crop image...\n")

    image_data = encode_image(image_path)

    response = requests.post(
        API_URL,
        params = {"api-key": API_KEY, "include-related-images": "false"},
        files  = {"images": (image_path, image_data, "image/jpeg")},
        data   = {"organs": ["leaf"]}
    )

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            top = results[0]
            return {
                "plant_name" : top["species"]["commonNames"][0]
                               if top["species"]["commonNames"]
                               else top["species"]["scientificName"],
                "scientific" : top["species"]["scientificName"],
                "confidence" : round(top["score"] * 100, 2),
                "family"     : top["species"]["family"]["scientificName"],
            }
    print("❌ Error:", response.status_code)
    return None

# ── Save result to CSV ────────────────────────────
def save_result(image_path, result):
    record = {
        "timestamp"  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image"      : image_path,
        "plant_name" : result["plant_name"],
        "scientific" : result["scientific"],
        "confidence" : result["confidence"],
        "family"     : result["family"],
        "status"     : "Healthy" if result["confidence"] > 70
                       else "Needs Attention"
    }

    try:
        df = pd.read_csv("crop_results.csv")
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([record])

    df.to_csv("crop_results.csv", index=False)
    print("✅ Saved to crop_results.csv")
    return df