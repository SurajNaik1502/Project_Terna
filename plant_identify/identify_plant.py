import json
import requests  
import wikipediaapi  
from rapidfuzz import process  # ✅ Import fuzzy matching

# 🌱 Load Plant Data
with open("plant_data.json", "r") as file:
    plant_info = json.load(file)

# 🌱 Step 1: Identify Plant using PlantNet API
API_KEY = "2b10ajuSO2cj0uKUvqf5iM4eu"
IMAGE_PATH = "rose_leaf.jpg"  
url = "https://my-api.plantnet.org/v2/identify/all"

files = {"images": open(IMAGE_PATH, "rb")}
params = {"api-key": API_KEY}
response = requests.post(url, files=files, params=params)
plant_data = response.json()

if "results" in plant_data and len(plant_data["results"]) > 0:
    best_match = plant_data["results"][0]  
    plant_name = best_match["species"]["scientificNameWithoutAuthor"]  # ✅ Dynamically update plant name
    common_names = ", ".join(best_match["species"].get("commonNames", ["No common names found"]))
    family = best_match["species"]["family"]["scientificNameWithoutAuthor"]
    score = best_match["score"]  

    print(f"🌿 Plant Name: {plant_name}")
    print(f"🪴 Common Names: {common_names}")
    print(f"🌱 Family: {family}")
    print(f"🔍 Confidence Score: {round(score * 100, 2)}%")
else:
    print("⚠️ Plant not recognized. Try another image.")
    exit()  # Stop script if plant is not recognized

# 🌱 Step 2: Fetch Additional Details from Wikipedia
def get_plant_details(plant_name):
    wiki = wikipediaapi.Wikipedia(user_agent="VirtualHerbalGardenBot/1.0 (your_email@example.com)", language='en')
    page = wiki.page(plant_name)  

    if page.exists():
        return page.summary[:500]  
    else:
        return "No additional details found."

# ✅ Get Wikipedia description
description = get_plant_details(plant_name)
print(f"📖 Description: {description}")

# 🌱 Step 3: Fetch Plant-Specific Details from Database (Improved Matching)
def get_closest_match(query, data_keys, threshold=70):
    """Finds the closest matching plant name in the dataset using fuzzy matching."""
    result = process.extractOne(query, data_keys, score_cutoff=threshold)  # ✅ Store result safely
    if result:  
        match, score, _ = result  # ✅ Unpack only if result is not None
        return match
    return None  # ✅ Return None if no match is found

# ✅ Find the closest match
matching_plant = get_closest_match(plant_name, plant_info.keys())

# ✅ Get details from the database if a match is found
if matching_plant:
    lifespan = plant_info[matching_plant].get("lifespan", "No lifespan info found")
    soil = plant_info[matching_plant].get("soil", "No soil info found")
    benefits = plant_info[matching_plant].get("benefits", "No medicinal benefits found")
else:
    lifespan = "No lifespan info found"
    soil = "No soil info found"
    benefits = "No medicinal benefits found"

# 🖥️ Display everything nicely
print(f"⏳ Lifespan: {lifespan}")
print(f"🌍 Soil Type: {soil}")
print(f"💊 Medicinal Benefits: {benefits}")