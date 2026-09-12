import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") # This creates a client object that knows how to communicate with Google's Gemini API.

client = genai.Client(api_key=API_KEY)

def analyze_threat(results):

    prompt = f"""
    Analyze the following cybersecurity threat intelligence data.

    Your task is to interpret the provided evidence and explain what it indicates.

    Rules:
    - Use only the information provided in the threat intelligence data.
    - Do not invent facts, detections, vendors, or events that are not present.
    - Clearly distinguish confirmed findings from assumptions and possibilities.
    - Do not declare an indicator safe, malicious, or a false positive unless the provided evidence supports that conclusion.
    - If the evidence is insufficient to determine something explicitly, say so.
    - Keep recommendations proportional to the evidence.



    Provide the analysis in these four sections:
    1. Important Security Findings
    2. Potential Threats
    3. Why the Findings Matter
    4. Recommended Actions

    Start each section on a new line.
    Do not repeat any section or the complete analysis.

    The Threat Intelligence Data:
    {results}
    """

    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = prompt
    )

    return response.text

if __name__ == "__main__":

    test_results = {
    "VirusTotal": {
        "Reputation": 720,
        "Analysis Stats": {
            "malicious": 1,
            "suspicious": 0,
            "undetected": 30,
            "harmless": 60
            }
        }
    }

    print(analyze_threat(test_results))