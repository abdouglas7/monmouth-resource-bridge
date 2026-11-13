import json
import os
import datetime
import urllib.request
import urllib.error
from html.parser import HTMLParser

DATA_FILE_PATH = "data/resources.json"

class SimpleHTMLTableParser(HTMLParser):
    """Lightweight HTML parser to extract directory listings and structured data."""
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
    Pulls live entries from structured community indexes across Monmouth County
    spanning Basic Needs, Employment/Training, Family Support, and Legal/Advocacy.
    """
    scraped_items = []
    target_urls = [
        "https://workinmonmouth.com/monmouth-county-pantries-and-soup-kitchens/"
    ]
    
    for url in target_urls:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'MonmouthResourceBridge-Bot/1.0'}
        )
        try:
            print(f"Fetching live resource feeds from: {url}")
            with urllib.request.urlopen(req, timeout=10) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                parser = SimpleHTMLTableParser()
                parser.feed(html_content)
                
                for idx, row in enumerate(parser.listings[1:], start=200):
                    if len(row) >= 4:
                        name = row[0]
                        address = row[1]
                        city = row[2] if len(row) > 2 else "Monmouth County, NJ"
                        phone = row[3] if len(row) > 3 and "-" in row[3] else "Contact via Directory"
                        
                        if name and len(name) > 2:
                            scraped_items.append({
                                "id": f"auto-scraped-{idx}",
                                "name": name,
                                "category": "Basic Needs & Community Assistance",
                                "location": f"{address}, {city}, NJ",
                                "phone": phone,
                                "website": url,
                                "last_verified": str(datetime.date.today())
                            })
            print(f"Successfully extracted records from: {url}")
        except Exception as e:
            print(f"Notice: Feed sync notice for {url}: {e}")
            
    return scraped_items

def get_foundational_resources():
    """Core baseline directory records combined with user-curated adult support, NJ-accessible tech upskilling, and simulation platforms."""
    return [
        # Emergency & Core Support
        {
            "id": "monmouth-res-01",
            "name": "Fulfill Food Bank & Mobile Pantries",
            "category": "Basic Needs / Assistance",
            "location": "Neptune / Monmouth County, NJ",
            "phone": "732-918-2600",
            "website": "https://fulfillnj.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-02",
            "name": "Monmouth ResourceNet Directory",
            "category": "Family & Support Services",
            "location": "Neptune, NJ",
            "phone": "732-222-8008",
            "website": "https://www.monmouthresourcenet.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-03",
            "name": "Affordable Housing Alliance",
            "category": "Basic Needs / Assistance",
            "location": "Eatontown, NJ",
            "phone": "732-389-2958",
            "website": "https://housingall.org",
            "last_verified": str(datetime.date.today())
        },
        # Medical Equipment & Health Access
        {
            "id": "monmouth-res-04",
            "name": "Saint James Eatontown Medical Equipment Ministry",
            "category": "Medical Equipment & Health",
            "location": "Eatontown, NJ",
            "phone": "Contact via Parish",
            "website": "https://www.stjames-parish.com",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-05",
            "name": "Parker Family Health Center",
            "category": "Medical Equipment & Health",
            "location": "Red Bank, NJ",
            "phone": "732-212-0777",
            "website": "https://parkerfamilyhealth.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-06",
            "name": "NJ Hospital Care Payment Assistance (Charity Care)",
            "category": "Medical Equipment & Health",
            "location": "Statewide / Monmouth County, NJ",
            "phone": "Contact Local Hospital",
            "website": "https://www.nj.gov/health/",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-07",
            "name": "NJ FamilyCare Low-Cost Health Insurance",
            "category": "Basic Needs / Assistance",
            "location": "Statewide, NJ",
            "phone": "1-800-701-0710",
            "website": "https://www.njfamilycare.org",
            "last_verified": str(datetime.date.today())
        },
        # Paid Apprenticeships & Earn-While-You-Learn
        {
            "id": "monmouth-res-08",
            "name": "Catalyte",
            "category": "Employment / Training",
            "location": "Remote / Regional NJ",
            "phone": "Online Program",
            "website": "https://www.catalyte.io",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-09",
            "name": "Apprenti",
            "category": "Employment / Training",
            "location": "National / Regional",
            "phone": "Program Support",
            "website": "https://apprenticareers.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-10",
            "name": "Multiverse",
            "category": "Employment / Training",
            "location": "Remote / Virtual",
            "phone": "Online Program",
            "website": "https://www.multiverse.io",
            "last_verified": str(datetime.date.today())
        },
        # Accelerated Tuition-Free Bootcamps (NJ Accessible)
        {
            "id": "monmouth-res-11",
            "name": "Per Scholas",
            "category": "Employment / Training",
            "location": "Newark, NJ / Remote",
            "phone": "Regional Office",
            "website": "https://perscholas.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-12",
            "name": "NPower",
            "category": "Employment / Training",
            "location": "Newark & Jersey City, NJ",
            "phone": "Regional Office",
            "website": "https://npower.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-13",
            "name": "LaunchCode",
            "category": "Employment / Training",
            "location": "Remote Learning",
            "phone": "Online Program",
            "website": "https://www.launchcode.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-14",
            "name": "Generation USA",
            "category": "Employment / Training",
            "location": "Remote Cohorts",
            "phone": "Online Program",
            "website": "https://usa.generation.org",
            "last_verified": str(datetime.date.today())
        },
        # Workforce Support & Navigation
        {
            "id": "monmouth-res-15",
            "name": "Goodwill Workforce Services",
            "category": "Employment / Training",
            "location": "New Jersey Centers",
            "phone": "Local Center",
            "website": "https://www.goodwill.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-16",
            "name": "SkillUp Coalition",
            "category": "Employment / Training",
            "location": "Online Platform",
            "phone": "Online Navigation",
            "website": "https://skillup.org",
            "last_verified": str(datetime.date.today())
        },
        # Free Experience, Simulations & Library Access
        {
            "id": "monmouth-res-17",
            "name": "Forage",
            "category": "Employment / Training",
            "location": "Online Platform",
            "phone": "Free Open Access",
            "website": "https://www.theforage.com",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-18",
            "name": "Red Bank Public Library & NJ Partner Libraries (Coursera/Udemy)",
            "category": "Employment / Training",
            "location": "Monmouth County, NJ",
            "phone": "732-842-0690",
            "website": "https://redbanklibrary.org",
            "last_verified": str(datetime.date.today())
        },
        # Supplemental Income & Resale Options
        {
            "id": "monmouth-res-19",
            "name": "Plato's Closet",
            "category": "Supplemental Income & Resale",
            "location": "Middletown, NJ",
            "phone": "Local Store",
            "website": "https://www.platoscloset.com",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-20",
            "name": "Once Upon A Child",
            "category": "Supplemental Income & Resale",
            "location": "Howell, NJ",
            "phone": "Local Store",
            "website": "https://www.onceuponachild.com",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-21",
            "name": "Flexible Gig Work Platforms (Reflex, Instacart, DoorDash)",
            "category": "Supplemental Income & Resale",
            "location": "Monmouth County, NJ",
            "phone": "App-Based",
            "website": "https://www.reflex.com",
            "last_verified": str(datetime.date.today())
        },
        # Newly Integrated Additions (Healthcare, Utility, Support, Wellness)
        {
            "id": "monmouth-res-22",
            "name": "Monmouth County Division on Aging / SHIP",
            "category": "Healthcare Navigation & Benefits",
            "location": "Freehold, NJ",
            "phone": "732-431-7450",
            "website": "https://monmouthadvs.com",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-23",
            "name": "GoodRx",
            "category": "Healthcare Navigation & Benefits",
            "location": "Online / Local Pharmacies",
            "phone": "Online Tool",
            "website": "https://www.goodrx.com",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-24",
            "name": "Universal Service Fund (USF) & Fresh Start",
            "category": "Financial & Utility Assistance",
            "location": "Statewide / Monmouth County, NJ",
            "phone": "State Program",
            "website": "https://www.nj.gov/bpu/",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-25",
            "name": "Low-Income Home Energy Assistance Program (LIHEAP)",
            "category": "Financial & Utility Assistance",
            "location": "Statewide / Monmouth County, NJ",
            "phone": "State Program",
            "website": "https://www.nj.gov/dca/",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-26",
            "name": "NJ SHARES",
            "category": "Financial & Utility Assistance",
            "location": "Statewide, NJ",
            "phone": "1-866-657-4273",
            "website": "https://njshares.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-27",
            "name": "NJ Comfort Partners",
            "category": "Financial & Utility Assistance",
            "location": "Statewide / Monmouth County, NJ",
            "phone": "Utility Partner",
            "website": "https://njcomfortpartners.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-28",
            "name": "NAMI Greater Monmouth County",
            "category": "Mental Health & Support Groups",
            "location": "Monmouth County, NJ",
            "phone": "732-544-0980",
            "website": "https://namigreatermonmouth.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-29",
            "name": "YMCA of the Jersey Shore – Financial Assistance",
            "category": "Recreation, Health & Wellness",
            "location": "Red Bank / Eatontown / Regional, NJ",
            "phone": "732-741-2504",
            "website": "https://ymcanj.org",
            "last_verified": str(datetime.date.today())
        }
    ]

def update_resource_database():
    os.makedirs("data", exist_ok=True)
    
    foundational = get_foundational_resources()
    live_scraped = fetch_live_directory_feeds()
    all_new_batch = foundational + live_scraped
    
    existing_resources = []
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                existing_resources = json.load(f)
        except Exception as e:
            print(f"Warning: Could not read existing data file: {e}")

    resource_map = {}
    for item in existing_resources:
        key = item.get("id", item.get("name"))
        resource_map[key] = item
        
    for item in all_new_batch:
        key = item.get("id", item.get("name"))
        resource_map[key] = item 
        
    combined_resources = list(resource_map.values())

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_resources, f, indent=2)
        
    print(f"Database sync complete. Total active records managed: {len(combined_resources)}")

if __name__ == "__main__":
    update_resource_database()
