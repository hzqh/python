# -*-coding:UTF-8-*- 
import hashlib
import binascii
import hmac
from Crypto.Cipher import AES

#  AES CBC PKCS7padding
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

def psd_sha256(psd):
    psd_sha256_hex = hashlib.sha256(psd).hexdigest()
    return binascii.unhexlify(psd_sha256_hex)

def hmac_sha256(key, req):
    hmac256 = hmac.new(key, req, digestmod=hashlib.sha256).digest()
    return hmac256

