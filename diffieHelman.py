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
bobDecryptedMessage = bobDecryptedMessage.decode().strip()
print("Alice decrypts the message:", bobDecryptedMessage)

cipher = AES.new(symmetric, AES.MODE_CBC, iv)
aliceDecryptedMessage = cipher.decrypt(aliceEncryptedMessage)
aliceDecryptedMessage = aliceDecryptedMessage.decode().strip()
print("Bob decrypts the message:", aliceDecryptedMessage)
