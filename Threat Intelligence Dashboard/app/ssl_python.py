import socket
import ssl

def check_ssl(domain):
    try:

        context = ssl.create_default_context() # It sets up secure default settings, including automatic verification of the server's authenticity and standard encryption protocols.

        with socket.create_connection((domain, 443), timeout=5) as connection:
            with context.wrap_socket(connection, server_hostname=domain) as ssl_socket: # context.wrap_socket: Wraps the basic socket with the SSL/TLS security rules defined by ssl.create_default_context().
                certificate = ssl_socket.getpeercert()

        return {
            "Domain": domain,
            "Issuer": certificate.get("issuer"),
            "Subject": certificate.get("subject"),
            "Valid From": certificate.get("notBefore"),
            "Valid Till": certificate.get("notAfter")
        }


    except Exception as e:
        return {
            "Error": f"SSL checked failed: {str(e)}"
        }

if __name__ == "__main__":
    print(check_ssl("google.com"))