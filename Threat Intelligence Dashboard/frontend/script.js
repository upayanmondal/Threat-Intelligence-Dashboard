const targetType = document.getElementById("targettype");
const target = document.getElementById("target");
const scanButton = document.getElementById("scanButton");

const pdfButton = document.getElementById("pdfButton");

function addIntelSection(title, Content)
{
    const section = document.createElement("div");
    section.className = "intel-section";

    const heading = document.createElement("h3");
    heading.textContent = title;

    const text = document.createElement("p");
    text.textContent = Content;

    section.appendChild(heading);
    section.appendChild(text);

    document.getElementById("intelligenceResults").appendChild(section);
}


scanButton.addEventListener("click", async function() {

    document.getElementById("loadingOverlay").style.display = "flex"; // make loading page visible

    const selectedType = targetType.value;
    const enteredTarget = target.value;

    const respose = await fetch("http://127.0.0.1:8000/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            target: enteredTarget,
            target_type: selectedType
        })
    });

    if(!respose.ok)
    {
        document.getElementById("loadingOverlay").style.display = "none"; // make loading page invisible

        const errorData = await respose.json();

        document.getElementById("targetStatus").textContent = "Error";

        const intelligenceResults = document.getElementById("intelligenceResults");

        intelligenceResults.textContent = errorData["detail"];

        return;
    }

    const data = await respose.json();
    document.getElementById("loadingOverlay").style.display = "none"; // make loading page invisible
    window.currentScanId = data["id"];

    if("Risk Score" in data["results"])
    {
        document.getElementById("riskScore").textContent = data.results["Risk Score"]["Risk Score"];
        document.getElementById("riskLevel").textContent = data.results["Risk Score"]["Risk Level"];
        document.getElementById("targetStatus").textContent = "Scanned";
    }

    else
    {
        document.getElementById("riskScore").textContent = "N/A";
        document.getElementById("riskLevel").textContent = "N/A";
        document.getElementById("targetStatus").textContent = "Scanned";
    }

    const intelligenceResults = document.getElementById("intelligenceResults");

    if(selectedType == "domain")
    {
        const dns = data["results"]["DNS"];
        intelligenceResults.textContent = "";

        // DNS
        if("Error" in dns)
        {
            /*intelligenceResults.textContent +=
            `DNS: ${dns["Error"]}`;*/
            addIntelSection("DNS", dns["Error"]);
        }

        else
        {
            addIntelSection(
                "DNS",
                `Domain: ${dns["Domain"]}
                IP Address: ${dns["IP Address"]}`
            );
        
            const virustotal = data["results"]["VirusTotal"];
            const whois = data["results"]["WHOIS"];
            const ssl = data["results"]["SSL"];

            // VirusTotal
            if("Error" in virustotal)
            {
                addIntelSection("VirusTotal", virustotal["Error"]);
            }


            else
            {
                addIntelSection(
                    "VirusTotal",
                    `VirusTotal Reputation: ${virustotal["Reputation"]}
                    
                    
                    Analysis stats:
                Malicious: ${virustotal["Analysis Stats"]["malicious"]}
                Suspicious: ${virustotal["Analysis Stats"]["suspicious"]}
                Harmless: ${virustotal["Analysis Stats"]["harmless"]}
                Undetected: ${virustotal["Analysis Stats"]["undetected"]}
                Timeout: ${virustotal["Analysis Stats"]["timeout"]}
                `
                );
            }

            // WHOIS
            if("Error" in whois)
            {
                addIntelSection("WHOIS", whois["Error"]);
            }

            else
            {
                addIntelSection(
                    "WHOIS",
                    `Registrar: ${whois["Registrar"]}
                    Creation Date: ${whois["Creation Date"]}
                    Expiration Date: ${whois["Expiration Date"]}
                    Name Servers: ${whois["Name Servers"].join(", ")}
                `
                );
            }

            // SSL
            if("Error" in ssl)
            {
                addIntelSection("SSL", ssl["Error"]);
            }

            else
            {
                addIntelSection(
                    "SSL",
                    `Issuer: ${ssl["Issuer"]}
                    Subject: ${ssl["Subject"]}
                    Valid From: ${ssl["Valid From"]}
                    Valid Till: ${ssl["Valid Till"]}`
                );
            }
        }
    }

    else if(selectedType == "ip")
    {

        const virustotal_ip = data["results"]["VirusTotal"];
        const abuseipdb = data["results"]["AbuseIPDB"];

        intelligenceResults.textContent = "";

        // VirusTotal
        if("Error" in virustotal_ip)
        {
            addIntelSection("Error", virustotal_ip["Error"]);
        }
        
        else
        {
            addIntelSection(
                    "VirusTotal",
                    `VirusTotal Reputation: ${virustotal["Reputation"]}
                    
                    
                Analysis stats:
                Malicious: ${virustotal_ip["Analysis Stats"]["malicious"]}
                Suspicious: ${virustotal_ip["Analysis Stats"]["suspicious"]}
                Harmless: ${virustotal_ip["Analysis Stats"]["harmless"]}
                Undetected: ${virustotal_ip["Analysis Stats"]["undetected"]}
                Timeout: ${virustotal_ip["Analysis Stats"]["timeout"]}
                `
                );
        }

        if("Error" in abuseipdb)
        {
            addIntelSection("Error", abuseipdb["Error"]);
        }

        else
        {
            addIntelSection(
                "AbuseIPDB",
                `IP Address: ${abuseipdb["IP Address"]}
                Abuse Confidence Score: ${abuseipdb["Abuse Confidence Score"]}
                Total Reports: ${abuseipdb["Total Reports"]}
                Country: ${abuseipdb["Country"]}
                ISP: ${abuseipdb["ISP"]}
                Domain: ${abuseipdb["Domain"]}
                Usage Type: ${abuseipdb["Usage Type"]}
                Last Reported: ${abuseipdb["Last Reported"]}`
            );
        }
    }


    const aiAnalysis = document.getElementById("aiAnalysis");

    aiAnalysis.textContent = data["ai_analysis"].replace(/\*\*/g, "");

    console.log(data);
    
})

pdfButton.addEventListener("click", function(){

    const scanId = window.currentScanId;

    if(!scanId)
    {
        alert("Please perform a scan first,");
        return;
    }

    window.open(`http://127.0.0.1:8000/scan/${scanId}`, "_blank");

});