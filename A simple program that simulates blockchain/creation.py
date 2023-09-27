from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

#Getting the public key
key_pem = "-----BEGIN PUBLIC KEY-----\n\
MIIBuDCCASwGByqGSM44BAEwggEfAoGBAOG8w5YEH1hKTOrNbt0ugxjE8sa7UmJA\n\
I6wuNgrRCbK99yensx/2LkTfc/poMKMSmbdmr0nd+vj0ZXTWEoxL5XowGYVwadCN\n\
6op4m4FV5KTcCZbe9iU0HxFD4m+CQa2GdGYWuO83o88Ba/5SW6qGyELirgy4eG/8\n\
YJVSbX7oqD+PAhUA9H1mL1r1tYQX5Z4QzshgXhHnyF8CgYEA3qJ7viYvHQKnAAI6\n\
4yQM3kz5umUdSCh4qaA4D/T2FjjFxfzEsGff/c/UX4hg7RAp0AiTC/5qEhDoBQ+1\n\
Bo0+F+6DGaPXMgwJnLpH3l7kiI0t2GE8cKhY/z/eMFuktHgY/5khSOdjgCLth8sx\n\
ldsAFnU6Jy/+XC3jr8k6GvipdOgDgYUAAoGBANn4uFXbVN9A+lr4Uafwfv6ro/Rs\n\
GbWLfSHTqLwHT+sV33609convCJ2CyoIlngw8EOjryTloZQuekkg5fEV80C6gKrW\n\
r3vFQK2jKiMPJNTsAo7le5QdxjpNstB44eFdS5YRtFT40x3mOUMd9bjSUqGWIQmy\n\
Q++gbFWQAE/iX4gd\n\
-----END PUBLIC KEY-----\n\
"

#Generating the g, p, q parameters
param_key = DSA.import_key(key_pem)
param = [param_key.p, param_key.q, param_key.g]
		
#Genrating the public/private key pair
key1 = DSA.generate(1024, domain = param)
with open("scriptPubKey.txt","w+") as file:
	#Opening the file and exporting the key in binary format and hexing it to a hexadecimal format
	hexofkey = key1.export_key(format = 'DER').hex()
	#OPCODE for 1 since this only need 1 signature
	file.write('51')
	file.write('\n')
	#Placing the hex of the key into the file
	file.write(hexofkey)
	#Placing the OPCODE for 1 and OPCODE for OP_CHECKMULTISIG at the end of the file
	file.write('51')
	file.write('ae')
	file.close()
	
#Generating the public/private key pair
key2 = DSA.generate(1024, domain = param)
with open("scriptPubKey2.txt","w+") as file:
	#Opening the file and exporting the key in binary format and hexing it to a hexadecimal format
	hexofkey1 = key1.export_key(format = 'DER').hex()
	hexofkey2 = key2.export_key(format = 'DER').hex()
	#OPCODE for 2 since this needs 2 signatures
	file.write('52')
	file.write('\n')
	#Placing the hex of the keys into the file
	file.write(hexofkey1)
	file.write('\n')
	file.write(hexofkey2)
	#Placing the OPCODE for 2,for the number of public key, and OPCODE for OP_CHECKMULTISIG at the end of the file
	file.write('52')
	file.write('ae')
	file.close()
	
#Generating the public/private key pair
key3 = DSA.generate(1024, domain = param)
with open("scriptPubKey3.txt","w+") as file:
	#Opening the file and exporting the key in binary format and hexing it to a hexadecimal format
	hexofkey1 = key1.export_key(format = 'DER').hex()
	hexofkey2 = key2.export_key(format = 'DER').hex()
	hexofkey3 = key3.export_key(format = 'DER').hex()
	#OPCODE for 2 since this needs 2 signatures
	file.write('52')
	file.write('\n')
	#Placing the hex of the keys into the file
	file.write(hexofkey1)
	file.write('\n')
	file.write(hexofkey2)
	file.write('\n')
	file.write(hexofkey3)
	#Placing the OPCODE for 3,for the number of public key, and OPCODE for OP_CHECKMULTISIG at the end of the file
	file.write('53')
	file.write('ae')
	file.close()
	
#Hasing the message
message = b"CSCI301 Contemporary Topics in Security 2023"
hash_obj = SHA256.new(message)

with open("scriptSig.txt","wb") as file:
	#Signing the message with the key
	signer = DSS.new(key1,'fips-186-3')
	signature = signer.sign(hash_obj)
	#Hexing the signature to be in a hexadecimal format
	signature_hex = binascii.hexlify(signature)
	#OPCODE for 0 and placing the hex of the signature into the file
	file.write(b'00')
	file.write(b'\n')
	file.write(signature_hex)
	file.close()
	
with open("scriptSig2.txt","wb") as file:
	#Signing the messages with the keys
	signer_key1 = DSS.new(key1,'fips-186-3')
	signature_key1 = signer_key1.sign(hash_obj)
	#Hexing the signature to be in a hexadecimal format
	signature_hex_key1 = binascii.hexlify(signature_key1)
	signer_key2 = DSS.new(key2,'fips-186-3')
	signature_key2 = signer_key2.sign(hash_obj)
	#Hexing the signature to be in a hexadecimal format
	signature_hex_key2 = binascii.hexlify(signature_key2)
	#OPCODE for 0 and placing the hex of the signatures into the file
	file.write(b'00')
	file.write(b'\n')
	file.write(signature_hex_key1)
	file.write(b'\n')
	file.write(signature_hex_key2)
	file.close()
	
with open("scriptSig3.txt","wb") as file:
	#Signing the messages with the keys
	signer_key2 = DSS.new(key2,'fips-186-3')
	signature_key2 = signer_key2.sign(hash_obj)
	#Hexing the signature to be in a hexadecimal format
	signature_hex_key2 = binascii.hexlify(signature_key2)
	signer_key3 = DSS.new(key3,'fips-186-3')
	signature_key3 = signer_key3.sign(hash_obj)
	#Hexing the signature to be in a hexadecimal format
	signature_hex_key3 = binascii.hexlify(signature_key3)
	#OPCODE for 0 and placing the hex of the signatures into the file
	file.write(b'00')
	file.write(b'\n')
	file.write(signature_hex_key2)
	file.write(b'\n')
	file.write(signature_hex_key3)
	file.close()



