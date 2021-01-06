from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

key = b'YOURKEYGYOURKEYG'
ciphered_data = base64.b64decode(input())
cipher = AES.new(key, AES.MODE_ECB) # CFB mode
result = unpad(cipher.decrypt(ciphered_data), 16)
result=str(result,'utf-8')
print(result)