import whois

def lookup_whois(domain):
    try:
        data = whois.whois(domain)
        return {
            "Domain": domain,
            "Registrar": data.registrar,
            "Creation Date": data.creation_date,
            "Expiration Date": data.expiration_date,
            "Name Servers": data.name_servers
        }
    except Exception as e:
        return
        {
            "Error": f"WHOIS lookup failed: {str(e)}"
        }
        
if __name__ == "__main__":
    print(lookup_whois("HelloWorld.xya"))