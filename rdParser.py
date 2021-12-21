
'''
Single Programmer Affidavit

I the undersigned promise that the attached assignment is my own work. While I was 
free to discuss ideas with others, the work contained is my own. I recognize that 
should this not be the case, I will be subject to penalties as outlined in the course 
syllabus. 

Damandeep Singh  (821195382)
'''


import re
from functools import *

class recDescent:
    # constructor to initialize and set class level variables
    def __init__(self, expr = ""):
        # string to be parsed
        self.expr = expr
        # tokens from lexer tokenization of the expression
        self.tokens = []
   
    # lexer - tokenize the expression into a list of tokens
    # the tokens are stored in an list which can be accessed by self.tokens
    def lex(self):
        self.tokens = re.findall("[-\(\)=]|[!<>]=|[<>]|\w+|[^ +]\W+", self.expr)

        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens)))) 

    
    # validate() function will return True if the expression is valid, False    otherwise 
    def validate(self):
        self.lex()
        return self.exp(0)[0]

    # Top level parsing procedure <exp>
    def exp(self, index):
        found = False
        curr = index
        isSuccess = self.term(curr)
        if isSuccess[0]:
            found = True
            curr  = isSuccess[1] 
            # while loop checks if there are any logical operators on the index
            while self.isOp(curr) and found and curr < len(self.tokens):
                curr += 1
                chk = self.term(curr)
                if chk[0] == False:
                    found = False
                else:
                    curr = chk[1]
            # Returns false when an <op> was expected but returns a term instead.        
            if (curr < len(self.tokens) and self.term(curr)[0]):        
                found = False
        return found, curr

    # term level parsing procedure (grammar)
    def term(self, index):
        found = False
        tkn = lambda val: self.tokens[val]
        curr = index
        # int - int
        if curr < len(self.tokens) and tkn(curr).isnumeric():
            curr += 1
            if curr < len(self.tokens) and tkn(curr) == '-':
                curr += 1
                if  curr < len(self.tokens) and tkn(curr).isnumeric():
                    found = True
                    curr += 1
        # <relop> int
        elif curr < len(self.tokens) and self.isRelop(curr):
            curr += 1
            if curr < len(self.tokens) and tkn(curr).isnumeric():
                found = True
                curr += 1
        else: # (<exp>) 
           if curr < len(self.tokens) and tkn(curr) == '(':
               curr += 1
               nxt = self.exp(curr)
               if nxt[0]:
                    curr = nxt[1]
                    if curr < len(self.tokens) and tkn(curr) == ')':
                        found = True
                        curr += 1
        return found, curr

     # <relop> grammar   
    def isRelop(self, index):
        if index < len(self.tokens) and self.tokens[index] in ['<', '>', '<=', '>=', '=', '!=', 'not']:
                return True
        else:
                return False

    # <op> grammar
    def isOp(self, index):
        if index < len(self.tokens) and self.tokens[index] in ['and', 'or', 'xor', 'nand', 'xnor']:
                return True
        else:
                return False   