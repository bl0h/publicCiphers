import random
import secrets
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# pow(6, 8, 5)

q = 37  #prime number
a = q-1   #a < q and a is a primitive root of q
#modifying a to be 1 results in the secret key always being 1
#modifying a to be q results in the public key always being 0 which makes the secret key always 0
#modifying a to be q-1 results in the public keys being 1 which makes the secret key 1

alicePrivate = random.randint(0, q)
alicePublic = pow(a, alicePrivate, q)
print("Alice public:", alicePublic, "private:", alicePrivate)

bobPrivate = random.randint(0, q)
bobPublic = pow(a, bobPrivate, q)
print("Bob public:", bobPublic, "private:", bobPrivate)

#mallory modifies both public keys to be q instead, which results in the secret key being 0
aliceSecret = pow(bobPublic, alicePrivate, q)
bobSecret = pow(alicePublic, bobPrivate, q)
print("Alice and Bobs shared secret key:", aliceSecret, bobSecret)

if(aliceSecret != bobSecret):
    print("Secret keys are not the same... exiting")
    exit()

symmetric = SHA256.new(aliceSecret.to_bytes(16, byteorder = 'big')).digest()

aliceMessage = "Hi Bob!"
bobMessage = "Hi Alice!"

iv = secrets.token_bytes(16)
cipher = AES.new(symmetric, AES.MODE_CBC, iv)
aliceEncryptedMessage = cipher.encrypt(pad(aliceMessage.encode(), AES.block_size))
cipher = AES.new(symmetric, AES.MODE_CBC, iv)
bobEncryptedMessage = cipher.encrypt(pad(bobMessage.encode(), AES.block_size))

cipher = AES.new(symmetric, AES.MODE_CBC, iv)
bobDecryptedMessage = cipher.decrypt(bobEncryptedMessage)
bobDecryptedMessage = bobDecryptedMessage.decode()
print("Alice decrypts the message:", bobDecryptedMessage)

cipher = AES.new(symmetric, AES.MODE_CBC, iv)
aliceDecryptedMessage = cipher.decrypt(aliceEncryptedMessage)
aliceDecryptedMessage = aliceDecryptedMessage.decode()
print("Bob decrypts the message:", aliceDecryptedMessage)
