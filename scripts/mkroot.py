from subprocess import check_output
import hashlib
import os

from fastecdsa import curve, ecdsa, keys
from fastecdsa.curve import Curve
from fastecdsa.point import Point
from fastecdsa.curve import P384
import gmpy2

# create directory structure if it doesn't exist
os.makedirs('ca', exist_ok=True)
os.makedirs('ssl', exist_ok=True)

SIG_PREFIX = b'  SEQUENCE {\n    # ecdsa'

def f2ascii(path):
    return pem2ascii(open(path, 'rb').read())
def ascii2f(path, data, cmd='x509'):
    print("Writing %s" % (path))
    return open(path, 'wb').write(ascii2pem(data, cmd))
def ascii2der(data):
    return check_output(["ascii2der"], input=data)
def der2ascii(data):
    return check_output(["der2ascii"], input=data)
def ascii2pem(data, cmd='x509'):
    return check_output(["openssl", cmd, "-inform", "der"], input=ascii2der(data))
def pem2ascii(data):
    return der2ascii(check_output(["openssl", "x509", "-outform", "der"], input=data))

# extracted from "Microsoft EV ECC Root Certificate Authority 2017"
x = 0x34ddf9d700abe1262a5f9a368bb0bcc9c00573ccd5d621cbf657fccfb58bbde634af20b13d49aac5675582e1ed30dd6b
y = 0xed45cb7c2da1acae971f3f7660517facca8bffa59b41e5d34af225d501dbfdfb6c4ec996a3ddf753342b771e3156c2bf
Q = Point(x, y, curve=P384)

# src: https://crypto.stackexchange.com/questions/8925
secret_x = 1337
k = gmpy2.invert(secret_x, P384.q)
G = k * Q
assert secret_x * G == Q
F384 = Curve('F-384', P384.p, P384.a, P384.b, P384.q, G.x, G.y)

print('Modified generator:')
print('04%096x%096x' % (G.x, G.y))

print('Serializing root.txt and self-sign root certificate')
data = open('/app/templates/root.txt', 'rb').read()
msg  = ascii2der(data[10:data.index(SIG_PREFIX)])
r, s = ecdsa.sign(msg, secret_x, curve=F384, hashfunc=hashlib.sha256)
data = data % (r, s)
ascii2f('ca/root.pem', data)

print('Serializing root private key')
data = open('/app/templates/root-key.txt', 'rb').read()
data = data % (secret_x, G.x, G.y, Q.x, Q.y)
ascii2f('ca/root-key.pem', data, 'ec')
