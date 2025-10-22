"""
Generate self-signed SSL certificate for HTTPS development.
This allows Flask to run on https://127.0.0.1:5000 for Schwab OAuth.
"""

from datetime import datetime, timedelta, timezone
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import ipaddress

def generate_self_signed_cert():
    """Generate a self-signed certificate for localhost development"""
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Create certificate subject
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Development"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Portfolio Analysis Dev"),
        x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1"),
    ])
    
    # Build certificate
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256(), default_backend())
    )
    
    # Write private key
    with open("key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    
    # Write certificate
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("✓ SSL certificate generated successfully!")
    print("  - cert.pem (certificate)")
    print("  - key.pem (private key)")
    print("\nThese files enable HTTPS for local development.")
    print("Your browser will show a security warning - this is normal for self-signed certificates.")
    print("Click 'Advanced' and 'Proceed to 127.0.0.1' to continue.")

if __name__ == "__main__":
    try:
        generate_self_signed_cert()
    except ImportError:
        print("Error: cryptography library not found.")
        print("Install it with: pip install cryptography")
