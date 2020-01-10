#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 11:39:11 2020

@author: nmbice
"""

from fol_atomic import atomic_evaluator
import string



#function to create a new name
def new_name(name, name_set, count=0): 
    if name in name_set: 
        n_name = name + str(count)
        count += 1
        return new_name(n_name, name_set, count)
    else: 
        return name
    
    

#function to replace bound variables by new variables
def bound_replace(formula, all_vars):
    formula = str(formula)
    q_ind = 0
    new_form = formula
    for n in range(len(formula)): 
        if formula[n] == 'U' or formula[n] == 'X': 
            q_ind = n
            for m in range(n+1,len(formula)): 
                if formula[m].isupper() or formula[m] == '(': 
                    old_var = formula[n+1:m]
                    break
            new_var = new_name(old_var, all_vars)
            all_vars.add(new_var)
            par_count = 0
            for m in range(n+2,len(formula)): 
                if formula[m] == '(': 
                    par_count +=1
                if formula[m] == ')': 
                    par_count -=1
                    if par_count == 0:
                        ind = m
                        break
            scope = formula[n:ind+1]
            rep = scope.replace(old_var, new_var)
            new_form = formula[:n] + rep + formula[ind+1:]
            break
    if 'U' not in formula[q_ind+1:] and 'X' not in formula[q_ind+1:]: 
        return new_form
    else: 
        final_form = new_form[:q_ind+1] + bound_replace(new_form[q_ind+1:], all_vars)
        return final_form
            

#function evaluates a universal quantifier applied to a sentence
def univ_eval(var, formula, MOD): 
    
    DOM = MOD.domain
    IN = MOD.interp.copy()
    all_vars = MOD.all_vars
    
    formula = bound_replace(formula, all_vars)
    #print (formula)

    for obj in DOM: 
        if str(obj) not in IN: 
            IN[str(obj)] = obj
        else: 
            IN[str(obj)+'_nc'] = obj
        
    EX_MOD = Model(DOM, all_vars)
    EX_MOD.interp = IN
        
    #print (EX_MOD.interp)
    
    values = []
    
    for obj in DOM: 
        if str(obj) in EX_MOD.interp: 
            new_form = str(formula).replace(var, str(obj))
        else: 
            new_form = str(formula).replace(var, str(obj)+'_nc')
            
        #print (new_form)
        new_form = parse(tokenize(new_form))
        
        val = new_form.eval(EX_MOD)
                    
        if type(val) != bool: 
            return None
        
        values.append(val)
    
    return all(values)
    


#function evaluates an existential quantifier applied to a sentence
def exist_eval(var, formula, MOD): 
    
    DOM = MOD.domain
    IN = MOD.interp.copy()
    all_vars = MOD.all_vars
    
    formula = bound_replace(formula, all_vars)
    
    for obj in DOM: 
        if str(obj) not in IN: 
            IN[str(obj)] = obj
        else: 
            IN[str(obj)+'_nc'] = obj
        
    EX_MOD = Model(DOM, all_vars)
    EX_MOD.interp = IN
    
    #print (IN)
    
    for obj in DOM: 
        if str(obj) in EX_MOD.interp: 
            new_form = str(formula).replace(var, str(obj))
        else: 
            new_form = str(formula).replace(var, str(obj)+'_nc')
        
        new_form = parse(tokenize(new_form))
        
        val = new_form.eval(EX_MOD)
        
        if type(val) != bool: 
            return None
        
        if val == True: 
            return True
        
    return False




#these initial classes treat formulas as syntax trees

class Not:
    opStr = '~'
    def __init__(self, formula):
        self.formula = formula
        
    #negations are represented in the form '~p'
    def __str__(self):
        return self.opStr + str(self.formula)
    def __repr__(self):
        return str(self)
    
    #a negation is true exactly if its main subformula is false, and the eval function treats it accordingly; here MOD is
    #a chosen model
    def eval(self, MOD):
        if self.formula.eval(MOD) == None:
            return None
        else:
            return not self.formula.eval(MOD)
        
#this is the main class for binary connectives, which have both left and right branches (corresponding to their left and right
#subformulas)
class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    #all binary connectives * are represented in the form '(p * q)'
    def __str__(self):
        return '(' + str(self.left) + ' ' + self.opStr + ' ' + \
               str(self.right) + ')'
    def __repr__(self):
        return str(self)
    
class And(BinaryOp): 
    opStr = '^'
    #a conjunction is true exactly if both conjuncts are true
    def eval(self, MOD):
        return self.left.eval(MOD) and self.right.eval(MOD)
    
class Or(BinaryOp): 
    opStr = 'v'
    #a disjunction is true exactly if either the first disjunct is true or the second disjunct is true or both
    def eval(self, MOD):
        return self.left.eval(MOD) or self.right.eval(MOD)
    
class Implies(BinaryOp):
    opStr = '>'
    #a material conditional is true exactly if the conjunction of the antecedent and the negation of the consequent is false
    def eval(self, MOD):
        return not(self.left.eval(MOD) and not(self.right.eval(MOD)))
    
class Bicond(BinaryOp):
    opStr = '-'
    #a biconditional is true exactly if either both sides are true or both sides are false
    def eval(self, MOD):
        return (self.left.eval(MOD) and self.right.eval(MOD)) or \
               (not(self.left.eval(MOD)) and not(self.right.eval(MOD)))
        
#this is a special class for creating a model; note that the domain of variables should be specified
#after instantiating the model, one should add interpretations for the characters in the language
#the domain is assumed to be a set of objects and the interpretation is assumed to be a dictionary with 
#expressions as keys and objects, sets of objects, or sets of tuples of objects as values
class Model:
    def __init__(self, domain, all_vars={'u','v','w','x','y','z'}): 
        self.domain = domain
        self.interp = {'=': {(x,x) for x in self.domain}}
        self.all_vars = all_vars
    
#this class handles atomic formulae
class Atomic:
    def __init__(self, formula):
        self.formula = formula
    def __str__(self):
        return str(self.formula)
    __repr__ = __str__
    def eval(self, MOD): 
        return atomic_evaluator(str(self.formula), MOD)
            
#this is a class for the two truth-values: True and False
class TruthValue:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        if self.value == True:
            return 'T'
        else:
            return 'F'
    __repr__ = __str__
    def eval(self, MOD):
        return self.value
    
#this is a class for the universal quantifier
class Universal: 
    def __init__(self, var, formula): 
        self.var = var
        self.formula = formula
    def __str__(self): 
        return 'U' + self.var + str(self.formula)
    __repr__ = __str__
    def eval(self, MOD): 
        return univ_eval(self.var, self.formula, MOD)
    
#this is a class for the existential quantifier
class Existential: 
    def __init__(self, var, formula): 
        self.var = var
        self.formula = formula
    def __str__(self): 
        return 'X' + self.var + str(self.formula)
    __repr__ = __str__
    def eval(self, MOD): 
        return exist_eval(self.var, self.formula, MOD)
    
    

#this is a list of special characters used by the parser to parse an inputted string
seps = ['(', ')', ',', '~', '^', 'v', '>', '-', 'T', 'F', 'U', 'X']


#next are functions for determining the type of a string


#this function returns True if the string is a term; terms must begin with lowercase letters
def TermTok(token): 
    if not token[0].islower(): 
        return False
    for char in token:
        if not(char in string.ascii_letters or char in string.digits) \
           or char == 'T' or char == 'F' or char == 'U' or char == 'X' or char == 'v':
            return False
    return True

#this function returns true if its input is a string of letters and numbers not including 'T', 'F', 'U', 'X', or 'v', all 
#of which have special meanings in the formal language
#predicates must begin with uppercase letters (or '=')
def PredTok(token):
    if not token[0].isupper() and not token[0] == '=': 
        return False
    for char in token:
        if not(char in string.ascii_letters or char in string.digits or char == '=') \
           or char == 'T' or char == 'F' or char == 'U' or char == 'X' or char == 'v':
            return False
    return True

#this function returns true if its input is 'T' or 'F'
def valueTok(token):
    return token == 'T' or token == 'F'

#this function returns true if its input is an atomic wff
def atomicTok(token): 
    return PredTok(token[0])


#this function converts a string into a list of its significant parts; e.g. '(UxP(x) ^ Q(c))' is converted into 
#['(', 'U', 'x', 'P(x)', '^', 'Q(c)', ')']
#atomic formulas are treated as wholes
def tokenize(inputString):
    result = []
    state = 'open'
    for n in range(len(inputString)):
        if inputString[n] in seps and inputString[n] != ',' and state != 'atomic':
            result.append(inputString[n])
            state = 'open'
        elif inputString[n] == ' ' and state != 'atomic':
            state = 'open'
        elif TermTok(inputString[n]) and state == 'open': 
            for m in range(n, len(inputString)): 
                if state == 'open' and (inputString[m] == '(' or PredTok(inputString[m]) or \
                                        inputString[m] == 'U' or inputString[m] == 'X' or inputString[m] == '~' \
                                        or valueTok(inputString[m])):
                    result.append(inputString[n:m])
                    state = 'var'
                    break
        elif state == 'atomic' and inputString[n] == ')': 
                    state = 'open'
        elif (state == 'var' and PredTok(inputString[n])) or state == 'open':
            #the character at index n must be the beginning of an atomic wff, and hence a new loop is constructed in order
            #to find the end of the wff and then add the whole wff to the list; this is done by noting 
            #that the end of an atomic wff will be a right parentheses
            for m in range(n, len(inputString)):
                if inputString[m] == ')':
                    result.append(inputString[n:m+1])
                    state = 'atomic'
                    break
    return result


#this function parses a list of significant expressions recursively and returns the appropriate syntax tree (an instance of 
#one of the classes above); the expected input is the output of the tokenize function (above) given a string as input
def parse(tokens):
    #this helper function takes an index and returns a tuple consisting of both the syntax tree beginning at that index 
    #and the index after the tree; if the string at the input index is a '(', then it corresponds to the beginning of a syntax 
    #tree for a binary connective, and hence the function is called recursively on the branches 
    #corresponding to that connective
    def parseForm(index):
        token = tokens[index]
        if valueTok(token):
            if token == 'T':
                return (TruthValue(True), index + 1)
            else:
                return (TruthValue(False), index + 1)
        elif atomicTok(token):
            return (Atomic(token), index + 1)
        elif token == 'U': 
            return (Universal(var=tokens[index+1], formula=parseForm(index + 2)[0]), index + 3)
        elif token == 'X': 
            return (Existential(var=tokens[index+1], formula=parseForm(index + 2)[0]), index + 3)
        elif token == '~':
            (tree, nextIndex) = parseForm(index + 1)
            return (Not(tree), nextIndex)
        else:
            #here we take advantage of the fact that in this case the string at the input index will be a '(', and hence 
            #the next index will correspond to the left branch of a binary connective
            (leftTree, opIndex) = parseForm(index + 1)
            op = tokens[opIndex]
            (rightTree, parIndex) = parseForm(opIndex + 1)
            if op == '^':
                return (And(leftTree, rightTree), parIndex + 1)
            elif op == 'v':
                return (Or(leftTree, rightTree), parIndex + 1)
            elif op == '>':
                return (Implies(leftTree, rightTree), parIndex + 1)
            elif op == '-':
                return (Bicond(leftTree, rightTree), parIndex + 1)
    #we then call the helper function on the index 0 to construct the full syntax tree, which is then returned
    try:
        (parsedForm, nextIndex) = parseForm(0)
        return parsedForm
    #this checks for common user input mistakes and prints an error message
    except (IndexError, TypeError):
        print ("That is not a well-formed formula.")

#now we have the functions necessary to determine the truth-value of an arbitrary sentence relative to a model
def evaluate(formula, MOD): 
    return parse(tokenize(formula)).eval(MOD)



