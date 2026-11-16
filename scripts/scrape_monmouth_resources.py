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

def get_original_foundational_resources():
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
            "description": (
                "Calico Cat provides food pantry services and emergency assistance to individuals and families in its service area.\n\n"
                "Food Pantry Hours:\n"
                "1st and 3rd Wednesdays only: 9:00 AM – 3:00 PM\n"
                "After 3:00 PM: by appointment only\n\n"
                "Emergency Assistance Fund:\n"
                "Provides one-time financial assistance for low-income households needing help with utility bills, rent, or mortgage payments.\n\n"
                "Serving select communities:\n"
                "Aberdeen, Atlantic Highlands, Belford, Cliffwood, Hazlet, Highlands, Holmdel, Keansburg, Keyport, Leonardo, Lincroft, Matawan, Middletown, Port Monmouth, Red Bank, and Union Beach."
            ),
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
                {
            "id": "perscholas-it-training",
            "category": "Employment, Education & Career Development",
            "name": "Per Scholas",
            "location": "12 Lombardy Street, Newark, NJ 07102",
            "description": "Tuition-free IT training, professional development, and career support services. They offer in-person, remote, and hybrid courses.\n\nHours of Operation:\nMonday \u2013 Friday: 9:00 AM \u2013 5:00 PM",
            "website": "https://perscholas.org",
            "phone": "(973) 803-4420",
            "email": "info@perscholas.org",
            "cost_label": "Free",
            "nj_access": "Age: 18+ (No upper limit)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "npower-tech-fundamentals",
            "category": "Employment, Education & Career Development",
            "name": "NPower",
            "location": "Newark, NJ",
            "description": "Offers tech fundamentals, cybersecurity, and cloud computing training for young adults and military veterans, with local NJ cohorts. They offer in-person, remote, and hybrid courses.\n\nEligibility Note:\nWhile NPower primarily targets young adults aged 18 to 26 for standard technology training cohorts, they offer specialized programs specifically designed for military veterans and military spouses that feature flexible or expanded age criteria which bypass the standard young adult age cap.\n\nHours of Operation:\nMonday \u2013 Friday: 9:00 AM \u2013 5:00 PM",
            "website": "https://npower.org",
            "phone": "(973) 445-4400",
            "email": "info.nj@npower.org",
            "cost_label": "Free",
            "nj_access": "Age: 18–26 (Veteran tracks vary)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "catalyte-software-development",
            "category": "Employment, Education & Career Development",
            "name": "Catalyte",
            "location": "Remote & Hybrid (Online)",
            "description": "Catalyte provides free education and placement into software development roles. They offer in-person, remote, and hybrid courses.\n\nEligibility Note:\nCatalyte does not require previous technical experience, college degrees, or resume screening for entry. Instead, applicants take a series of cognitive, problem-solving, and capability assessments designed to measure an individual's natural capacity for software development and technical learning.\n\nHours of Operation:\nMonday \u2013 Friday: 9:00 AM \u2013 5:00 PM",
            "website": "https://catalyte.io",
            "phone": "(888) 748-3838",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Age: 18+",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "climb-hire-salesforce",
            "category": "Employment, Education & Career Development",
            "name": "Climb Hire",
            "location": "Remote & Hybrid (Online)",
            "description": "A community-based program focused on training individuals for Salesforce administration and operations roles. They offer in-person, remote, and hybrid courses.\n\nProgram Note:\nThis program utilizes income share agreements, which means students pay bash upfront for tuition and only begin repaying the cost of the program as a fixed percentage of their income after they secure a well-paying job in their new field.\n\nHours of Operation:\nMonday \u2013 Friday: 9:00 AM \u2013 5:00 PM",
            "website": "https://climbhire.co",
            "phone": "",
            "email": "",
            "cost_label": "Free (bash Upfront)",
            "nj_access": "Age: Typically 18–24",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "coop-careers-fellowship",
            "category": "Employment, Education & Career Development",
            "name": "COOP Careers",
            "location": "Greater NYC / Tri-State Commuting Area (accessible to Monmouth County)",
            "description": "A community-driven digital fellowship focused on launching careers in digital marketing, data analytics, and financial services for first-generation or low-income college graduates. They offer hybrid courses (combining live evening remote sessions with required monthly in-person regional programming).\n\nEligibility Note:\nCandidates must live within a two-hour commuting distance of New York City and meet underemployment criteria (unemployed, working less than 35 hours a week, or earning under 0,000/year), making it fully accessible to eligible Monmouth County residents.\n\nHours of Operation:\nMonday \u2013 Wednesday: 6:30 PM \u2013 9:30 PM (Live Sessions)",
            "website": "https://www.coopcareers.org",
            "phone": "",
            "email": "recruiting@coopcareers.org",
            "cost_label": "Free",
            "nj_access": "Age: 21+ (within 10 yrs of college graduation)",
            "last_verified": str(datetime.date.today())
        },
        {
            "id": "the-knowledge-house-tech",
            "category": "Employment, Education & Career Development",
            "name": "The Knowledge House",
            "location": "Greater NYC / Tri-State Area",
            "description": "A tech training and fellowship program providing comprehensive pathways in coding, software engineering, data science, web development, and user design. They offer hybrid and in-person courses.\n\nEligibility Note:\nWhile open to the broader tri-state area depending on specific fellowship grants (such as regional employer partnerships), applicants should verify local geographic and transit feasibility to physical hub locations, as some core tracks require regular in-person attendance.\n\nHours of Operation:\nMonday \u2013 Friday: 9:00 AM \u2013 5:00 PM",
            "website": "https://www.theknowledgehouse.org",
            "phone": "",
            "email": "info@theknowledgehouse.org",
            "cost_label": "Free",
            "nj_access": "Age: Varies by track (Youth 16–21, Adult 18+)",
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
            "description": (
                "Charitable pharmacy providing life-saving maintenance medications at zero cost to uninsured and underinsured community members.\n\n"
                "Hours of Operation:\n"
                "Monday, Tuesday & Thursday: 11:00 AM – 4:00 PM\n"
                "Friday: 10:00 AM – 3:00 PM\n"
                "Wednesday, Saturday & Sunday: Closed"
            ),
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
        },
        {
            "id": "linkedin-jobs",
            "category": "Employment, Education & Career Development",
            "name": "LinkedIn Jobs",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA professional networking and general job-search platform used across all industries, experience levels, and career stages. Connects job seekers with recruiters, enables direct applications, and supports professional brand building.",
            "website": "https://www.linkedin.com/jobs/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "indeed-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Indeed",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA massive, general job search engine aggregating listings across every major industry, including healthcare, administration, customer service, education, and entry-level to executive roles.",
            "website": "https://www.indeed.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "glassdoor-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Glassdoor",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA comprehensive job-search engine that combines open job listings with anonymous employee reviews, salary estimates, company culture insights, and interview preparation resources.",
            "website": "https://www.glassdoor.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "monster-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Monster",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA traditional global job board featuring open employment opportunities across diverse commercial and corporate sectors.",
            "website": "https://www.monster.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "careerbuilder-jobs",
            "category": "Employment, Education & Career Development",
            "name": "CareerBuilder",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA general employment platform offering traditional job searches, resume hosting tools, salary tracking, and personalized job matching across various industries.",
            "website": "https://www.careerbuilder.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "ziprecruiter-jobs",
            "category": "Employment, Education & Career Development",
            "name": "ZipRecruiter",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA fast-matching job board that uses automated AI algorithms to push job openings to candidates and distribute applications directly to multiple employers at once.",
            "website": "https://www.ziprecruiter.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "simplyhired-jobs",
            "category": "Employment, Education & Career Development",
            "name": "SimplyHired",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA straightforward job aggregation platform that pulls listings from employers, staffing agencies, and company career sites across multiple standard industries.",
            "website": "https://www.simplyhired.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "the-muse-jobs",
            "category": "Employment, Education & Career Development",
            "name": "The Muse",
            "location": "Online / Digital Platform",
            "description": "Job Focus: In-Person, Hybrid & Remote\n\nWebsite Purpose:\nA career guidance and job-search platform that focuses heavily on company culture, behind-the-scenes workplace spotlights, and career coaching alongside curated listings.",
            "website": "https://www.themuse.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "idealist-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Idealist",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Non-Profit & Social Impact (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nA specialized job board dedicated exclusively to the non-profit, mission-driven, and social impact sector, featuring full-time jobs, internships, and volunteer opportunities.",
            "website": "https://www.idealist.org/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "dice-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Dice",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Technology & IT (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nA specialized technology-focused job board designed specifically for IT professionals, software developers, cybersecurity experts, data engineers, and cloud infrastructure specialists.",
            "website": "https://www.dice.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "wellfound-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Wellfound",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Startups & Tech (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nA startup-focused job platform (formerly AngelList Talent) connecting candidates directly with early-stage and high-growth startup companies across tech, product, and business roles.",
            "website": "https://wellfound.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "built-in-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Built In",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Tech & Startups (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nA tech and startup employment platform that highlights local tech hubs, digital innovation ecosystems, company spotlights, and technical job openings.",
            "website": "https://builtin.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "welcome-to-the-jungle-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Welcome to the Jungle",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Tech & Creative (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nA modern employer branding and job platform focused on tech and startup companies, featuring immersive video profiles of work environments alongside open listings.",
            "website": "https://www.welcometothejungle.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "google-careers",
            "category": "Employment, Education & Career Development",
            "name": "Google Careers",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Tech, Engineering & Corporate (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nThe official corporate employment portal for Google, featuring technical, engineering, product, operations, and business roles worldwide.",
            "website": "https://www.google.com/about/careers/applications/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "we-work-remotely",
            "category": "Employment, Education & Career Development",
            "name": "We Work Remotely",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nOne of the largest dedicated remote-work communities, specializing in programming, design, customer support, and digital marketing roles that allow work from home.",
            "website": "https://weworkremotely.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "remote-ok-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Remote OK",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home (Tech & Digital)\n\nWebsite Purpose:\nA fast-moving remote job board featuring work-from-home positions in software engineering, design, writing, and digital operations.",
            "website": "https://remoteok.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "flexjobs-screened",
            "category": "Employment, Education & Career Development",
            "name": "FlexJobs",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote & Hybrid (Screened & Scam-Free)\n\nWebsite Purpose:\nA curated job platform that manually screens every single listing to guarantee 100% legitimate remote, hybrid, flexible schedule, and freelance opportunities without scams or multi-level marketing.",
            "website": "https://www.flexjobs.com/",
            "phone": "",
            "email": "",
            "cost_label": "Paid subscription",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "dynamite-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Dynamite Jobs",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA curated platform featuring remote-first companies and professional work-from-home positions across operations, tech, customer support, and marketing.",
            "website": "https://dynamitejobs.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "jobspresso-remote",
            "category": "Employment, Education & Career Development",
            "name": "Jobspresso",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA curated remote job board highlighting professional, high-quality work-from-home opportunities in tech, marketing, and customer service.",
            "website": "https://jobspresso.co/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "working-nomads-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Working Nomads",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA remote-work platform curated for digital professionals seeking work-from-home and location-flexible opportunities across various career tracks.",
            "website": "https://www.workingnomads.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "skipthedrive-jobs",
            "category": "Employment, Education & Career Development",
            "name": "SkipTheDrive",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA work-from-home job board that aggregates remote employment opportunities and provides telework calculators, guides, and tips.",
            "website": "https://www.skipthedrive.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "remote-co-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Remote.co",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA remote job platform organized strictly by professional category, offering resources and work-from-home listings for remote job seekers.",
            "website": "https://remote.co/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "remotehub-jobs",
            "category": "Employment, Education & Career Development",
            "name": "RemoteHub",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote & Freelance\n\nWebsite Purpose:\nA global remote work network combining work-from-home job listings, freelance project boards, and professional portfolio profiles.",
            "website": "https://www.remotehub.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "remoters-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Remoters",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA resource hub and job board designed specifically for professionals seeking work-from-home employment and remote career guides.",
            "website": "https://remoters.net/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "workew-jobs",
            "category": "Employment, Education & Career Development",
            "name": "Workew",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Remote / Work from Home\n\nWebsite Purpose:\nA remote job board focused on work-from-home opportunities in technology, marketing, customer care, and design.",
            "website": "https://workew.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "usajobs-civil-service",
            "category": "Employment, Education & Career Development",
            "name": "USAJOBS",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Federal Civil Service & Government (In-Person & Remote)\n\nWebsite Purpose:\nThe official federal government employment portal for finding and applying to civil service jobs across federal agencies, departments, and public sectors in New Jersey and nationwide.",
            "website": "https://www.usajobs.gov/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "government-jobs-portal",
            "category": "Employment, Education & Career Development",
            "name": "GovernmentJobs.com",
            "location": "Online / Digital Platform",
            "description": "Job Focus: State, County & Municipal Government (In-Person & Remote)\n\nWebsite Purpose:\nA specialized portal for finding and applying to public-sector career opportunities at local, municipal, county, and state government levels.",
            "website": "https://www.governmentjobs.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "apprenticeship-gov-dol",
            "category": "Employment, Education & Career Development",
            "name": "Apprenticeship.gov",
            "location": "Online / Digital Platform",
            "description": "Job Focus: Registered Apprenticeships & Paid Trade Training (In-Person)\n\nWebsite Purpose:\nAn official federal platform sponsored by the U.S. Department of Labor to help individuals find registered apprenticeships, earn-while-you-learn programs, and skilled trade career pathways.",
            "website": "https://www.apprenticeship.gov/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Statewide (NJ)",
            "last_verified": "2026-11-15"
        },
        {
            "id": "handshake-early-career",
            "category": "Employment, Education & Career Development",
            "name": "Handshake",
            "location": "Online / Digital Platform",
            "description": "Job Focus: College Students & Recent Graduates (In-Person, Hybrid & Remote)\n\nWebsite Purpose:\nThe premier career platform built specifically for college students and recent graduates, connecting early-career talent with entry-level jobs, internships, and campus recruiters.",
            "website": "https://joinhandshake.com/",
            "phone": "",
            "email": "",
            "cost_label": "Free",
            "nj_access": "Age: Early Career (Students & Grads)",
            "last_verified": "2026-11-15"
        },
            {
                "category": "Mental Health & Emotional Support",
                "name": "Monmouth ACTS — ResourceConnect",
                "cost_label": "Free",
                "description": "Program Overview:\nMonmouth County’s resource-navigation service. Residents can speak with someone who helps identify and connect them with local mental health services, counseling, substance-use support, housing assistance, and other community resources.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM",
                "website": "https://monmouthacts.org/",
                "id": "monmouth-acts-resourceconnect",
                "location": "Monmouth County (Countywide Resource Navigation)",
                "phone": "(732) 683-8959",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "Monmouth County Office of Mental Wellness and Supportive Services",
                "cost_label": "Free",
                "description": "Program Overview:\nCounty government office providing information and referrals for mental health and substance-use services. It advocates for residents who need help accessing services, assists with consumer concerns, and coordinates behavioral health resources throughout Monmouth County.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM",
                "website": "https://www.co.monmouth.nj.us/page.aspx?ID=5009",
                "id": "monmouth-office-mental-wellness",
                "location": "Freehold, NJ (Countywide Coordination)",
                "phone": "(732) 431-6451",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "Mental Health Association of Monmouth County",
                "cost_label": "Free  ·  Low-cost options (Program dependent)",
                "description": "Program Overview:\nA local nonprofit organization offering mental health education, family support, community-based assistance, recovery resources, and outpatient treatment programs that feature insurance/self-pay and sliding-scale options.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM",
                "website": "https://www.mentalhealthmonmouth.org/",
                "id": "mental-health-association-monmouth",
                "location": "119 Ave of the Commons, Suite 203, Shrewsbury, NJ 07702",
                "phone": "(732) 542-6422",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "CONTACT of Ocean & Monmouth Counties",
                "cost_label": "Free",
                "description": "Program Overview:\nProvides free, confidential emotional support through trained volunteer listeners. Individuals can call when they feel lonely, overwhelmed, depressed, distressed, or simply need someone to listen, alongside referrals to community resources.\n\nHours:\n24/7, subject to volunteer availability",
                "website": "https://contactoceanmonmouth.org/",
                "id": "contact-ocean-monmouth",
                "location": "Monmouth & Ocean Counties (24/7 Support Line)",
                "phone": "(732) 240-6100 · Toll-Free: (800) 272-4630",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "NAMI Greater Monmouth",
                "cost_label": "Free",
                "description": "Program Overview:\nLocal affiliate of the National Alliance on Mental Illness offering peer-led mental health support groups, family support groups, education, and community resources for individuals and families affected by mental health conditions.\n\nHours:\nMeeting schedules vary by group (consult website for calendar)",
                "website": "https://www.namigm.org/",
                "id": "nami-greater-monmouth",
                "location": "Monmouth County (Community Support Groups & Virtual)",
                "phone": "(732) 414-2422",
                "email": ""
            },
            {
                "category": "Healthcare & Medical Resources",
                "name": "YMCA of the Jersey Shore — Counseling & Social Services",
                "cost_label": "Low-cost options · Paid service (Insurance dependent · Sliding-scale available)",
                "description": "Program Overview:\nProvides confidential counseling and behavioral health services for children, adolescents, adults, and families, including individual, family, and group counseling, psychiatric services (accessed through clinical staff for clients receiving counseling), and substance-use support. Sliding-scale fees are available.",
                "website": "https://ymcanj.org/locations/counseling-social-services/",
                "id": "ymca-counseling-social-services",
                "location": "Centers in Freehold, Matawan & Shrewsbury, NJ",
                "phone": "(732) 671-5505",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "CPC Integrated Health",
                "cost_label": "Low-cost options · Paid service (Insurance dependent · Sliding-scale available)",
                "description": "Program Overview:\nA nonprofit behavioral health organization providing outpatient mental health and substance-use treatment for children, adolescents, adults, and families, including individual therapy, group counseling, psychiatric evaluations, and medication monitoring.\n\nHours:\nMonday – Thursday: 8:00 AM – 8:00 PM\nFriday: 8:00 AM – 5:00 PM",
                "website": "https://cpcintegratedhealth.org/",
                "id": "cpc-integrated-health",
                "location": "Outpatient Centers in Red Bank, Aberdeen & Freehold, NJ",
                "phone": "(732) 842-2000",
                "email": ""
            },
            {
                "category": "Healthcare & Medical Resources",
                "name": "Monmouth Family Health Center — Behavioral Health",
                "cost_label": "Cost not verified (Sliding-scale fee available based on income)",
                "description": "Program Overview:\nA community health center in Long Branch providing behavioral health services, including individual therapy, couples counseling, medication-management coordination, and referrals to higher levels of care and substance-use treatment.\n\nHours:\nMonday – Friday: 9:00 AM – 5:00 PM",
                "website": "https://www.mfhcnj.org/patient-services/behavioral-health",
                "id": "monmouth-family-health-behavioral",
                "location": "270 Broadway, Long Branch, NJ 07740",
                "phone": "(732) 923-7100",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "Wholehearted Healing Collective",
                "cost_label": "Low-cost options · Paid service (Insurance dependent · Sliding-scale options)",
                "description": "Program Overview:\nA West Long Branch counseling practice offering individual therapy, couples counseling, family therapy, group counseling, and specialized mental wellness programming accepting private insurance and self-pay with sliding-scale options.\n\nHours:\nBy appointment",
                "website": "https://wholeheartedhc.org/",
                "id": "wholehearted-healing-collective",
                "location": "86 Monmouth Rd, West Long Branch, NJ 07764",
                "phone": "(732) 852-7377",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "Monmouth Medical Center — Psychiatric Emergency Screening Services (PESS)",
                "cost_label": "Paid service (Emergency assistance available regardless of ability to pay)",
                "description": "Program Overview:\nMonmouth County’s designated psychiatric emergency screening service providing crisis assessments, psychiatric evaluations, emergency intervention, stabilization, mobile outreach, family crisis services, and a 24-hour crisis hotline.\n\nHours:\n24/7 Availability",
                "website": "https://www.rwjbh.org/monmouth-medical-center/treatment-care/mental-health-and-behavioral-health/mental-health-services/psychiatric-emergency-screening-services/",
                "id": "monmouth-medical-pess",
                "location": "300 Second Ave, Long Branch, NJ 07740",
                "phone": "(732) 923-6999 (24/7 Crisis Hotline & Mobile Screening)",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "Monmouth Medical Center — Early Intervention Support Services (EISS)",
                "cost_label": "Cost not verified (Rapid-access outpatient program)",
                "description": "Program Overview:\nProvides up to 30 days of rapid-access outpatient mental health treatment for Monmouth County residents age 18 and older who need immediate support to avoid hospital-based care and can safely receive treatment in the community. Services include therapy, medication evaluation, recovery planning, and connections to community resources.\n\nHours:\nOn-call staff available 24/7\ncontact the program for treatment and walk-in hours.",
                "website": "https://www.rwjbh.org/monmouth-medical-center/treatment-care/mental-health-and-behavioral-health/mental-health-services/early-intervention-support-services-eiss-/",
                "id": "monmouth-medical-eiss",
                "location": "3301 Route 66, Neptune, NJ 07753",
                "phone": "(732) 923-6500",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "PerformCare — Children’s System of Care",
                "cost_label": "Free to call; service costs and coverage vary",
                "description": "Program Overview:\nNew Jersey’s access point for publicly funded behavioral health, substance-use treatment, and intellectual/developmental disability services for eligible youth and their families. Behavioral-health services primarily serve youth age 5 until their 21st birthday, with eligibility varying by service.\n\nHours:\n24/7 Availability",
                "website": "https://www.performcarenj.org/",
                "id": "performcare-childrens-system",
                "location": "Statewide (New Jersey)",
                "phone": "(877) 652-7624 (24/7 Toll-Free Access Line)",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "180 Turning Lives Around",
                "cost_label": "Free",
                "description": "Program Overview:\nA Monmouth County-based nonprofit supporting survivors of domestic violence and sexual violence by providing free, confidential services including counseling, legal advocacy, emergency shelter, and 24/7 hotlines.\n\nHours:\n24/7 Hotlines & Emergency Services\nOffice: Monday – Friday: 9:00 AM – 5:00 PM",
                "website": "https://180nj.org/",
                "id": "180-turning-lives-around",
                "location": "Monmouth County (Confidential Locations & Countywide Outreach)",
                "phone": "(888) 843-9262 (24/7 Domestic Violence) · (888) 264-7273 (24/7 Sexual Assault) · Office: (732) 264-4111",
                "email": ""
            },
            {
                "category": "Mental Health & Emotional Support",
                "name": "2NDFLOOR — New Jersey Youth Helpline",
                "cost_label": "Free",
                "description": "Program Overview:\nA free, confidential, and anonymous emotional support text and call line for New Jersey youth and young adults ages 10–24 to talk about mental health, family challenges, relationships, and school stress (subject to mandatory reporting obligations regarding abuse and harm to self or others).\n\nHours:\n24/7 Availability",
                "website": "https://www.2ndfloor.org/",
                "id": "2ndfloor-youth-helpline",
                "location": "Statewide (New Jersey)",
                "phone": "1-888-222-2228 (Call or Text 24/7)",
                "email": ""
            },
    ]


