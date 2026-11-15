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
        }
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
