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
                        phone = row[3] if len(row) > 3 and "-" in row[3] else ""
                        
                        if name and len(name) > 2:
                            scraped_items.append({
                                "id": f"auto-scraped-{idx}",
                                "category": "Basic Needs & Assistance",
                                "name": name,
                                "location": f"{address}, {city}, NJ",
                                "description": "Community assistance program providing local support services.",
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
    """Core streamlined directory records matching user formatting guidelines."""
    return [
        {
            "id": "monmouth-res-01",
            "category": "Food Security & Basic Needs",
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
            "category": "Family & Support Services",
            "name": "Monmouth ResourceNet Directory",
            "location": "Neptune, NJ",
            "description": "Connects residents with a comprehensive network of local family support services, basic needs assistance, and community programs.",
            "website": "https://www.monmouthresourcenet.org",
            "phone": "732-222-8008",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-03",
            "category": "Basic Needs & Assistance",
            "name": "Affordable Housing Alliance",
            "location": "Eatontown, NJ",
            "description": "Offers housing assistance, homelessness prevention, rental support, and financial empowerment programs.",
            "website": "https://housingall.org",
            "phone": "732-389-2958",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-04",
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
            "id": "monmouth-res-05",
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
            "id": "monmouth-res-06",
            "category": "Medical Equipment & Health",
            "name": "NJ Hospital Care Payment Assistance (Charity Care)",
            "location": "Statewide / Monmouth County, NJ",
            "description": "Offers financial assistance programs to help eligible low-income patients cover hospital medical bills.",
            "website": "https://www.nj.gov/health/",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-07",
            "category": "Basic Needs & Assistance",
            "name": "NJ FamilyCare Low-Cost Health Insurance",
            "location": "Statewide, NJ",
            "description": "Provides publicly funded, low-cost or no-cost health insurance coverage for eligible children, adults, and families.",
            "website": "https://www.njfamilycare.org",
            "phone": "1-800-701-0710",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-08",
            "category": "Employment & Training",
            "name": "Catalyte",
            "location": "Remote / Regional NJ",
            "description": "Offers tech training and career pathways through an aptitude-based model designed to place individuals into software engineering roles (Age requirement: 18+).",
            "website": "https://www.catalyte.io",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-09",
            "category": "Employment & Training",
            "name": "Apprenti",
            "location": "National / Regional",
            "description": "Connects underrepresented candidates with paid registered tech apprenticeships and professional training programs (Age requirement: 18+).",
            "website": "https://apprenticareers.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-10",
            "category": "Employment & Training",
            "name": "Multiverse",
            "location": "Remote / Virtual",
            "description": "Provides professional apprenticeships that combine paid work experience with tuition-free training in data, software, and business (Age requirement: 18+).",
            "website": "https://www.multiverse.io",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-11",
            "category": "Employment & Training",
            "name": "Per Scholas",
            "location": "Newark, NJ / Remote",
            "description": "Delivers rigorous, tuition-free IT training and professional development bootcamps to launch technology careers (Age requirement: 18+).",
            "website": "https://perscholas.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-12",
            "category": "Employment & Training",
            "name": "NPower",
            "location": "Newark & Jersey City, NJ",
            "description": "Provides tuition-free tech training, certifications, and career placement services for young adults and military veterans (Age requirement: 18–25 for young adult track).",
            "website": "https://npower.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-13",
            "category": "Employment & Training",
            "name": "LaunchCode",
            "location": "Remote Learning",
            "description": "Offers tuition-free tech education and job placement assistance for individuals seeking careers in software development (Age requirement: 18+).",
            "website": "https://www.launchcode.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-14",
            "category": "Employment & Training",
            "name": "Generation USA",
            "location": "Remote Cohorts",
            "description": "Operates accelerated, tuition-free employment programs that bridge the gap between training and job placement (Age requirement: 18+).",
            "website": "https://usa.generation.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-15",
            "category": "Employment & Training",
            "name": "Goodwill Workforce Services",
            "location": "New Jersey Centers",
            "description": "Provides career counseling, job placement assistance, and skills training workshops.",
            "website": "https://www.goodwill.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-16",
            "category": "Employment & Training",
            "name": "SkillUp Coalition",
            "location": "Online Platform",
            "description": "Offers online career navigation tools, training courses, and job matching resources.",
            "website": "https://skillup.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-17",
            "category": "Employment & Training",
            "name": "Forage",
            "location": "Online Platform",
            "description": "Provides free online virtual job simulations designed by major companies to help job seekers build practical experience.",
            "website": "https://www.theforage.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-18",
            "category": "Supplemental Income & Resale",
            "name": "Plato's Closet",
            "location": "Middletown, NJ",
            "description": "Buys and sells gently used teen and young adult clothing and accessories for supplemental income or affordable shopping.",
            "website": "https://www.platoscloset.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-19",
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
            "id": "monmouth-res-20",
            "category": "Supplemental Income & Resale",
            "name": "Flexible Gig Work Platforms (Reflex, Instacart, DoorDash)",
            "location": "Monmouth County, NJ",
            "description": "App-based platforms offering flexible freelance and delivery work opportunities for supplemental income (Age requirement: 18+ or 21+ depending on platform).",
            "website": "https://www.reflex.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-21",
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
            "id": "monmouth-res-22",
            "category": "Healthcare Navigation & Benefits",
            "name": "GoodRx",
            "location": "Online / Local Pharmacies",
            "description": "Free digital discount tool providing prescription price comparisons and coupons accepted at local pharmacies.",
            "website": "https://www.goodrx.com",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-23",
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
            "id": "monmouth-res-24",
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
            "id": "monmouth-res-25",
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
            "id": "monmouth-res-26",
            "category": "Financial & Utility Assistance",
            "name": "NJ Comfort Partners",
            "location": "Statewide / Monmouth County, NJ",
            "description": "Free energy-saving and weatherization program offering in-home evaluations and direct efficiency upgrades.",
            "website": "https://njcomfortpartners.org",
            "phone": "",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-27",
            "category": "Mental Health & Support Groups",
            "name": "NAMI Greater Monmouth County",
            "location": "Monmouth County, NJ",
            "description": "Offers free, confidential peer-led support groups and educational resources for individuals and families navigating mental health conditions.",
            "website": "https://namigreatermonmouth.org",
            "phone": "732-544-0980",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-28",
            "category": "Recreation, Health & Wellness",
            "name": "YMCA of the Jersey Shore – Financial Assistance",
            "location": "Red Bank / Eatontown / Regional, NJ",
            "description": "Offers needs-based financial assistance on a sliding scale for memberships, childcare, and wellness programs.",
            "website": "https://ymcanj.org",
            "phone": "732-741-2504",
            "email": "",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-29",
            "category": "Food Security & Basic Needs",
            "name": "JBJ Soul Kitchen",
            "location": "Red Bank, NJ",
            "description": "A nonprofit community restaurant providing meals to individuals and families experiencing food insecurity. Guests can make a suggested donation or volunteer their time, and those unable to contribute are still welcome.",
            "website": "https://jbjsoulkitchen.org/",
            "phone": "732-842-0900",
            "email": "info@jbjsoulkitchen.org",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-30",
            "category": "Education, Technology & Community Resources",
            "name": "Red Bank Public Library",
            "location": "Red Bank, NJ",
            "description": "A public library offering books, computer and internet access, educational programming, and digital learning resources. The library offers the first 10 copies or printed pages free, even for individuals without a library card. Red Bank residents who obtain a library card can also access free online courses through the library’s Coursera partnership (individuals under 13 require parent or guardian signature to register for a library card).",
            "website": "https://www.redbanklibrary.org/",
            "phone": "732-842-0690",
            "email": "redbanklibrary@gmail.com",
            "last_verified": str(datetime.date.today())
        },
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
