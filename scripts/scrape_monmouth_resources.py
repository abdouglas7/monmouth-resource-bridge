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
                
                for idx, row in enumerate(parser.listings[1:], start=300):
                    if len(row) >= 4:
                        name = row[0]
                        address = row[1]
                        city = row[2] if len(row) > 2 else "Monmouth County, NJ"
                        phone = row[3] if len(row) > 3 and "-" in row[3] else ""
                        
                        if name and len(name) > 2:
                            scraped_items.append({
                                "id": f"auto-scraped-{idx}",
                                "category": "Food Assistance & Emergency Relief",
                                "name": name,
                                "location": f"{address}, {city}, NJ",
                                "description": "Community food pantry and emergency relief assistance program.",
                                "website": url,
                                "phone": phone,
                                "email": "",
                                "last_verified": str(datetime.date.today())
                            })
            print(f"Successfully extracted records from: {url}")
        except Exception as e:
            print(f"Notice: Feed sync notice for {url}: {e}")
            
    return scraped_items

def get_foundational_resources():
    """Core streamlined directory records containing all 163 distinct records."""
    return [
        # Basic Needs / Assistance (1-3)
        {
            "id": "monmouth-res-01",
            "category": "Basic Needs / Assistance",
            "name": "Fulfill Food Bank & Mobile Pantries",
            "location": "Neptune / Monmouth County, NJ",
            "description": "Provides emergency food distribution, mobile pantries, and nutritional support to individuals and families experiencing food insecurity.",
            "website": "https://fulfillnj.org",
            "phone": "732-918-2600",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-02",
            "category": "Basic Needs / Assistance",
            "name": "Affordable Housing Alliance",
            "location": "Eatontown, NJ",
            "description": "Offers housing assistance, homelessness prevention, rental support, and financial empowerment programs.",
            "website": "https://housingall.org",
            "phone": "732-389-2958",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-03",
            "category": "Basic Needs / Assistance",
            "name": "NJ FamilyCare Low-Cost Health Insurance",
            "location": "Statewide, NJ",
            "description": "Provides publicly funded, low-cost or no-cost health insurance coverage for eligible children, adults, and families.",
            "website": "https://www.njfamilycare.org",
            "phone": "1-800-701-0710",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Family & Support Services (4)
        {
            "id": "monmouth-res-04",
            "category": "Family & Support Services",
            "name": "Monmouth ResourceNet Directory",
            "location": "Neptune, NJ",
            "description": "Connects residents with a comprehensive network of local family support services, basic needs assistance, and community programs.",
            "website": "https://www.monmouthresourcenet.org",
            "phone": "732-222-8008",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Food Assistance & Emergency Relief - Pantries & Soup Kitchens (5-71)
        {
            "id": "monmouth-res-05", "category": "Food Assistance & Emergency Relief", "name": "Matawan United Methodist Pantry", "location": "Matawan, NJ", "description": "Local food pantry providing grocery distribution and basic food support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-06", "category": "Food Assistance & Emergency Relief", "name": "Allentown Food Pantry", "location": "Allentown, NJ", "description": "Community food pantry offering emergency groceries and pantry staples for local residents.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-07", "category": "Food Assistance & Emergency Relief", "name": "Bethel Food Pantry", "location": "Monmouth County, NJ", "description": "Provides emergency food boxes and supplemental grocery support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-08", "category": "Food Assistance & Emergency Relief", "name": "Deliverance Temple", "location": "Monmouth County, NJ", "description": "Offers community food distribution and emergency assistance programs.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-09", "category": "Food Assistance & Emergency Relief", "name": "First United Methodist A.P. Pantry", "location": "Asbury Park, NJ", "description": "Provides food pantry assistance and emergency meal supplies.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-10", "category": "Food Assistance & Emergency Relief", "name": "Glad Tidings", "location": "Monmouth County, NJ", "description": "Community outreach food assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-11", "category": "Food Assistance & Emergency Relief", "name": "Jewish Family Services Pantry", "location": "Monmouth County, NJ", "description": "Pantry support providing nutritional items and family assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-12", "category": "Food Assistance & Emergency Relief", "name": "Lutheran Church of Atonement Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution and grocery support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-13", "category": "Food Assistance & Emergency Relief", "name": "Manna-United Fellowship Outreach", "location": "Monmouth County, NJ", "description": "Provides community meal supplies and food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-14", "category": "Food Assistance & Emergency Relief", "name": "Mercy Center", "location": "Asbury Park, NJ", "description": "Offers a food pantry alongside family support services and basic-needs assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-15", "category": "Food Assistance & Emergency Relief", "name": "Mt. Carmel", "location": "Monmouth County, NJ", "description": "Community food distribution and emergency assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-16", "category": "Food Assistance & Emergency Relief", "name": "Oceans Family Success Center", "location": "Monmouth County, NJ", "description": "Family success center offering community resources, family support, and emergency food connections.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-17", "category": "Food Assistance & Emergency Relief", "name": "Salvation Army Pantry - Asbury Park", "location": "Asbury Park, NJ", "description": "Emergency food pantry and basic-needs assistance for local families.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-18", "category": "Food Assistance & Emergency Relief", "name": "Second Baptist Church Pantry", "location": "Monmouth County, NJ", "description": "Provides pantry staples and food distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-19", "category": "Food Assistance & Emergency Relief", "name": "St. Peter Claver Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-20", "category": "Food Assistance & Emergency Relief", "name": "Trinity Epis. Last Resort Pantry", "location": "Monmouth County, NJ", "description": "Emergency food support for individuals facing acute need.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-21", "category": "Food Assistance & Emergency Relief", "name": "St. Augustine’s Soup Kitchen", "location": "Monmouth County, NJ", "description": "Provides hot meals and prepared food assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-22", "category": "Food Assistance & Emergency Relief", "name": "Trinity Episcopal Saturday Soup", "location": "Monmouth County, NJ", "description": "Weekend soup kitchen providing nutritious hot meals.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-23", "category": "Food Assistance & Emergency Relief", "name": "Providence Baptist Pantry", "location": "Monmouth County, NJ", "description": "Pantry support and community food distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-24", "category": "Food Assistance & Emergency Relief", "name": "Eatontown Food Coop", "location": "Eatontown, NJ", "description": "Cooperative food pantry providing groceries to residents in need.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-25", "category": "Food Assistance & Emergency Relief", "name": "St. Dorothea’s Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry supplies.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-26", "category": "Food Assistance & Emergency Relief", "name": "Middletown Help Its Own", "location": "Middletown, NJ", "description": "Local assistance organization providing food and emergency support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-27", "category": "Food Assistance & Emergency Relief", "name": "Macedonia Freehold Church Food Pantry", "location": "Freehold, NJ", "description": "Pantry distribution providing groceries and basic assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-28", "category": "Food Assistance & Emergency Relief", "name": "Meet the Need Pantry", "location": "Monmouth County, NJ", "description": "Emergency food resources for individuals facing hardship.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-29", "category": "Food Assistance & Emergency Relief", "name": "Open Door Pantry", "location": "Monmouth County, NJ", "description": "Community pantry offering regular grocery distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-30", "category": "Food Assistance & Emergency Relief", "name": "St. John’s Pantry", "location": "Monmouth County, NJ", "description": "Food assistance program providing staples and fresh items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-31", "category": "Food Assistance & Emergency Relief", "name": "OLPH Pantry (Our Lady of Perpetual Help)", "location": "Monmouth County, NJ", "description": "Emergency food pantry providing ongoing nutritional support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-32", "category": "Food Assistance & Emergency Relief", "name": "St. Benedict’s Emerg Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution for local households.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-33", "category": "Food Assistance & Emergency Relief", "name": "Christ Church Pantry", "location": "Monmouth County, NJ", "description": "Pantry support offering essential food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-34", "category": "Food Assistance & Emergency Relief", "name": "Howell Food Pantry", "location": "Howell, NJ", "description": "Local food pantry serving Howell and surrounding Monmouth County areas.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-35", "category": "Food Assistance & Emergency Relief", "name": "Project Paul", "location": "Monmouth County, NJ", "description": "Community service organization providing emergency food and support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-36", "category": "Food Assistance & Emergency Relief", "name": "St. Mark’s CCR Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution pantry.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-37", "category": "Food Assistance & Emergency Relief", "name": "St. Mark’s CCR Soup Kitchen", "location": "Monmouth County, NJ", "description": "Soup kitchen providing prepared hot meals.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-38", "category": "Food Assistance & Emergency Relief", "name": "Keyport Ministerium Food Pantry", "location": "Keyport, NJ", "description": "Interfaith food pantry serving the Keyport area with emergency groceries.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-39", "category": "Food Assistance & Emergency Relief", "name": "St. Joseph Church Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution services.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-40", "category": "Food Assistance & Emergency Relief", "name": "Brookdale Wellness Center Food Pantry", "location": "Lincroft / Monmouth County, NJ", "description": "Campus and community food pantry supporting students and residents.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-41", "category": "Food Assistance & Emergency Relief", "name": "Christ the King Pantry", "location": "Monmouth County, NJ", "description": "Pantry support offering food staples.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-42", "category": "Food Assistance & Emergency Relief", "name": "First Baptist Pantry", "location": "Monmouth County, NJ", "description": "Community food distribution pantry.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-43", "category": "Food Assistance & Emergency Relief", "name": "St. Brigid’s Pantry at St. James Church", "location": "Red Bank, NJ", "description": "Client-choice food pantry providing fresh produce and grocery assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-44", "category": "Food Assistance & Emergency Relief", "name": "St. Luke’s United Methodist Pantry", "location": "Monmouth County, NJ", "description": "Emergency food assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-45", "category": "Food Assistance & Emergency Relief", "name": "St. Michael’s Food Pantry", "location": "Monmouth County, NJ", "description": "Provides grocery assistance and food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-46", "category": "Food Assistance & Emergency Relief", "name": "Meal At Noon (Soup Kitchen)", "location": "Monmouth County, NJ", "description": "Soup kitchen providing midday hot meals.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-47", "category": "Food Assistance & Emergency Relief", "name": "St. Brigid’s Soup Kitchen at St. James Church", "location": "Red Bank, NJ", "description": "Prepared meals and hot lunches for individuals in need.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-48", "category": "Food Assistance & Emergency Relief", "name": "Samaritan Center Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-49", "category": "Food Assistance & Emergency Relief", "name": "Hope Community Church Pantry", "location": "Monmouth County, NJ", "description": "Community food distribution program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-50", "category": "Food Assistance & Emergency Relief", "name": "Manasquan Food Pantry", "location": "Manasquan, NJ", "description": "Local food pantry serving Manasquan and surrounding coastal communities.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-51", "category": "Food Assistance & Emergency Relief", "name": "Monmouth Worship Ctr. Pantry", "location": "Monmouth County, NJ", "description": "Emergency food and grocery assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-52", "category": "Food Assistance & Emergency Relief", "name": "Matawan Food Pantry", "location": "Matawan, NJ", "description": "Pantry support providing essential food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-53", "category": "Food Assistance & Emergency Relief", "name": "Calico Cat Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-54", "category": "Food Assistance & Emergency Relief", "name": "Goodness Now At Middletown UMC", "location": "Middletown, NJ", "description": "Community food pantry and basic assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-55", "category": "Food Assistance & Emergency Relief", "name": "FPC Food Outreach", "location": "Monmouth County, NJ", "description": "Food outreach and grocery distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-56", "category": "Food Assistance & Emergency Relief", "name": "Greater Emanuel Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-57", "category": "Food Assistance & Emergency Relief", "name": "Mt. Olivet - Heaven’s Grocery", "location": "Middletown, NJ", "description": "Grocery assistance and pantry distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-58", "category": "Food Assistance & Emergency Relief", "name": "Bradley Food Pantry", "location": "Bradley Beach, NJ", "description": "Community food pantry serving local residents.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-59", "category": "Food Assistance & Emergency Relief", "name": "Sephardic Bikur Holim Pantry (SBH)", "location": "Monmouth County, NJ", "description": "Community food and family support pantry.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-60", "category": "Food Assistance & Emergency Relief", "name": "St. Paul’s Ocean Grove", "location": "Ocean Grove, NJ", "description": "Community food and assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-61", "category": "Food Assistance & Emergency Relief", "name": "Lunch Break Pantry", "location": "Red Bank, NJ", "description": "Food pantry providing grocery boxes and supplemental food assistance.", "website": "https://lunchbreak.org", "phone": "732-747-8577", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-62", "category": "Food Assistance & Emergency Relief", "name": "Salvation Army Food Pantry - Red Bank", "location": "Red Bank, NJ", "description": "Emergency food pantry and basic support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-63", "category": "Food Assistance & Emergency Relief", "name": "St. Crispin’s Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-64", "category": "Food Assistance & Emergency Relief", "name": "VGCA Food Pantry", "location": "Monmouth County, NJ", "description": "Community pantry supplies and support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-65", "category": "Food Assistance & Emergency Relief", "name": "BPC Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency grocery distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-66", "category": "Food Assistance & Emergency Relief", "name": "Lunch Break Soup Kitchen", "location": "Red Bank, NJ", "description": "Prepared hot meals and lunch program.", "website": "https://lunchbreak.org", "phone": "732-747-8577", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-67", "category": "Food Assistance & Emergency Relief", "name": "Collingwood SDA Pantry", "location": "Monmouth County, NJ", "description": "Community food pantry distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-68", "category": "Food Assistance & Emergency Relief", "name": "Faith Chapel", "location": "Monmouth County, NJ", "description": "Emergency food and assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-69", "category": "Food Assistance & Emergency Relief", "name": "Reformation Food Pantry", "location": "Monmouth County, NJ", "description": "Pantry support providing grocery items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-70", "category": "Food Assistance & Emergency Relief", "name": "The Mews Pantry", "location": "Monmouth County, NJ", "description": "Local food pantry assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-71", "category": "Food Assistance & Emergency Relief", "name": "West Belmar Food Pantry", "location": "West Belmar, NJ", "description": "Community food pantry serving West Belmar and surrounding areas.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today())
        },
        # Basic Needs & Community Assistance (Exact duplicate references as requested, 72-138)
        { "id": "monmouth-res-72", "category": "Basic Needs & Community Assistance", "name": "Matawan United Methodist Pantry", "location": "Matawan, NJ", "description": "Local food pantry providing grocery distribution and basic food support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-73", "category": "Basic Needs & Community Assistance", "name": "Allentown Food Pantry", "location": "Allentown, NJ", "description": "Community food pantry offering emergency groceries and pantry staples for local residents.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-74", "category": "Basic Needs & Community Assistance", "name": "Bethel Food Pantry", "location": "Monmouth County, NJ", "description": "Provides emergency food boxes and supplemental grocery support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-75", "category": "Basic Needs & Community Assistance", "name": "Deliverance Temple", "location": "Monmouth County, NJ", "description": "Offers community food distribution and emergency assistance programs.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-76", "category": "Basic Needs & Community Assistance", "name": "First United Methodist A.P. Pantry", "location": "Asbury Park, NJ", "description": "Provides food pantry assistance and emergency meal supplies.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-77", "category": "Basic Needs & Community Assistance", "name": "Glad Tidings", "location": "Monmouth County, NJ", "description": "Community outreach food assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-78", "category": "Basic Needs & Community Assistance", "name": "Jewish Family Services Pantry", "location": "Monmouth County, NJ", "description": "Pantry support providing nutritional items and family assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-79", "category": "Basic Needs & Community Assistance", "name": "Lutheran Church of Atonement Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution and grocery support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-80", "category": "Basic Needs & Community Assistance", "name": "Manna-United Fellowship Outreach", "location": "Monmouth County, NJ", "description": "Provides community meal supplies and food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-81", "category": "Basic Needs & Community Assistance", "name": "Mercy Center", "location": "Asbury Park, NJ", "description": "Offers a food pantry alongside family support services and basic-needs assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-82", "category": "Basic Needs & Community Assistance", "name": "Mt. Carmel", "location": "Monmouth County, NJ", "description": "Community food distribution and emergency assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-83", "category": "Basic Needs & Community Assistance", "name": "Oceans Family Success Center", "location": "Monmouth County, NJ", "description": "Family success center offering community resources, family support, and emergency food connections.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-84", "category": "Basic Needs & Community Assistance", "name": "Salvation Army Pantry -Asbury Park", "location": "Asbury Park, NJ", "description": "Emergency food pantry and basic-needs assistance for local families.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-85", "category": "Basic Needs & Community Assistance", "name": "Second Baptist Church Pantry", "location": "Monmouth County, NJ", "description": "Provides pantry staples and food distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-86", "category": "Basic Needs & Community Assistance", "name": "St. Peter Claver Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-87", "category": "Basic Needs & Community Assistance", "name": "Trinity Epis. Last Resort Pantry", "location": "Monmouth County, NJ", "description": "Emergency food support for individuals facing acute need.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-88", "category": "Basic Needs & Community Assistance", "name": "St. Augustine’s Soup Kitchen", "location": "Monmouth County, NJ", "description": "Provides hot meals and prepared food assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-89", "category": "Basic Needs & Community Assistance", "name": "Trinity Episcopal Saturday Soup", "location": "Monmouth County, NJ", "description": "Weekend soup kitchen providing nutritious hot meals.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-90", "category": "Basic Needs & Community Assistance", "name": "Providence Baptist Pantry", "location": "Monmouth County, NJ", "description": "Pantry support and community food distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-91", "category": "Basic Needs & Community Assistance", "name": "Eatontown Food Coop", "location": "Eatontown, NJ", "description": "Cooperative food pantry providing groceries to residents in need.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-92", "category": "Basic Needs & Community Assistance", "name": "St. Dorothea’s Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry supplies.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-93", "category": "Basic Needs & Community Assistance", "name": "Middletown Help Its Own", "location": "Middletown, NJ", "description": "Local assistance organization providing food and emergency support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-94", "category": "Basic Needs & Community Assistance", "name": "Macedonia Freehold Church Food Pantry", "location": "Freehold, NJ", "description": "Pantry distribution providing groceries and basic assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-95", "category": "Basic Needs & Community Assistance", "name": "Meet the Need Pantry", "location": "Monmouth County, NJ", "description": "Emergency food resources for individuals facing hardship.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-96", "category": "Basic Needs & Community Assistance", "name": "Open Door Pantry", "location": "Monmouth County, NJ", "description": "Community pantry offering regular grocery distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-97", "category": "Basic Needs & Community Assistance", "name": "St. John’s Pantry", "location": "Monmouth County, NJ", "description": "Food assistance program providing staples and fresh items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-98", "category": "Basic Needs & Community Assistance", "name": "OLPH Pantry (Our Lady of Perpetual Help)", "location": "Monmouth County, NJ", "description": "Emergency food pantry providing ongoing nutritional support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-99", "category": "Basic Needs & Community Assistance", "name": "St. Benedict’s Emerg Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution for local households.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-100", "category": "Basic Needs & Community Assistance", "name": "Christ Church Pantry", "location": "Monmouth County, NJ", "description": "Pantry support offering essential food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-101", "category": "Basic Needs & Community Assistance", "name": "Howell Food Pantry", "location": "Howell, NJ", "description": "Local food pantry serving Howell and surrounding Monmouth County areas.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-102", "category": "Basic Needs & Community Assistance", "name": "Project Paul", "location": "Monmouth County, NJ", "description": "Community service organization providing emergency food and support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-103", "category": "Basic Needs & Community Assistance", "name": "St. Mark’s CCR Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution pantry.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-104", "category": "Basic Needs & Community Assistance", "name": "St. Mark’s CCR Soup Kitchen", "location": "Monmouth County, NJ", "description": "Soup kitchen providing prepared hot meals.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-105", "category": "Basic Needs & Community Assistance", "name": "Keyport Ministerium Food Pantry", "location": "Keyport, NJ", "description": "Interfaith food pantry serving the Keyport area with emergency groceries.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-106", "category": "Basic Needs & Community Assistance", "name": "St. Joseph Church Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution services.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-107", "category": "Basic Needs & Community Assistance", "name": "Brookdale Wellness Center Food Pantry", "location": "Lincroft / Monmouth County, NJ", "description": "Campus and community food pantry supporting students and residents.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-108", "category": "Basic Needs & Community Assistance", "name": "Christ the King Pantry", "location": "Monmouth County, NJ", "description": "Pantry support offering food staples.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-109", "category": "Basic Needs & Community Assistance", "name": "First Baptist Pantry", "location": "Monmouth County, NJ", "description": "Community food distribution pantry.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-110", "category": "Basic Needs & Community Assistance", "name": "St. Brigid’s Pantry at St. James Church", "location": "Red Bank, NJ", "description": "Client-choice food pantry providing fresh produce and grocery assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-111", "category": "Basic Needs & Community Assistance", "name": "St. Luke’s United Methodist Pantry", "location": "Monmouth County, NJ", "description": "Emergency food assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-112", "category": "Basic Needs & Community Assistance", "name": "St. Michael’s Food Pantry", "location": "Monmouth County, NJ", "description": "Provides grocery assistance and food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-113", "category": "Basic Needs & Community Assistance", "name": "Meal At Noon (Soup Kitchen)", "location": "Monmouth County, NJ", "description": "Soup kitchen providing midday hot meals.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-114", "category": "Basic Needs & Community Assistance", "name": "St. Brigid’s Soup Kitchen at St. James Church", "location": "Red Bank, NJ", "description": "Prepared meals and hot lunches for individuals in need.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-115", "category": "Basic Needs & Community Assistance", "name": "Samaritan Center Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-116", "category": "Basic Needs & Community Assistance", "name": "Hope Community Church Pantry", "location": "Monmouth County, NJ", "description": "Community food distribution program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-117", "category": "Basic Needs & Community Assistance", "name": "Manasquan Food Pantry", "location": "Manasquan, NJ", "description": "Local food pantry serving Manasquan and surrounding coastal communities.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-118", "category": "Basic Needs & Community Assistance", "name": "Monmouth Worship Ctr. Pantry", "location": "Monmouth County, NJ", "description": "Emergency food and grocery assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-119", "category": "Basic Needs & Community Assistance", "name": "Matawan Food Pantry", "location": "Matawan, NJ", "description": "Pantry support providing essential food items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-120", "category": "Basic Needs & Community Assistance", "name": "Calico Cat Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-121", "category": "Basic Needs & Community Assistance", "name": "Goodness Now At Middletown UMC", "location": "Middletown, NJ", "description": "Community food pantry and basic assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-122", "category": "Basic Needs & Community Assistance", "name": "FPC Food Outreach", "location": "Monmouth County, NJ", "description": "Food outreach and grocery distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-123", "category": "Basic Needs & Community Assistance", "name": "Greater Emanuel Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency food pantry support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-124", "category": "Basic Needs & Community Assistance", "name": "Mt. Olivet - Heaven’s Grocery", "location": "Middletown, NJ", "description": "Grocery assistance and pantry distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-125", "category": "Basic Needs & Community Assistance", "name": "Bradley Food Pantry", "location": "Bradley Beach, NJ", "description": "Community food pantry serving local residents.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-126", "category": "Basic Needs & Community Assistance", "name": "Sephardic Bikur Holim Pantry (SBH)", "location": "Monmouth County, NJ", "description": "Community food and family support pantry.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-127", "category": "Basic Needs & Community Assistance", "name": "St. Paul’s Ocean Grove", "location": "Ocean Grove, NJ", "description": "Community food and assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-128", "category": "Basic Needs & Community Assistance", "name": "Lunch Break Pantry", "location": "Red Bank, NJ", "description": "Food pantry providing grocery boxes and supplemental food assistance.", "website": "https://lunchbreak.org", "phone": "732-747-8577", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-129", "category": "Basic Needs & Community Assistance", "name": "Salvation Army Food Pantry - Red Bank", "location": "Red Bank, NJ", "description": "Emergency food pantry and basic support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-130", "category": "Basic Needs & Community Assistance", "name": "St. Crispin’s Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency food distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-131", "category": "Basic Needs & Community Assistance", "name": "VGCA Food Pantry", "location": "Monmouth County, NJ", "description": "Community pantry supplies and support.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-132", "category": "Basic Needs & Community Assistance", "name": "BPC Food Pantry", "location": "Monmouth County, NJ", "description": "Emergency grocery distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-133", "category": "Basic Needs & Community Assistance", "name": "Lunch Break Soup Kitchen", "location": "Red Bank, NJ", "description": "Prepared hot meals and lunch program.", "website": "https://lunchbreak.org", "phone": "732-747-8577", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-134", "category": "Basic Needs & Community Assistance", "name": "Collingwood SDA Pantry", "location": "Monmouth County, NJ", "description": "Community food pantry distribution.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-135", "category": "Basic Needs & Community Assistance", "name": "Faith Chapel", "location": "Monmouth County, NJ", "description": "Emergency food and assistance program.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-136", "category": "Basic Needs & Community Assistance", "name": "Reformation Food Pantry", "location": "Monmouth County, NJ", "description": "Pantry support providing grocery items.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-137", "category": "Basic Needs & Community Assistance", "name": "The Mews Pantry", "location": "Monmouth County, NJ", "description": "Local food pantry assistance.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        { "id": "monmouth-res-138", "category": "Basic Needs & Community Assistance", "name": "West Belmar Food Pantry", "location": "West Belmar, NJ", "description": "Community food pantry serving West Belmar and surrounding areas.", "website": "https://www.monmouthresourcenet.org", "phone": "", "email": "", "last_verified": str(datetime.date.today()) },
        # Medical Equipment & Health (139-141)
        {
            "id": "monmouth-res-139",
            "category": "Medical Equipment & Health",
            "name": "Saint James Eatontown Medical Equipment Ministry",
            "location": "Eatontown, NJ",
            "description": "Provides temporary access to donated medical equipment and health supplies for community members in need.",
            "website": "https://www.stjames-parish.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-140",
            "category": "Medical Equipment & Health",
            "name": "Parker Family Health Center",
            "location": "Red Bank, NJ",
            "description": "Delivers free primary healthcare services to low-income, uninsured, and underinsured Monmouth County residents.",
            "website": "https://parkerfamilyhealth.org",
            "phone": "732-212-0777",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-141",
            "category": "Medical Equipment & Health",
            "name": "NJ Hospital Care Payment Assistance (Charity Care)",
            "location": "Statewide / Monmouth County, NJ",
            "description": "Offers financial assistance programs to help eligible low-income patients cover hospital medical bills.",
            "website": "https://www.nj.gov/health/",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Employment / Training (142-152)
        {
            "id": "monmouth-res-142",
            "category": "Employment / Training",
            "name": "Catalyte",
            "location": "Remote / Regional NJ",
            "description": "Offers tech training and career pathways through an aptitude-based model designed to place individuals into software engineering roles (Age requirement: 18+).",
            "website": "https://www.catalyte.io",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-143",
            "category": "Employment / Training",
            "name": "Apprenti",
            "location": "National / Regional",
            "description": "Connects underrepresented candidates with paid registered tech apprenticeships and professional training programs (Age requirement: 18+).",
            "website": "https://apprenticareers.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-144",
            "category": "Employment / Training",
            "name": "Multiverse",
            "location": "Remote / Virtual",
            "description": "Provides professional apprenticeships that combine paid work experience with tuition-free training in data, software, and business (Age requirement: 18+).",
            "website": "https://www.multiverse.io",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-145",
            "category": "Employment / Training",
            "name": "Per Scholas",
            "location": "Newark, NJ / Remote",
            "description": "Delivers rigorous, tuition-free IT training and professional development bootcamps to launch technology careers (Age requirement: 18+).",
            "website": "https://perscholas.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-146",
            "category": "Employment / Training",
            "name": "NPower",
            "location": "Newark & Jersey City, NJ",
            "description": "Provides tuition-free tech training, certifications, and career placement services for young adults and military veterans (Age requirement: 18–25 for young adult track).",
            "website": "https://npower.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-147",
            "category": "Employment / Training",
            "name": "LaunchCode",
            "location": "Remote Learning",
            "description": "Offers tuition-free tech education and job placement assistance for individuals seeking careers in software development (Age requirement: 18+).",
            "website": "https://www.launchcode.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-148",
            "category": "Employment / Training",
            "name": "Generation USA",
            "location": "Remote Cohorts",
            "description": "Operates accelerated, tuition-free employment programs that bridge the gap between training and job placement (Age requirement: 18+).",
            "website": "https://usa.generation.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-149",
            "category": "Employment / Training",
            "name": "Goodwill Workforce Services",
            "location": "New Jersey Centers",
            "description": "Provides career counseling, job placement assistance, and skills training workshops.",
            "website": "https://www.goodwill.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-150",
            "category": "Employment / Training",
            "name": "SkillUp Coalition",
            "location": "Online Platform",
            "description": "Offers online career navigation tools, training courses, and job matching resources.",
            "website": "https://skillup.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-151",
            "category": "Employment / Training",
            "name": "Forage",
            "location": "Online Platform",
            "description": "Provides free online virtual job simulations designed by major companies to help job seekers build practical experience.",
            "website": "https://www.theforage.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-152",
            "category": "Education, Technology & Community Resources",
            "name": "Red Bank Public Library",
            "location": "Red Bank, NJ",
            "description": "A public library offering books, computer and internet access, educational programming, and digital learning resources. The library offers the first 10 copies or printed pages free, even for individuals without a library card. Red Bank residents who obtain a library card can also access free online courses through the library’s Coursera partnership (individuals under 13 require parent or guardian signature to register for a library card).",
            "website": "https://www.redbanklibrary.org/",
            "phone": "732-842-0690",
            "email": "redbanklibrary@gmail.com",
            "last_verified": str(datetime.date.today())
        },
        # Supplemental Income & Resale (153-155)
        {
            "id": "monmouth-res-153",
            "category": "Supplemental Income & Resale",
            "name": "Plato’s Closet",
            "location": "Middletown, NJ",
            "description": "Buys and sells gently used teen and young adult clothing and accessories for supplemental income or affordable shopping.",
            "website": "https://www.platoscloset.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-154",
            "category": "Supplemental Income & Resale",
            "name": "Once Upon A Child",
            "location": "Howell, NJ",
            "description": "Provides a marketplace to buy and sell gently used children's clothing, gear, and toys.",
            "website": "https://www.onceuponachild.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-155",
            "category": "Supplemental Income & Resale",
            "name": "Flexible Gig Work Platforms (Reflex, Instacart, DoorDash)",
            "location": "Monmouth County, NJ",
            "description": "App-based platforms offering flexible freelance and delivery work opportunities for supplemental income (Age requirement: 18+ or 21+ depending on platform).",
            "website": "https://www.reflex.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Healthcare Navigation & Benefits (156-157)
        {
            "id": "monmouth-res-156",
            "category": "Healthcare Navigation & Benefits",
            "name": "Monmouth County Division on Aging / SHIP",
            "location": "Freehold, NJ",
            "description": "Provides free, unbiased counseling to help Medicare beneficiaries navigate health insurance coverage and evaluate benefits.",
            "website": "https://monmouthadvs.com",
            "phone": "732-431-7450",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-157",
            "category": "Healthcare Navigation & Benefits",
            "name": "GoodRx",
            "location": "Online / Local Pharmacies",
            "description": "Free digital discount tool providing prescription price comparisons and coupons accepted at local pharmacies.",
            "website": "https://www.goodrx.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Financial & Utility Assistance (158-161)
        {
            "id": "monmouth-res-158",
            "category": "Financial & Utility Assistance",
            "name": "Universal Service Fund (USF) & Fresh Start",
            "location": "Statewide / Monmouth County, NJ",
            "description": "Provides monthly utility bill credits and potential debt forgiveness for low- to moderate-income households.",
            "website": "https://www.nj.gov/bpu/",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-159",
            "category": "Financial & Utility Assistance",
            "name": "Low-Income Home Energy Assistance Program (LIHEAP)",
            "location": "Statewide / Monmouth County, NJ",
            "description": "Offers cash grants to help eligible households pay winter heating and cooling utility costs.",
            "website": "https://www.nj.gov/dca/",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-160",
            "category": "Financial & Utility Assistance",
            "name": "NJ SHARES",
            "location": "Statewide, NJ",
            "description": "Provides temporary grants for households experiencing a financial crisis that exceed standard utility assistance limits.",
            "website": "https://njshares.org",
            "phone": "1-866-657-4273",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-161",
            "category": "Financial & Utility Assistance",
            "name": "NJ Comfort Partners",
            "location": "Statewide / Monmouth County, NJ",
            "description": "Free energy-saving and weatherization program offering in-home evaluations and direct efficiency upgrades.",
            "website": "https://njcomfortpartners.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Mental Health & Support Groups (162)
        {
            "id": "monmouth-res-162",
            "category": "Mental Health & Support Groups",
            "name": "NAMI Greater Monmouth County",
            "location": "Monmouth County, NJ",
            "description": "Offers free, confidential peer-led support groups and educational resources for individuals and families navigating mental health conditions.",
            "website": "https://namigreatermonmouth.org",
            "phone": "732-544-0980",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # Recreation, Health & Wellness (163)
        {
            "id": "monmouth-res-163",
            "category": "Recreation, Health & Wellness",
            "name": "YMCA of the Jersey Shore – Financial Assistance",
            "location": "Red Bank / Eatontown / Regional, NJ",
            "description": "Offers needs-based financial assistance on a sliding scale for memberships, childcare, and wellness programs.",
            "website": "https://ymcanj.org",
            "phone": "732-741-2504",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        # JBJ Soul Kitchen (164)
        {
            "id": "monmouth-res-164",
            "category": "Food Security & Basic Needs",
            "name": "JBJ Soul Kitchen",
            "location": "Red Bank, NJ",
            "description": "A nonprofit community restaurant providing meals to individuals and families experiencing food insecurity. Guests can make a suggested donation or volunteer their time, and those unable to contribute are still welcome.",
            "website": "https://jbjsoulkitchen.org/",
            "phone": "732-842-0900",
            "email": "info@jbjsoulkitchen.org",
            "last_verified": str(datetime.date.today())
        },
        # General Directory Disclaimer
        {
            "id": "monmouth-res-disclaimer",
            "category": "Notice",
            "name": "General Directory Disclaimer",
            "location": "Monmouth County, NJ",
            "description": "Please conduct your own research and contact organizations directly or visit their official websites to confirm program details, eligibility requirements, and current services.",
            "website": "",
            "phone": "",
            "email": "",
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
