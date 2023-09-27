from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import json, hashlib
import time
import os

#To create the block 0 for the block chain
block0 = json.dumps({'Block number': 0, 'Hash': "Genesis",'Transaction': ""}, sort_keys=True, indent=4,separators=(',', ': '))
fw = open("0.json", "w+")
fw.write(block0)
fw.close()

transactions = [ "[3, 4, 5, 6]", "[4, 5, 6, 7]", "[5, 6, 7, 8]", "[6, 7, 8, 9]", "[7, 8, 9, 10]", "[8, 9, 10, 11]", "[9, 10, 11, 12]", "[10, 11, 12, 13]", "[11, 12, 13, 14]", "[12, 13, 14, 15]", "[13, 14, 15, 16]"]

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-653e767f-dc39-441d-a172-2a27384aeecf'
pnconfig.publish_key = 'pub-c-46cc4a80-0e0c-4d8c-92e2-5c39804d62e0'
pnconfig.user_id = "alice"
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
       	    pass
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            #pubnub.publish().channel('Channel-Barcelona').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        cond = True
        fileexist = True
        #To check for the message sent by Bob after the mining for Alice is done. 
        #Loops to wait for Bob to send the message
        while(cond):
        	if(message.message != ""):
        		cond = False
        	else:
        		print("Waiting for Bob to mine")
        	time.sleep(3)
        #Retreiving the block number from the message
        blknum = message.message["Block number"]
        #Check if Alice created the json file for the current block chain
        while(fileexist):
        	path = str(blknum) + '.json'
        	check_file = os.path.isfile(path)
        	if(check_file):
        		fileexist = False
        	else:
        		print("Waiting for Alice to finish mining")
        	time.sleep(3)
        #Retreiving the information from the file into a variable as a json
       	with open(str(blknum)+".json", "r") as f:
       		data = json.load(f)
       	#Retrieving the nonce from both alice and bob to compare. The player with the smaller nonce wins. For bob we subtract
       	#1,000,000,001 to retreive the number of nonces
        nonceofalice = data["Nonce"]
        nonceofbob = message.message["Nonce"]
        nonceofbob = nonceofbob-1000000001
        #If bob wins, it will overwrite the block chain json file created by alice
        if(nonceofbob<nonceofalice):
        	print("Bob has won this round")
        	#This also check for the verification of the block at the same time. It retreives the hash from the current
        	#block that won and it hashes the previous block to compare
        	fw = open(str(blknum)+".json","w+")
        	newjson = json.dumps(message.message)
        	fw.write(newjson)
        	fw.close()
        	fr = open(str(blknum-1)+".json","r")
        	preblk = fr.read()
        	prehash = hashlib.sha256(preblk.encode()).hexdigest()
        	#If the hash is the same, it will print that the block is verified
        	if (prehash == message.message["Hash"]):
        		print("Block verified")
        	else:
        		print("Block not verified")
        else:
        	print("You have won this round")
        	
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('Channel-Alice').execute()
blknum = 0
#Creating the block chain
for i in transactions:
			#A sleep timer to delay the creation of the block chain
			time.sleep(10)
			#Hashing the previous block
			blknum = blknum+1
			fr = open(str(blknum-1)+".json", "r")
			preblk = (fr.read())
			fr.close()
			prehash =  hashlib.sha256(preblk.encode()).hexdigest()
			nonce = 0
			cond = True
			print("\n")
			#Looping to get the correct nonce for the current block
			while(cond):
				tx = json.dumps({'Block number': blknum, 'Hash': prehash,'Transaction':i, 'Nonce':nonce})
				hashcheck =  hashlib.sha256(tx.encode()).hexdigest()
				if int(hashcheck[0:8],16)<= int("00000fff",16):
					cond = False
				else:
					nonce = nonce+1
			#Creating the json file for the current block chain
			fw = open(str(blknum)+".json", "w+")
			print(tx)
			fw.write(tx)
			fw.close()
			#Sending the message to bob via PubNub
			pubnub.publish().channel('Channel-Bob').message({'Block number': blknum, 'Hash': prehash,'Transaction':i, 'Nonce':nonce}).pn_async(my_publish_callback)
			#Sleep timer to delay
			time.sleep(10)
			#Once it reaches the end of the program it exits
			message2 = input("Press the Enter key to mine next block once the result is shown")
			if(i == 10):
				print("All blocks mined, exiting program...")
				break
			

