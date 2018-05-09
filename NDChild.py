class NDChild(object):
    def __init__ (self, learningrate, conslearningrate,language):

        self.grammar = {"lang":language,"SP": .5, "HIP": .5, "HCP": .5, "OPT": .5, "NS": .5, "NT": .5,"WHM": .5, "PI": .5, "TM": .5, "VtoI": .5, "ItoC": .5,"AH": .5, "QInv": .5}
        self.r = learningrate #simulation will pass child a learning rate
        self.conservativerate = conslearningrate

    def consumeSentence(self, s): #child is fed a list containing [lang, inflec, sentencestring]
        self.spEtrigger(s)    #parameter 1
        self.hipEtrigger(s)   #parameter 2
        self.hcpEtrigger(s)   #parameter 3
        self.optEtrigger(s)   #parameter 4
        self.nsEtrigger(s)    #parameter 5
        self.ntEtrigger(s)    #parameter 6
        self.whmEtrigger(s)   #parameter 7
        self.piEtrigger(s)    #parameter 8
        self.tmEtrigger(s)    #parameter 9
        self.VtoIEtrigger(s)  #parameter 10
        self.ItoCEtrigger(s)  #parameter 11
        self.ahEtrigger(s)    #parameter 12
        self.QInvEtrigger(s)  #parameter 13

    #etriggers for parameters
    # first parameter Subject Position
    def spEtrigger(self, s):
        # Check if O1 and S are in the sentence and sent is declarative
        if "O1" in s.sentenceList and "S" in s.sentenceList and s.inflection == "DEC":
            O1index = s.sentenceList.index("O1")
            Sindex = s.sentenceList.index("S") # Sindex is position of S in sentList
            # Make sure O1 is non-sentence-initial and before S
            if O1index > 0 and O1index < s.sentenceList.index("S"):
                # set towards Subject final
                self.adjustweight ("SP",1, self.r)
            # S occurs before 01
            elif Sindex > 0 and O1index > s.sentenceList.index("S"): # S cannot be Sent initial
                # set towards Subject initial
                self.adjustweight("SP",0,self.r)

    # second parameter Head IP, VP, PP, etc
    def hipEtrigger(self, s):
        if "O3" in s.sentenceList and "P" in s.sentenceList:
            O3index = s.sentenceList.index("O3")
            Pindex = s.sentenceList.index("P")
            # O3 followed by P and not topicalized
            if O3index > 0 and Pindex == O3index + 1:
                self.adjustweight ("HIP", 1, self.r)
            elif O3index > 0 and Pindex == O3index - 1:
                self.adjustweight ("HIP", 0, self.r)

        # If imperative, make sure Verb directly follows O1
        elif s.inflection == "IMP" and "O1" in s.sentenceList and "Verb" in s.sentenceList:
            if s.sentenceList.index("O1") == s.sentenceList.index("Verb") - 1:
                self.adjustweight ("HIP", 1, self.r)
            elif s.sentenceList.index("Verb") == (s.sentenceList.index("O1") - 1):
                self.adjustweight("HIP", 0, self.r)

    # third parameter Head in CP
    def hcpEtrigger(self, s):
        if s.inflection == "Q":
            # ka or aux last in question
            if s.sentenceList[-1] == 'ka' or ("ka" not in s.sentenceList and s.sentenceList[-1] == "Aux"):
                self.adjustweight("HCP", 1, self.r)
            # ka or aux first in question
            elif s.sentenceList[0] == "ka" or ("ka" not in s.sentenceList and s.sentenceList[0]=="Aux"):
                self.adjustweight("HCP", 0, self.r)


    #fourth parameter Optional Topic (0 is obligatory,  1 is optional)
    def optEtrigger(self, s):
        if self.grammar["TM"] > 0.5 and "[+WA]" not in s.sentenceStr:
            self.adjustweight("OPT",1,self.r)
        
        elif self.grammar["TM"] > 0.5 and "[+WA]" in s.sentenceStr:
            self.adjustweight("OPT",0, self.conservativerate)
         
        #first word in sentence is any of those & overt subject and full complemenets in VP
        elif (s.sentenceList[0] in ["ka","Verb","Aux","Not","Never"]) and ("S" in s.sentenceStr) and ("01" in s.sentenceStr) and ("02" in s.sentenceStr) and ("03" in s.sentenceStr) and ("P" in s.sentenceStr) and ("Adv" in s.sentenceStr):#all of [O1, O2, P O3, Adv] in VP:
            self.adjustweight("OPT",1,self.r) #Opt to 1 unambig
         
        

    def nsEtrigger(self, s):
        if s.inflection == "DEC" and "S" not in s.sentenceStr and s.outOblique():
            self.adjustweight("NS",1,self.r)
            self.adjustweight("OPT",1, self.r)
            
        elif s.inflection == "DEC" and "S" in s.sentenceStr and s.outOblique():
            self.adjustweight("NS",0,self.conservativerate)

    def ntEtrigger(self, s):
        if s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" not in s.sentenceStr:
            self.adjustweight("NT",1,self.r)
            self.adjustweight("OPT", 0, self.r) #null topic necessitates obligatory topic

        elif s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" in s.sentenceStr and "O3" in s.sentenceStr and "S" in s.sentenceStr and "Adv" in s.sentenceStr:
            self.adjustweight("NT",0,self.conservativerate)
        #if all possible complements of VP are in sentence, then the sentence is not Null Topic

    def whmEtrigger(self, s):
        if s.inflection == "Q" and "+WH" in s.sentenceStr:
            if ("+WH" in s.sentenceList[0]) or ("P" in s.sentenceList[0] and "O3[+WH]" == s.sentenceList[1]):
                self.adjustweight("WHM",1,self.conservativerate)
            else:
                self.adjustweight("WHM",0,self.r)

    def piEtrigger(self, s):
        pIndex = s.indexString("P")
        O3Index = s.indexString("O3")
        if pIndex > -1 and O3Index > -1:
            if abs(pIndex - O3Index) > 1:
                self.adjustweight("PI", 1, self.r)

            elif ((pIndex + O3Index) == 1):
                self.adjustweight ("PI",0,self.conservativerate)

    def tmEtrigger(self, s):
        if "[+WA]" in s.sentenceStr:
            self.adjustweight("TM",1,self.r)
        elif "O1" in s.sentenceList and "O2" in s.sentenceList and (abs(s.sentenceList.index("O1")-s.sentenceList.index("O2")) > 1):
            self.adjustweight("TM",0,self.r)

    def VtoIEtrigger(self, s):
        if "Verb" in s.sentenceStr and "O1" in s.sentenceStr:
            o1index = s.indexString("O1")
            if o1index != 0 and abs(s.indexString("Verb") - o1index) > 1:
                self.adjustweight("VtoI", 1, self.r)
                self.adjustweight("AH", 0, self.r)

        #no need to explicitly check inflection because only Q and DEC have AUX
        elif "Aux" in s.sentenceList:
            self.adjustweight("VtoI", 0, self.conservativerate)

            
    def ItoCEtrigger(self, s):
        sp = self.grammar['SP']
        hip = self.grammar['HIP']
        hcp = self.grammar['HCP']
         
        
        if s.inflection == "DEC" and "S" in s.sentenceList and "Aux" in s.sentenceList:
            if sp < 0.5 and hip < 0.5: # (Word orders 1, 5) subject and IP initial, aux to the right of Subject
                Sindex = s.sentenceList.index("S")
                if Sindex > 0 and s.sentenceList.index("Aux") == Sindex + 1:
                    self.adjustweight("ItoC", 0, self.r)
                
                elif hcp < 0.5 and (s.sentenceList.index("Aux") - s.sentenceList.index("S")) < 0: 
                #above code aux - s position less than 0 means aux precedes s 
                    self.adjustweight("ItoC", 1, self.r)

                elif hcp > 0.5 and s.sentenceList[-1] == "Aux":                                                     
                    self.adjustweight("ItoC", 1, self.r)

        
            elif sp > 0.5 and hip > 0.5: # (Word orders 2, 6) #subject and IP final, aux to the left of subject
                AuxIndex = s.sentenceList.index("Aux")
                if (AuxIndex > 0 and s.sentenceList.index("S") == AuxIndex + 1):
                    self.adjustweight("ItoC", 0, self.r)
                
                elif s.sentenceList.index("Aux") == 0:
                    self.adjustweight("ItoC", 1, self.r)
                
                elif hcp < 0.5 and (s.sentenceList.index("Aux") < s.sentenceList.index("Verb")):
                    self.adjustweight("ItoC", 1, self.r)
                
                elif s.sentenceList[-1] == "Aux" and s.sentenceList.index("S") == (AuxIndex - 1):
                    self.adjustweight("ItoC", 1, self.r)
              
           
            elif sp > 0.5 and hip < 0.5 and hcp > 0.5 and "Verb" in s.sentenceList: #subject and C final, IP initial, Aux immediately follows verb
                if s.sentenceList.index("Verb") == s.sentenceList.index("Aux") + 1:
                    self.adjustweight("ItoC", 0, self.conservativerate)
                elif s.sentenceList.index("Aux") == 0: # if it's Comp Final and aux is first, it did not move to C.
                    self.adjustweight("ItoC", 0, self.r)
                elif s.sentenceList[-1] == "Aux": #if it's the last thing in the sentence it moved to C. If it's first it did not.
                    self.adjustweight("ItoC", 1, self.r)

            elif sp < 0.5 and hip > 0.5 and hcp < 0.5 and "Verb" in s.sentenceList: #subject and C initial, IP final, Aux immediately precedes verb
                if s.sentenceList.index("Aux") == s.sentenceList.index("Verb") + 1:
                    self.adjustweight("ItoC", 0, self.r)
                else:
                    self.adjustweight("ItoC", 1, self.conservativerate)
                    #will experiment with aggressive rate
  
            elif "Aux" in s.sentenceStr and "Verb" in s.sentenceList: #check if aux and verb in sentence and something comes between them
                Vindex = s.sentenceList.index("Verb")
                Auxindex = s.sentenceList.index("Aux")
                indexlist = [] #tokens that would shed light if between 
                if "S" in s.sentenceList:
                    Sindex = s.sentenceList.index ("S")
                    indexlist.append(Sindex)
                    
                if "O1" in s.sentenceList:
                    O1index = s.sentenceList.index ("O1")
                    indexlist.append(O1index)
                    
                if "O2" in s.sentenceList:
                    O2index = s.sentenceList.index ("O2")
                    indexlist.append(O2index)
                
                if abs(Vindex - Auxindex) != 1: #if verb and aux not adjacent
                    for idx in indexlist:
                        if ( Vindex < idx < Auxindex ) or (Vindex > idx > Auxindex): #if item in index list between them
                            self.adjustweight("ItoC", 1, self.r) #set toward 1
                            break
                            
