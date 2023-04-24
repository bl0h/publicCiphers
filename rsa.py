from platform import python_implementation
from Crypto.Util.number import getPrime


def generate_key(key_size):
    e = 65537
    p = getPrime(key_size)
    q = getPrime(key_size)
    while (q == p or e >= p or e >= q):
        q = getPrime(key_size)
        p = getPrime(key_size)
    n = p*q
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)  # modular inverse
    return ((e, n), (d, n))  # pub and private keys


def encrypt(message):
    hex_str = message.encode("utf-8").hex()
    int_message = int(hex_str, 16)  # convert to ascii to hex then int
    cipher = pow(int_message, pub_key[0], pub_key[1])
    return cipher


def decrypt(cipher):
    hex_val = pow(cipher, priv_key[0], priv_key[1])
    hex_str = hex(hex_val)[2:]
    b = bytes.fromhex(hex_str)
    plain = b.decode("utf-8")
    return plain


keys = generate_key(256)
pub_key = keys[0]
priv_key = keys[1]

message = "hello world!"
c = encrypt(message)
print("starting message: ", message)
print("cipher: ", c)
plain = decrypt(c)
print("plain: ", plain)
