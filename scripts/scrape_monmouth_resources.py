import json
import os
import datetime
import urllib.request
import urllib.error
from html.parser import HTMLParser

DATA_FILE_PATH = "data/resources.json"

class SimpleHTMLTableParser(HTMLParser):
    """Lightweight zero-dependency HTML table extractor."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_cell = []
        self.current_row = []
        self.listings = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            self.current_row.append(" ".join("".join(self.current_cell).split()))
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if any(self.current_row):
                self.listings.append(self.current_row)
        elif tag == "table":
            self.in_table = False

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)

def scrape_workinmonmouth_pantries():
    """Scrapes community pantries directly from workinmonmouth.com."""
    url = "https://workinmonmouth.com/community-food-pantries/"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    scraped_items = []
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                html_content = response.read().decode("utf-8", errors="ignore")
                parser = SimpleHTMLTableParser()
                parser.feed(html_content)
                
                for idx, row in enumerate(parser.listings[1:], start=900):
                    if len(row) >= 4:
                        name = row[0]
                        address = row[1]
                        city = row[2] if len(row) > 2 else "Monmouth County, NJ"
                        phone = row[3] if len(row) > 3 and "-" in row[3] else ""
                        
                        # Skip the bare-bones scraped duplicate of Calico Cat;
                        # the full "Calico Cat Food Pantry" entry is kept below.
                        if name.strip().lower() == "calico cat pantry":
                            continue

                        if name and len(name) > 2:
                            scraped_items.append({
                                "id": f"auto-scraped-{idx}",
                                "category": "Basic Needs & Assistance",
                                "name": name,
                                "location": f"{address}, {city}, NJ",
                                "description": "Community food pantry and emergency relief assistance program.",
                                "website": "",
                                "phone": phone,
                                "email": "",
                                "cost_label": "Free",
                                "nj_access": "Monmouth County",
                                "last_verified": str(datetime.date.today())
                            })
    except Exception as e:
        print(f"Notice: Live scrape fallback active ({e}). Using verified foundation list.")
        
    return scraped_items

def get_foundational_resources():
    """Returns curated Monmouth County resources across the 7 streamlined categories."""
    return [
        # ==========================================
        # 1. BASIC NEEDS & ASSISTANCE
        # ==========================================
        {
            "id": "lunch-break",
            "category": "Basic Needs & Assistance",
            "name": "Lunch Break",
            "location": "121 Drs James Parker Blvd, Red Bank, NJ 07701",
            "description": "Lunch Break freely provides food, clothing, life skills, and fellowship to those in need in Monmouth County and beyond. Operating as a comprehensive social service hub, Lunch Break offers hot community meals six days a week, a client-choice food pantry, clothing boutique, and outreach support. Through its Life Skills Center, participants access career coaching, job readiness training, resume assistance, and financial literacy workshops. Comprehensive emergency assistance helps families stabilize during immediate crises while working toward sustainable upward mobility.",
            "website": "https://lunchbreak.org",
            "phone": "732-747-8577",
            "email": "info@lunchbreak.org",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "affordable-housing-alliance",
            "category": "Basic Needs & Assistance",
            "name": "Affordable Housing Alliance",
            "location": "59 Broad St, Eatontown, NJ 07724",
            "description": "Community housing agency providing utility assistance programs (PAGE, TRUE, USF/LIHEAP), housing counseling, first-time homebuyer education, and eviction prevention.",
            "website": "https://housingall.org",
            "phone": "732-389-2958",
            "email": "",
            "cost_label": "Low-Cost / Sliding Scale",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "calico-cat-pantry",
            "category": "Basic Needs & Assistance",
            "name": "Calico Cat Food Pantry",
            "location": "96 Kings Hwy, Middletown Twp, NJ 07748",
            "description": "Calico Cat provides food pantry services and emergency assistance to individuals and families in its service area. Serving select communities: Aberdeen, Atlantic Highlands, Belford, Cliffwood, Hazlet, Highlands, Holmdel, Keansburg, Keyport, Leonardo, Lincroft, Matawan, Middletown, Port Monmouth, Red Bank, and Union Beach. Emergency Assistance Fund provides one-time financial assistance to help low-income households with utility bills, rent, or mortgage payments. Food Pantry Hours: 1st and 3rd Wednesdays only, 9:00 AM - 3:00 PM (after 3:00 PM by appointment only).",
            "website": "https://www.communityoutreachgroupinc.com",
            "phone": "732-671-8775",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "allentown-food-pantry",
            "category": "Basic Needs & Assistance",
            "name": "Allentown Food Pantry",
            "location": "23 Church St, Allentown, NJ 08501",
            "description": "Provides non-perishable food items, seasonal fresh produce, and emergency assistance to local families facing food insecurity.",
            "website": "",
            "phone": "609-259-7289",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "bethel-food-pantry",
            "category": "Basic Needs & Assistance",
            "name": "Bethel AME Food Pantry",
            "location": "Water Street, Freehold, NJ 07728",
            "description": "Faith-based food pantry offering groceries, emergency pantry bags, and seasonal outreach to Freehold area residents.",
            "website": "",
            "phone": "732-462-0826",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "mercy-center-asbury",
            "category": "Basic Needs & Assistance",
            "name": "Mercy Center",
            "location": "1106 Main St, Asbury Park, NJ 07712",
            "description": "Provides comprehensive emergency services, including an extensive food pantry, family stabilization programs, utility guidance, and educational advocacy.",
            "website": "https://mercycenternj.org",
            "phone": "732-774-9897",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 2. EMPLOYMENT & CAREER DEVELOPMENT
        # ==========================================
        {
            "id": "monmouth-county-workforce",
            "category": "Employment, Education & Career Development",
            "name": "Monmouth County Workforce Development Board",
            "location": "170 State Route 35, Eatontown, NJ 07724",
            "description": "One-Stop Career Center delivering federally-funded workforce training grants, career counseling, resume optimization, job fairs, and youth employment initiatives.",
            "website": "https://www.co.monmouth.nj.us",
            "phone": "732-683-8850",
            "email": "workforce@co.monmouth.nj.us",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "brookdale-community-college",
            "category": "Employment, Education & Career Development",
            "name": "Brookdale Community College Continuing Education",
            "location": "765 Newman Springs Rd, Lincroft, NJ 07738",
            "description": "Offers accelerated industry credentials, healthcare certifications, technical certificates, and programs eligible for New Jersey Community College Opportunity Grant funding.",
            "website": "https://www.brookdalecc.edu",
            "phone": "732-224-2345",
            "email": "",
            "cost_label": "Financial Aid / Grant Eligible",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "nj-apprenticeship-network",
            "category": "Employment, Education & Career Development",
            "name": "New Jersey Apprenticeship Network",
            "location": "Trenton, NJ (Statewide Programs)",
            "description": "Statewide earn-while-you-learn apprenticeship framework placing candidates into paid training programs across advanced manufacturing, clean energy, healthcare, and IT.",
            "website": "https://www.nj.gov/labor/apprenticeship",
            "phone": "609-292-2323",
            "email": "",
            "cost_label": "Paid Program / Earn While You Learn",
            "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "forage-virtual-internships",
            "category": "Employment, Education & Career Development",
            "name": "Forage Virtual Work Simulations",
            "location": "Online / Remote",
            "description": "Open-access digital platform featuring 5-6 hour virtual work simulations designed by leading employers (JPMorgan, BCG, Citi) to build tangible resume experience.",
            "website": "https://www.theforage.com",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Nationwide / Remote",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 3. FAMILY & SUPPORT SERVICES
        # ==========================================
        {
            "id": "monmouth-county-social-services",
            "category": "Family & Support Services",
            "name": "Monmouth County Division of Social Services",
            "location": "3000 Kozloski Rd, Freehold, NJ 07728",
            "description": "County agency processing and managing NJ SNAP (food stamps), WorkFirst NJ/TANF, General Assistance, Medicaid enrollment, and emergency housing vouchers.",
            "website": "https://www.co.monmouth.nj.us",
            "phone": "732-431-6000",
            "email": "",
            "cost_label": "Free Public Agency",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "oceans-family-success-center",
            "category": "Family & Support Services",
            "name": "Oceans Family Success Center",
            "location": "1200 Memorial Dr, Asbury Park, NJ 07712",
            "description": "Community-based family gathering center offering parent education, financial workshops, life skills classes, health navigation, and youth activities.",
            "website": "https://www.oceansfsc.org",
            "phone": "732-455-5272",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "aarp-tax-aide-monmouth",
            "category": "Family & Support Services",
            "name": "AARP Foundation Tax-Aide (Monmouth County)",
            "location": "Multiple County Library Branches",
            "description": "IRS-certified volunteer tax preparation service providing free electronic federal and state tax filing for low- to moderate-income taxpayers, with special attention to seniors.",
            "website": "https://www.aarp.org/money/taxes/aarp_taxaide/",
            "phone": "888-227-7669",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 4. HEALTHCARE & MEDICAL RESOURCES
        # ==========================================
        {
            "id": "monmouth-res-pharmacy-01",
            "category": "Healthcare & Medical Resources",
            "name": "Ritesh Shah Charitable Pharmacy",
            "location": "224 Shrewsbury Avenue, Red Bank, NJ 07701",
            "description": "Charitable pharmacy providing life-saving maintenance medications at zero cost to uninsured and underinsured community members. Hours: Monday, Tuesday, and Thursday 11:00 AM - 4:00 PM; Friday 10:00 AM - 3:00 PM.",
            "website": "https://rscprx.org",
            "phone": "732-784-8999",
            "email": "info@rscharitablepharmacy.org",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "parker-family-health-center",
            "category": "Healthcare & Medical Resources",
            "name": "Parker Family Health Center",
            "location": "211 Shrewsbury Ave, Red Bank, NJ 07701",
            "description": "Volunteer-driven free health clinic serving low-income, uninsured Monmouth County residents with primary medical care, chronic disease management, and preventative screenings.",
            "website": "https://www.parkerfamilyhealthcenter.org",
            "phone": "732-212-0777",
            "email": "",
            "cost_label": "Free for Uninsured",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "vna-central-jersey",
            "category": "Healthcare & Medical Resources",
            "name": "Visiting Nurse Association Health Group (VNA)",
            "location": "23 Main St, Suite D1, Holmdel, NJ 07733",
            "description": "Delivers community health clinics, mobile primary care, prenatal nursing, children's health clinics, and specialized in-home chronic condition management.",
            "website": "https://vnahg.org",
            "phone": "732-224-6920",
            "email": "",
            "cost_label": "Sliding Scale / Medicaid",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 5. MENTAL HEALTH & EMOTIONAL SUPPORT
        # ==========================================
        {
            "id": "monmouth-res-crisis-01",
            "category": "Mental Health & Emotional Support",
            "name": "988 Suicide & Crisis Lifeline",
            "location": "Available Nationwide (Call or Text)",
            "description": "24/7, free, and confidential support for people in suicidal crisis or emotional distress. Dial or text 988 anywhere in New Jersey for immediate trained intervention.",
            "website": "https://988lifeline.org",
            "phone": "988",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide & Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-crisis-02",
            "category": "Mental Health & Emotional Support",
            "name": "ReachNJ Addiction Helpline",
            "location": "Statewide Centralized Intake (NJ)",
            "description": "Statewide 24/7 addiction helpline coordinating real-time treatment placement, inpatient and outpatient detox services, regardless of insurance status.",
            "website": "https://www.reachnj.gov",
            "phone": "844-732-2465",
            "email": "",
            "cost_label": "Free Guidance",
            "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "mental-health-association-monmouth",
            "category": "Mental Health & Emotional Support",
            "name": "Mental Health Association of Monmouth County",
            "location": "119 Avenue at the Common, Shrewsbury, NJ 07702",
            "description": "Provides free and low-cost mental health navigation, supportive counseling, suicide prevention education, and homeless advocacy initiatives.",
            "website": "https://www.mhamc.org",
            "phone": "732-542-6422",
            "email": "",
            "cost_label": "Free / Low-Cost Navigation",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 6. HEALTH, RECREATION & WELLNESS
        # ==========================================
        {
            "id": "monmouth-county-ymca",
            "category": "Health, Recreation & Wellness",
            "name": "YMCA of Greater Monmouth County",
            "location": "170 Patterson Ave, Shrewsbury, NJ 07702",
            "description": "Provides youth sports, swimming lessons, summer day camps, family fitness facilities, and income-based financial assistance scholarships.",
            "website": "https://ymcanj.org",
            "phone": "732-741-2504",
            "email": "",
            "cost_label": "Sliding-Scale / Financial Assistance Available",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-county-park-system",
            "category": "Health, Recreation & Wellness",
            "name": "Monmouth County Park System",
            "location": "805 Newman Springs Rd, Lincroft, NJ 07738",
            "description": "Manages over 40 county parks, 140+ miles of recreational trails, and nature centers offering free and low-cost health and wellness outdoor programs.",
            "website": "https://www.monmouthcountyparks.com",
            "phone": "732-842-4000",
            "email": "",
            "cost_label": "Free Entry / Low-Cost Programs",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 7. NEW JERSEY & LOCAL COMMUNITY RESOURCES
        # ==========================================
        {
            "id": "monmouth-res-crisis-03",
            "category": "New Jersey & Local Community Resources",
            "name": "NJ 211 Community Resource Directory",
            "location": "Dial 211 Statewide (Available 24/7)",
            "description": "Dial 211 or visit online for immediate referral to essential health and human services across New Jersey, including emergency housing, food security, and heating help.",
            "website": "https://www.nj211.org",
            "phone": "211",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-county-library-system",
            "category": "New Jersey & Local Community Resources",
            "name": "Monmouth County Library System (Headquarters)",
            "location": "125 Symmes Dr, Manalapan, NJ 07726",
            "description": "County library network offering free high-speed public computers, Wi-Fi, meeting spaces, digital Coursera courses, and career development databases.",
            "website": "https://monmouthcountylib.org",
            "phone": "732-431-7220",
            "email": "",
            "cost_label": "Free for Cardholders",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # EDITORIAL DISCLAIMER
        # ==========================================
        {
            "id": "general-directory-disclaimer",
            "category": "Notice",
            "name": "General Directory Disclaimer",
            "location": "Monmouth County, NJ",
            "description": "Please conduct your own research. We do not independently verify resources, as we are not a case management agency. While we strive to provide helpful and accurate information, resources may change their hours, eligibility criteria, or service offerings without notice. Always contact the provider directly to confirm current details.",
            "website": "",
            "phone": "",
            "email": "",
            "cost_label": "Notice",
            "nj_access": "Countywide",
            "last_verified": str(datetime.date.today())
        }
    ]

# Fake test listings and duplicates that must never appear on the site.
BLOCKED_IDS = {
    "test-batch-01", "test-batch-02", "test-batch-03", "test-batch-04", "test-batch-05",
    "auto-scraped-948",
}
BLOCKED_NAMES = {"calico cat pantry"}

def is_legitimate_resource(item):
    """Returns False for fake test listings, placeholder 555 numbers, and the Calico Cat duplicate."""
    item_id = str(item.get("id", "")).strip().lower()
    name = str(item.get("name", "")).strip().lower()
    phone = str(item.get("phone", ""))
    if item_id in BLOCKED_IDS or item_id.startswith("test-"):
        return False
    if name in BLOCKED_NAMES or name.startswith("test "):
        return False
    if "555-" in phone:
        return False
    return True

def update_resource_database():
    """Merges scraped records with foundational resources and writes clean JSON."""
    foundational = get_foundational_resources()
    scraped = scrape_workinmonmouth_pantries()
    
    # Merge strategy: foundational curated resources take precedence by ID and name
    combined_dict = {}
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    if isinstance(item, dict) and "id" in item:
                        combined_dict[item["id"]] = item
        except Exception:
            pass
    for item in foundational:
        combined_dict[item["id"]] = item
        
    for item in scraped:
        if item["id"] not in combined_dict:
            combined_dict[item["id"]] = item

    # Filter out blocked test records, placeholder numbers, and duplicates
    combined_resources = [item for item in combined_dict.values() if is_legitimate_resource(item)]

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_resources, f, indent=2)
        
    print(f"Database sync complete. Total active records managed: {len(combined_resources)}")

if __name__ == "__main__":
    update_resource_database()
