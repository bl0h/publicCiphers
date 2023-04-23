import random
import secrets
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# pow(6, 8, 5)

q = 37  #prime number
a = 5   #a < q and a is a primitive root of q

alicePrivate = random.randint(0, q)
alicePublic = pow(a, alicePrivate, q)
print("Alice public:", alicePublic, "private:", alicePrivate)

bobPrivate = random.randint(0, q)
bobPublic = pow(a, bobPrivate, q)
print("Bob public:", bobPublic, "private:", bobPrivate)

aliceSecret = pow(bobPublic, alicePrivate, q)
bobSecret = pow(alicePublic, bobPrivate, q)
print("Alice and Bobs shared secret key:", aliceSecret, bobSecret)

aliceSharedSecret = SHA256.new(aliceSecret)  
bobSharedSecret = SHA256.new(bobSecret)

aliceMessage = "Hi Bob!"
bobMessage = "Hi Alice!"

iv = secrets.token_bytes(16)
cipher = AES.new(aliceSharedSecret, AES.MODE_CBC, iv)

aliceEncryptedMessage = cipher.encrypt(pad(aliceMessage, AES.block_size))
bobEncryptedMessage = cipher.encrypt(pad(bobMessage, AES.block_size))