import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("AbuseIPDB_API_Key")

Headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}

def check_ip_up(ip_add):
    url = "https://api.abuseipdb.com/api/v2/check"

    parameters = {
        "ipAddress": ip_add
    }

    response = requests.get(
        url,
        headers = Headers,
        params = parameters
    )

    if response.status_code != 200:
        return {
            "Error": f"AbuseIPDB request failed: {response.status_code}"
        }
    
    Data = response.json()["data"]

    return {
        "IP Address": Data["ipAddress"],
        "Abuse Confidence Score": Data["abuseConfidenceScore"],
        "Total Reports": Data["totalReports"],
        "Country": Data["countryCode"],
        "ISP": Data["isp"],
        "Domain": Data["domain"],
        "Usage Type": Data["usageType"],
        "Last Reported": Data["lastReportedAt"]
    }

if __name__ == "__main__":
    print(check_ip_up("x.x.x.x"))