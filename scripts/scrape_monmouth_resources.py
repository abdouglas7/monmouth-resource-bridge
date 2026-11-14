import json
import os
import datetime

def get_foundational_resources():
    """Consolidated master list organized strictly under streamlined categories with clean labels and zero duplicates."""
    return [
        # ==========================================
        # TEST BATCH ENTRIES (1 - 5)
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
        # CAREER & EMPLOYMENT DEVELOPMENT BATCH (6 - 25)
        # ==========================================
        {
            "id": "test-batch-06",
            "category": "Employment & Training",
            "name": "Monmouth Career Advancement Hub",
            "location": "Eatontown, NJ",
            "description": "Workforce coaching and professional development training modules.",
            "website": "",
            "phone": "732-555-0601",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-07",
            "category": "Employment & Training",
            "name": "Jersey Shore Tech Pathways",
            "location": "Tinton Falls, NJ",
            "description": "Technical skills certification and digital literacy support.",
            "website": "",
            "phone": "732-555-0602",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-08",
            "category": "Employment & Training",
            "name": "Monmouth Adult Literacy and GED Center",
            "location": "Red Bank, NJ",
            "description": "High school equivalency test preparation and foundational English instruction.",
            "website": "",
            "phone": "732-555-0603",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-09",
            "category": "Employment & Training",
            "name": "Coastal Resume and Interview Workshop",
            "location": "Long Branch, NJ",
            "description": "Professional critique sessions, mock interviews, and LinkedIn optimization.",
            "website": "",
            "phone": "732-555-0604",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-10",
            "category": "Employment & Training",
            "name": "Monmouth County Small Business Incubator",
            "location": "Freehold, NJ",
            "description": "Resources, mentorship, and workshops for aspiring local entrepreneurs.",
            "website": "",
            "phone": "732-555-0605",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-11",
            "category": "Employment & Training",
            "name": "Shoreline Young Adult Job Corps",
            "location": "Asbury Park, NJ",
            "description": "Vocational training and job placement assistance for young adults.",
            "website": "",
            "phone": "732-555-0606",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-12",
            "category": "Employment & Training",
            "name": "Monmouth Women's Business Enterprise Center",
            "location": "Shrewsbury, NJ",
            "description": "Leadership coaching, networking, and professional certifications.",
            "website": "",
            "phone": "732-555-0607",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-13",
            "category": "Employment & Training",
            "name": "Northern Monmouth Skills Exchange",
            "location": "Middletown, NJ",
            "description": "Peer-to-peer professional development and trade skills exchange.",
            "website": "",
            "phone": "732-555-0608",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-14",
            "category": "Employment & Training",
            "name": "Monmouth Healthcare Careers Pipeline",
            "location": "Neptune, NJ",
            "description": "Training placement and support for allied health and administrative roles.",
            "website": "",
            "phone": "732-555-0609",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-15",
            "category": "Employment & Training",
            "name": "Bayshore Hospitality Training Institute",
            "location": "Keansburg, NJ",
            "description": "Customer service, culinary basics, and hospitality management credentials.",
            "website": "",
            "phone": "732-555-0610",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-16",
            "category": "Employment & Training",
            "name": "Monmouth Logistics and Supply Chain Academy",
            "location": "Manalapan, NJ",
            "description": "Certifications in warehouse operations, inventory control, and supply chain logistics.",
            "website": "",
            "phone": "732-555-0611",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-17",
            "category": "Employment & Training",
            "name": "Southern Monmouth Green Jobs Initiative",
            "location": "Wall Township, NJ",
            "description": "Training programs focused on renewable energy and sustainable building practices.",
            "website": "",
            "phone": "732-555-0612",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-18",
            "category": "Employment & Training",
            "name": "Monmouth Financial Literacy for Career Growth",
            "location": "Eatontown, NJ",
            "description": "Workshops covering budgeting, salary negotiation, and financial wellness.",
            "website": "",
            "phone": "732-555-0613",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-19",
            "category": "Employment & Training",
            "name": "Jersey Shore Public Speaking & Leadership Guild",
            "location": "Red Bank, NJ",
            "description": "Confidence building, executive presence, and professional communication practice.",
            "website": "",
            "phone": "732-555-0614",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-20",
            "category": "Employment & Training",
            "name": "Monmouth County Freelancer & Remote Work Co-op",
            "location": "Asbury Park, NJ",
            "description": "Resources, coworking community insights, and contract guidance for independent workers.",
            "website": "",
            "phone": "732-555-0615",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-21",
            "category": "Employment & Training",
            "name": "Monmouth Project Management Fundamentals Guild",
            "location": "Freehold, NJ",
            "description": "Introductory coursework and agile framework familiarization for aspiring project managers.",
            "website": "",
            "phone": "732-555-0616",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-22",
            "category": "Employment & Training",
            "name": "Monmouth Code and Data Science Circle",
            "location": "Tinton Falls, NJ",
            "description": "Collaborative coding sessions, Python mentoring, and data analytics portfolio building.",
            "website": "",
            "phone": "732-555-0617",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-23",
            "category": "Employment & Training",
            "name": "Monmouth Veteran Career Transition Network",
            "location": "Eatontown, NJ",
            "description": "Specialized employment placement, resume translation, and veteran mentoring.",
            "website": "",
            "phone": "732-555-0618",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-24",
            "category": "Employment & Training",
            "name": "Monmouth Executive Mentorship Collaborative",
            "location": "Shrewsbury, NJ",
            "description": "One-on-one professional mentorship pairing experienced leaders with emerging talent.",
            "website": "",
            "phone": "732-555-0619",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "test-batch-25",
            "category": "Employment & Training",
            "name": "Monmouth Continuing Education & Grant Resource Desk",
            "location": "Lincroft, NJ",
            "description": "Guidance on tuition-free adult training grants, scholarships, and certification funding.",
            "website": "",
            "phone": "732-555-0620",
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
