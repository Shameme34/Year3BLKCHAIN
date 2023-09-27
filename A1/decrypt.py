from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import glob
from pathlib import Path

#Taking the private key to be used for decryption
file_in = open("CK.bin","rb")
#Reading the private key
sk = RSA.import_key(open("private.pem").read())
Ck = file_in.read(sk.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(sk)
#Decrypting the private key
k = cipher_rsa.decrypt(Ck)
file_in.close()


try:
	secretno = 1
	#Reading all files with .enc extension
	for filename in glob.glob('*.enc'):
		with open(filename) as f_input:
			#Taking the first line as the crypted message in file
			reading = f_input.readlines()
			CM_line = str(reading[0])
			CM_line2 = str(CM_line.split())
			#Removing the brackets in the beginning and end of string
			CM_line3 = CM_line2[2:-2]
			#Reading the encoded iv in the encoded file
			iv_line = reading[1]
			#Decoding both iv and cm using base64 decoder
			iv = b64decode(iv_line)
			CM = b64decode(CM_line3)
			#Getting the cipher to be used to decrypt the encoded message
			cipher = AES.new(k, AES.MODE_CBC, iv)
			M = unpad(cipher.decrypt(CM),AES.block_size)
			print('Decryted message number '+str(secretno)+':',M)
			secretno +=1
			#Changing the out put of the file back to the original message and 
			#changing the file back to txt file
			Fileout = open(filename, 'w')
			edit_M = str(M)[2:-1]
			Fileout.writelines(edit_M)
			Fileout.close()
			p = Path(filename)
			p.rename(p.with_suffix('.txt'))
		
except ValueError:
	print("Incorrect decryption")
except KeyError:
	print("Incorrect Key")
