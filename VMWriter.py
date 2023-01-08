#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 14:54:43 2022

"""

import SymbolTable

# Define the class
class VMWriter:
    # Define the constructor
    # def __init__(self, InputXMLFilename, OutputVMFilename):
    def __init__(self, OutputVMFilename):
        # self.f1 = open(InputXMLFilename)
        self.f2 = open(OutputVMFilename ,'w')
    
    def readXMLFile(self):
        return
    
    def writeTest(self):
        self.f2.writelines('Test')
        return

    def writePush(self, Segment, Index):
        if(Segment == 'CONSTANT'):
            self.f2.writelines('push constant ' + str(Index) + '\n')
        elif(Segment == 'VAR'):
            self.f2.writelines('push local ' + str(Index) + '\n')
        elif(Segment == 'ARG'):
            self.f2.writelines('push argument ' + str(Index) + '\n')
        elif(Segment == 'FIELD'):
            self.f2.writelines('push field ' + str(Index) + '\n')
        elif(Segment == 'POINTER'):
            self.f2.writelines('push pointer ' + str(Index) + '\n')
        elif(Segment == 'THIS'):
            self.f2.writelines('push this ' + str(Index) + '\n')
        elif(Segment == 'THAT'):
            self.f2.writelines('push that ' + str(Index) + '\n')
        elif(Segment == 'TEMP'):
            self.f2.writelines('push temp ' + str(Index) + '\n')
        elif(Segment == 'STATIC'):
            self.f2.writelines('push static ' + str(Index) + '\n')
        return

    def writePop(self, Segment, Index):
        if(Segment == 'VAR'):
            self.f2.writelines('pop local ' + str(Index) + '\n')
        elif(Segment == 'ARG'):
            self.f2.writelines('pop argument ' + str(Index) + '\n')
        elif(Segment == 'CONSTANT'):
            self.f2.writelines('pop constant ' + str(Index) + '\n')
        elif(Segment == 'FIELD'):
            self.f2.writelines('pop field ' + str(Index) + '\n')
        elif(Segment == 'THIS'):
            self.f2.writelines('pop this ' + str(Index) + '\n')
        elif(Segment == 'POINTER'):
            self.f2.writelines('pop pointer ' + str(Index) + '\n')
        elif(Segment == 'TEMP'):
            self.f2.writelines('pop temp ' + str(Index) + '\n')
        elif(Segment == 'THAT'):
            self.f2.writelines('pop that ' + str(Index) + '\n')
        elif(Segment == 'STATIC'):
            self.f2.writelines('pop static ' + str(Index) + '\n')
        return

    def writeArithmetic(self, command):
        return
    
    def writeLabel(self, label):
        self.f2.writelines('label ' + label + '\n')
        return
    
    def writeGoto(self, label):
        self.f2.writelines('goto ' + label + '\n')
        return 
    
    def writeIf(self, label):
        self.f2.writelines('if-goto ' + label + '\n')
        return
    
    def writeCall(self, name, nArgs):
        self.f2.writelines('call ' + name + ' ' + str(nArgs) + '\n')
        return
    
    def writeFunction(self, name, nLocals):
        self.f2.writelines('function ' + name + ' ' + str(nLocals) + '\n')
        return
    
    def writeReturn(self):
        self.f2.writelines('return\n')
        return
    
    def close(self):
        return
    
    def writeExpression(self, ElementArray, S):
        while '(' in ElementArray:
            ElementArray.remove('(')
        while ')' in ElementArray:
            ElementArray.remove(')')
        for i in range(len(ElementArray)):
            if(ElementArray[i].isdigit()):
                VMWriter.writePush(self, 'CONSTANT', ElementArray[i])
            elif(ElementArray[i] == '+'):
                self.f2.writelines('add\n')
            elif(ElementArray[i] == '*'):
                self.f2.writelines('call Math.multiply 2\n')
        return