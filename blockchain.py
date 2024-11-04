import hashlib
import json
from datetime import datetime

class Block():
    def __init__(self,tstamp,name,voter_id,party,prevhash=''):
        
        self.tstamp=tstamp
        self.name=name
        self.voter_id=voter_id
        self.party=party
        self.prevhash=prevhash
        self.hash=self.calcHash()

    def calcHash(self):
        block_string=json.dumps({"tstamp":self.tstamp,"name":self.name,"reason":self.voter_id,"detail":self.party,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        
        string="tstamp: "+str(self.tstamp)+"\n"
        string+="name: "+str(self.name)+"\n"
        string+="voter_id"+str(self.voter_id)+"\n"
        string+="party"+str(self.party)+"\n"
        string+="prevhash: "+str(self.prevhash)+"\n"
        string+="hash: "+str(self.hash)+"\n"
        return string
    def printHashes(self):
        print("prevhash",self.prevhash)
        print("hash",self.hash)

##bblock=Block(1,"01/02/2019",100)
##bblock.printHashes()

class BlockChain():
    def __init__(self):
        self.chain=[self.generateGenesisBlock(),]
    def generateGenesisBlock(self):
        return Block("gensis name","gensis voter_id","01/01/2019","Gensis Block")
    def getLastBlock(self):
        return self.chain[-1]
    def addBlock(self,newBlock):
        newBlock.prevhash=self.getLastBlock().hash
        newBlock.hash=newBlock.calcHash()
        self.chain.append(newBlock)

# osa=BlockChain()
# print(type(datetime.now().date()))
# li=[]
# li2=[]
# #here  you  can manually enter the block details...for checking

# li.append("2017/01/27")
# li.append("saran")
# li.append("12548")
# li.append("ADMK")
# osa.addBlock(Block(li[0],li[1],li[2],li[3]))
# print(osa)
# for i in osa.chain:
#     print(i.tstamp)
#     print(i.name)
#     print(i.voter_id)
#     print(i.party)
    
#     print(i.prevhash)
#     print(i.hash)
