import os
import pymupdf as fitz  # PyMuPDF
import docx
import csv

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIR = os.path.join(BASE_DIR, "sample_docs")
DOMAIN1_DIR = os.path.join(SAMPLE_DIR, "domain1_it_cloud")
DOMAIN2_DIR = os.path.join(SAMPLE_DIR, "domain2_healthcare")

os.makedirs(DOMAIN1_DIR, exist_ok=True)
os.makedirs(DOMAIN2_DIR, exist_ok=True)

def create_pdf(path, title, content_paragraphs):
    doc = fitz.open()
    page = doc.new_page()
    
    # Simple PDF generation
    y = 50
    page.insert_text((50, y), title, fontsize=16)
    y += 30
    
    for p in content_paragraphs:
        # Wrap simple text
        lines = p.split('\n')
        for line in lines:
            if y > 750:
                page = doc.new_page()
                y = 50
            page.insert_text((50, y), line[:90], fontsize=10)
            y += 15
        y += 10
        
    doc.save(path)
    doc.close()

def create_docx(path, title, sections):
    doc = docx.Document()
    doc.add_heading(title, level=1)
    
    for heading, body in sections:
        doc.add_heading(heading, level=2)
        doc.add_paragraph(body)
        
    doc.save(path)

# --- DOMAIN 1: IT Cloud Infrastructure & DevOps ---

# 1. PDF: cloud_architecture_guide.pdf
pdf1_title = "Cloud Infrastructure & Microservices Architecture Guide"
pdf1_paragraphs = [
    "Overview:\nThis document specifies the target multi-region cloud deployment architecture for high-availability enterprise services.",
    "Kubernetes Cluster Architecture:\nThe primary container orchestration system consists of managed Kubernetes clusters deployed across 3 availability zones in us-east-1 and eu-west-1. Nodes auto-scale based on CPU utilization exceeding 75% or memory threshold exceeding 80%.",
    "Load Balancing & Traffic Routing:\nIngress controllers route external HTTPS traffic using NGINX with TLS 1.3 encryption. Global Server Load Balancing (GSLB) ensures automatic failover to the secondary region within 15 seconds of region outage detection.",
    "Database Persistence & Replication:\nPrimary transactional data is stored in PostgreSQL with asynchronous multi-region replication. Read-heavy workloads utilize Redis cluster caching with LRU eviction policy."
]
create_pdf(os.path.join(DOMAIN1_DIR, "cloud_architecture_guide.pdf"), pdf1_title, pdf1_paragraphs)

# 2. DOCX: devops_deployment_handbook.docx
docx1_title = "DevOps Continuous Deployment & Incident Handbook"
docx1_sections = [
    ("Blue-Green Deployment Protocol", "All production deployments must follow Blue-Green environment switching. The green environment is provisioned, warm-up tests are executed, and DNS traffic weights are shifted incrementally over a 20-minute window (10%, 25%, 50%, 100%)."),
    ("Automated Rollback Triggers", "Automated rollbacks are executed instantly if the HTTP 5xx error rate exceeds 0.5% over a 3-minute rolling window, or if latency p99 exceeds 450ms. The deployment pipeline restores traffic to the previous Blue environment within 12 seconds."),
    ("Incident Escalation Protocol", "For Severity 1 (P1) outages impacting core payment or authentication services, the Incident Commander must open an emergency bridge within 5 minutes and notify the VP of Engineering within 15 minutes.")
]
create_docx(os.path.join(DOMAIN1_DIR, "devops_deployment_handbook.docx"), docx1_title, docx1_sections)

# 3. TXT: api_security_spec.txt
txt1_content = """RESTful API Security Specification & Authentication Policy

1. OAuth2 Authentication Framework:
All client applications must authenticate using OAuth2.0 Client Credentials or Authorization Code flow with PKCE. Tokens are issued by the Central Identity Provider (IdP) and signed using RS256 algorithm.

2. Access Token Lifecycle:
Access Tokens expire exactly 60 minutes after issuance. Refresh Tokens remain valid for 14 days, provided they are rotated on each token renewal request. Token revocation endpoints must respond within 100ms.

3. API Rate Limiting Policy:
Standard public endpoints are rate-limited to 100 requests per minute per IP address. Authenticated tier APIs allow up to 5,000 requests per hour. Excess requests trigger HTTP 429 Too Many Requests response with Retry-After header.

4. Data Encryption Standards:
All data in transit must enforce TLS 1.3 or TLS 1.2 minimum. Data at rest in S3 buckets and RDS volumes must be encrypted using AWS KMS managed keys with AES-256 encryption.
"""
with open(os.path.join(DOMAIN1_DIR, "api_security_spec.txt"), "w", encoding="utf-8") as f:
    f.write(txt1_content)

