"""Create Cert."""
from OpenSSL import crypto
from os.path import join

CERT_FILE = 'cert.crt'
KEY_FILE = 'cert.key'
LOCAL_TMP_DIR = ''


def create_cert():
    """証明書（cert）を作成."""
    # create key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    # create self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = 'JP'
    cert.get_subject().ST = 'test'
    cert.get_subject().L = 'test'
    cert.get_subject().O = 'test'
    cert.get_subject().OU = 'test'
    cert.get_subject().CN = 'test'
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.add_extensions([
        crypto.X509Extension(
            'basicConstraints'.encode('ascii'), False, 'CA:FALSE'.encode('ascii')),
        crypto.X509Extension(
            'keyUsage'.encode('ascii'), True, 'Digital Signature, Non Repudiation'.encode('ascii')),
        crypto.X509Extension(
            'issuerAltName'.encode('ascii'), False, 'email:'.encode('ascii')+'test'.encode('ascii'))
    ])
    # v3
    cert.set_version(2)
    # self signature
    cert.sign(key, 'sha256')
    
    # save cert
    open(join(LOCAL_TMP_DIR, CERT_FILE), 'wt').write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8'))
    
    # save private key
    open(join(LOCAL_TMP_DIR, KEY_FILE), 'wt').write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('utf-8'))
    print('ok')


create_cert()