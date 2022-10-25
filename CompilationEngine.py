#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 11:27:04 2022
@author: katamoto
"""

import JackTokenizer

# Define the class
class CompilationEngine:
    # Define the constructor
    def __init__(self, J, OutputFilename):
        #self.name = name
        self.J = J
        self.f = open(OutputFilename ,'w')
        self.indent = 0
        self.indent_str = '  '
        self.adCount = 0
        self.op = ['+','-','*','/','&','|','<','>','=']
        self.unaryOp = False

    def compileClass(self):
        self.f.writelines('<class>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.J.advance()
        self.adCount = self.adCount + 1
        while(self.J.Keyword() != '}'):
            if(self.J.Keyword() == 'static' or self.J.Keyword() == 'field'):
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileClassVarDec(self)
                # self.J.advance()
            elif(self.J.Keyword() == 'function' or self.J.Keyword() == 'constructor' or self.J.Keyword() == 'method'):
                CompilationEngine.compileSubroutine(self)
                # if(self.J.Keyword() == '}'):
                #     continue
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        self.f.writelines('</class>\n')
        print('class : ' + str(self.adCount))
        return

    def compileClassVarDec(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<classVarDec>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        while(self.J.Keyword() != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
            space = self.indent_str * self.indent
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')     
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</classVarDec>\n')
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        print('classVarDec : ' + str(self.adCount))
        return

    def compileSubroutine(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<subroutineDec>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        # while(self.J.Keyword() != '{' and self.J.hasMoreTokens()):
        while(self.J.Keyword() != '}'):
            if(self.J.Keyword() == '('):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileParameterList(self)
            elif(self.J.Keyword() == '{'):
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileSubroutineBody(self)
                if(self.J.Keyword() == '}'):
                    break
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</subroutineDec>\n')
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        # self.J.advance()
        print('SubRoutine : ' + str(self.adCount))
        return

    def compileParameterList(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<parameterList>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        while(self.J.Keyword() != ')'):
            # self.J.advance()
            if(self.J.Keyword() != '('):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</parameterList>\n')
        # self.J.advance()
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        print('ParameterList : ' + str(self.adCount))
        return

    def compileSubroutineBody(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<subroutineBody>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.J.advance()
        self.adCount = self.adCount + 1
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        while(self.J.Keyword() != '}'):
            
            if(self.J.Keyword() == 'var'):
                CompilationEngine.compileVarDec(self)
            elif(self.J.Keyword() == 'let' or self.J.Keyword() == 'if' or self.J.Keyword() == 'while' or self.J.Keyword() == 'do' or self.J.Keyword() == 'return'):
                CompilationEngine.compileStatements(self)
                if(self.J.Keyword() == '}'):
                    break
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</subroutineBody>\n')
        print('SubboutineBody : ' + str(self.adCount))
        return

    def compileVarDec(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<varDec>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        while(self.J.Keyword() != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</varDec>\n')
        print('VarDec : ' + str(self.adCount))
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
        # print(self.J.Keyword())
        self.f.writelines(space + '</statements>\n')
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        print('Statements : ' + str(self.adCount))
        return

    def compileDo(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<doStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')

        while(self.J.Keyword() != ';'):
            # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            if(self.J.Keyword() == '('):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileExpressionList(self)
                if(self.J.Keyword() == ')'):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                continue
                # self.f.writelines(space + '<expressionList>\n')
                # self.f.writelines(space + '</expressionList>\n')
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            # self.J.advance()
            # self.adCount = self.adCount + 1
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</doStatement>\n')
        print('Do : ' + str(self.adCount))
        return

    def compileLet(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<letStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.J.advance()
        self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        
        while(self.J.Keyword() != ';'):
            if(self.J.Keyword() == '='):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                if(self.J.Keyword() == ';'):
                    break
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '['):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                if(self.J.Keyword() == ';'):
                    break
                elif(self.J.Keyword() != ']' and self.J.tokenList[self.J.token_index] != ';'):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    self.J.advance()
                    self.adCount = self.adCount + 1
                    # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    break
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</letStatement>\n')
        print('Let : ' + str(self.adCount))
        return

    def compileWhile(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<whileStatement>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')

        while(self.J.Keyword() != '}'):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            if(self.J.Keyword() == '('):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '{'):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileStatements(self)
                # self.f.writelines(space + '<statements>\n')
                # self.f.writelines(space + '</statements>\n')
                # print(self.J.Keyword())
                continue
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</whileStatement>\n')
        print('While : ' + str(self.adCount))
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
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</returnStatement>\n')
        print('Return : ' + str(self.adCount))
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
        # while(self.J.Keyword() != '}' or numIf < 2):
        while(self.J.Keyword() != '}'):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            if(self.J.Keyword() == '('):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '{'):
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileStatements(self)
                # self.f.writelines(space + '<statements>\n')
                # self.f.writelines(space + '</statements>\n')
                numIf = numIf + 1
                # print(self.J.Keyword())
                continue
            self.J.advance()
            self.adCount = self.adCount + 1
        self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</ifStatement>\n')
        print('If : ' + str(self.adCount))
        return

    def compileExpression(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<expression>\n')
        self.indent = self.indent + 1
        CompilationEngine.compileTerm(self)
        if(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] != ';'):
            self.J.advance()
            self.adCount = self.adCount + 1
        elif(self.unaryOp and not(self.J.Keyword() in self.op)):
            self.J.advance()
            self.adCount = self.adCount + 1
            self.unaryOp = False
        while(self.J.Keyword() in self.op):
            space = self.indent_str * self.indent
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
            # print('4 Next is ' + self.J.Keyword())
            if(self.J.Keyword() == ','):
                continue
            # print(self.J.Keyword())
            if(self.J.Keyword() == ')' and self.J.tokenList[self.J.token_index] == ';'):
                # print('Current is ' + self.J.Keyword())
                # print('Next is ' + self.J.tokenList[self.J.token_index])
                break
            elif(self.J.tokenList[self.J.token_index] == ')' and self.J.tokenList[self.J.token_index+1] == ';'):
                # self.J.advance()
                # self.adCount = self.adCount + 1
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                # print('3 Next is ' + self.J.tokenList[self.J.token_index])
                # self.J.advance()
                # self.adCount = self.adCount + 1
                # continue
                break
            elif(self.J.tokenList[self.J.token_index] == ')' and self.J.tokenList[self.J.token_index+1] != ';'):
                # self.J.advance()
                # self.adCount = self.adCount + 1
                # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                # print('3 Next is ' + self.J.tokenList[self.J.token_index])
                # self.J.advance()
                # self.adCount = self.adCount + 1
                # continue
                self.J.advance()
                self.adCount = self.adCount + 1
                continue
            # elif(self.J.Keyword() == ']' and self.J.tokenList[self.J.token_index] == ';'):
            #     # print('Current is ' + self.J.Keyword())
            #     # print('Next is ' + self.J.tokenList[self.J.token_index])
            #     self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            #     break
            # if(self.J.Keyword() == ')'):
            #     print('Current is ' + self.J.Keyword())
            #     print('Next is ' + self.J.tokenList[self.J.token_index])
            #     break
            # elif(self.J.Keyword() in self.op):
            #     continue
            self.J.advance()
            self.adCount = self.adCount + 1
            
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</expression>\n')
        # if(self.J.Keyword() != ')'):
        #     self.J.advance()
        #     self.adCount = self.adCount + 1
        #     print('Executed here')
        print(self.J.Keyword())
        print('Expression : ' + str(self.adCount))
        return

    def compileTerm(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<term>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        # self.J.advance()
        # self.adCount = self.adCount + 1
        if(self.J.tokenType() == 'integerConstant' or self.J.tokenType() == 'stringConstant' or self.J.Keyword() in self.J.KeywordConstant):
            if(self.J.tokenType() == 'stringConstant'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword()[1:-1] + ' </' + self.J.tokenType() + '>\n')
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            
        elif(self.J.Keyword() == '('):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            CompilationEngine.compileExpression(self)
            # self.J.advance()
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        elif(self.J.Keyword() == '-' or self.J.Keyword() == '~'):
            self.unaryOp = True
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
            CompilationEngine.compileTerm(self)
            if(self.J.tokenType() == 'integerConstant'):
                self.J.advance()
                self.adCount = self.adCount + 1
            # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        elif(self.J.tokenType() == 'identifier'):
            self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            if(self.J.tokenList[self.J.token_index] != ')'):
                # print('0 Next is ' + self.J.Keyword())
                # print('1 Next is ' + self.J.tokenList[self.J.token_index])
                # print('2 Next is ' + self.J.tokenList[self.J.token_index+1])
                self.J.advance()
                self.adCount = self.adCount + 1
            
            if(self.J.Keyword() == '('):
                CompilationEngine.compileExpressionList(self)
                self.J.advance()
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '['):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                CompilationEngine.compileExpression(self)
                if(self.J.Keyword() == ']' and self.J.tokenList[self.J.token_index] == ';'):
                    # print('Current is ' + self.J.Keyword())
                    # print('Next is ' + self.J.tokenList[self.J.token_index]
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                    # self.J.advance()
                    # self.adCount = self.adCount + 1
                    # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            elif(self.J.Keyword() == '.'):
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                self.J.advance()
                self.adCount = self.adCount + 1
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                CompilationEngine.compileExpressionList(self)
                # self.J.advance()
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            # if(self.unaryOp):
            #     self.J.advance()
            #     self.adCount = self.adCount + 1
            #     self.unaryOp = False
            # elif(self.J.tokenList[self.J.token_index] == ')'):
            #     # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            #     self.J.advance()
            #     self.adCount = self.adCount + 1
            #     print('00 Next is ' + self.J.Keyword())
        # self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</term>\n')
        # print('Term : ' + str(self.adCount))
        # print('Current is ' + self.J.Keyword())
        # print('1 Next is ' + self.J.tokenList[self.J.token_index])
        return

    def compileExpressionList(self):
        space = self.indent_str * self.indent
        self.f.writelines(space + '<expressionList>\n')
        self.indent = self.indent + 1
        space = self.indent_str * self.indent
        self.J.advance()
        self.adCount = self.adCount + 1
        while(self.J.Keyword() != ')'):
            if(self.J.Keyword() != ','):
                CompilationEngine.compileExpression(self)
                if(self.J.Keyword() == ','):
                    self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
                elif(self.J.Keyword() == ')'):
                    break
                # elif(self.J.tokenList[self.J.token_index] == ')'):
                #     break
            else:
                self.f.writelines(space + '<' + self.J.tokenType() + '> ' + self.J.Keyword() + ' </' + self.J.tokenType() + '>\n')
            self.J.advance()
            self.adCount = self.adCount + 1
        self.indent = self.indent - 1
        space = self.indent_str * self.indent
        self.f.writelines(space + '</expressionList>\n')
        print('Expression : ' + str(self.adCount))
        return

    
    
    
    
    
    