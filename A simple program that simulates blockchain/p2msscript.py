from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

#Function to get the OPCODE from the files
def getOPCODE(string):
	if(string == '00'):
		return 0
	elif (string == '51'):
		return 1
	elif(string == '52'):
		return 2
	elif (string == '53'):
		return 3
	elif(string == '54'):
		return 4
	elif (string == '55'):
		return 5
	elif(string == '56'):
		return 6
	elif (string == '57'):
		return 7
	elif(string == '58'):
		return 8
	elif (string == '59'):
		return 9
	elif(string == '00'):
		return 10
	elif (string == '51'):
		return 11
	elif(string == '00'):
		return 12
	elif (string == '51'):
		return 13
	elif(string == '00'):
		return 14
	elif (string == '51'):
		return 15
	elif(string == '00'):
		return 16
	elif (string == 'ae'):
		return OP_CHECKMULTISIG

#Creating a stack
stack = []
#Hash object to be used to verify 
hash_obj = SHA256.new(b"CSCI301 Contemporary Topics in Security 2023")
#Tally to be used to check if the script is valid at the end
tally = 0

with open('scriptSig3.txt') as filename:
	#Opens and read the file
	reading = filename.readlines()
	#Gets the number related to the OPCODE and pushes it into the stack
	x = getOPCODE(reading[0].strip())
	stack.append(x)
	#Loops thru the list that has all the lines from the digital signature file
	for i in range (len(reading)):
		if(i+1==len(reading)):
			break
		#Pushes the digital signature to the stack and removes all newlines
		stack.append(reading[i+1].strip())

with open('scriptPubKey3.txt') as filename:
	#Opens and read the public key file
	reading = filename.readlines()
	for i in range (len(reading)):
		if (i==0):
			#Gets the number related to the OPCODE and pushes it into the stack
			x = getOPCODE(reading[0].strip())
			#Tally will be used later for comparison
			tally2 = int(x)
			stack.append(x)
		elif (i == len(reading)-1):
			#Reads the last line in the file and removes the '0x' at the front
			newstring = reading[i].strip()
			if (newstring[0:2] == '0x'):
				newstring = newstring[2:]
			#This checks if the file is a P2MS script
			#Once it reaches the last line, it checks for the OPCODE 'ae' which is the OP_CHECKMULTISIG 
			#If it is present it will continue with the script processing to check if it is a valid scirpt
			if(newstring[-2:] != 'ae'):
				print("Not a P2MS script")
				print("Exiting program ...")
				print("\n")
				break
			else:
				newstring = newstring[:-2]
				print("This is a P2MS script")
				print("Continuing with the program...")
				print("\n")
			
			#After removing the additonal '0x' and the ending OPCODE it pushes the 
			#key into the stack
			newcode = newstring[-2:]
			#This is the number of keys and pushes it into the stack
			lastOPC = getOPCODE(newcode)
			newstring = newstring[:-2]
			stack.append(newstring)
			stack.append(lastOPC)
			#Creating the key list	
			pubkey_list = []
			numberOFpubkey = stack.pop()
			
			#Popping the key and pushing it into the list
			for i in range(numberOFpubkey):
				pubkey = stack.pop()
				pubkey_list.append(pubkey)
			#Reversing the list to get the proper order
			pubkey_list = pubkey_list[::-1]
			
			#Creating the signature list
			sigs_list = []
			
			#Placing all the signatures into the list and then reversing the list to get the 
			#proper order
			numberofsigs = stack.pop()
			for i in range(numberofsigs):
				sigs = stack.pop()
				sigs_list.append(sigs)
			sigs_list = sigs_list[::-1]	
			
			#Setting flags to break out of loops
			break_while = False
			break_out_flag = False
			for i in range(len(sigs_list)):
				for j in range(len(pubkey_list)):
					#Iterates thru the loop to check if a public key is set to ignore
					#If it is 'ignore' it will increment the public key loop
					while(pubkey_list[j] == 'ignore' ):
						j = j+1
						#if it is not ignore it will break out of the if loop
						if(pubkey_list[j] != 'ignore' ):
							break_while = False
							break
					#Breaking out of the while loop if it is not an 'ignore'
					if break_while:
						break
					
					#un-hexing the signature
					newmess = binascii.unhexlify(sigs_list[i])
					#Getting the key and un-hexing it
					currpub = DSA.import_key(bytes.fromhex(pubkey_list[j]))
					#verifying the message with the key and digital signature
					verifier = DSS.new(currpub, 'fips-186-3')
					try:
						#If the message is authentic, it will add to the tally and also
						#increment the sig_list so that it will not iterate thru the rest of the list
						verifier.verify(hash_obj,newmess)
						print("The message is authentic")
						tally = tally+1
						i = i+1
						#it will also set the key to ignore so that it will be ignored when
						#sig_list is iterated
						pubkey_list[j] = 'ignore'
						#Once the number of tally matches it breaks out of all the loops
						if(tally == tally2):
							break_out_flag = True
							break
					except ValueError:
						#if message is not authentic it will raise an error
						print("The message is not authentic")
				if break_out_flag:
					break
							
						
			#Once the tally is the same and the loop is done, it will all a 1 to the stack	
			if (tally == tally2):
				stack.clear()
				stack.append(1)
			
			#if the stack has a 1, the script will be valid
			if(stack.pop()!= 1):
				print("\n")
				print("The script is not valid")
			else:
				print("\n")
				print("The script is valid")
			
		else:
			#Reads all the lines inbetween the last line and first line and pushes it 
			#into the stack after removing the '0x' and newlines
			beforeend = reading[i]
			if (beforeend[0:2] == '0x'):
				beforeend = beforeend[2:]
			beforeend = beforeend.strip()
			stack.append(beforeend)
	
	