# 4. CSV: infrastructure_cost_analysis.csv
csv1_headers = ["Provider", "Service_Category", "Region", "Monthly_Cost_USD", "SLA_Uptime_Pct"]
csv1_rows = [
    ["AWS", "Compute EC2", "us-east-1", 4500.0, 99.99],
    ["AWS", "Storage S3", "us-east-1", 1200.0, 99.999999999],
    ["GCP", "Compute GKE", "us-central1", 4200.0, 99.95],
    ["GCP", "Storage Cloud Storage", "us-central1", 1100.0, 99.999999999],
    ["Azure", "Compute AKS", "eastus", 4700.0, 99.95],
    ["Azure", "Storage Blob", "eastus", 1250.0, 99.999999999]
]
with open(os.path.join(DOMAIN1_DIR, "infrastructure_cost_analysis.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv1_headers)
    writer.writerows(csv1_rows)


# --- DOMAIN 2: Healthcare & Medical Protocols ---

# 1. PDF: patient_triage_protocol.pdf
pdf2_title = "Emergency Department Patient Triage & Assessment Protocol"
pdf2_paragraphs = [
    "Clinical Objective:\nEstablish standardized 5-tier triage classification for incoming emergency patients to prioritize acute intervention.",
    "Triage Level 1 - Resuscitation (Immediate):\nPatients presenting with cardiac arrest, respiratory arrest, severe anaphylaxis, or major trauma. Immediate physician evaluation required without delay.",
    "Triage Level 2 - Emergent (Within 15 minutes):\nChest pain suspicious for acute coronary syndrome, stroke symptoms within 4.5 hours window, severe dyspnea, or severe pain rating (>8/10).",
    "Triage Level 3 - Urgent (Within 30 minutes):\nModerate abdominal pain, high fever (>39.0C) with systemic symptoms, complex fractures, or moderate asthma exacerbation. Vital signs mandatory every 30 minutes."
]
create_pdf(os.path.join(DOMAIN2_DIR, "patient_triage_protocol.pdf"), pdf2_title, pdf2_paragraphs)

# 2. DOCX: clinical_trial_guidelines.docx
docx2_title = "Clinical Trial Protocol & Adverse Event Reporting Guidelines"
docx2_sections = [
    ("Informed Consent Administration", "Informed consent must be obtained voluntarily from all prospective trial participants prior to initiating any study-related procedure. The consent document must be signed in duplicate with one physical copy provided to the patient."),
    ("Serious Adverse Event (SAE) Reporting", "Any Serious Adverse Event—defined as death, life-threatening condition, hospitalization, or persistent disability—must be reported to the Principal Investigator and Institutional Review Board (IRB) within 24 hours of clinical notification."),
    ("Double-Blind Protocol Maintenance", "Blinding codes for experimental drug vs placebo are maintained by an unblinded biostatistician. Emergency unblinding is permitted only when immediate clinical treatment decisions depend on knowing the exact assignment.")
]
create_docx(os.path.join(DOMAIN2_DIR, "clinical_trial_guidelines.docx"), docx2_title, docx2_sections)

# 3. TXT: hospital_discharge_policy.txt
txt2_content = """Hospital Inpatient Discharge & Post-Acute Care Policy

1. Discharge Readiness Criteria:
Inpatients are eligible for discharge when vital signs remain stable for 24 consecutive hours, oral intake is tolerated, surgical incisions show no signs of infection, and pain is adequately controlled with oral analgesics.

2. Medication Reconciliation Procedure:
The attending physician and clinical pharmacist must perform a full medication reconciliation comparing pre-admission medications with discharge prescriptions. Discontinued medications must be explicitly highlighted to prevent accidental duplication.

3. Follow-Up Appointment Scheduling:
High-risk patients (heart failure, COPD, diabetes) must have a post-discharge clinic follow-up scheduled within 7 business days of discharge. A discharge summary must be transmitted to the primary care provider within 48 hours.

4. Patient Discharge Education:
Nurses must deliver verbal and written discharge instructions covering wound care, warning signs requiring ER return, activity restrictions, and emergency contact numbers.
"""
with open(os.path.join(DOMAIN2_DIR, "hospital_discharge_policy.txt"), "w", encoding="utf-8") as f:
    f.write(txt2_content)

# 4. CSV: drug_inventory_registry.csv
csv2_headers = ["Drug_Name", "Category", "Storage_Condition", "Stock_Units", "Expiry_Date"]
csv2_rows = [
    ["Amoxicillin 500mg", "Antibiotic", "Room Temp (<25C)", 1200, "2027-08-15"],
    ["Lisinopril 10mg", "Antihypertensive", "Room Temp (<25C)", 3400, "2028-02-20"],
    ["Metformin 850mg", "Antidiabetic", "Room Temp (<25C)", 2100, "2027-11-30"],
    ["Atorvastatin 20mg", "Statin", "Room Temp (<25C)", 1800, "2028-05-10"],
    ["Albuterol Inhaler", "Bronchodilator", "Protect from heat", 450, "2026-12-01"],
    ["Insulin Glargine 100U", "Insulin", "Refrigerated (2-8C)", 280, "2026-10-15"]
]
with open(os.path.join(DOMAIN2_DIR, "drug_inventory_registry.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv2_headers)
    writer.writerows(csv2_rows)

print("Sample documents generated successfully across both domains (PDF, DOCX, TXT, CSV).")
