#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:26:05 2022
"""

# Define the class
class SymbolTable:
    # Define the constructor
    def __init__(self):
        self.StaticTable = []
        self.FieldTable = []
        self.ArgTable = []
        self.VarTable = []
        self.StaticIdx = 0
        self.FieldIdx = 0
        self.ArgIdx = 0
        self.VarIdx = 0
        self.ClassName = ''

    def startSubroutine(self):
        self.ArgTable = []
        self.VarTable = []
        self.ArgIdx = 0
        self.VarIdx = 0
        # self.define('this', self.ClassName, 'ARG')
        return

    def define(self, name, types, kind):
        if(kind == 'STATIC'):
            self.StaticTable.append({'name': name, 'type':types, 'kind': kind, "idx":self.StaticIdx})
            self.StaticIdx = self.StaticIdx + 1
        elif(kind == 'FIELD'):
            self.FieldTable.append({'name': name, 'type':types, 'kind': kind, "idx":self.FieldIdx})
            self.FieldIdx = self.FieldIdx + 1
        elif(kind == 'ARG'):
            self.ArgTable.append({'name': name, 'type':types, 'kind': kind, "idx":self.ArgIdx})
            self.ArgIdx = self.ArgIdx + 1
        elif(kind == 'VAR'):
            self.VarTable.append({'name': name, 'type':types, 'kind': kind, "idx":self.VarIdx})
            self.VarIdx = self.VarIdx + 1
        return

    def varCount(self, kind):
        if(kind == 'STATIC'):
            return self.StaticIdx
        elif(kind == 'FIELD'):
            return self.FieldIdx
        elif(kind == 'ARG'):
            return self.ArgIdx
        elif(kind == 'VAR'):
            return self.VarIdx
    
    def kindOf(self, name):
        if(self.StaticTable != []):
            for i in range(self.StaticIdx):
                if(name in self.StaticTable[i]['name']):
                    return 'STATIC'
        if(self.FieldTable != []):
            for i in range(self.FieldIdx):
                if(name in self.FieldTable[i]['name']):
                    return 'FIELD'
        if(self.ArgTable != []):
            for i in range(self.ArgIdx):
                if(name in self.ArgTable[i]['name']):
                    return 'ARG'
        if(self.VarTable != []):
            for i in range(self.VarIdx):
                # print(i)
                if(name in self.VarTable[i]['name']):
                    return 'VAR'
        return 'NONE'
    
    def typeOf(self, name):
        if(self.StaticTable != []):
            for i in range(self.StaticIdx):
                if(name in self.StaticTable[i].values()):
                    return self.StaticTable[i]['type']
        if(self.FieldTable != []):
            for i in range(self.FieldIdx):
                if(name in self.FieldTable[i].values()):
                    return self.FieldTable[i]['type']
        if(self.ArgTable != []):
            for i in range(self.ArgIdx):
                if(name in self.ArgTable[i].values()):
                    return self.ArgTable[i]['type']
        if(self.VarTable != []):
            for i in range(self.VarIdx):
                if(name in self.VarTable[i].values()):
                    return self.VarTable[i]['type']
    
    def indexOf(self, name):
        if(self.StaticTable != []):
            for i in range(self.StaticIdx):
                if(name in self.StaticTable[i].values()):
                    return i
        if(self.FieldTable != []):
            for i in range(self.FieldIdx):
                if(name in self.FieldTable[i].values()):
                    return i
        if(self.ArgTable != []):
            for i in range(self.ArgIdx):
                if(name in self.ArgTable[i].values()):
                    return i
        if(self.VarTable != []):
            for i in range(self.VarIdx):
                if(name in self.VarTable[i].values()):
                    return i









