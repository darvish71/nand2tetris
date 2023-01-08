#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 11:27:04 2022
@author: katamoto
"""

import JackTokenizer
import VMWriter

# Define the class
class CompilationEngine:
    # Define the constructor
    def __init__(self, J, S, V, OutputFilename, OutputVMFilename):
        self.J = J
        self.S = S
        self.V = V
        self.f = open(OutputFilename ,'w')
        self.f2 = open(OutputVMFilename ,'w')
        self.indent = 0
        self.indent_str = '  '
        self.adCount = 0
        self.op = ['+','-','*','/','&','|','<','>','=']
        self.unaryOp = False
        self.unaryOperand = ''
        self.IdName = ''
        self.IdType = ''
        self.IdKind = ''
        self.IdCount = 0
        self.NumExpression = 0
        self.ExClass = ''
        self.ElementArray = []
        self.VarName = ''
        self.Subroutine = ''
        self.method = False
        self.num_label = 1
        self.FuncIsVoid = False
        self.NumField = 0
        self.IsConstructor = False
        self.IsScopeConstructor = False
        self.IsMethod = False
        self.ObjName = ''
        self.IsObj = False
        self.DefArray = False
        self.SubRoutineCall = False
        self.LeftHandExpression = False

    def compileClass(self):
        self.f.writelines('<class>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.J.advance()
        self.adCount = self.adCount + 1
        while(self.J.Keyword() != '}'):
            if(self.J.Keyword() == 'static' or self.J.Keyword() == 'field'):
                if(self.J.Keyword() == 'field'):
                    self.NumField = self.NumField + (self.IdCount-2)//2+1
                CompilationEngine.compileClassVarDec(self)
                
                # print('Number of field variables is  : ' + str((self.IdCount-2)//2+1))
                # print(self.NumField)
            elif(self.J.Keyword() == 'function' or self.J.Keyword() == 'constructor' or self.J.Keyword() == 'method'):
                CompilationEngine.compileSubroutine(self)
                
            else:
                if(self.J.tokenType() == 'identifier'):
                    self.S.ClassName = self.J.Keyword()
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'CLASS ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    # self.V.writeTest()
                else:
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        self.f.writelines('</class>\n')
        # print('class : ' + str(self.adCount))
        return

    def compileClassVarDec(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<classVarDec>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        if(self.J.Keyword() == 'static'):
            self.IdKind = 'STATIC'
        elif(self.J.Keyword() == 'field'):
            self.IdKind = 'FIELD'
        # self.IdKind = 'STATIC'
        self.IdCount = 0
        
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        while(self.J.Keyword() != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
            self.IdCount = self.IdCount + 1
            space = self.indent_str * self.indent
            if(self.IdCount == 1):
                self.IdType = self.J.Keyword()
            elif(self.IdCount%2 == 0):
                self.IdName = self.J.Keyword()
                self.S.define(self.IdName, self.IdType, self.IdKind)
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.IdKind +' ' + self.IdType + ' ' + str(self.S.indexOf(self.IdName)) + ' ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                continue
            
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')     
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</classVarDec>\n')
        # print('classVarDec : ' + str(self.adCount))
        return

    def compileSubroutine(self):
        self.S.startSubroutine()
        space = self.indent_str * self.indent
        self.f.writelines(space + '<subroutineDec>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.Subroutine = ''
        self.FuncIsVoid = False
        self.IsConstructor = False
        self.IsMethod = False
        self.ObjName = ''
        self.IsObj = False
        
        while(self.J.Keyword() != '}'):
            if(self.J.Keyword() == '('):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileParameterList(self)
                # if(self.IdCount < 3):
                #     self.V.writeFunction(self.S.ClassName + '.' + self.Subroutine, 0)
                # else:
                #     self.V.writeFunction(self.S.ClassName + '.' + self.Subroutine, self.S.VarIdx)
            elif(self.J.Keyword() == '{'):
                
                # if(self.IsMethod):
                #     self.V.writePush('POINTER', 0)
                CompilationEngine.compileSubroutineBody(self)
                if(self.J.Keyword() == '}'):
                    break
            else:
                if(self.J.tokenType() == 'identifier'):
                    if(self.J.Keyword() == self.S.ClassName):
                        self.f.writelines(space + '<' + self.J.tokenType() + '> ' +'CLASS ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    else:
                        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'SUBROUTINE ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                        self.Subroutine = self.J.Keyword()
                        # self.V.writeFunction(self.S.ClassName + '.' + self.J.Keyword(), 0)
                elif(self.J.Keyword() == 'void'):
                    self.FuncIsVoid = True
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                elif(self.J.Keyword() == 'constructor'):
                    self.IsConstructor = True
                    self.IsScopeConstructor = True
                elif(self.J.Keyword() == 'method'):
                    self.IsMethod = True
                else:
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</subroutineDec>\n')
        # self.IsScopeConstructor = False
        print('SubRoutine : ' + str(self.adCount))
        return

    def compileParameterList(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<parameterList>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.IdKind = ''
        self.IdCount = 0
        while(self.J.Keyword() != ')'):
            if(self.J.Keyword() != '('):
                if(self.J.tokenType() == 'identifier' ):
                    if(self.S.kindOf(self.J.Keyword()) == 'NONE'):
                        self.IdKind = 'ARG'
                    else:
                        self.IdKind= 'VAR'
                if(self.IdCount%3 == 2 and self.IdCount != 0):
                    self.IdName = self.J.Keyword()
                    if(self.IsMethod and self.IdKind == 'ARG' and self.S.ArgIdx == 0):
                        # self.S.ArgIdx = self.S.ArgIdx + 1
                        self.S.define(self.ObjName, '', self.IdKind)
                    self.S.define(self.IdName, self.IdType, self.IdKind)
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.IdKind +' ' + self.IdType + ' ' + str(self.S.indexOf(self.IdName)) + ' ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                else:
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            if(self.IdCount == 1):
                self.IdType = self.J.Keyword()
            # elif(self.IdCount%3 == 2 and self.IdCount != 0):
            #     self.IdName = self.J.Keyword()
            #     self.S.define(self.IdName, self.IdType, self.IdKind)
            #     self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.IdKind +' ' + self.IdType + ' ' + str(self.S.indexOf(self.IdName)) + ' ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            #     self.J.advance()
            #     self.adCount = self.adCount + 1
            #     self.IdCount = self.IdCount + 1
            #     continue
            self.J.advance()
            self.adCount = self.adCount + 1
            self.IdCount = self.IdCount + 1
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</parameterList>\n')
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        # print('ParameterList : ' + str(self.adCount))
        return

    def compileSubroutineBody(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<subroutineBody>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.J.advance()
        self.adCount = self.adCount + 1
        while(self.J.Keyword() != '}'):
            
            if(self.J.Keyword() == 'var'):
                CompilationEngine.compileVarDec(self)
            elif(self.J.Keyword() == 'let' or self.J.Keyword() == 'if' or self.J.Keyword() == 'while' or self.J.Keyword() == 'do' or self.J.Keyword() == 'return'):
                if(self.IsMethod):
                    self.V.writeFunction(self.S.ClassName + '.' + self.Subroutine, self.S.VarIdx)
                    self.V.writePush('ARG', 0)
                    self.V.writePop('POINTER', 0)
                elif(self.IsConstructor):
                    self.V.writeFunction(self.S.ClassName + '.' + self.Subroutine, self.S.VarIdx)
                    self.V.writePush('CONSTANT', self.NumField)
                    self.V.writeCall('Memory.alloc', 1)
                    self.V.writePop('POINTER', 0)
                    self.IsConstructor = False
                else:
                    self.V.writeFunction(self.S.ClassName + '.' + self.Subroutine, self.S.VarIdx)
                CompilationEngine.compileStatements(self)
                if(self.J.Keyword() == '}'):
                    break
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</subroutineBody>\n')
        # print('SubboutineBody : ' + str(self.adCount))
        return

    def compileVarDec(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<varDec>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.IdKind = 'VAR'
        self.IdCount = 0
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        while(self.J.Keyword() != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
            self.IdCount = self.IdCount + 1
            if(self.IdCount == 1):
                self.IdType = self.J.Keyword()
            elif(self.IdCount%2 == 0):
                self.IdName = self.J.Keyword()
                self.S.define(self.IdName, self.IdType, self.IdKind)
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.IdKind +' ' + self.IdType + ' ' + str(self.S.indexOf(self.IdName)) + ' ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                continue
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</varDec>\n')
        # print('VarDec : ' + str(self.adCount))
        return

    def compileStatements(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<statements>\n')
        self.indent = self.indent + 1
        # self.J.advance()
        while(self.J.Keyword() == 'let' or self.J.Keyword() == 'if' or self.J.Keyword() == 'while' or self.J.Keyword() == 'do' or self.J.Keyword() == 'return'):      
            if(self.J.Keyword() == 'do'):
                CompilationEngine.compileDo(self)
            elif(self.J.Keyword() == 'let'):
                CompilationEngine.compileLet(self)
            elif(self.J.Keyword() == 'while'):
                CompilationEngine.compileWhile(self)
            elif(self.J.Keyword() == 'return'):
                CompilationEngine.compileReturn(self)
            elif(self.J.Keyword() == 'if'):
                CompilationEngine.compileIf(self)
            self.J.advance()
            print(self.J.Keyword())
            self.adCount = self.adCount + 1
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</statements>\n')
        # print('Statements : ' + str(self.adCount))
        return

    def compileDo(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<doStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.method = False
        # Subroutine = ''
        # self.ExClass = ''
        
        while(self.J.Keyword() != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
            if(self.J.Keyword() == '('):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileExpressionList(self)
                
                # some procedure for Expression list
                # self.V.writeExpression(self.ElementArray)
                if((self.IsMethod or self.IsScopeConstructor or self.IsConstructor) and not(self.method)):
                    self.V.writePush('POINTER', 0)
                elif(self.IsObj):
                    self.V.writePush('THIS', self.S.indexOf(self.ObjName))
                CompilationEngine.writeExpression(self, self.ElementArray)
                # print(self.ElementArray)
                self.ElementArray= []
                if(self.method):
                    if(self.IsObj):
                        # if(self.S.kindOf(self.ObjName) == 'STATIC' or self.S.kindOf(self.ObjName) == 'FIELD'):
                        #     self.V.writePush('THIS', 0)
                        if(self.S.kindOf(self.ObjName) == 'VAR'):
                            self.V.writePush('VAR', self.S.indexOf(self.ObjName))
                        elif(self.S.kindOf(self.ObjName) == 'ARG'):
                            self.V.writePush('ARG', self.S.indexOf(self.ObjName))
                        self.V.writeCall(self.S.typeOf(self.ObjName) + '.' + self.Subroutine, str(self.NumExpression+1))
                        self.IsObj = False
                        self.V.writePop('TEMP', 0)
                    else:
                        self.V.writeCall(self.ExClass + '.' + self.Subroutine, str(self.NumExpression))
                        self.V.f2.writelines('pop temp 0\n')
                    # if(self.FuncIsVoid or self.IsObj):
                    #     # self.V.f2.writelines('This function is void\n')
                    #     self.V.f2.writelines('pop temp 0\n')
                else:
                    if(self.IsConstructor):
                        # self.V.writePush('POINTER', 0)
                        self.V.writeFunction(self.S.ClassName + '.' + self.Subroutine, str(self.NumExpression+1))
                        self.V.writePop('TEMP', 0)
                    elif(self.IsMethod or self.IsScopeConstructor):
                        # self.V.writePush('POINTER', 0)
                        CompilationEngine.writeExpression(self, self.ElementArray)
                        self.V.writeCall(self.S.ClassName + '.' + self.Subroutine, str(self.NumExpression+1))
                        self.V.writePop('TEMP', 0)
                        # print('This line was executed.')
                    else:
                        self.V.writeFunction(self.Subroutine, str(self.NumExpression))
                
                if(self.J.Keyword() == ')'):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                continue
            else:
                if(self.J.tokenType() == 'identifier'):
                    if(self.J.tokenList[self.J.token_index] == '.'):
                        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'CLASS ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                        if(self.S.kindOf(self.J.Keyword()) == 'FIELD' or self.S.kindOf(self.J.Keyword()) == 'VAR'):
                            self.ObjName = self.J.Keyword()
                            self.IsObj = True
                        else:
                            self.ExClass = self.J.Keyword()
                        self.method = True
                    else:
                        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'SUBROUTINE ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                        self.Subroutine = self.J.Keyword()
                else:
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</doStatement>\n')
        # print('Do : ' + str(self.adCount))
        return

    def compileLet(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<letStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.J.advance()
        self.adCount = self.adCount + 1
        self.VarName = self.J.Keyword()
        self.method = False
        self.DefArray = False
        self.IsObj = False
        self.LeftHandExpression = False
        # self.Subroutine = ''
        # self.ExClass = ''
        
        if(self.J.tokenType() == 'identifier'):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.S.kindOf(self.J.Keyword()) +' ' + self.S.typeOf(self.J.Keyword()) + ' ' + str(self.S.indexOf(self.J.Keyword())) + ' ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        else:
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        
        while(self.J.Keyword() != ';'):
            if(self.J.Keyword() == '='):
                self.LeftHandExpression = False
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                if(self.J.tokenType() == 'identifier'):
                    if(self.J.tokenList[self.J.token_index] == '.'):
                        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'CLASS ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                        if(self.S.kindOf(self.J.Keyword()) == 'FIELD' or self.S.kindOf(self.J.Keyword()) == 'VAR'):
                            self.ObjName = self.J.Keyword()
                            self.IsObj = True
                print('Current word is : ' + self.J.Keyword())
                print('Next element is : ' + self.J.tokenList[self.J.token_index])
                CompilationEngine.compileExpression(self)
                # print('Current word is : ' + self.J.Keyword())
                # self.V.writeExpression(self.ElementArray)
                # self.ElementArray.append(']')
                CompilationEngine.writeExpression(self, self.ElementArray)
                print('Current word is : ' + self.J.Keyword())
                print('Current element is : ')
                print(self.ElementArray)
                self.ElementArray= []
                # print('Current word is : ' + self.J.Keyword())
                # if(self.method and (not self.IsObj)):
                #     # print('This line was executed.')
                #     # print('Current class is : ' + self.ExClass)
                #     self.V.writeCall(self.ExClass + '.' + self.Subroutine, str(self.NumExpression))
                # elif(self.IsObj):
                #     self.V.writeCall(self.S.typeOf(self.ObjName) + '.' + self.Subroutine, str(self.NumExpression+1))
                    # if(self.FuncIsVoid):
                    #     self.V.f2.writelines('pop temp 0\n')
                if(self.J.Keyword() == ';'):
                    break
            elif(self.J.Keyword() == '['):
                self.DefArray = True
                self.LeftHandExpression = True
                self.ElementArray.append(self.VarName)
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.ElementArray.append(self.J.Keyword())
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                self.ElementArray.append(']')
                CompilationEngine.writeExpression(self, self.ElementArray)
                print('--------------------------')
                print(self.ElementArray)
                print('--------------------------')
                self.ElementArray = []
                # CompilationEngine.writeArray(self, self.ElementArray)
                self.ElementArray= []
                if(self.J.Keyword() == ';'):
                    break
                elif(self.J.tokenList[self.J.token_index] == ']' and self.J.tokenList[self.J.token_index+1] == '='):
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    continue
                elif(self.J.Keyword() != ']' and self.J.tokenList[self.J.token_index] != ';'):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    break
                elif(self.J.Keyword() == '='):
                    # self.J.advance()
                    # self.adCount = self.adCount + 1
                    # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    continue
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            # else:
            #     self.ElementArray.append(self.J.Keyword())
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        if(not self.DefArray):
            if(self.IsConstructor or self.IsMethod and self.S.kindOf(self.J.Keyword()) != 'NONE'):
                self.V.writePop('THIS', self.S.indexOf(self.VarName))
            elif(self.S.kindOf(self.VarName) == 'FIELD'):
                self.V.writePop('THIS', self.S.indexOf(self.VarName))
            elif(self.S.kindOf(self.VarName) == 'VAR'):
                self.V.writePop('VAR', self.S.indexOf(self.VarName))
            else:
                if(self.S.kindOf(self.VarName) == 'FIELD'):
                    self.V.writePop('THIS', self.S.indexOf(self.VarName))
                else:
                    self.V.writePop(self.S.kindOf(self.VarName), self.S.indexOf(self.VarName))
        elif(self.DefArray):
            self.V.writePush('TEMP', 2)
            self.V.writePop('POINTER', 1)
            self.V.writePop('THAT', 0)
        self.f.writelines(space + '</letStatement>\n')
        # print('Let : ' + str(self.adCount))
        return

    def compileWhile(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<whileStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        Start = 'LABEL_' + str(self.num_label)
        self.V.writeLabel(Start)
        self.num_label = self.num_label + 1
        Goal = 'LABEL_' + str(self.num_label)
        self.num_label = self.num_label + 1
        
        while(self.J.Keyword() != '}'):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            if(self.J.Keyword() == '('):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                CompilationEngine.writeExpression(self, self.ElementArray)
                self.V.f2.writelines('not\n')
                self.ElementArray= []
                self.V.writeIf(Goal)
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '{'):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileStatements(self)
                continue
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</whileStatement>\n')
        # print('While : ' + str(self.adCount))
        self.V.writeGoto(Start)
        self.V.writeLabel(Goal)
        return

    def compileReturn(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<returnStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')

        while(self.J.Keyword() != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
            if(self.J.Keyword() != ';'):
                CompilationEngine.compileExpression(self)
                CompilationEngine.writeExpression(self, self.ElementArray)
                self.ElementArray= []
                if(self.J.Keyword() == ';'):
                    # self.J.advance()
                    # self.adCount = self.adCount + 1
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    break
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</returnStatement>\n')
        if(self.FuncIsVoid):
            # self.V.f2.writelines('This function is void\n')
            self.V.writePush('CONSTANT', 0)
        # elif(self.IsConstructor):
        #     # self.V.f2.writelines('This function is void\n')
        #     self.V.writePush('POINTER', 0)
        self.V.writeReturn()
        # print('Return : ' + str(self.adCount))
        return

    def compileIf(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<ifStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        numIf = 0
        self.J.advance()
        self.adCount = self.adCount + 1
        
        Start = 'LABEL_' + str(self.num_label)
        self.num_label = self.num_label + 1
        Goal = 'LABEL_' + str(self.num_label)
        self.num_label = self.num_label + 1
        
        while(self.J.Keyword() != '}'):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            if(self.J.Keyword() == '('):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                CompilationEngine.writeExpression(self, self.ElementArray)
                self.V.f2.writelines('not\n')
                # print(self.ElementArray)
                self.ElementArray= []
                self.V.writeIf(Start)
                if(self.J.Keyword() in self.J.KeywordConstant and self.J.tokenList[self.J.token_index] == ')'):
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    continue
                elif(self.J.tokenList[self.J.token_index] == ')'):
                    self.J.advance()
                    self.adCount = self.adCount + 1
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '{'):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileStatements(self)
                numIf = numIf + 1
                self.V.writeGoto(Goal)
                continue
            self.J.advance()
            self.adCount = self.adCount + 1
        if(self.J.tokenList[self.J.token_index] == 'else'):
            self.V.writeLabel(Start)
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            
            self.J.advance()
            self.adCount = self.adCount + 1
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1      
            CompilationEngine.compileStatements(self)
            self.V.writeLabel(Goal)
        else:
            self.V.writeLabel(Start)
            self.V.writeLabel(Goal)
            # self.V.writeGoto(Start)
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</ifStatement>\n')
        # print('If : ' + str(self.adCount))
        return

    def compileExpression(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<expression>\n')
        self.indent = self.indent + 1
        CompilationEngine.compileTerm(self)
        CurrentOperand = ''
        # self.ElementArray.append(self.J.Keyword())
        
        if(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] != ';' and (not self.method)):
            self.J.advance()
            self.adCount = self.adCount + 1
        elif(self.unaryOp and not(self.J.Keyword() in self.op) and (not self.J.Keyword() == ';')):
            self.J.advance()
            self.adCount = self.adCount + 1
            self.unaryOp = False
        elif(self.J.tokenList[self.J.token_index] == ')' and (not self.method)):
            self.J.advance()
            self.adCount = self.adCount + 1
        elif(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
        elif(self.J.tokenType() == 'integerConstant' and self.J.tokenList[self.J.token_index] in self.op):
            self.J.advance()
            self.adCount = self.adCount + 1
        elif(self.J.tokenList[self.J.token_index] in self.op and (not self.method)):
            self.J.advance()
            self.adCount = self.adCount + 1
        # self.ElementArray.append(self.J.Keyword())
            
        while(self.J.Keyword() in self.op):
            space = self.indent_str * self.indent
            CurrentOperand = self.J.Keyword()
            if(self.J.Keyword() == '<'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + '&lt;' + ' </' + self.J.tokenType() + '>\n')     
            elif(self.J.Keyword() == '>'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + '&gt;' + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '&'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + '&amp;' + ' </' + self.J.tokenType() + '>\n')
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            CompilationEngine.compileTerm(self)
            if(self.J.Keyword() == ','):
                continue
            if(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] == ';'):
                self.ElementArray.append(self.J.Keyword())
                break     
            elif(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] == '{'):
                break
            elif(self.J.tokenList[self.J.token_index] == ')' and self.J.tokenList[self.J.token_index+1] == ';'):
                self.ElementArray.append(self.J.tokenList[self.J.token_index])
                break
            elif(self.J.tokenList[self.J.token_index] == ')' and self.J.tokenList[self.J.token_index+1] != ';'):
                self.J.advance()
                self.adCount = self.adCount + 1
                continue
            elif(self.J.Keyword() == ';'):
                break
            elif(self.J.tokenList[self.J.token_index] == ';'):
                break
            self.J.advance()
            self.adCount = self.adCount + 1
        if(CurrentOperand != ''):
            self.ElementArray.append(CurrentOperand)
            # a=1
        # elif(self.unaryOperand != ''):
        #     # a=1
        #     self.ElementArray.append(self.unaryOperand)
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</expression>\n')
        # print(self.J.Keyword())
        # print('Expression : ' + str(self.adCount))
        return

    def compileTerm(self):
        self.SubRoutineCall = False
        space = self.indent_str * self.indent
        self.f.writelines(space + '<term>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        if(self.J.Keyword() != '~' and self.J.Keyword() != '-'):
            self.ElementArray.append(self.J.Keyword())
        else:
            self.unaryOperand = self.J.Keyword()
    
        MinusOp = ''
        
        if(self.J.tokenType() == 'integerConstant' or self.J.tokenType() == 'stringConstant' or self.J.Keyword() in self.J.KeywordConstant):
            if(self.J.tokenType() == 'stringConstant'):
                print('stringConstant is ' + self.J.Keyword() )
                StConst = self.J.Keyword()
                while(self.J.Keyword()[-1] != '"'):
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    StConst = StConst + self.J.Keyword()
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + StConst + ' </' + self.J.tokenType() + '>\n')
                self.V.writePush('CONSTANT', str(len(StConst[1:-1])))
                NumStr = 0
                for i in range(len(StConst[1:-1])):
                    if(NumStr == 0):
                        self.V.writeCall('String.new', 1)
                    self.V.writePush('CONSTANT', str(ord(StConst[i+1])))
                    self.V.writeCall('String.appendChar', 2)
                    NumStr = NumStr + 1
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')          
        elif(self.J.Keyword() == '('):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            CompilationEngine.compileExpression(self)
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        elif(self.J.Keyword() == '-' or self.J.Keyword() == '~'):
            self.unaryOp = True
            if(self.J.Keyword == '~'):
                self.unaryOperand = self.J.Keyword()
            MinusOp =self.J.Keyword()
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            if(MinusOp == '-'):
                MinusOp = MinusOp + self.J.Keyword()
            CompilationEngine.compileTerm(self)
            if(MinusOp != '' and MinusOp[0] == '-'):
                del self.ElementArray[-1]
                # del self.ElementArray[-1]
                self.ElementArray.append(MinusOp)
            elif(MinusOp != '' and MinusOp[0] == '~'):
                # del self.ElementArray[-1]
                self.ElementArray.append(MinusOp)
                # a=1
            # del self.ElementArray[-1]
            # self.ElementArray.append(MinusOp)
            if(self.J.tokenType() == 'integerConstant' and self.J.tokenList[self.J.token_index] != ')'):
                self.J.advance()
                self.adCount = self.adCount + 1
        elif(self.J.tokenType() == 'identifier'):
            # if(self.J.tokenList[self.J.token_index] == '.'):
            #     self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'CLASS ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            #     if(self.S.kindOf(self.J.Keyword()) == 'FIELD' or self.S.kindOf(self.J.Keyword()) == 'VAR'):
            #         self.ObjName = self.J.Keyword()
            #         self.IsObj = True
            
            if(self.S.kindOf(self.J.Keyword()) != 'NONE'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.S.kindOf(self.J.Keyword()) +' ' + self.S.typeOf(self.J.Keyword()) + ' ' + str(self.S.indexOf(self.J.Keyword())) + ' ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                # Subroutine = self.J.Keyword()
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + 'CLASS ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.ExClass = self.J.Keyword()
            # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        
            if(self.J.tokenList[self.J.token_index] != ')' and self.J.tokenList[self.J.token_index] != ';' and self.J.tokenList[self.J.token_index] != ']'):
                print('Executed here.')
                print('Current word is : ' + self.J.Keyword())
                self.J.advance()
                self.adCount = self.adCount + 1
            if(self.J.Keyword() == '('):
                CompilationEngine.compileExpressionList(self)
                # self.V.writeCall(self.ExClass + '.' + Subroutine, str(self.NumExpression))
                self.J.advance()
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '['):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.ElementArray.append(self.J.Keyword())
                self.J.advance()
                self.adCount = self.adCount + 1
                # self.V.f2.writelines('--------------Test---------------\n')
                # self.V.writePush(self.S.kindOf(self.ElementArray[0]), self.S.indexOf(self.ElementArray[0]))
                # self.ElementArray = []
                CompilationEngine.compileExpression(self)
                if(self.J.tokenList[self.J.token_index] == ']' or self.J.Keyword() == ']'):
                    self.ElementArray.append(']')
                # self.ElementArray.append('ArrayAssign')
                
                # self.V.f2.writelines('add\n')
                # self.V.writePop('POINTER', 1)
                # self.V.f2.writelines('--------------Test---------------\n')
                if(self.J.Keyword() == ']' and self.J.tokenList[self.J.token_index] == ';'):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                elif(self.J.tokenList[self.J.token_index] == ']' and self.J.tokenList[self.J.token_index+1] == ';'):
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                elif(self.J.tokenList[self.J.token_index] == ']'):
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '.'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                if(self.J.tokenType() == 'identifier' and self.S.kindOf(self.J.Keyword()) == 'NONE'):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> '  + 'SUBROUTINE ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    self.Subroutine = self.J.Keyword()
                    self.SubRoutineCall = True
                    self.method = True
                    
                    ClassName = self.ElementArray[-1]
                    del self.ElementArray[-1]
                    
                    self.ElementArray.append(ClassName + '.' + self.J.Keyword())
                    
                    # This procedure is necessary because subroutine name is not expression element.
                    # del self.ElementArray[-1]
                else:
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileExpressionList(self)
                # self.V.writeCall(self.ExClass + '.' + Subroutine, str(self.NumExpression))
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        # print('Term end Current word is : ' + self.J.Keyword())
        self.f.writelines(space + '</term>\n')
        return

    def compileExpressionList(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<expressionList>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.NumExpression = 0
        self.J.advance()
        self.adCount = self.adCount + 1
        while(self.J.Keyword() != ')'):
            if(self.J.Keyword() != ','):
                CompilationEngine.compileExpression(self)
                self.NumExpression = self.NumExpression + 1
                if(self.J.Keyword() == ','):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                elif(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] == ';'):
                    # self.J.advance()
                    # self.adCount = self.adCount + 1
                    break
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</expressionList>\n')
        # print('Expression : ' + str(self.adCount))
        return
    
    def writeExpression(self, ElementArray):
        InsertOffset = 0
        while '(' in ElementArray:
            ElementArray.remove('(')
        while ')' in ElementArray:
            ElementArray.remove(')')
        SqBracketEndIndList = [i for i, x in enumerate(ElementArray) if x == ']']
        if(len(SqBracketEndIndList) != 0):
            for i in range(len(SqBracketEndIndList)):
                if(i == len(SqBracketEndIndList)-1 and self.LeftHandExpression):
                    ElementArray.insert(SqBracketEndIndList[i]+InsertOffset, 'ArrayAssignLeft')
                    InsertOffset = InsertOffset + 1
                else:
                    ElementArray.insert(SqBracketEndIndList[i]+InsertOffset, 'ArrayAssign')
                    InsertOffset = InsertOffset + 1
        while '[' in ElementArray:
            ElementArray.remove('[')
        while ']' in ElementArray:
            ElementArray.remove(']')
        
        IsSkip = False
        
        for i in range(len(ElementArray)):
            if(IsSkip):
                IsSkip = False
                continue
            
            if(CompilationEngine.is_num(ElementArray[i])):
                if(int(ElementArray[i]) < 0):
                    self.V.writePush('CONSTANT', ElementArray[i][1:])
                    self.V.f2.writelines('neg\n')
                else:
                    self.V.writePush('CONSTANT', ElementArray[i])
            elif(self.S.kindOf(ElementArray[i]) == 'VAR'):
                self.V.writePush('VAR', self.S.indexOf(ElementArray[i]))
                # self.V.f2.writelines('-----------\n')
            elif(self.S.kindOf(ElementArray[i]) == 'ARG'):
                self.V.writePush('ARG', self.S.indexOf(ElementArray[i]))
            elif(self.S.kindOf(ElementArray[i]) == 'STATIC'):
                self.V.writePush('STATIC', self.S.indexOf(ElementArray[i]))
            elif(ElementArray[i] == '+'):
                self.V.f2.writelines('add\n')
            elif(ElementArray[i] == '-'):
                self.V.f2.writelines('sub\n')
            elif(ElementArray[i] == '*'):
                self.V.f2.writelines('call Math.multiply 2\n')
            elif(ElementArray[i] == '/'):
                self.V.f2.writelines('call Math.divide 2\n')
            elif(ElementArray[i] == 'true'):
                self.V.writePush('CONSTANT', 0)
                self.V.f2.writelines('not\n')
            elif(ElementArray[i] == 'false' or ElementArray[i] == 'null'):
                self.V.writePush('CONSTANT', 0)
            elif(ElementArray[i] == '='):
                self.V.f2.writelines('eq\n')
            elif(ElementArray[i] == '>'):
                self.V.f2.writelines('gt\n')
            elif(ElementArray[i] == '<'):
                self.V.f2.writelines('lt\n')
            elif(ElementArray[i] == '~'):
                self.V.f2.writelines('not\n')
            elif(ElementArray[i] == '&'):
                self.V.f2.writelines('and\n')
            elif(ElementArray[i] == '|'):
                self.V.f2.writelines('or\n')
            elif(ElementArray[i] == 'this'):
                self.V.writePush('POINTER', 0)
            elif(self.IsMethod and self.S.kindOf(ElementArray[i]) == 'FIELD'):
                self.V.writePush('THIS', self.S.indexOf(ElementArray[i]))
            elif(self.S.kindOf(ElementArray[i]) == 'FIELD'):
                self.V.writePush('THIS', self.S.indexOf(ElementArray[i]))
            elif(ElementArray[i] == 'ArrayAssign'):
                self.V.f2.writelines('add\n')
                self.V.writePop('POINTER', 1)
                self.V.writePush('THAT', 0)
            elif(ElementArray[i] == 'ArrayAssignLeft'):
                self.V.f2.writelines('add\n')
                self.V.writePop('TEMP', 2)
            elif('.' in ElementArray[i]):
                self.V.writePush('CONSTANT', ElementArray[i+1])
                self.V.writeCall(ElementArray[i], 1)
                IsSkip = True
        return

    def writeArray(self, ElementArray):
        for i in range(len(ElementArray)):
            if(self.S.kindOf(ElementArray[i]) == 'VAR'):
                self.V.writePush('VAR', self.S.indexOf(ElementArray[i]))
            elif(ElementArray[i] == '['):
                CompilationEngine.writeExpression(self, self.ElementArray[i:])
                self.V.f2.writelines('add\n')
                self.V.writePop('TEMP', 2)
                return
        return

    def is_num(a):
        try:
            int(a)
        except:
            return False
        return True
    
    
    
    
    
    