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
    return [        {
            "id": "test-live-verify-01",
            "category": "Basic Needs & Assistance",
            "name": "Monmouth Test Community Pantry",
            "location": "Eatontown, NJ",
            "description": "Verification test entry to confirm live automated append-only database updates.",
            "website": "",
            "phone": "732-555-0199",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        # ==========================================
        # 1. BASIC NEEDS & ASSISTANCE
        # ==========================================
        {
            "id": "monmouth-res-01",
            "category": "Basic Needs & Assistance",
            "name": "Fulfill Food Bank & Mobile Pantries",
            "location": "Neptune / Monmouth County, NJ",
            "description": "Provides emergency food distribution, mobile pantries, and nutritional support to individuals and families experiencing food insecurity.",
            "website": "https://fulfillnj.org",
            "phone": "732-918-2600",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "monmouth-res-29",
            "category": "Basic Needs & Assistance",
            "name": "JBJ Soul Kitchen",
            "location": "Red Bank, NJ",
            "description": "A nonprofit community restaurant providing meals to individuals and families experiencing food insecurity. Guests can make a suggested donation or volunteer their time, and those unable to contribute are still welcome.",
            "website": "https://jbjsoulkitchen.org/",
            "phone": "732-842-0900",
            "email": "info@jbjsoulkitchen.org",
            "cost_label": "Donation-Based",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "lunch-break-hub",
            "category": "Basic Needs & Assistance",
            "name": "Lunch Break",
            "location": "Red Bank, NJ",
            "description": "Community support hub providing grocery boxes, supplemental food assistance, and prepared hot meals/lunch programs. Also operates a community clothing and household goods thrift store.",
            "website": "https://lunchbreak.org/",
            "phone": "732-747-8577",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
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
            "cost_label": "Low-Cost / Sliding Scale",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "calico-cat-pantry",
            "category": "Basic Needs & Assistance",
            "name": "Calico Cat Food Pantry",
            "location": "Monmouth County, NJ",
            "description": "Calico Cat provides food pantry services and emergency assistance to individuals and families in its service area. Emergency Assistance Fund: Provides one-time financial assistance to help low-income households with utility bills, rent, or mortgage payments for residents of Aberdeen, Atlantic Highlands, Belford, Cliffwood, Hazlet, Highlands, Holmdel, Keansburg, Keyport, Leonardo, Lincroft, Matawan, Middletown, Port Monmouth, Red Bank, and Union Beach.",
            "website": "",
            "phone": "732-671-0550",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Select Communities",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "allentown-food-pantry",
            "category": "Basic Needs & Assistance",
            "name": "Allentown Food Pantry",
            "location": "20 High St. (Presbyterian Ch.), Allentown, NJ",
            "description": "Community food pantry and emergency relief assistance program.",
            "website": "",
            "phone": "609-259-7289",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Select Communities",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 2. EMPLOYMENT, EDUCATION & CAREER DEVELOPMENT
        # ==========================================
        {
            "id": "monmouth-res-30",
            "category": "Employment, Education & Career Development",
            "name": "Red Bank Public Library",
            "location": "Red Bank, NJ",
            "description": "A public library offering books, computer and internet access, educational programming, and digital learning resources. Red Bank residents who obtain a library card can access free online courses through its Coursera partnership.",
            "website": "https://www.redbanklibrary.org/",
            "phone": "732-842-0690",
            "email": "redbanklibrary@gmail.com",
            "cost_label": "Free",
            "nj_access": "Monmouth County",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-01", "category": "Employment, Education & Career Development", "name": "LinkedIn Jobs", "location": "Online / National",
            "description": "Search employment opportunities, connect with recruiters, and build professional relationships.", "website": "https://www.linkedin.com/jobs/",
            "phone": "", "email": "", "cost_label": "Paid", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-02", "category": "Employment, Education & Career Development", "name": "Indeed", "location": "Online / National",
            "description": "Search jobs across industries, including technology, healthcare, administration, and customer service.", "website": "https://www.indeed.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-03", "category": "Employment, Education & Career Development", "name": "Glassdoor", "location": "Online / National",
            "description": "Search job openings and explore employer reviews, salary information, and interview insights.", "website": "https://www.glassdoor.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-10", "category": "Employment, Education & Career Development", "name": "Dice", "location": "Online / National",
            "description": "Technology-focused job board featuring IT support, software development, cybersecurity, data, cloud, and infrastructure careers.", "website": "https://www.dice.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-15", "category": "Employment, Education & Career Development", "name": "We Work Remotely", "location": "Online / Remote",
            "description": "Search remote opportunities in programming, customer support, marketing, design, and other professional fields.", "website": "https://weworkremotely.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-17", "category": "Employment, Education & Career Development", "name": "FlexJobs", "location": "Online / Remote",
            "description": "Explore screened remote, hybrid, flexible, freelance, and part-time employment opportunities.", "website": "https://www.flexjobs.com/",
            "phone": "", "email": "", "cost_label": "Paid", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-26", "category": "Employment, Education & Career Development", "name": "USAJOBS", "location": "Online / Federal",
            "description": "Official federal government employment website featuring federal jobs in technology, administration, healthcare, and other fields.", "website": "https://www.usajobs.gov/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-28", "category": "Employment, Education & Career Development", "name": "New Jersey Department of Labor — Career Services", "location": "Trenton / Statewide, NJ",
            "description": "Access New Jersey employment services, job-search assistance, career guidance, and workforce training resources.", "website": "https://www.nj.gov/labor/career-services/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Statewide (NJ)", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch1-job-31", "category": "Employment, Education & Career Development", "name": "Upwork", "location": "Online / Freelance",
            "description": "Freelance marketplace connecting professionals with businesses for technology, writing, design, administrative, and other projects.", "website": "https://www.upwork.com/",
            "phone": "", "email": "", "cost_label": "Paid", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-comm-01", "category": "Employment, Education & Career Development", "name": "Tech Ladies", "location": "Online / Professional Community",
            "description": "Professional community connecting women in technology with career resources, networking, and employment opportunities.", "website": "https://www.hiretechladies.com/",
            "phone": "", "email": "", "cost_label": "Paid", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-comm-05", "category": "Employment, Education & Career Development", "name": "GitHub", "location": "Online / Developer Platform",
            "description": "Developer platform for hosting code, building portfolios, collaborating on projects, and connecting with the software development community.", "website": "https://github.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-emp-01", "category": "Employment, Education & Career Development", "name": "Amazon Jobs", "location": "Online / Corporate Portal",
            "description": "Search corporate, technology, operations, and other employment opportunities at Amazon.", "website": "https://www.amazon.jobs/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch2-emp-02", "category": "Employment, Education & Career Development", "name": "Microsoft Careers", "location": "Online / Corporate Portal",
            "description": "Explore employment opportunities in software, cloud, cybersecurity, business, and operations.", "website": "https://careers.microsoft.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 3. FAMILY & SUPPORT SERVICES
        # ==========================================
        {
            "id": "monmouth-res-02",
            "category": "Family & Support Services",
            "name": "Monmouth ResourceNet Directory",
            "location": "Neptune, NJ",
            "description": "Connects residents with a comprehensive network of local family support services, basic needs assistance, and community programs.",
            "website": "https://www.monmouthresourcenet.org",
            "phone": "732-222-8008",
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
            "location": "Red Bank, NJ",
            "description": "New Jersey's first charitable pharmacy, providing free prescription medications to uninsured and underserved individuals to reduce health disparities.",
            "website": "https://rscprx.org/",
            "phone": "732-784-8999",
            "email": "pharmacist@rscprx.org",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },

        # ==========================================
        # 5. MENTAL HEALTH & EMOTIONAL SUPPORT
        # ==========================================
        {
            "id": "batch3-mh-01", "category": "Mental Health & Emotional Support", "name": "Open Path Psychotherapy Collective", "location": "Online / National",
            "description": "Connects eligible individuals and families with affordable in-person and online therapy through participating mental health professionals.", "website": "https://openpathcollective.org/",
            "phone": "", "email": "", "cost_label": "Low-Cost / Sliding Scale", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-02", "category": "Mental Health & Emotional Support", "name": "Psychology Today — Therapist Finder", "location": "Online / National",
            "description": "Search for therapists, psychologists, psychiatrists, and other mental health professionals by location, specialty, insurance, and treatment approach.", "website": "https://www.psychologytoday.com/us/therapists",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-03", "category": "Mental Health & Emotional Support", "name": "Headway", "location": "Online / New Jersey",
            "description": "Find therapists and mental health professionals who accept participating health insurance plans with zero cost to use the matching directory.",
            "website": "https://headway.co/therapists/new-jersey",
            "phone": "", "email": "", "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-08", "category": "Mental Health & Emotional Support", "name": "Therapy for Black Girls", "location": "Online / National",
            "description": "Therapist-search resource centered on the mental wellness of Black women and girls. Helps visitors find culturally responsive mental health professionals.", "website": "https://providers.therapyforblackgirls.com/",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-11", "category": "Mental Health & Emotional Support", "name": "Therapy for Black Men", "location": "Online / National",
            "description": "Therapist directory and mental health resource designed to help Black men find culturally responsive mental health support.", "website": "https://therapyforblackmen.org/therapists",
            "phone": "", "email": "", "cost_label": "Free", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-19", "category": "Mental Health & Emotional Support", "name": "The Loveland Foundation — Therapy Fund", "location": "Online / National",
            "description": "Provides therapy financial assistance to eligible Black women and nonbinary individuals in the United States.", "website": "https://thelovelandfoundation.org/therapy-fund/",
            "phone": "", "email": "", "cost_label": "Low-Cost / Sliding Scale", "nj_access": "Nationwide / Online", "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-mh-23", "category": "Mental Health & Emotional Support", "name": "NJ MentalHealthCares", "location": "Statewide, NJ",
            "description": "New Jersey’s behavioral health information and referral service offering free, confidential emotional support, information, and referrals.", "website": "https://www.mhanj.org/new-jersey-mental-health-cares/",
            "phone": "866-202-4357", "email": "", "cost_label": "Free", "nj_access": "Statewide (NJ)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "batch3-crisis-01", "category": "Mental Health & Emotional Support", "name": "988 Suicide & Crisis Lifeline", "location": "Nationwide",
            "description": "Free, confidential, 24/7 support for people experiencing emotional distress, suicidal thoughts, or mental health and substance-use crises. Call or text 988.",
            "website": "https://988lifeline.org/",
            "phone": "988", "email": "", "cost_label": "Free",
            "nj_access": "Nationwide / Online",
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
            "phone": "211", "email": "", "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
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

    # Merge and deduplicate by 'id' or 'name' so we APPEND safely without wiping
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
