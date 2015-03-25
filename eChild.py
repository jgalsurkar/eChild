import random
import pickle

###Load surface equivalence dictionary###
SEfile = open('/Users/JohnnyXD1/Desktop/RESEARCH/SEpickled.txt','rU')
SEdict = pickle.load(SEfile)
SEfile.close()


#index returns the index of a value in a list; returns -1 if value not in list
def index(listP, value):
    try:
        i = list.index(listP, value)
        return i
    except ValueError:
        return -1

#Returns the index of value in the list, in this case it can find the value as a substring in the index of the list    
def first_substring(listP, value):
    return next((i for i, string in enumerate(listP) if value in string),-1)
    
#######################################################
################# Child Class #########################
#######################################################

class Child(object):
    
    def __init__(self):
        #This boolean is False unless the function checkIfLearned sets it to True (which happens when the grammar is acquired). The main program will while-loop until
        #grammarLearned == True
        self.grammarLearned = False
        
        #in time sits the number of sentences (discrete time units) the echild has been exposed to at the current time
        self.time = 0
        
        self.grammar = "0 0 0 0 0 0 1 0 0 0 0 0 0".split()
    
    #This function will set the current information about the sentence and the sentence itself for the child
    def setInfo(self, info):

        info = info.replace('\n','')
        info = info.replace('\"','')
        self.infoList =  info.rsplit("\t",3)
        
        
    def isQuestion(self):
        if self.infoList[1] == "Q":
            return True
        return False
    
    def isImperative(self):
        if self.infoList[1] == "IMP":
            return True
        return False
    
    def isDeclarative(self):
        if self.infoList[1] == "DEC":
            return True
        return False
    
    def outOblique(self):
        temp = self.infoList[2].split()
        i = first_substring(temp,"O1")
        j = first_substring(temp,"O2") 
        k = first_substring(temp,"P O3")
        l = first_substring(temp,"O3 P")

        if i != -1 and j != -1 and k != -1 and i < j < k:  
            return False
        elif i != -1 and j != -1 and l != -1 and l < j < i:
            return False
        return True
        
        
    def setParameters(self):
        self.setSubjPos()    #Parameter 1
        self.setHead()       #Parameter 2
        self.setHeadCP()     #Parameter 3
        #Parameter 4 - Obligatory Topic : Problem parameter
        self.setNullSubj()   #Parameter 5
        self.setNullTopic()  #Parameter 6
        self.setWHMovement() #Parameter 7
        self.setPrepStrand() #Parameter 8
        self.setTopicMark()  #Parameter 9
        self.vToI()          #Parameter 10
        #Parameter 11 - I to C movement : Problem parameter
        self.affixHop()      #Parameter 12
        #Parameter 13 - Question Inversion : Problem parameter
        
        
    #1st parameter
    def setSubjPos(self):
        if "O1" in self.infoList[2] and "S" in self.infoList[2]: #Check if O1 and S are in the sentence
            temp = self.infoList[2].split()
            first = first_substring(temp,"01") #Find index of O1
            if first > 0 and first < first_substring(temp,"S"): # Make sure O1 is non-sentence-initial and before S
                self.grammar[0] = '1'
                
    #2nd parameter
    def setHead(self):
        temp = self.infoList[2].split()
        if "O3" in self.infoList[2] and "P" in self.infoList[2]:
            first = first_substring(temp,"O3")
            if first > 0 and first_substring(temp,"P") == first + 1: #O3 followed by P
                self.grammar[1] = '1'
        #If imperative, make sure Verb directly follows O1
        if self.isImperative() and "O1" in self.infoList[2] and "Verb" in self.infoList[2]:
            if first_substring(temp, "O1") == first_substring(temp, "Verb") - 1:
                self.grammar[1] = '1'
                
                
    #3rd parameter 
    def setHeadCP(self):
        temp = self.infoList[2].split()
        if(self.isQuestion()):
            if index(temp, "ka") == len(temp)-1 or ("ka" not in temp and index(temp, "Aux") == len(temp)-1):
                self.grammar[2] = '1'
                
                
    #5th parameter
    #Only works for full, not necessarily with CHILDES distribution
    def setNullSubj(self):
        if self.isDeclarative() and "S" not in self.infoList[2] and self.outOblique():
            print self.outOblique()
            self.grammar[4] = '1'

    #6th parameter   
    def setNullTopic(self):
        if "O2" in self.infoList[2] and "O1" not in self.infoList[2] :
            self.grammar[5] = '1'
    
    #7th parameter
    def setWHMovement(self):
        if first_substring(self.infoList[2].split(), "+WH") > 0:
            self.grammar[6] = '0'
                
    #8th parameter
    def setPrepStrand(self):
        if "P" in self.infoList[2] and "O3" in self.infoList[2] :
            temp = self.infoList[2].split()
            i = first_substring(temp,"P") #Get index of P
            j = first_substring(temp,"O3")#Get index of O3
            if i != -1 and j != -1 and abs(i - j) != 1 : #If they exist, make sure they aren't adjacent
                self.grammar[7] = '1'  
    
    
    #9th parameter
    def setTopicMark(self):
        if "WA" in self.infoList[2] :
            self.grammar[8] = '1' 
    
    #10th parameter
    def vToI(self):
        if "O1" in self.infoList[2] and "Verb" in self.infoList[2] :
            temp = self.infoList[2].split()
            i = first_substring(temp,"O1")
            j = first_substring(temp,"Verb")
            if i > 0 and j != -1 and abs(i - j) != 1 :
                self.grammar[9] = '1' 
            
    
    #12th parameter
    def affixHop(self):
        if "Never Verb O1" in self.infoList[2]:
            self.grammar[11] = 1
        if first_substring(self.infoList[2].split(), "O1") > 0 and "O1 Verb Never" in self.infoList[2]:
            self.grammar[11] = 1
    

                
#######################################################
################# End of Child Class ##################
#######################################################




#######################################################
######################## MAIN #########################
#######################################################

infoFile = open('/Users/JohnnyXD1/Desktop/RESEARCH/french.txt','rU') # 0001001100011
sentenceInfo = infoFile.readlines()
infoFile.close()
#print ''.join('v{}: {}'.format(v, i) for v, i in enumerate(sentenceInfo))
eChild = Child()

count = 0

while eChild.grammarLearned == False :
    eChild.setInfo(random.choice(sentenceInfo))
    print eChild.infoList
    eChild.setParameters()
    if count == 10000:
        eChild.grammarLearned = True
    count+=1
print eChild.grammar
    


errFile = open('/Users/JohnnyXD1/Desktop/RESEARCH/Statistics/error.txt','w')

errFile.close()

###########################################################
######################## End MAIN #########################
###########################################################

