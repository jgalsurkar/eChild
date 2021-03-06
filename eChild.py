import time
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

get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)

    
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

        self.grammar = "2 2 2 0 0 0 1 0 0 0 1 0 1".split()
    
    #This function will set the current information about the sentence and the sentence itself for the child
    def setInfo(self, info):
        info = info.replace('\n','')
        info = info.replace('\"','')
        self.infoList =  info.rsplit("\t",3)
        self.sentence = self.infoList[2].split()
        self.expectedGrammar = " ".join(get_bin(int(self.infoList[0]),13)).split()
        self.time += 1
        
        
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
    
    def containsTopicalizable(self):
        i = first_substring(self.sentence,"S")
        j = first_substring(self.sentence,"O1")
        k = first_substring(self.sentence,"O2") 
        l= first_substring(self.sentence,"O3")
        m = first_substring(self.sentence,"Adv")
        
        if i == 0 or j == 0 or k == 0 or l == 0 or m == 0 :
            return True
        return False
    
    def outOblique(self):
        i = first_substring(self.sentence,"O1")
        j = first_substring(self.sentence,"O2") 
        k = first_substring(self.sentence,"P")
        l = first_substring(self.sentence,"O3")

        if i != -1 and j != -1 and k != -1 and (i < j < k and l == k+1):  
            return False
        elif i != -1 and j != -1 and k != -1 and ( l < j < i and k == l+1):
            return False
        elif (i != -1 and j != -1 and k != -1 and l != -1):
            return True
    
    
    def S_Aux(self):
        if self.isDeclarative():
            i = first_substring(self.sentence, "S")
            if i > 0 and first_substring(self.sentence, "Aux") == i + 1:
                return True
        return False
            
    def Aux_S(self):
        if self.isDeclarative():
            i = first_substring(self.sentence, "Aux")
            if i > 0 and first_substring(self.sentence, "S") == i + 1:
                return True
        return False
    
    def Aux_Verb(self):
        if self.isDeclarative() and (first_substring(self.sentence, "Aux") == first_substring(self.sentence, "Verb") - 1):
            return True
        return False
    
    def Verb_Aux(self):
        if self.isDeclarative() and (first_substring(self.sentence, "Verb") == first_substring(self.sentence, "Aux") - 1):
            return True
        return False
    
    def Never_Verb(self):
        if self.isDeclarative() and (first_substring(self.sentence, "Never") == first_substring(self.sentence, "Verb") - 1) and "Aux" not in self.sentence:
            return True
        return False
    
    def Verb_Never(self):
        if self.isDeclarative() and (first_substring(self.sentence, "Verb") == first_substring(self.sentence, "Never") - 1) and "Aux" not in self.sentence:
            return True
        return False
    
    def hasKa(self):
        if "ka" in self.sentence:
            return True
        return False
    
    
    def setParameters(self):
        if self.grammar[0] == '2':
            self.noSubjPos()
        if self.grammar[0] != '1':
            self.setSubjPos()    #Parameter 1
        
        if self.grammar[1] == '2':
            self.noHead()  
        if self.grammar[1] != '1':
            self.setHead()       #Parameter 2

        if self.grammar[2] == '2':
            self.noHeadCP()    
        if self.grammar[2] != '1':
            self.setHeadCP()     #Parameter 3
            
        if not (self.grammar[3] == '0' and self.grammar[5] == '1'):
            self.setObligTopic() #Parameter 4 - Obligatory Topic : Problem parameter
        if self.grammar[4] == '0':
            self.setNullSubj()   #Parameter 5
        if self.grammar[5] == '0':
            self.setNullTopic()  #Parameter 6
        if self.grammar[6] == '1':
            self.setWHMovement() #Parameter 7
        if self.grammar[7] == '0':
            self.setPrepStrand() #Parameter 8
        if self.grammar[8] == '0':
            self.setTopicMark()  #Parameter 9
        if self.grammar[9] == '0':
            self.vToI()          #Parameter 10
        #Parameter 11 - I to C movement : Problem parameter
        if self.grammar[10] == '1':
            self.iToC()
        if self.grammar[11] == '0':
            self.affixHop()      #Parameter 12
        #Parameter 13 - Question Inversion : Problem parameter
        if self.grammar[12] == '1':
            self.questionInver()
        
        if(self.grammar == self.expectedGrammar):
            self.grammarLearned = True
               
    #1st parameter
    def setSubjPos(self):
        if "O1" in self.infoList[2] and "S" in self.infoList[2]: #Check if O1 and S are in the sentence
            first = first_substring(self.sentence,"O1") #Find index of O1
            if first > 0 and first < first_substring(self.sentence,"S"): # Make sure O1 is non-sentence-initial and before S
                self.grammar[0] = '1'
                
    def noSubjPos(self):
        if "O1" in self.infoList[2] and "S" in self.infoList[2]: #Check if O1 and S are in the sentence
            first = first_substring(self.sentence,"S") #Find index of O1
            if first >= 0 and first < first_substring(self.sentence,"O1"): # Make sure O1 is non-sentence-initial and before S
                self.grammar[0] = '0'
    
    #2nd parameter
    def setHead(self):
        if "O3" in self.infoList[2] and "P" in self.infoList[2]:
            first = first_substring(self.sentence,"O3")
            if first > 0 and first_substring(self.sentence,"P") == first + 1: #O3 followed by P
                self.grammar[1] = '1'
        #If imperative, make sure Verb directly follows O1
        if self.isImperative() and "O1" in self.infoList[2] and "Verb" in self.infoList[2]:
            if first_substring(self.sentence, "O1") == first_substring(self.sentence, "Verb") - 1:
                self.grammar[1] = '1'
    
    def noHead(self):
        if "O3" in self.infoList[2] and "P" in self.infoList[2]:
            first = first_substring(self.sentence,"P")
            if first > 0 and first_substring(self.sentence,"O3") == first + 1: #O3 followed by P
                self.grammar[1] = '0'
        #If imperative, make sure Verb directly follows O1
        if self.isImperative() and "O1" in self.infoList[2] and "Verb" in self.infoList[2]:
            if first_substring(self.sentence, "Verb") == first_substring(self.sentence, "O1") - 1:
                self.grammar[1] = '0'    
                
    #3rd parameter 
    def setHeadCP(self):
        if(self.isQuestion()):
            if index(self.sentence, "ka") == len(self.sentence)-1 or ("ka" not in self.sentence and index(self.sentence, "Aux") == len(self.sentence)-1):
                self.grammar[2] = '1'
    
    def noHeadCP(self):
        if(self.isQuestion()):
            if index(self.sentence, "ka") == 0 or ("ka" not in self.sentence and index(self.sentence, "Aux") == 0):
                self.grammar[2] = '0'
                
    #4th parameter
    def setObligTopic(self):
        if self.isDeclarative():
            if "O2" in self.infoList[2] and "O1" not in self.infoList[2] :
                self.grammar[5] = '1'
                if self.grammar[3] == '1':
                    self.grammar[3] = '0'
            else:
                if(self.containsTopicalizable()) :
                    self.grammar[3] = '1'
                
    #5th parameter
    #Only works for full, not necessarily with CHILDES distribution
    def setNullSubj(self):
        if self.isDeclarative() and "S" not in self.infoList[2] and self.outOblique():
            self.grammar[4] = '1'
            print self.grammar[4]

    #6th parameter   
    def setNullTopic(self):
        if "O2" in self.infoList[2] and "O1" not in self.infoList[2] :
            self.grammar[5] = '1'
    
    #7th parameter
    def setWHMovement(self):
        if first_substring(self.sentence, "+WH") > 0 and "O3[+WH]" not in self.infoList[2]:
            self.grammar[6] = '0'
                
    #8th parameter
    def setPrepStrand(self):
        if "P" in self.infoList[2] and "O3" in self.infoList[2] :
            i = first_substring(self.sentence,"P") #Get index of P
            j = first_substring(self.sentence,"O3")#Get index of O3
            if i != -1 and j != -1 and abs(i - j) != 1 : #If they exist, make sure they aren't adjacent
                self.grammar[7] = '1'  
    
    
    #9th parameter
    def setTopicMark(self):
        if "WA" in self.infoList[2] :
            self.grammar[8] = '1' 
    
    #10th parameter
    def vToI(self):
        if "O1" in self.infoList[2] and "Verb" in self.infoList[2] :
            i = first_substring(self.sentence,"O1")
            j = first_substring(self.sentence,"Verb")
            if i > 0 and j != -1 and abs(i - j) != 1 :
                self.grammar[9] = '1' 
               
    #11th parameter
    def iToC(self):
        if self.grammar[0] == '0' and self.grammar[1] == '0' and self.grammar[2] == '0' and self.S_Aux():
            self.grammar[10] = '0'
        if self.grammar[0] == '1' and self.grammar[1] == '1' and self.grammar[2] == '1' and self.Aux_S():
            self.grammar[10] = '0'
        if self.grammar[0] == '1' and self.grammar[1] == '0' and self.grammar[2] == '1' and self.Aux_Verb():
            self.grammar[10] = '0'
        if self.grammar[0] == '0' and self.grammar[1] == '1' and self.grammar[2] == '0' and self.Verb_Aux():
            self.grammar[10] = '0'
        if self.grammar[0] == '0' and self.grammar[1] == '0' and self.grammar[2] == '1' and self.S_Aux():
            self.grammar[10] = '0'
        if self.grammar[0] == '1' and self.grammar[1] == '1' and self.grammar[2] == '0' and self.Aux_S():
            self.grammar[10] = '0'
        if self.grammar[0] == '1' and self.grammar[1] == '0' and self.grammar[2] == '0' and (self.Never_Verb() or self.hasKa()):
            self.grammar[10] = '0'
        if self.grammar[0] == '0' and self.grammar[1] == '1' and self.grammar[2] == '1' and (self.Verb_Never() or self.hasKa()):
            self.grammar[10] = '0'
    
    #12th parameter
    def affixHop(self):
        if "Never Verb[+FIN] O1" in self.infoList[2]:
            self.grammar[11] = '1'
        if first_substring(self.sentence, "O1") > 0 and "O1 Verb[+FIN] Never" in self.infoList[2]:
            self.grammar[11] = '1'
    
    #13th parameter
    def questionInver(self):
        if "ka" in self.infoList[2]:
            self.grammar[12] = '0'
    

                
#######################################################
################# End of Child Class ##################
#######################################################


#######################################################
######################## MAIN #########################
#######################################################
def main():
    infoFile = open('/Users/JohnnyXD1/Desktop/RESEARCH/french.txt','rU') # 0001001100011
    sentenceInfo = infoFile.readlines()
    infoFile.close()
    #print ''.join('v{}: {}'.format(v, i) for v, i in enumerate(sentenceInfo))
    eChild = Child()
    
    count = 0
    
    while eChild.grammarLearned == False :
        eChild.setInfo(random.choice(sentenceInfo))
       # print eChild.infoList
        eChild.setParameters()
        if count == 1000:
            eChild.grammarLearned = True
        count+=1
    print eChild.grammar
    print eChild.expectedGrammar
    print eChild.time
    
    
    errFile = open('/Users/JohnnyXD1/Desktop/RESEARCH/Statistics/error.txt','w')
    errFile.write("Japanese: " + str(eChild.time))
    errFile.close()
    
###########################################################
######################## End MAIN #########################
###########################################################

if __name__ == '__main__':
    start = time.time() 
    main()
    end = time.time() - start
    print "Time to complete:", end