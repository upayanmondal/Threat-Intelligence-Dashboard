import requests
from dotenv import load_dotenv
import os

# Load variables from .env into the environment
load_dotenv()

# Environment = information/settings available to a process
API_KEY = os.getenv("VirusTotal_API_Key")

HEADERS = {
    "x-apikey": API_KEY
}

def check_domain(domain):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    response = requests.get(
        url,
        headers = HEADERS
    )
    
    if response.status_code != 200:
        return {
            "Error": f"VirusTotal request failed: {response.status_code}"
        }

    data = response.json()["data"]["attributes"] # response.json() means "Take the response's body/content, which is formatted as JSON, and convert it into Python objects."
    
    result = {
        "Reputation": data["reputation"],
        "Analysis Stats": data["last_analysis_stats"],
        "Categories": data["categories"]
    }

    return result

def check_ip(ip_add):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_add}"

    response = requests.get(
        url,
        headers = HEADERS
    )

    if response.status_code != 200:
        return {
            "Error": f"VirusTotal request failed: {response.status_code}"
        }

    data = response.json()["data"]["attributes"]

    results = {
        "Reputation": data["reputation"],
        "Analysis Stats": data["last_analysis_stats"],
        "Country": data.get("country", "N/A"),
        "AS Owner": data["as_owner"]
    }
    return results

if __name__ == "__main__":
    print(check_ip("x.x.x.x"))
    print(check_ip("example.org"))