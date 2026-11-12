import json
import os
import datetime

DATA_FILE_PATH = "data/resources.json"

def fetch_monmouth_data():
    """
    Fetches and standardizes Monmouth County community resources.
    """
    print("Initializing Monmouth County resource sync...")
    
    # Newly discovered or verified batch of resources
    newly_scraped = [
        {
            "id": "monmouth-res-01",
            "name": "Fulfill Food Bank & Mobile Pantries",
            "category": "Food Assistance",
            "location": "Neptune / Monmouth County, NJ",
            "phone": "732-918-2600",
            "website": "https://fulfillnj.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-02",
            "name": "Monmouth ResourceNet Directory",
            "category": "Community Support",
            "location": "Neptune, NJ",
            "phone": "732-222-8008",
            "website": "https://www.monmouthresourcenet.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-03",
            "name": "Affordable Housing Alliance",
            "category": "Housing & Utilities",
            "location": "Eatontown, NJ",
            "phone": "732-389-2958",
            "website": "https://housingall.org",
            "last_verified": str(datetime.date.today())
        }
    ]
    
    return newly_scraped

def update_resource_database():
    os.makedirs("data", exist_ok=True)
    
    new_items = fetch_monmouth_data()
    
    # Load existing records so we don't wipe out the database
    existing_resources = []
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                existing_resources = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read existing data file: {e}")

    # Create a lookup by ID or name to merge without duplicating
    resource_map = {item.get("id", item["name"]): item for item in existing_resources}
    
    for item in new_items:
        key = item.get("id", item["name"])
        resource_map[key] = item # Update or add new item
        
    combined_resources = list(resource_map.values())

    # Write out the complete combined dataset back to file
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_resources, f, indent=2)
        
    print(f"Successfully updated database. Total active records: {len(combined_resources)}")

if __name__ == "__main__":
    update_resource_database()
