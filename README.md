**Threat Intelligence Dashboard**
A Python-based threat intelligence dashboard that analyzes domains and IP addresses using multiple security intelligence sources and presents the results through a web interface.
The project combines cybersecurity APIs, automated risk scoring, AI-assisted analysis, database storage, and PDF report generation into a single dashboard.

**Features**
• Analyze Domain Names and IP Addresses
• VirusTotal threat intelligence
• AbuseIPDB analysis for IP addresses
• DNS resolution
• WHOIS information
• SSL/TLS certificate information
• Automated Risk Score and Risk Level
• Gemini-powered AI threat analysis
• SQLite database for storing scan results
• PDF report generation
• Input validation for domains and IP addresses
• Handling of unresolved/invalid targets
• Loading indicator during scans
• Web-based dashboard interface

**Tech Stack**
**Backend**
• Python
• FastAPI
• SQLAlchemy
• SQLite
• ReportLab

**Security Intelligence**
• VirusTotal API
• AbuseIPDB API
• WHOIS
• DNS
• SSL/TLS

**AI**
• Google Gemini API

**Frontend**
• HTML
• CSS
• JavaScript

**Project Structure**
Threat Intelligence Dashboard/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── virustotal.py
│   ├── dns_lookup.py
│   ├── whois_lookup.py
│   ├── ssl_python.py
│   ├── abuseipdb.py
│   ├── target_validation.py
│   ├── risk_engine.py
│   ├── ai_analysis.py
│   └── pdf_report.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── .env
│
└── threat_intelligence.db


**How It Works**
The dashboard follows this general workflow:
User enters Domain/IP
        │
        ▼
Target Validation
        │
        ▼
Security Intelligence Collection
        │
        ├── VirusTotal
        ├── AbuseIPDB
        ├── DNS
        ├── WHOIS
        └── SSL/TLS
        │
        ▼
Risk Engine
        │
        ▼
Risk Score + Risk Level
        │
        ▼
Gemini AI Analysis
        │
        ▼
Store Scan in SQLite
        │
        ▼
Display Results
        │
        ▼
Generate PDF Report

**Domain Analysis**
For domain targets, the dashboard collects information from:
DNS
Retrieves the IP address associated with the domain.

**VirusTotal**
Retrieves information such as:
• Reputation
• Malicious detections
• Suspicious detections
• Harmless detections
• Undetected results
• Timeout results

**WHOIS**
Retrieves information such as:
• Registrar
• Creation date
• Expiration date
• Name servers

**SSL/TLS**
Retrieves certificate information such as:
• Issuer
• Subject
• Valid-from date
• Valid-until date

**IP Analysis**
For IP addresses, the dashboard uses:
**VirusTotal**
Provides reputation and security analysis information.

**AbuseIPDB**
Provides information such as:
• Abuse confidence score
• Total reports
• Country
• ISP
• Domain
• Usage type
• Last reported date

**Risk Engine**
The project calculates an automated risk score based on the collected threat intelligence.
The current scoring logic considers:
Malicious detections × 10
+
Suspicious detections × 5
+
Abuse Confidence Score ÷ 10
The resulting score is capped at 100.
The dashboard then assigns a corresponding risk level based on the score.
This provides a simple numerical representation of the collected threat intelligence before the results are passed to the AI analysis stage.

**AI Threat Analysis**
After the intelligence is collected, the project uses the Google Gemini API to interpret the collected information.
The AI analysis is organized into sections including:
• Important Findings
• Potential Threats
• Why It Matters
• Recommended Actions
The purpose of the AI layer is not to replace the underlying security intelligence sources, but to provide a more understandable interpretation of the collected information.


**Database**
The project uses SQLite with SQLAlchemy.
Scan records contain information including:
• Scan ID
• Target
• Target type
• Scan results
• AI Analysis
The database file is:
threat_intelligence.db


**PDF Reports**
After a scan is completed, the dashboard can generate a PDF report containing the collected threat intelligence and analysis.
The backend exposes a scan-specific endpoint for generating the report:
/scan/{scan_id}
The frontend stores the scan ID returned by the backend and uses it when the user selects Generate PDF Report.

**Target Validation**
Before performing the scan, the application validates whether the supplied target matches the selected target type.
Supported target types:
Domain
IP
Invalid targets are rejected before unnecessary external API requests are performed.
The application also handles targets that cannot be resolved.
For an unresolvable target, the application does not continue with the AI analysis and reports that the analysis could not be performed.

**Environment Variables**
API keys are stored in a .env file rather than being hard-coded into the application.
Example:
VirusTotal_API_Key=your_virustotal_api_key
ABUSEIPDB_API_KEY=your_abuseipdb_api_key
GEMINI_API_KEY=your_gemini_api_key


**Installation**
Clone the repository:
git clone <your-repository-url>
Move into the project directory:
cd "Threat Intelligence Dashboard"
Create a virtual environment:
python -m venv venv
Activate it.
Windows
venv\Scripts\activate
Linux/macOS
source venv/bin/activate
Install the required dependencies:
pip install -r requirements.txt
Create the .env file and add the required API keys.


**Running the Application**
Start the FastAPI backend from the project directory:
Fastapi dev app/main.py
The FastAPI server will run on:
http://127.0.0.1:8000
Then open the frontend:
frontend/index.html
in a browser.


**API**
Scan Target
POST /scan
Example request:
{
    "target": "example.com",
    "target_type": "domain"
}
The endpoint performs the appropriate intelligence collection and returns the scan results.
Generate PDF Report
GET /scan/{scan_id}
Example:
http://127.0.0.1:8000/scan/1
This generates the PDF report for the corresponding scan.


**Security Considerations**
•	API keys are kept in environment variables.
•	External API failures are handled by the application.
•	Invalid targets are validated before scanning.
•	Unresolvable targets are handled without attempting unnecessary AI analysis.


**Future Improvements**
Possible improvements for a future version include:
•	User authentication
•	More threat intelligence sources
•	Persistent scan history interface
•	Advanced threat correlation
•	Improved risk scoring
•	Background scan processing
•	More detailed reporting
•	Production deployment
•	Improved dashboard visualizations
•	Additional AI-assisted security capabilities


**Project Status**
Threat Intelligence Dashboard V1 — Completed
V1 focuses on building the complete end-to-end pipeline:
Input
→ Validation
→ Intelligence Collection
→ Risk Calculation
→ AI Analysis
→ Database Storage
→ Dashboard
→ PDF Report
The project is intended as a practical demonstration of integrating Python development, FastAPI, cybersecurity APIs, threat intelligence, databases, AI, and web development into one application.




Author
**Upayan Mondal**
B.Tech Information Technology
GitHub: https://github.com/upayanmondal
LinkedIn: https:// www.linkedin.com/in/upayan-mondal-3b9235247
