import json
import os
import datetime
import urllib.request
import urllib.error
from html.parser import HTMLParser

DATA_FILE_PATH = "data/resources.json"

class SimpleHTMLTableParser(HTMLParser):
    """Lightweight HTML parser to extract directory details without heavy external dependencies."""
    def __init__(self):
        super().__init__()
        self.listings = []
        self.in_row = False
        self.current_cells = []
        self.current_cell_data = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.in_row = True
            self.current_cells = []
        elif tag in ['td', 'th']:
            self.current_cell_data = ""

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.current_cells:
                self.listings.append(self.current_cells)
            self.in_row = False
        elif tag in ['td', 'th']:
            self.current_cells.append(self.current_cell_data.strip())

    def handle_data(self, data):
        if self.in_row:
            self.current_cell_data += data

def fetch_live_directory_feeds():
    """
    Pulls live entries from structured community indexes across Monmouth County.
    """
    scraped_items = []
    
    # Target URL endpoint representing regional directory info
    target_url = "https://workinmonmouth.com/monmouth-county-pantries-and-soup-kitchens/"
    
    req = urllib.request.Request(
        target_url, 
        headers={'User-Agent': 'MonmouthResourceBridge-Bot/1.0'}
    )
    
    try:
        print(f"Fetching live resource feeds from: {target_url}")
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            parser = SimpleHTMLTableParser()
            parser.feed(html_content)
            
            # Parse directory table rows (Agency, Address, City, Phone Number, Hours)
            for idx, row in enumerate(parser.listings[1:], start=100):
                if len(row) >= 4:
                    name = row[0]
                    address = row[1]
                    city = row[2] if len(row) > 2 else "Monmouth County, NJ"
                    phone = row[3] if len(row) > 3 and "-" in row[3] else "Contact via Directory"
                    
                    if name and len(name) > 2:
                        resource_id = f"auto-scraped-{idx}"
                        scraped_items.append({
                            "id": resource_id,
                            "name": name,
                            "category": "Food Assistance & Emergency Relief",
                            "location": f"{address}, {city}, NJ",
                            "phone": phone,
                            "website": target_url,
                            "last_verified": str(datetime.date.today())
                        })
        print(f"Successfully extracted {len(scraped_items)} records from live feeds.")
    except Exception as e:
        print(f"Notice: Live feed sync encountered a network condition, relying on base safety net: {e}")
        
    return scraped_items

def get_foundational_resources():
    """Core baseline verified directory records."""
    return [
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

def update_resource_database():
    os.makedirs("data", exist_ok=True)
    
    # Gather base + freshly scraped live items
    foundational = get_foundational_resources()
    live_scraped = fetch_live_directory_feeds()
    all_new_batch = foundational + live_scraped
    
    # Load existing records so historical entries are safely preserved
    existing_resources = []
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                existing_resources = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read existing data file: {e}")

    # Build unique lookup map to merge records seamlessly without duplicates
    resource_map = {}
    for item in existing_resources:
        key = item.get("id", item.get("name"))
        resource_map[key] = item
        
    for item in all_new_batch:
        key = item.get("id", item.get("name"))
        resource_map[key] = item # Updates existing fields or appends new ones dynamically
        
    combined_resources = list(resource_map.values())

    # Save output dataset
    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_resources, f, indent=2)
        
    print(f"Database sync complete. Total active records managed: {len(combined_resources)}")

if __name__ == "__main__":
    update_resource_database()
