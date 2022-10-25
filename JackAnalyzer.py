#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 11:27:04 2022

@author: katamoto
"""

import sys
import CompilationEngine
import JackTokenizer
import glob

args = sys.argv
InputFile = glob.glob(args[1])

# Compile from Sys.vm
IPath = args[1][:-5]
Extention = '.xml'
OutputFile = IPath + Extention
f = open(OutputFile, 'w')

LabelDict = {}

J = JackTokenizer.JackTokenizer(str(InputFile)[2:-2])

J.createTokenList()

while(J.hasMoreLines()):
     J.createTokenList()
     
C = CompilationEngine.CompilationEngine(J, OutputFile)
C.compileClass()

#f.write('<tokens>' + '\n')

# while(J.hasMoreTokens()):
#     J.advance()
#     J.tokenType()
#     f.write('<' + J.tokentype + '>' + ' ')
#     if(J.tokenType() == 'stringConstant'):
#         f.write(J.token[1:-1] + ' ')
#     elif(J.token == '<'):
#         f.write('&lt;' + ' ')
#     elif(J.token == '>'):
#         f.write('&gt;' + ' ')
#     elif(J.token == '&'):
#         f.write('&amp;' + ' ')
#     else:
#         f.write(J.token + ' ')
#     f.write('</' + J.tokentype + '>' + '\n')
    
# f.write('</tokens>' + '\n')

#f.close()


