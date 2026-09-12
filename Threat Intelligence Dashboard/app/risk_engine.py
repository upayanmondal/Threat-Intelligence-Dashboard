def calculate_risk(results, target_type):
    score = 0

    if target_type == "domain":

        virustotal = results.get("VirusTotal", {})
        analysis = virustotal.get("Analysis Stats", {})


        malicious = analysis.get("malicious", 0)
        suspicious = analysis.get("suspicious", 0)

        score += malicious * 10
        score += suspicious * 5
    
    elif target_type == "ip":

        virustotal = results.get("VirusTotal", {})
        analysis = results.get("Analysis Stats", {})


        malicious = analysis.get("malicious", 0)
        suspicious = analysis.get("suspicious", 0)

        score += malicious * 10
        score += suspicious * 5

        abuseipdb = results.get("AbuseIPDB", {})

        abuseipdb_score = abuseipdb.get("Abuse Confidence Score", 0)

        score += abuseipdb_score // 10
    
    score = min(score, 100)

    if score >= 80:
        risk_level = "CRITICAL"
    elif score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "Risk Score": score,
        "Risk Level": risk_level
    }