# Approved online mental health resources are retained during every update.
APPROVED_WELLNESS_RESOURCES = [{'id': 'wellness-black-female-therapists', 'name': 'Black Female Therapists', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Provider Fees Vary (Sliding-Scale & Insurance Options)', 'area': 'Nationwide Directory (Includes New Jersey Licensed Clinicians)', 'location': 'Online Directory', 'phone': 'Contact individual therapists via directory', 'website': 'https://www.blackfemaletherapists.com/directory', 'email': '', 'description': 'Service Area:\nNationwide Directory (Includes New Jersey Licensed Clinicians)\n\nService Focus:\nCulturally Responsive Care · Anxiety · Depression · Trauma · Relationships · Emotional Wellness\n\nProgram Overview:\nAn online directory helping individuals connect with Black female mental-health professionals. Users can search and filter by location, insurance participation, virtual or in-person sessions, sliding-scale availability, and clinical specialties.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-melanin-mental-health', 'name': 'Melanin & Mental Health', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Provider Fees Vary (Sliding-Scale Options)', 'area': 'Nationwide & New Jersey Directory Listings', 'location': 'Online Directory', 'phone': 'Contact individual providers via directory', 'website': 'https://www.melaninandmentalhealth.com/directory-therapists/', 'email': '', 'description': 'Service Area:\nNationwide & New Jersey Directory Listings\n\nService Focus:\nCulturally Competent Care · BIPOC Mental Health · Therapist Matching\n\nProgram Overview:\nPromotes culturally responsive mental health care for communities of color. Its "Find a Therapist" directory allows users to filter by state, treatment modality, concerns addressed, meeting format, age range, language, and clinician background.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-dear-black-women-project', 'name': 'Dear Black Women Project', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Educational & Resource Access', 'area': 'Online Resource Hub (Accessible Countywide)', 'location': 'Online Resource Hub', 'phone': 'Online platform / links to national crisis lines', 'website': 'https://dearblackwomenproject.com/', 'email': '', 'description': 'Service Area:\nOnline Resource Hub (Accessible Countywide)\n\nService Focus:\nMental Health Education · Directory Referrals · Crisis Lifelines · Self-Care Support\n\nProgram Overview:\nAn affirmative wellness and mental health resource hub connecting Black women with therapist directories, crisis hotlines, LGBTQIA+-affirming organizations, and self-care materials.\n\nHours:\nWebsite accessible 24/7'}, {'id': 'wellness-black-mental-wellness', 'name': 'Black Mental Wellness', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Educational & Directory Access', 'area': 'Nationwide Online Resource (Accessible Countywide)', 'location': 'Online Resource Hub', 'phone': 'Contact through website', 'website': 'https://www.blackmentalwellness.com/', 'email': '', 'description': 'Service Area:\nNationwide Online Resource (Accessible Countywide)\n\nService Focus:\nMental Health Education · Evidence-Based Fact Sheets · Therapist Directory Referrals\n\nProgram Overview:\nAn organization dedicated to increasing mental health awareness and culturally responsive information for Black communities through evidence-based educational materials and curated links to clinician directories.\n\nHours:\nWebsite accessible 24/7'}, {'id': 'wellness-the-black-girl-doctor', 'name': 'The Black Girl Doctor', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Private Practice Fees Vary (Insurance & Self-Pay Options)', 'area': 'Virtual Practice (Clinicians Licensed in Select States, Including NJ)', 'location': 'Virtual Psychology Practice', 'phone': 'Contact via online inquiry', 'website': 'https://theblackgirldoctor.com/', 'email': '', 'description': 'Service Area:\nVirtual Practice (Clinicians Licensed in Select States, Including NJ)\n\nService Focus:\nIndividual Therapy · Couples Counseling · Wellness Coaching · Racial Trauma · Burnout\n\nProgram Overview:\nA virtual psychology practice emphasizing culturally responsive mental health care tailored to Black women and professionals, addressing anxiety, career stress, perfectionism, and life transitions.\n\nHours:\nBy appointment'}, {'id': 'wellness-national-association-of-black-counselors-nabc', 'name': 'National Association of Black Counselors (NABC)', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Counseling Fees Vary by Clinician', 'area': 'National Directory (Searchable by New Jersey Licensure)', 'location': 'Online Directory', 'phone': 'Contact individual counselors via directory', 'website': 'https://www.nabcounselors.org/', 'email': '', 'description': 'Service Area:\nNational Directory (Searchable by New Jersey Licensure)\n\nService Focus:\nCounselor Search · Professional Resources · Culturally Responsive Counseling\n\nProgram Overview:\nA national professional association connecting clients with Black mental health counselors. Its "Find a Counselor" directory filters professionals by credentials, state licensure, and clinical specialties.\n\nHours:\nWebsite accessible 24/7; clinician appointment hours vary'}, {'id': 'wellness-association-of-black-psychologists-abpsi', 'name': 'Association of Black Psychologists (ABPsi)', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Online Information · Program/Provider Fees Vary', 'area': 'National Organization with Virtual Programs', 'location': 'Online Organization & Resource Hub', 'phone': 'Contact via website', 'website': 'https://abpsi.org/', 'email': '', 'description': 'Service Area:\nNational Organization with Virtual Programs\n\nService Focus:\nAfrican-Centered Psychology · Sawubona Healing Circles · Black Wellness Directory\n\nProgram Overview:\nA professional organization advancing Black psychology and community well-being. Features community healing circles, educational resources, and clinician networking through its wellness directory.\n\nHours:\nWebsite accessible 24/7; event schedules vary'}, {'id': 'wellness-boris-lawrence-henson-foundation', 'name': 'Boris Lawrence Henson Foundation', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free (Up to 5 Free Therapy Sessions for Accepted Applicants)', 'area': 'Nationwide (Open to Eligible New Jersey Residents)', 'location': 'Online Support Programs', 'phone': 'Contact via website', 'website': 'https://borislhensonfoundation.org/', 'email': '', 'description': 'Service Area:\nNationwide (Open to Eligible New Jersey Residents)\n\nService Focus:\nFree Therapy Vouchers · Youth & HBCU Wellness · Stigma Reduction\n\nProgram Overview:\nFounded by Taraji P. Henson to eradicate mental health stigma in Black communities. Offers free therapy assistance covering up to five sessions with licensed, culturally competent providers during open enrollment periods.\n\nHours:\nWebsite accessible 24/7; enrollment cycles open quarterly'}, {'id': 'wellness-african-american-behavioral-health-center-of-excellence', 'name': 'African American Behavioral Health Center of Excellence', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Public Resources · Training Fees May Apply', 'area': 'Nationwide Educational & Training Resource', 'location': 'Online Resource & Training Center', 'phone': 'Contact via website', 'website': 'https://africanamericanbehavioralhealth.org/', 'email': '', 'description': 'Service Area:\nNationwide Educational & Training Resource\n\nService Focus:\nBehavioral Health Workforce Training · Technical Assistance · Trauma-Informed Care\n\nProgram Overview:\nA SAMHSA-funded national center providing training, evidence-based research, and toolkits to help healthcare organizations and clinicians deliver culturally responsive behavioral health services.\n\nHours:\nWebsite accessible 24/7; scheduled webinars vary'}, {'id': 'wellness-national-queer-and-trans-therapists-of-color-network-nqttcn', 'name': 'National Queer and Trans Therapists of Color Network (NQTTCN)', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Provider Fees Vary (Sliding-Scale & Mental Health Fund)', 'area': 'Nationwide Directory (Includes New Jersey Providers)', 'location': 'Online Directory', 'phone': 'Contact individual therapists via directory', 'website': 'https://nqttcn.com/directory/', 'email': '', 'description': 'Service Area:\nNationwide Directory (Includes New Jersey Providers)\n\nService Focus:\nQTBIPOC Mental Health · Affirming Psychotherapy · Financial Assistance Fund\n\nProgram Overview:\nA healing justice organization committed to transforming mental health for queer and trans Black, Indigenous, and people of color. Features a searchable directory of QTBIPOC practitioners and periodic funding assistance.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-lgbtqia-health-nj-provider-directory', 'name': 'LGBTQIA+ Health NJ — Provider Directory', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Provider Fees Vary (Accepts Medicaid & Low-Cost Filters)', 'area': 'Statewide New Jersey (Searchable by Monmouth County & Telehealth)', 'location': 'Online Directory', 'phone': 'Contact individual clinicians via directory', 'website': 'https://www.lgbtqiahealthnj.org/directory', 'email': '', 'description': 'Service Area:\nStatewide New Jersey (Searchable by Monmouth County & Telehealth)\n\nService Focus:\nAffirming Mental Health Care · Psychotherapy · Psychiatric Care · Gender-Affirming Support\n\nProgram Overview:\nA dedicated New Jersey 501(c)(3) directory linking LGBTQIA+ residents with trained affirming healthcare and behavioral health providers. Search by county, telehealth availability, insurance, and sliding-scale options.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-alma', 'name': 'Alma', 'category': 'Mental Health & Emotional Support', 'cost_label': 'In-Network Insurance Accepted · Copays / Self-Pay Vary by Plan', 'area': 'New Jersey Statewide (Virtual & In-Person Providers)', 'location': 'Online Platform', 'phone': 'Contact individual clinicians via directory', 'website': 'https://helloalma.com/', 'email': '', 'description': 'Service Area:\nNew Jersey Statewide (Virtual & In-Person Providers)\n\nService Focus:\nIndividual Therapy · Couples Counseling · Psychiatric Evaluation · Medication Management\n\nProgram Overview:\nA mental health platform helping people find in-network therapists and psychiatric prescribers licensed in New Jersey. Filter by insurance carrier, cultural background, clinical specialty, and virtual care.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-american-psychological-association-psychologist-locator', 'name': 'American Psychological Association — Psychologist Locator', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Clinician Fees Vary (Insurance / Self-Pay)', 'area': 'Nationwide Directory (Searchable by New Jersey City / Zip)', 'location': 'Online Directory', 'phone': 'Contact individual psychologists via directory', 'website': 'https://locator.apa.org/', 'email': '', 'description': "Service Area:\nNationwide Directory (Searchable by New Jersey City / Zip)\n\nService Focus:\nLicensed Psychologists · Clinical Assessment · Psychological Testing · Psychotherapy\n\nProgram Overview:\nThe APA's official national locator tool connecting individuals with licensed doctoral-level psychologists across New Jersey. Filter by clinical specialty, age group, and treatment approach.\n\nHours:\nWebsite accessible 24/7; clinician appointment hours vary"}, {'id': 'wellness-clinicians-of-color-directory', 'name': 'Clinicians of Color Directory', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Provider Fees Vary (Sliding-Scale & Insurance Available)', 'area': 'Nationwide & New Jersey Statewide Directory', 'location': 'Online Directory', 'phone': 'Contact individual clinicians via directory', 'website': 'https://www.cliniciansofcolor.org/', 'email': '', 'description': 'Service Area:\nNationwide & New Jersey Statewide Directory\n\nService Focus:\nDiverse Clinician Matching · BIPOC Mental Health · Culturally Competent Psychotherapy\n\nProgram Overview:\nAn inclusive directory connecting clients with therapists of color. Search filters include race/ethnicity, clinical focus, accepted insurance, sliding-scale availability, and in-person or telehealth formats in NJ.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-african-american-therapists-directory', 'name': 'African American Therapists Directory', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Directory Access · Provider Fees Vary', 'area': 'Nationwide & Regional East Coast / New Jersey Listings', 'location': 'Online Directory', 'phone': 'Contact individual therapists via directory', 'website': 'https://africanamericantherapists.com/african-american-therapists-directory/', 'email': '', 'description': 'Service Area:\nNationwide & Regional East Coast / New Jersey Listings\n\nService Focus:\nAfrican American Psychologists · Marriage & Family Therapists · Licensed Counselors\n\nProgram Overview:\nAn online directory organizing Black mental health professionals by region and major metro areas, including New Jersey suburbs and nearby metropolitan centers.\n\nHours:\nWebsite accessible 24/7; provider appointment hours vary'}, {'id': 'wellness-beam-black-emotional-and-mental-health-collective', 'name': 'BEAM — Black Emotional and Mental Health Collective', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Public Resources & Healing Circles · Check Specific Programs', 'area': 'Nationwide Online Organization (Accessible to NJ Residents)', 'location': 'Online Wellness Community', 'phone': 'Contact via website', 'website': 'https://beam.community/', 'email': '', 'description': 'Service Area:\nNationwide Online Organization (Accessible to NJ Residents)\n\nService Focus:\nPeer Support Circles · Emotional Wellness · Healing Justice · Mental Health Education\n\nProgram Overview:\nA national training and advocacy collective offering community healing circles (Heart Space), peer support spaces, psychoeducational toolkits, and virtual mental wellness workshops designed for Black communities.\n\nHours:\nWebsite accessible 24/7; workshop and circle schedules vary'}, {'id': 'wellness-bad-b-ches-have-bad-days-too', 'name': 'Bad B**ches Have Bad Days Too', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free to Access (Costs for External Services Vary)', 'area': 'Online Resource Hub (Accessible Countywide)', 'location': 'Online Resource Hub', 'phone': 'Online platform / links to national crisis lines', 'website': 'https://tinyurl.com/BBHBDTMTS', 'email': '', 'description': 'Service Area:\nOnline Resource Hub (Accessible Countywide)\n\nService Focus:\nFree & Affordable Therapy Links · BIPOC Mental Health · Crisis Lifelines · LGBTQIA+ Helplines\n\nProgram Overview:\nA curated mental health resource platform created to dismantle mental health stigma for women of color and underserved groups. Connects visitors with low-cost therapy networks, crisis lifelines, and wellness tools.\n\nHours:\nWebsite accessible 24/7'}, {'id': 'wellness-anxiety-is-watching-me', 'name': 'Anxiety Is Watching Me', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free to Access (Costs for External Services Vary)', 'area': 'Online Resource Hub (Accessible Countywide)', 'location': 'Online Resource Hub', 'phone': 'Online platform / links to community resources', 'website': 'https://anxietyiswatchingme.com/', 'email': '', 'description': 'Service Area:\nOnline Resource Hub (Accessible Countywide)\n\nService Focus:\nAnxiety Navigation · Intersectional Mental Health Directories · Community Healing\n\nProgram Overview:\nAn online resource hub that aggregates culturally affirmative mental health organizations and support networks across Black, LGBTQIA+, AAPI, Indigenous, and Latine communities.\n\nHours:\nWebsite accessible 24/7'}, {'id': 'wellness-black-women-s-mental-health-institute-bwmhi', 'name': 'Black Women’s Mental Health Institute (BWMHI)', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free Sister Support Meetups & Community Wellness Groups · Virtual Registration Required', 'area': 'National Virtual Programs (Accessible to Monmouth County Residents)', 'location': 'Online Community Programs', 'phone': 'Contact via website', 'website': 'https://www.bwmhi.org/', 'email': '', 'description': 'Service Area:\nNational Virtual Programs (Accessible to Monmouth County Residents)\n\nService Focus:\nPsychoeducational Support Groups · Sister Support Meetups · Mental Health Education\n\nProgram Overview:\nA dedicated organization offering virtual peer support groups, monthly Sister Support meetups, and psychoeducational workshops aimed at strengthening emotional wellness for Black women and young adults.\n\nHours:\nWebsite accessible 24/7; monthly meetup schedules vary'}]

# Approved community updates take precedence over legacy pantry aliases.
APPROVED_COMMUNITY_RESOURCES = [{'id': 'catholic-charities-diocese-of-trenton', 'name': 'Catholic Charities — Diocese of Trenton', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Open to All Monmouth County Residents', 'location': '145 Maple Ave, Red Bank, NJ 07701', 'phone': '(800) 360-7711 (Access, Help and Information Center)', 'website': 'https://www.catholiccharitiestrenton.org/locations/monmouth-county/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nEmergency Assistance · Case Management · Community Support\n\nProgram Overview:\nProvides multi-faceted social support services across Monmouth County, including parish-referred emergency financial assistance, case management, and resource referrals for individuals and families facing adversity.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM'}, {'id': 'monmouth-county-division-of-social-services', 'name': 'Monmouth County Division of Social Services', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Open to All Monmouth County Residents (Income eligibility applies to specific benefit programs)', 'location': '3000 Kozloski Rd, Freehold, NJ 07728', 'phone': '(732) 431-6000', 'website': 'http://www.visitmonmouth.com/socialservices', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nPublic Benefits · Emergency Assistance · Housing Assistance · Medicaid & SNAP\n\nProgram Overview:\nThe county welfare and social services agency providing financial assistance, safety-net programs, emergency aid, food assistance (SNAP), medical coverage (Medicaid), temporary cash assistance (TANF/GA), and housing support services for eligible county residents.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM'}, {'id': 'interfaith-neighbors', 'name': 'Interfaith Neighbors', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Monmouth County Working Households Facing Housing Crisis', 'location': '810 4th Ave, Asbury Park, NJ 07712', 'phone': '(732) 775-0525 ext. 198', 'website': 'https://interfaithneighbors.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nRental & Mortgage Arrears · Eviction Prevention · Security Deposit Assistance\n\nProgram Overview:\nProvides emergency rental, mortgage, and utility assistance to working Monmouth County families facing sudden financial crises, helping prevent eviction and homelessness while fostering long-term stability.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM'}, {'id': 'carc-community-affairs-and-resource-center', 'name': 'CARC — Community Affairs and Resource Center', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Open to All Monmouth County Residents', 'location': '913 Sewall Ave, Asbury Park, NJ 07712', 'phone': '(732) 774-3282', 'website': 'https://carcnj.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nBilingual Social Services · Energy Assistance (LIHEAP) · Housing Counseling · Eviction Prevention\n\nProgram Overview:\nA comprehensive community action agency offering bilingual support, LIHEAP energy assistance, housing counseling, employment services, and citizenship assistance to underserved and immigrant communities in Monmouth County.\n\nHours:\nMonday – Friday: 9:00 AM – 5:00 PM'}, {'id': 'auto-scraped-921', 'name': 'Middletown Helps Its Own', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Middletown Township Residents Only', 'location': '121 Port Monmouth Rd, Middletown, NJ 07748', 'phone': '(732) 787-3604', 'website': 'https://middletownhelpsitsown.com/', 'email': '', 'area': 'Middletown Township (including Belford, Leonardo, Lincroft, Navesink, Port Monmouth, and Middletown-area sections)', 'description': 'Towns Served:\nMiddletown Township (including Belford, Leonardo, Lincroft, Navesink, Port Monmouth, and Middletown-area sections)\n\nService Focus:\nEmergency Food Assistance · Community Outreach\n\nProgram Overview:\nAn all-volunteer community organization delivering emergency non-perishable groceries and holiday food baskets directly to Middletown families, seniors, and disabled neighbors experiencing emergency hardship.\n\nHours:\nCall for distribution schedule and intake'}, {'id': 'morganville-united-methodist-church', 'name': 'Morganville United Methodist Church', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Local Area Residents Facing Hardship', 'location': '215 Conover Rd, Morganville, NJ 07751', 'phone': '(732) 946-4247', 'website': '', 'email': '', 'area': 'Morganville & Marlboro Township', 'description': 'Towns Served:\nMorganville & Marlboro Township\n\nService Focus:\nEmergency Community Assistance · Benevolence Fund · Utility & Rent Referrals\n\nProgram Overview:\nCommunity church ministry offering local benevolence funds, emergency support, and direct community referrals for families in Morganville and Marlboro experiencing sudden financial or basic-needs distress.\n\nHours:\nCall church office for pastoral assistance and referral intake'}, {'id': 'navicore-solutions', 'name': 'Navicore Solutions', 'category': 'New Jersey & Local Community Resources', 'cost_label': 'Free / Sliding Scale', 'nj_access': 'Open to All Monmouth County & NJ Residents', 'location': '200 Route 9, Manalapan, NJ 07726', 'phone': '(732) 409-6281 ext. 80455', 'website': 'https://navicoresolutions.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nFinancial Counseling · Housing Counseling · Budget Coaching · Credit Guidance\n\nProgram Overview:\nA national HUD-approved nonprofit counseling agency based in Manalapan offering comprehensive financial health guidance, personal budgeting assistance, pre-purchase and rental housing counseling, and debt management services.\n\nHours:\nMonday – Friday: 8:30 AM – 5:00 PM'}, {'id': 'family-support-organization-of-monmouth-county', 'name': 'Family Support Organization of Monmouth County', 'category': 'Mental Health & Emotional Support', 'cost_label': 'Free', 'nj_access': 'Parents and Caregivers of Children with Behavioral or Emotional Challenges', 'location': '187 Hwy 36, Suite 210, West Long Branch, NJ 07764', 'phone': '(732) 542-2502', 'website': 'https://www.fsoofmonmouth.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nFamily Peer Support · Mental Health Navigation · Parent Support Groups · Youth Advocacy\n\nProgram Overview:\nA family-run, county-based nonprofit providing peer-to-peer support, advocacy, education, and guidance for parents and caregivers raising children with emotional, behavioral, developmental, or mental health challenges.\n\nHours:\nMonday – Friday: 9:00 AM – 5:00 PM'}, {'id': 'lunch-break-family-promise-of-monmouth-county', 'name': 'Lunch Break — Family Promise of Monmouth County', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Monmouth County Families with Minor Children', 'location': '121 Drs James Parker Blvd, Red Bank, NJ 07701', 'phone': '(732) 495-1050 · (732) 747-8577', 'website': 'https://lunchbreak.org/family-promise/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nFamily Homelessness Prevention · Emergency Shelter Network · Stabilization\n\nProgram Overview:\nA dedicated partnership program preventing family homelessness and providing shelter, compassionate case management, financial literacy, and rapid re-housing support to families with minor children experiencing housing crises.\n\nHours:\nMonday – Friday: 8:30 AM – 4:00 PM'}, {'id': 'emergency-housing-assistance-program-ehap', 'name': 'Emergency Housing Assistance Program (EHAP)', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Income Eligibility Required', 'location': '3000 Kozloski Rd, Freehold, NJ 07728', 'phone': '(732) 431-6000 ext. 4613', 'website': 'http://www.visitmonmouth.com/socialservices', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nEmergency Shelter Placement · Motel Vouchers · Eviction Prevention\n\nProgram Overview:\nCounty-administered program delivering rapid emergency housing placement, temporary motel vouchers, and supportive diversion counseling for individuals and families who are literally homeless or facing imminent displacement.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM (24/7 emergency placement via NJ 211)'}, {'id': 'love-thy-neighbor', 'name': 'Love Thy Neighbor', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Local Families in Need', 'location': 'Long Branch, NJ 07740', 'phone': '(732) 542-7012', 'website': 'https://lovethyneighbornj.org/', 'email': '', 'area': 'Long Branch, West Long Branch, Oceanport, Monmouth Beach, and Coastal Monmouth', 'description': 'Towns Served:\nLong Branch, West Long Branch, Oceanport, Monmouth Beach, and Coastal Monmouth\n\nService Focus:\nCommunity Care · Essential Household Support · Clothing & Furnishings\n\nProgram Overview:\nFaith-based community outreach initiative delivering practical household furnishings, basic life essentials, clothing, and personalized assistance directly to local families rebuilding after financial or personal crisis.\n\nHours:\nCall for appointment and intake'}, {'id': 'habcore', 'name': 'HABcore', 'category': 'Family & Support Services', 'cost_label': 'Free / Subsidized', 'nj_access': 'Low-Income Individuals with Special Needs or Experiencing Homelessness', 'location': '280 Broadway, Long Branch, NJ 07740', 'phone': '(732) 544-1975', 'website': 'https://habcore.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nSupportive Housing · Housing Stability · Boarding Home Care · Veteran Placements\n\nProgram Overview:\nProvides permanent supportive housing, safe boarding home placements, and individualized stability services for homeless individuals, veterans, and individuals living with disabilities or special needs across Monmouth County.\n\nHours:\nMonday – Friday: 9:00 AM – 5:00 PM'}, {'id': 'garden-state-home-street-outreach', 'name': 'Garden State Home — Street Outreach', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Households At or Below 120% AMI (Section 8 & Undocumented Populations Fully Eligible)', 'location': '141 Raritan Ave, Highland Park, NJ 08904 (Direct Monmouth Outreach Field Staff)', 'phone': '(732) 532-6865', 'website': 'https://www.gardenstatehome.org/street-outreach', 'email': 'info@gardenstatehome.org', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nStreet Outreach · Homelessness Prevention · Direct Needs Assistance · Housing Stabilization\n\nProgram Overview:\nEngages unsheltered households and those at imminent risk of homelessness, linking them directly to supportive housing services across Monmouth County. Staff provide direct basic-needs assistance including food, clothing, transportation, personal hygiene items, and stabilization case management.\n\nHours:\nMonday – Friday: 9:00 AM – 5:00 PM'}, {'id': 'welcome-home-foundation', 'name': 'Welcome Home Foundation', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Families & Individuals Transitioning Out of Homelessness', 'location': '100 Matawan Rd, Suite 325, Matawan, NJ 07747', 'phone': '(866) 943-1630 · (732) 807-5506', 'website': 'https://welcomehomefoundationnj.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nTransition Housing Support · Move-In Setup · Furniture & Dignified Home Packages\n\nProgram Overview:\nAssists families and individuals moving out of shelters or homelessness into permanent residences by delivering beds, household furnishings, kitchen essentials, and starter home goods to establish a dignified living environment.\n\nHours:\nCall for referral intake and program coordination'}, {'id': 'women-s-hospitality-network', 'name': "Women's Hospitality Network", 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Unaccompanied Single Women Experiencing Homelessness', 'location': 'Asbury Park, NJ 07712', 'phone': '(732) 481-4202', 'website': 'https://www.womenshospitalitynetwork.org/', 'email': '', 'area': 'Asbury Park, Neptune, and Coastal Monmouth Communities', 'description': 'Towns Served:\nAsbury Park, Neptune, and Coastal Monmouth Communities\n\nService Focus:\nEmergency Winter Shelter · Safe Haven · Supportive Case Management · Evening Respite\n\nProgram Overview:\nA coalition of community volunteers and faith communities providing seasonal overnight emergency shelter, warm meals, safe respite, and personalized advocacy for single, unaccompanied women experiencing homelessness in Monmouth County.\n\nHours:\nSeasonal Evening Intake: 5:30 PM – 7:30 PM; Administrative: Monday – Friday: 9:00 AM – 3:00 PM'}, {'id': 'iep-youth-services', 'name': 'IEP Youth Services', 'category': 'Family & Support Services', 'cost_label': 'Free / State-Referred', 'nj_access': 'Youth & Young Adults Ages 8–21', 'location': '705 Stone Rd, Freehold, NJ 07728', 'phone': '(732) 431-4997', 'website': 'https://iepyouthservices.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nResidential Youth Care · Transitional Living · Independent Living Skills\n\nProgram Overview:\nProvides safe residential facilities, independent living skills instruction, transitional housing, and intense clinical supportive counseling for at-risk, abused, abandoned, and homeless youth and young adults.\n\nHours:\nAdministrative: Monday – Friday: 9:00 AM – 5:00 PM (Residential crisis placements operate 24/7)'}, {'id': 'market-street-mission-jersey-shore-rescue-mission', 'name': 'Market Street Mission — Jersey Shore Rescue Mission', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Men in Need of Recovery & Local Neighbors in Crisis', 'location': '701 Memorial Dr, Asbury Park, NJ 07712', 'phone': '(732) 988-0242', 'website': 'https://www.marketstreet.org/jersey-shore/', 'email': '', 'area': 'Asbury Park, Neptune, and Surrounding Monmouth Communities', 'description': 'Towns Served:\nAsbury Park, Neptune, and Surrounding Monmouth Communities\n\nService Focus:\nAddiction Recovery Program · Emergency Shelter · Free Community Meals · Thrift Store\n\nProgram Overview:\nOperates a residential life-change and addiction recovery program for men, alongside nightly emergency shelter, daily free hot community meals, and thrift shop vouchers for local families in crisis.\n\nHours:\nDaily Community Dinners: 5:00 PM; Office & Intake: Monday – Friday: 9:00 AM – 5:00 PM'}, {'id': 'em-power-me-of-monmouth-county', 'name': 'Em-Power Me of Monmouth County', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Local Youth and Families', 'location': '1012B Springwood Ave, Asbury Park, NJ 07712', 'phone': '(732) 361-3606', 'website': '', 'email': 'empowermenj@gmail.com', 'area': 'Asbury Park, Neptune, and Surrounding Coastal Monmouth Communities', 'description': 'Towns Served:\nAsbury Park, Neptune, and Surrounding Coastal Monmouth Communities\n\nService Focus:\nCommunity Advocacy · Youth Mentoring · Family Resource Connections\n\nProgram Overview:\nA grassroots community organization offering direct family support, youth mentorship, workforce readiness guidance, and resource navigation for Asbury Park and Monmouth County residents.\n\nHours:\nMonday – Friday: 9:00 AM – 4:00 PM'}, {'id': 'hope-for-children-foundation-nj', 'name': 'Hope For Children Foundation NJ', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Children & Families with Critical Medical or Financial Needs', 'location': 'Marlboro, NJ 07746', 'phone': '(732) 834-9000', 'website': 'https://hopeforchildrenfoundationnj.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nPediatric Hardship Grants · Adaptive Medical Equipment · Emergency Micro-Aid\n\nProgram Overview:\nProvides emergency micro-grants, adaptive medical equipment funding, and tangible aid to Monmouth County families with children facing critical medical hardships, developmental challenges, or unforeseen family tragedies.\n\nHours:\nInquiries handled by phone and email'}, {'id': 'community-hope-supportive-services-for-veteran-families-ssvf', 'name': 'Community Hope — Supportive Services for Veteran Families (SSVF)', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Military Veterans and Veteran Families At or Below 50% AMI', 'location': 'Serving Monmouth County', 'phone': '(855) 483-8465 (Veteran Referral Hotline)', 'website': 'https://www.communityhope-nj.org/veterans-support/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nVeteran Rapid Re-Housing · Rental Subsidies · Utility Assistance · VA Benefit Advocacy\n\nProgram Overview:\nDedicated federally funded program providing rapid re-housing assistance, rental subsidies, emergency utility assistance, and comprehensive case management for veterans and their families who are homeless or at imminent risk of eviction.\n\nHours:\nMonday – Friday: 8:30 AM – 5:00 PM'}, {'id': 'soldier-on-supportive-services-for-veteran-families-ssvf', 'name': 'Soldier On — Supportive Services for Veteran Families (SSVF)', 'category': 'Family & Support Services', 'cost_label': 'Free', 'nj_access': 'Military Veterans and Veteran Families', 'location': 'Serving Monmouth County', 'phone': '(866) 406-8449', 'website': 'https://wesoldieron.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nVeteran Homelessness Prevention · Permanent Housing Placement · Peer Advocacy\n\nProgram Overview:\nProvides end-to-end supportive services to veterans, including permanent housing placement, landlord mediation, temporary financial assistance for rent/moving costs, and legal/health care advocacy.\n\nHours:\nMonday – Friday: 8:30 AM – 4:30 PM'}, {'id': 'auto-scraped-912', 'name': 'Salvation Army — Asbury Park Corps', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Coastal Monmouth Residents', 'location': '605 Asbury Ave, Asbury Park, NJ 07712', 'phone': '(732) 775-8698', 'website': 'https://newjersey.salvationarmy.org/NewJersey/asbury-park/asbury-avenue-corps/', 'email': '', 'area': 'Asbury Park, Neptune, Ocean Grove, Bradley Beach, Neptune City, Ocean Township, Allenhurst, Deal, and Loch Arbour', 'description': 'Towns Served:\nAsbury Park, Neptune, Ocean Grove, Bradley Beach, Neptune City, Ocean Township, Allenhurst, Deal, and Loch Arbour\n\nService Focus:\nFood Pantry · Emergency Assistance · Community Care\n\nProgram Overview:\nProvides emergency food assistance through an on-site choice food pantry, holiday assistance, and social support services for individuals and families in coastal Monmouth County.\n\nHours:\nFood Pantry: Thursday, 9:00 AM – 11:00 AM\nOffice Hours: Monday – Thursday, 9:00 AM – 3:00 PM; Friday, 9:00 AM – 12:00 PM'}, {'id': 'auto-scraped-957', 'name': 'Salvation Army — Red Bank Corps', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Northern & Central Monmouth Residents', 'location': '180 Newman Springs Rd, Red Bank, NJ 07701', 'phone': '(732) 747-1626', 'website': 'https://newjersey.salvationarmy.org/NewJersey/redbank', 'email': '', 'area': 'Red Bank, Fair Haven, Shrewsbury, Little Silver, Eatontown, Rumson, and Surrounding Communities', 'description': 'Towns Served:\nRed Bank, Fair Haven, Shrewsbury, Little Silver, Eatontown, Rumson, and Surrounding Communities\n\nService Focus:\nFood Pantry · Emergency Assistance · Case Management\n\nProgram Overview:\nProvides Monmouth County residents with a choice food pantry, emergency community resource assistance, and seasonal support programs by appointment.\n\nHours:\nFood Pantry & Office: Monday – Thursday, 9:00 AM – 3:30 PM (Call ahead for pantry appointment slots)'}, {'id': 'fn-02', 'name': 'St. Vincent de Paul Society — Regional Conferences', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Local Parish Area Residents', 'location': 'Network of Local Monmouth County Parish Conferences', 'phone': '(732) 224-1395 (St. Catharine Referral Line) · (732) 747-4180', 'website': 'https://stcatharine.net/st-vind-p', 'email': '', 'area': 'Local parish conference areas including Holmdel (St. Catharine), Long Branch (Christ the King), Eatontown (St. Dorothea), Keyport (St. Joseph), and surrounding neighborhoods', 'description': 'Towns Served:\nLocal parish conference areas including Holmdel (St. Catharine), Long Branch (Christ the King), Eatontown (St. Dorothea), Keyport (St. Joseph), and surrounding neighborhoods\n\nService Focus:\nFood Pantry · Direct Financial Assistance · Rental & Utility Aid\n\nProgram Overview:\nNetwork of parish-based volunteer groups offering person-to-person emergency assistance for local residents, including food distributions, direct financial aid for rent, utilities, and essential household expenses.\n\nHours:\nOperates on scheduled monthly distribution days or by appointment'}, {'id': 'auto-scraped-958', 'name': 'St. Crispin House / Saint Crispin Society', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Local Area Residents Facing Hardship', 'location': '121 Bridge Ave, Red Bank, NJ 07701', 'phone': '(732) 747-0813 x109', 'website': 'https://saintcrispinsociety.com/', 'email': '', 'area': 'Red Bank, Shrewsbury, and Surrounding Communities', 'description': 'Towns Served:\nRed Bank, Shrewsbury, and Surrounding Communities\n\nService Focus:\nCommunity Assistance · Food Pantry · Basic Needs Support\n\nProgram Overview:\nA community outreach initiative offering food pantry access, charitable aid, and emergency hardship support to community members facing severe economic challenges.\n\nHours:\nTuesday & Thursday: 10:00 AM – 12:00 PM'}, {'id': 'fn-01', 'name': 'Fulfill — The FoodBank of Monmouth & Ocean Counties', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Open to All Monmouth & Ocean County Residents', 'location': '3300 Rte 66, Neptune, NJ 07753', 'phone': '(732) 918-2600', 'website': 'https://fulfillnj.org/', 'email': '', 'area': 'Countywide (All 53 Monmouth County Municipalities)', 'description': 'Towns Served:\nCountywide (All 53 Monmouth County Municipalities)\n\nService Focus:\nRegional Food Distribution · SNAP Enrollment Assistance · Mobile Pantry Network\n\nProgram Overview:\nThe regional food distribution hub supplying food pantries across Monmouth County while providing on-site SNAP benefits enrollment counseling, culinary training, and mobile pantry stops.\n\nHours:\nMonday – Friday: 8:00 AM – 4:00 PM'}, {'id': 'monmouth-res-29', 'name': 'JBJ Soul Kitchen', 'category': 'Basic Needs & Assistance', 'cost_label': 'Pay-What-You-Can / Volunteer in Exchange', 'nj_access': 'Open to All', 'location': '207 Monmouth St, Red Bank, NJ 07701', 'phone': '(732) 842-0900', 'website': 'https://jbjsoulkitchen.org/', 'email': '', 'area': 'Open to All Monmouth County Residents & Visitors', 'description': 'Towns Served:\nOpen to All Monmouth County Residents & Visitors\n\nService Focus:\nDignified Community Dining · Three-Course Meals · Resource Connections\n\nProgram Overview:\nA community restaurant serving hot, nutritious three-course meals in a warm, dignified setting. In-need diners can eat with dignity by volunteering on-site, with no cash required.\n\nHours:\nWednesday – Friday: 5:00 PM – 7:00 PM; Saturday: 11:30 AM – 1:30 PM; Sunday: 10:30 AM – 1:30 PM'}, {'id': 'auto-scraped-930', 'name': 'Project PAUL', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Low-Income Residents in Specific Service Towns', 'location': '211 Carr Ave, Keansburg, NJ 07734', 'phone': '(732) 787-4887', 'website': 'https://www.projpaul.org/', 'email': '', 'area': 'Keansburg, Middletown, Rumson, Red Bank, Keyport, Union Beach, Manalapan, Matawan, and Hazlet', 'description': 'Towns Served:\nKeansburg, Middletown, Rumson, Red Bank, Keyport, Union Beach, Manalapan, Matawan, and Hazlet\n\nService Focus:\nFood Pantry · Eviction Prevention & Rental Aid · Thrift Store · Senior Support\n\nProgram Overview:\nServes low-income families and seniors in its designated service municipalities with a large client-choice food pantry, emergency homelessness prevention/rental aid, and community thrift shop vouchers.\n\nHours:\nMonday – Friday: 9:00 AM – 3:00 PM'}, {'id': 'auto-scraped-924', 'name': 'Freehold Area Open Door', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Residents of Specified Municipalities', 'location': '39 Throckmorton St, Freehold, NJ 07728', 'phone': '(732) 780-1089', 'website': 'https://freeholdareaopendoor.org/', 'email': '', 'area': 'Freehold Borough, Freehold Township, Colts Neck, Farmingdale, Howell, and Marlboro / Morganville', 'description': "Towns Served:\nFreehold Borough, Freehold Township, Colts Neck, Farmingdale, Howell, and Marlboro / Morganville\n\nService Focus:\nFood Pantry · Emergency Financial Assistance · Prescription & Utility Aid\n\nProgram Overview:\nAn interfaith agency providing emergency food packages, utility and prescription assistance, emergency housing support, and children's school programs for Freehold-area residents in need.\n\nHours:\nMonday – Friday: 10:00 AM – 1:00 PM"}, {'id': 'allentown-food-pantry', 'name': 'Allentown Presbyterian Church Food Pantry', 'category': 'Basic Needs & Assistance', 'cost_label': 'Free', 'nj_access': 'Western Monmouth & Upper Freehold Area Residents', 'location': '20 High St, Allentown, NJ 08501', 'phone': '(609) 259-7289', 'website': 'https://allentownpc.org/', 'email': '', 'area': 'Allentown, Upper Freehold, Millstone, and Roosevelt', 'description': 'Towns Served:\nAllentown, Upper Freehold, Millstone, and Roosevelt\n\nService Focus:\nCommunity Food Pantry · Emergency Assistance\n\nProgram Overview:\nServes western Monmouth County and Upper Freehold households facing food insecurity with monthly groceries, non-perishable staples, and seasonal holiday meal support.\n\nHours:\nMonday & Wednesday: 10:00 AM – 1:00 PM; or by appointment'}]
APPROVED_COMMUNITY_ALIASES = {'auto-scraped-921': ['Middletown Help Its Own', 'Middletown Helps Its Own'], 'auto-scraped-912': ['Salvation Army Pantry -Asbury Park', 'Salvation Army — Asbury Park Corps'], 'auto-scraped-957': ['Salvation Army Food Pantry - Red Bank', 'Salvation Army — Red Bank Corps'], 'fn-02': ['St. Vincent de Paul Society (Monmouth County)', 'St. Vincent de Paul Society — Regional Conferences'], 'auto-scraped-958': ["St. Crispin's Food Pantry", 'St. Crispin House / Saint Crispin Society'], 'fn-01': ['FoodBank of Monmouth and Ocean Counties', 'Fulfill Food Bank & Mobile Pantries', 'Fulfill — The FoodBank of Monmouth & Ocean Counties'], 'monmouth-res-29': ['JBJ Soul Kitchen', 'JBJ Soul Kitchen'], 'auto-scraped-930': ['Project Paul', 'Project PAUL'], 'auto-scraped-924': ['Open Door Pantry', 'Freehold Area Open Door'], 'allentown-food-pantry': ['Allentown Food Pantry', 'Allentown Food Pantry', 'Allentown Presbyterian Church Food Pantry']}

def get_foundational_resources():
    foundational = get_original_foundational_resources()
    by_id = {item['id']: item for item in foundational}
    for approved in APPROVED_COMMUNITY_RESOURCES + APPROVED_WELLNESS_RESOURCES:
        aliases = APPROVED_COMMUNITY_ALIASES.get(approved['id'], [approved['name']])
        matched = [item_id for item_id, item in by_id.items()
                   if item_id == approved['id'] or item.get('name') in aliases]
        for item_id in matched:
            by_id[item_id] = {**by_id[item_id], **approved, 'id': item_id}
        if approved['id'] not in by_id:
            by_id[approved['id']] = approved.copy()
    return list(by_id.values())

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
