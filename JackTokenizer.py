#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:24:46 2022

@author: katamoto
"""

#import collections

# Define the class
class JackTokenizer:
    # Define the constructor
    def __init__(self, Filename):
        #self.name = name
        self.f = open(Filename)
        self.linestatus = True
        self.status = True
        self.token = ''
        self.tokentype = ''
        self.CurrentLine = ""
        self.keyword = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
        self.KeywordConstant = ['true', 'false', 'null', 'this']
        self.symbol = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
        self.tokenList = []
        self.token_index = 0
        self.debug = True
    
    def createTokenList(self):
        Iscomment = False
        tokenCandidate = self.f.readline()
        self.linestatus = ("" != tokenCandidate)
        
        tokenCandidate = tokenCandidate.lstrip()
        # Delete comment
        if(tokenCandidate[0:2] == '//'):
            Iscomment = True
        elif(tokenCandidate[0:2] == '/*' and tokenCandidate[-3:-1] == '*/'):
            Iscomment = True
        elif(tokenCandidate[0:2] == '/*' and tokenCandidate[-3:-1] != '*/'):
            while(tokenCandidate[-3:-1] != '*/'):
                tokenCandidate = self.f.readline()
            tokenCandidate = self.f.readline()
        
        # Check if there is a string
        ExistString = False
        # Used to store the position of " in a sentence as it is read from a file.
        string_index = []
        
        if('"' in tokenCandidate):
            ExistString = True
            string_index.append(tokenCandidate.find('"'))
            string_index.append(tokenCandidate.rfind('"'))
            string_index.append(tokenCandidate.rfind(';'))
            # The reason for the final '+2' is that string variables are always declared
            # at the end of a line , followed by a terminating character ';'
            #stringTmp = tokenCandidate[string_index[0]+1 : string_index[1]]+tokenCandidate[string_index[1]+1]
            stringTmp = tokenCandidate[string_index[0] : string_index[2]+1]
            # if(string_index[2] == string_index[1] + 1):
            #     stringTmp = tokenCandidate[string_index[0] : string_index[1]+2]
            # else:
            #     stringTmp = tokenCandidate[string_index[0] : string_index[1]+2]
            
        tokenCandidate = tokenCandidate.lstrip()
        tokenCandidate = tokenCandidate.split()
        
        # Used to refer to a location in an array that contains ".
        string_index2 = []
        string_index3 = []
        for i in range(len(tokenCandidate)):
            for j in range(len(tokenCandidate[i])):
                if(tokenCandidate[i][j] == '"'):
                    string_index2.append(i)
                    string_index3.append(j)
        
        if(ExistString and string_index2[0] != string_index2[1]):
            #TK_first_half = tokenCandidate[0:string_index[0]+1]
            TK_second_half = tokenCandidate[string_index[1]:]
            if(string_index3[0] == 0):
                tokenCandidate[string_index2[0]] = stringTmp
            else:
                tokenCandidate[string_index2[0]] = tokenCandidate[string_index2[0]][:string_index3[0]] + stringTmp
            tokenCandidate[string_index2[0]+1:] = TK_second_half
            #delnum = string_index2[1] - string_index2[0]
            # for k in range(delnum):
            #     del tokenCandidate[-1]
        
        # token list creation
        #token_index = 0
        
        for i in range(len(tokenCandidate)):
            if(tokenCandidate[i] == '//'):
                break
            elif(not Iscomment):
                symbol_index=[]
                ExistSymbol = False
                for j in range(len(tokenCandidate[i])):
                    if(tokenCandidate[i][j] in self.symbol):
                        symbol_index.append(j)
                        if(not ExistSymbol):
                            ExistSymbol = True
                        
                if(ExistSymbol):
                    for k in range(len(symbol_index)):
                        if(len(symbol_index) == 1):
                            if(symbol_index[k] == 0):
                                if(len(tokenCandidate[i]) == 1):
                                    if(self.debug):
                                        print(tokenCandidate[i])
                                    self.tokenList.append(tokenCandidate[i])
                                else:
                                    if(self.debug):
                                        print('first case : ')
                                        print(tokenCandidate[i][k])
                                        print(tokenCandidate[i][k+1:])
                                    self.tokenList.append(tokenCandidate[i][k])
                                    self.tokenList.append(tokenCandidate[i][k+1:])
                            elif(symbol_index[k] == len(tokenCandidate[i])-1):
                                if(self.debug):
                                    print('last case : ')
                                    print(tokenCandidate[i][:symbol_index[k]])
                                    print(tokenCandidate[i][symbol_index[k]])
                                self.tokenList.append(tokenCandidate[i][:symbol_index[k]])
                                self.tokenList.append(tokenCandidate[i][symbol_index[k]])
                            else:
                                if(self.debug):
                                    print('midle case : ')
                                    print(tokenCandidate[i][0:symbol_index[k]])
                                    print(tokenCandidate[i][symbol_index[k]])
                                    print(tokenCandidate[i][symbol_index[k]+1:])
                                self.tokenList.append(tokenCandidate[i][0:symbol_index[k]])
                                self.tokenList.append(tokenCandidate[i][symbol_index[k]])
                                self.tokenList.append(tokenCandidate[i][symbol_index[k]+1:])
                        else:
                            if(k != len(symbol_index)-1 and k == 0):
                                if(symbol_index[k] == 0):
                                    if(self.debug):
                                        print('case1-1 : ')
                                        print(tokenCandidate[i][0])
                                    self.tokenList.append(tokenCandidate[i][0])
                                else:
                                    if(self.debug):
                                        print('case1-2 : ')
                                        print(tokenCandidate[i][:symbol_index[k]])
                                    self.tokenList.append(tokenCandidate[i][:symbol_index[k]])
                            elif(k != len(symbol_index)-1 and k != 0):
                                if(self.debug):
                                    print('case2 : ')
                                if(symbol_index[k-1] != 0):
                                    if(self.debug):
                                        print(tokenCandidate[i][symbol_index[k-1]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k-1]])
                                if(self.debug):
                                    print(tokenCandidate[i][symbol_index[k-1]])
                                if(symbol_index[k-1]+1 != symbol_index[k]):
                                    if(self.debug):
                                        print(tokenCandidate[i][symbol_index[k-1]+1:symbol_index[k]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k-1]+1:symbol_index[k]])
                            else:
                                if(symbol_index[k-1] == 0):
                                    if(self.debug):
                                        print('case3-1 : ')
                                        print(tokenCandidate[i][1:symbol_index[k]])
                                        print(tokenCandidate[i][symbol_index[k]])
                                    if(symbol_index[k] != 1):
                                        self.tokenList.append(tokenCandidate[i][1:symbol_index[k]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k]])
                                    #if(k == len(symbol_index)):
                                    if(symbol_index[k] != len(tokenCandidate[i])-1):
                                        self.tokenList.append(tokenCandidate[i][symbol_index[k]+1:])
                                    
                                elif(symbol_index[k-1] != 0 and k == len(symbol_index)-1):
                                    if(self.debug):
                                        print('case3-2 : ')
                                        print(tokenCandidate[i][symbol_index[k-1]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k-1]])
                                    if(symbol_index[k-1]+1 != symbol_index[k]):
                                        if(self.debug):
                                            print(tokenCandidate[i][symbol_index[k-1]+1:symbol_index[k]])
                                        self.tokenList.append(tokenCandidate[i][symbol_index[k-1]+1:symbol_index[k]])
                                    #print(tokenCandidate[i][symbol_index[k]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k]])
                                    if(symbol_index[k] != len(tokenCandidate[i])-1):
                                        self.tokenList.append(tokenCandidate[i][symbol_index[k]+1:])
                                    # if(k == len(symbol_index)):
                                    #     self.tokenList.append(tokenCandidate[i][symbol_index[k]+1:])
                                else:
                                    if(self.debug):
                                        print('case3-3: ')
                                        print(k)
                                        print(len(symbol_index))
                                        print(tokenCandidate[i][symbol_index[k-1]:symbol_index[k]])
                                        print(tokenCandidate[i][symbol_index[k]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k-1]:symbol_index[k]])
                                    self.tokenList.append(tokenCandidate[i][symbol_index[k]])
                else:
                    if(self.debug):
                        print(tokenCandidate[i])
                    self.tokenList.append(tokenCandidate[i])
                #print(tokenCandidate[i]
    
    def hasMoreLines(self):
        return self.linestatus
    
    def hasMoreTokens(self):
        self.status = (self.token_index < len(self.tokenList))
        return self.status
    
    def advance(self):
        self.token = self.tokenList[self.token_index]
        self.token_index = self.token_index + 1
        #print(self.token)
    
    def getNext(self):
        # self.token = self.tokenList[self.token_index]
        # self.token_index = self.token_index + 1
        return self.tokenList[self.token_index+1]
    
    def tokenType(self):
        if(self.token in self.keyword):
            self.tokentype = 'keyword'
        elif(self.token in self.symbol):
            self.tokentype = 'symbol'
        elif(self.token.isdecimal()):
            self.tokentype = 'integerConstant'
        elif(self.token[0] == '"'):
            self.tokentype = 'stringConstant'
        else:
            self.tokentype = 'identifier'
        #print(self.tokentype)
        return self.tokentype
        
    def Keyword(self):
        return self.token
        
    def symbol(self):
        return self.token
    
    def identifier(self):
        return self.token
    
    def intVal(self):
        return self.token
    
    def stringVal(self):
        return self.token
    
    