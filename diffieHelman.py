import random
import secrets
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# pow(6, 8, 5)

q = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371

a = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5

#a < q and a is a primitive root of q

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

symmetric = SHA256.new(aliceSecret.to_bytes(128, byteorder = 'big')).digest()
symmetric = symmetric[:16]

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
