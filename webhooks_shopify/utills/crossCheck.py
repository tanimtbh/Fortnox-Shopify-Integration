import hmac
import hashlib
import base64
from globalConfig import SECRET


def verify_webhook(data, hmac_header):    
    digest = hmac.new(SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    genHmac = base64.b64encode(digest)
    return hmac.compare_digest(genHmac, hmac_header.encode('utf-8'))