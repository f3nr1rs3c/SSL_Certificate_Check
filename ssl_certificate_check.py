import socket
import ssl
import datetime

# SSL Son Kullanma Tarihi.
def get_ssl_expiry_date(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()
    
    expiry_date = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
    return expiry_date

# Sertifika Detaylarını Alıyoruz.
def get_ssl_certificate_details(hostname):
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()    
    return certificate

# Sertifika Detaylarını Ekrana Bastırıyoruz.
def print_certificate_details(certificate):
    for key, value in certificate.items():
        if key == 'subject':
            print(f"Subject:")
            for item in value:
                for attr in item:
                    print(f"  {attr[0]}: {attr[1]}")
        elif key == 'issuer':
            print(f"Issuer:")
            for item in value:
                for attr in item:
                    print(f"  {attr[0]}: {attr[1]}")
        elif key == 'notBefore' or key == 'notAfter':
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")
            
# Kullanıcıdan İstenilen Site Url Giriyoruz.
def main():
    hostname = input("Lütfen SSL sertifikasını kontrol etmek istediğiniz web sitesinin alan adını girin (örneğin, www.google.com): ")
    
    print("\nSSL Certficate Detays:")
    try:
        certificate = get_ssl_certificate_details(hostname)
        print_certificate_details(certificate)
        
        expiry_date = get_ssl_expiry_date(hostname)
        print(f"\nSSL Sertifikasının Son Kullanma Tarihi: {expiry_date}")
        
        days_to_expiry = (expiry_date - datetime.datetime.now()).days
        print(f"SSL sertifikasının süresinin dolmasına kalan gün sayısı: {days_to_expiry}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
