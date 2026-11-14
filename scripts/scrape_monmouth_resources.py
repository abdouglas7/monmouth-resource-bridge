import json
import os
import datetime

def get_foundational_resources():
    """Consolidated master list organized strictly under streamlined categories with clean labels and zero duplicates."""
    return [
        # ==========================================
        # TEST BATCH ENTRIES
        # ==========================================
        {
            "id": "test-batch-01",
            "category": "Basic Needs & Assistance",
            "name": "Monmouth Test Resource Alpha",
            "location": "Eatontown, NJ",
            "description": "Batch verification test entry one.",
            "website": "",
            "phone": "732-555-0111",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-02",
            "category": "Health & Wellness",
            "name": "Monmouth Test Resource Beta",
            "location": "Red Bank, NJ",
            "description": "Batch verification test entry two.",
            "website": "",
            "phone": "732-555-0222",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-03",
            "category": "Employment & Training",
            "name": "Monmouth Test Resource Gamma",
            "location": "Long Branch, NJ",
            "description": "Batch verification test entry three.",
            "website": "",
            "phone": "732-555-0333",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-04",
            "category": "Youth & Family Services",
            "name": "Monmouth Test Resource Delta",
            "location": "Asbury Park, NJ",
            "description": "Batch verification test entry four.",
            "website": "",
            "phone": "732-555-0444",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-05",
            "category": "Housing & Utilities",
            "name": "Monmouth Test Resource Epsilon",
            "location": "Freehold, NJ",
            "description": "Batch verification test entry five.",
            "website": "",
            "phone": "732-555-0555",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        # ==========================================
        # 1. BASIC NEEDS & ASSISTANCE
        # ==========================================
        {
            "id": "fn-01",
            "category": "Basic Needs & Assistance",
            "name": "FoodBank of Monmouth and Ocean Counties",
            "location": "Neptune, NJ",
            "description": "Distributes food and essentials through a network of partner pantries and programs.",
            "website": "https://foodbankmoc.org",
            "phone": "732-918-2600",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": "2026-11-14"
        },
        {
            "id": "fn-02",
            "category": "Basic Needs & Assistance",
            "name": "St. Vincent de Paul Society (Monmouth County)",
            "location": "Various Locations, NJ",
            "description": "Emergency assistance with food, utilities, clothing, and rent.",
            "website": "",
            "phone": "732-747-4180",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": "2026-11-14"
        },
        # ==========================================
        # 2. EMPLOYMENT & TRAINING
        # ==========================================
        {
            "id": "et-01",
            "category": "Employment & Training",
            "name": "Monmouth County Division of Workforce Development",
            "location": "Neptune, NJ",
            "description": "Job seeker services, career counseling, resume workshops, and training grants.",
            "website": "https://www.visitmonmouth.com",
            "phone": "732-683-8850",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": "2026-11-14"
        },
        {
            "id": "et-02",
            "category": "Employment & Training",
            "name": "Brookdale Community College Workforce Development",
            "location": "Lincroft, NJ",
            "description": "Certification courses, professional training programs, and career credentials.",
            "website": "https://www.brookdalecc.edu",
            "phone": "732-224-2315",
            "email": "",
            "cost_label": "Varies",
            "nj_access": "Monmouth County",
            "last_verified": "2026-11-14"
        }
    ]

def load_existing_resources(filepath="data/resources.json"):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_resources(resources, filepath="data/resources.json"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)

def main():
    print("Starting Monmouth Resource scraping and merge process...")
    foundational = get_foundational_resources()
    existing = load_existing_resources()

    existing_ids = {r.get("id") for r in existing if r.get("id")}
    
    added_count = 0
    merged_list = list(existing)

    for item in foundational:
        if item.get("id") not in existing_ids:
            merged_list.append(item)
            existing_ids.add(item.get("id"))
            added_count += 1

    save_resources(merged_list)
    print(f"Sync complete! Added {added_count} new resources. Total records: {len(merged_list)}")

if __name__ == "__main__":
    main()
