import random
import secrets
from Crypto.Hash import SHA256

# pow(6, 8, 5)

q = 37  #prime number
a = 5   #a < q and a is a primitive root of q

alicePublic = random.randint(0, q)
alicePrivate = pow(a, alicePublic, q)

bobPublic = random.randint(0, q)
bobPrivate = pow(a, bobPublic, q)

aliceSecret = pow(bobPublic, alicePrivate, q)

bobSecret = pow(alicePublic, bobPrivate, q)

aliceSharedSecret = SHA256.new(aliceSecret)  
bobSharedSecret = SHA256.new(bobSecret)

aliceMessage = "Hi Bob!"
bobMessage = "Hi Alice!"

iv = secrets.token_bytes(16)