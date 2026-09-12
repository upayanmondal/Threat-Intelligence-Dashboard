import socket

def lookup_domain(domain):
    try:
        
        ip_address = socket.gethostbyname(domain)

        return {
            "Domain": domain,
            "IP Address": ip_address
        }

    except socket.gaierror:
        return {
            "Error": "Domain could not be resolved"
        }
        

if __name__ == "__main__":
    print(lookup_domain("example.com"))
    