#        elif s.inflection == "DEC" and "Never" in s.sentenceStr and "Verb" in s.sentenceStr and "O1" in s.sentenceStr:
#            neverPos = s.indexString("Never")
#            verbPos = s.indexString("Verb")
#            O1Pos = s.indexString("O1")
            
#            if (neverPos > -1 and verbPos == neverPos+1 and O1Pos == verbPos+1) or (O1Pos > -1 and verbPos == O1Pos+1 and neverPos == verbPos + 1):
#                self.adjustweight("ItoC", 0, self.r)
             

    def ahEtrigger(self, s):
        if (s.inflection == "DEC" or s.inflection == "Q") and ("Aux" not in s.sentenceStr and "Never" in s.sentenceStr and "Verb" in s.sentenceStr and "O1" in s.sentenceStr):
            neverPos = s.indexString("Never")
            verbPos = s.indexString("Verb")
            O1Pos = s.indexString("O1")

            if (neverPos > -1 and verbPos == neverPos+1 and O1Pos == verbPos+1) or (O1Pos > -1 and verbPos == O1Pos+1 and neverPos == verbPos + 1):
                self.adjustweight("AH", 1, self.r)
                self.adjustweight("VtoI", 0, self.r)

        elif "Aux" in s.sentenceStr and self.grammar["AH"] <= 0.5:
            self.adjustweight ("AH",0,self.conservativerate)
            #if self.grammar["VtoI"] > 0.5: #If not affix hopping language, vtoi is either 0 or 1, but if evidence of vtoi towards 1 has alreadybeen observed, increase confidence 1VtoI given 0AH
            #   self.adjustweight("VtoI", 1, self.conservativerate)

    def QInvEtrigger(self, s):
        if s.inflection == "Q" and "ka" in s.sentenceStr:
            self.adjustweight("QInv", 0, self.r)
            self.adjustweight("ItoC",0, self.r)
            
        elif s.inflection == "Q"and "ka" not in s.sentenceStr and "WH" not in s.sentenceStr:
            self.adjustweight("QInv", 1, self.r)
#            self.adjustweight("ItoC", 1, self.conservativerate)
     
                            
            
    def adjustweight(self, parameter, direction, rate):
        if direction == 0:
            self.grammar[parameter] -= rate*self.grammar[parameter]
        elif direction == 1:
            self.grammar[parameter] += rate*(1-self.grammar[parameter])
