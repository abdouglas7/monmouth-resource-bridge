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
    """Pulls live entries from structured community indexes across Monmouth County."""
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
                
                for idx, row in enumerate(parser.listings[1:], start=900):
                    if len(row) >= 4:
                        name = row[0]
                        address = row[1]
                        city = row[2] if len(row) > 2 else "Monmouth County, NJ"
                        phone = row[3] if len(row) > 3 and "-" in row[3] else ""
                        
                        if name and len(name) > 2:
                            # Skip duplicate scraped Calico Cat pantry; foundational record is maintained below
                            if "calico cat" in name.lower():
                                continue
                            scraped_items.append({
                                "id": f"auto-scraped-{idx}",
                                "category": "Basic Needs & Assistance",
                                "name": name,
                                "location": f"{address}, {city}, NJ",
                                "description": "Community food pantry and emergency relief assistance program.",
                                "website": url,
                                "phone": phone,
                                "email": "",
                                "cost_label": "Free",
                                "nj_access": "Monmouth County",
                                "last_verified": str(datetime.date.today())
                            })
            print(f"Successfully extracted records from: {url}")
        except Exception as e:
            print(f"Notice: Feed sync notice for {url}: {e}")
            
    return scraped_items

def get_foundational_resources():
    """Consolidated master list organized strictly under streamlined categories with clean labels and zero duplicates."""
    return [
        {
            "id": "monmouth-res-01", "category": "Basic Needs & Assistance", "name": "Fulfill Food Bank & Mobile Pantries", "location": "Neptune, NJ",
            "description": "Distributes food and essentials through a network of partner pantries, mobile food distributions, and community nutrition programs.", "website": "https://fulfillnj.org/",
            "phone": "732-918-2600", "email": "info@fulfillnj.org", "cost_label": "Free", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-29", "category": "Basic Needs & Assistance", "name": "JBJ Soul Kitchen", "location": "Red Bank / Toms River, NJ",
            "description": "Community restaurant serving paying and in-need customers with dignity, offering volunteer opportunities and support services.", "website": "https://jbjsoulkitchen.org/",
            "phone": "732-842-0900", "email": "info@jbjsoulkitchen.org", "cost_label": "Free or Donation", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "lunch-break-hub", "category": "Basic Needs & Assistance", "name": "Lunch Break", "location": "121 Drs James Parker Blvd, Red Bank, NJ",
            "description": "Comprehensive community support center providing food pantry services, hot meals, clothing boutique, social services navigation, and life skills.", "website": "https://lunchbreak.org/",
            "phone": "732-747-8577", "email": "info@lunchbreak.org", "cost_label": "Free", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-03", "category": "Basic Needs & Assistance", "name": "Affordable Housing Alliance", "location": "Eatontown, NJ",
            "description": "Housing counseling, utility payment assistance (PAGE / LIHEAP), rental stabilization, and homeownership education programs.", "website": "https://housingall.org/",
            "phone": "732-389-2958", "email": "info@housingall.org", "cost_label": "Free", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "calico-cat-pantry", "category": "Basic Needs & Assistance", "name": "Calico Cat Food Pantry", "location": "Monmouth County, NJ",
            "description": "Calico Cat provides food pantry services and emergency assistance to individuals and families in its service area. Emergency Assistance Fund: Provides one-time financial assistance to help low-income households with utility bills, rent, or mortgage payments for residents of Aberdeen, Atlantic Highlands, Belford, Cliffwood, Hazlet, Highlands, Holmdel, Keansburg, Keyport, Leonardo, Lincroft, Matawan, Middletown, Port Monmouth, Red Bank, and Union Beach.", "website": "",
            "phone": "732-671-0550", "email": "", "cost_label": "Free", "nj_access": "Select Communities",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "allentown-food-pantry", "category": "Basic Needs & Assistance", "name": "Allentown Food Pantry", "location": "Allentown, NJ",
            "description": "Local food pantry providing food support and staple goods to eligible community members.", "website": "",
            "phone": "609-259-7289", "email": "", "cost_label": "Free", "nj_access": "Select Communities",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-30", "category": "Employment, Education & Career Development", "name": "Red Bank Public Library", "location": "84 W Front St, Red Bank, NJ",
            "description": "Community public library offering adult literacy classes, career resume workshops, public computer labs, high-speed Wi-Fi, and printing access.", "website": "https://www.redbanklibrary.org/",
            "phone": "732-842-0690", "email": "", "cost_label": "Free", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-01", "category": "Employment, Education & Career Development", "name": "LinkedIn Jobs", "location": "Online / Nationwide",
            "description": "Professional network and job board featuring salary insights, easy-apply options, and personalized job alerts across all industries.", "website": "https://www.linkedin.com/jobs/",
            "phone": "", "email": "", "cost_label": "Free / Optional paid membership", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-02", "category": "Employment, Education & Career Development", "name": "Indeed", "location": "Online / Nationwide",
            "description": "Global job search engine aggregating millions of listings with company reviews, salary tools, and direct employer applications.", "website": "https://www.indeed.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-03", "category": "Employment, Education & Career Development", "name": "Glassdoor", "location": "Online / Nationwide",
            "description": "Job board coupled with anonymous employee reviews, CEO approval ratings, salary reports, and interview question guides.", "website": "https://www.glassdoor.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-10", "category": "Employment, Education & Career Development", "name": "Dice", "location": "Online / Nationwide",
            "description": "Dedicated career platform for technology professionals specializing in software development, data, cybersecurity, and engineering roles.", "website": "https://www.dice.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-15", "category": "Employment, Education & Career Development", "name": "We Work Remotely", "location": "Online / Nationwide",
            "description": "Global remote-work community listing verified remote roles in programming, design, customer support, and product management.", "website": "https://weworkremotely.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-17", "category": "Employment, Education & Career Development", "name": "FlexJobs", "location": "Online / Nationwide",
            "description": "Hand-screened job board specialized in remote, hybrid, and flexible schedule careers free of scam listings.", "website": "https://www.flexjobs.com/",
            "phone": "", "email": "", "cost_label": "Paid membership", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-26", "category": "Employment, Education & Career Development", "name": "USAJOBS", "location": "Online / Nationwide",
            "description": "Official federal government employment portal listing civilian opportunities across federal agencies and public health departments.", "website": "https://www.usajobs.gov/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide (Federal)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-28", "category": "Employment, Education & Career Development", "name": "New Jersey Department of Labor — Career Services", "location": "Statewide / Multiple County Offices, NJ",
            "description": "New Jersey state career hubs providing job fairs, resume assistance, re-employment workshops, and training grants.", "website": "https://www.nj.gov/labor/career-services/",
            "phone": "609-292-2121", "email": "", "cost_label": "Free", "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-31", "category": "Employment, Education & Career Development", "name": "Upwork", "location": "Online / Nationwide",
            "description": "Freelance marketplace connecting independent professionals with businesses for contract roles in technology, writing, marketing, and design.", "website": "https://www.upwork.com/",
            "phone": "", "email": "", "cost_label": "Free to search / Commission on earnings", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-comm-01", "category": "Employment, Education & Career Development", "name": "Tech Ladies", "location": "Online / Global",
            "description": "Professional community connecting women and non-binary tech professionals with job boards, mentorship programs, and salary guidance.", "website": "https://www.hiretechladies.com/",
            "phone": "", "email": "", "cost_label": "Free basic / Paid premium", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-comm-05", "category": "Employment, Education & Career Development", "name": "GitHub", "location": "Online / Global",
            "description": "Global developer platform for open-source collaboration, code hosting, and technical portfolio demonstration.", "website": "https://github.com/",
            "phone": "", "email": "", "cost_label": "Free tier available", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-emp-01", "category": "Employment, Education & Career Development", "name": "Amazon Jobs", "location": "Online / Multiple NJ Locations",
            "description": "Career portal for corporate technology, cloud computing (AWS), logistics, and fulfillment center roles across New Jersey.", "website": "https://www.amazon.jobs/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "New Jersey / Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-emp-02", "category": "Employment, Education & Career Development", "name": "Microsoft Careers", "location": "Online / Multiple NJ Locations",
            "description": "Official career portal for software engineering, cloud services, and technical enterprise positions.", "website": "https://careers.microsoft.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "New Jersey / Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-02", "category": "Healthcare & Medical Resources", "name": "Monmouth ResourceNet Directory", "location": "Monmouth County, NJ",
            "description": "Community health and family resource directory providing vetted listings for pediatric care, youth programs, and family support.", "website": "https://www.monmouthresourcenet.org/",
            "phone": "", "email": "", "cost_label": "Free directory", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-pharmacy-01", "category": "Healthcare & Medical Resources", "name": "Ritesh Shah Charitable Pharmacy", "location": "Red Bank, NJ",
            "description": "Charitable pharmacy providing life-saving maintenance medications at zero cost to uninsured and underinsured community members.", "website": "https://www.rscharitablepharmacy.org/",
            "phone": "732-842-0200", "email": "info@rscharitablepharmacy.org", "cost_label": "Free", "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-01", "category": "Mental Health & Emotional Support", "name": "Open Path Psychotherapy Collective", "location": "Online / Nationwide",
            "description": "Non-profit network providing affordable in-office and online psychotherapy sessions ($30–$70/session) for clients without insurance.", "website": "https://openpathcollective.org/",
            "phone": "", "email": "", "cost_label": "Low-cost ($30–$70) / Lifetime membership fee ($65)", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-02", "category": "Mental Health & Emotional Support", "name": "Psychology Today — Therapist Finder", "location": "Online / Nationwide",
            "description": "Comprehensive therapist directory allowing users to filter by sliding-scale fees, insurance accepted, cultural background, and location.", "website": "https://www.psychologytoday.com/us/therapists",
            "phone": "", "email": "", "cost_label": "Free directory / Fees vary", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-03", "category": "Mental Health & Emotional Support", "name": "Headway", "location": "Online / Nationwide",
            "description": "Platform connecting individuals with in-network mental health providers using their insurance benefits, with instant co-pay estimates.", "website": "https://headway.co/",
            "phone": "", "email": "", "cost_label": "Insurance co-pay", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-08", "category": "Mental Health & Emotional Support", "name": "Therapy for Black Girls", "location": "Online / Nationwide",
            "description": "Culturally affirming therapist directory and community platform dedicated to the mental well-being of Black women and girls.", "website": "https://therapyforblackgirls.com/",
            "phone": "", "email": "", "cost_label": "Free directory / Fees vary", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-11", "category": "Mental Health & Emotional Support", "name": "Therapy for Black Men", "location": "Online / Nationwide",
            "description": "National directory providing culturally competent mental health guidance and financial assistance vouchers for Black men seeking therapy.", "website": "https://therapyforblackmen.org/",
            "phone": "", "email": "", "cost_label": "Free directory / Therapy financial grants available", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-19", "category": "Mental Health & Emotional Support", "name": "The Loveland Foundation — Therapy Fund", "location": "Online / Nationwide",
            "description": "Provides financial therapy vouchers covering 4 to 12 sessions for Black women and girls nationwide.", "website": "https://thelovelandfoundation.org/",
            "phone": "", "email": "", "cost_label": "Free financial therapy grants", "nj_access": "Nationwide",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-23", "category": "Mental Health & Emotional Support", "name": "NJ MentalHealthCares", "location": "Statewide, NJ",
            "description": "New Jersey's free, confidential mental health information, referral, and supportive counseling hotline.", "website": "https://www.mhanj.org/nj-mentalhealthcares/",
            "phone": "1-866-202-4357", "email": "", "cost_label": "Free", "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-crisis-01", "category": "Mental Health & Emotional Support", "name": "988 Suicide & Crisis Lifeline", "location": "National / Local routing",
            "description": "Free, confidential 24/7 lifeline connecting anyone experiencing emotional distress or crisis with trained crisis counselors by phone or text.", "website": "https://988lifeline.org/",
            "phone": "988", "email": "", "cost_label": "Free", "nj_access": "National / Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-crisis-02", "category": "Mental Health & Emotional Support", "name": "ReachNJ", "location": "Statewide, NJ",
            "description": "New Jersey’s 24/7 substance-use assistance line connecting people and families with addiction treatment and support services.", "website": "https://www.nj.gov/humanservices/dmhas/",
            "phone": "1-844-732-2465", "email": "", "cost_label": "Free", "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-crisis-03", "category": "Mental Health & Emotional Support", "name": "NJ 211", "location": "Statewide, NJ",
            "description": "Statewide information and referral service connecting residents with housing, food, healthcare, transportation, and other social services.", "website": "https://www.nj211.org/",
            "phone": "211", "email": "", "cost_label": "Free", "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        }
    ]

def is_legitimate_resource(item):
    """Filter out fake test listings and duplicate scraped pantries."""
    item_id = str(item.get("id", ""))
    name = str(item.get("name", "")).lower()
    phone = str(item.get("phone", ""))
    desc = str(item.get("description", "")).lower()

    if item_id.startswith("test-batch-") or "555-0" in phone:
        return False
    if "monmouth test resource" in name or "batch verification" in desc:
        return False
    if item_id == "auto-scraped-948" or (name == "calico cat pantry" and item_id != "calico-cat-pantry"):
        return False

    return True

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
        if is_legitimate_resource(item):
            key = item.get("id", item.get("name"))
            resource_map[key] = item
        
    for item in all_new_batch:
        if is_legitimate_resource(item):
            key = item.get("id", item.get("name"))
            resource_map[key] = item 
        
    combined_resources = [item for item in resource_map.values() if is_legitimate_resource(item)]

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_resources, f, indent=2)
        
    print(f"Database sync complete. Total active records managed: {len(combined_resources)}")

if __name__ == "__main__":
    update_resource_database()
