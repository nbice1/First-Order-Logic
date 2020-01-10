#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:21:55 2020

@author: nmbice
"""

from fol_syntax_semantics import evaluate, Model
import re
import string

#model = Model({1,2,3})
#model.interp = {'L': {(1,2), (2,1), (3,1)}, 'E': {2}, 'P': {}, 'G': {(2,1), (3,1), (3,2)}, '=': {(1,1), (2,2), (3,3)}, \
#            '1': 1, '2': 2, '3': 3, 'N': {1,2,3}}



#print (evaluate('(Ux=(x,x) ^ (XyG(2,y) > =(2,2)))', model))

#this is the evaluator program, which requests a string from the user as input and either outputs the 
#truth-value of the corresponding logical formula or constructs a model
def evaluator():
    while True:
        e = input('%')
        if e == 'model': 
            print ('Please specify the domain of your model, with objects separated by commas.')
            d = input('%')
            dom = d.split(',')
            model = Model(set([eval(x) for x in dom]))
            interpreting = True
            while interpreting == True: 
                print ('Please specify an expression to interpret. Type "done" when there are no more expressions to interpret.')
                exp = input('%')
                if exp == 'done': 
                    break
                print ('Please specify its interpretation, using commas to separate elements.')
                i = input('%')
                r = re.compile(r'(?:[^,(]|\([^)]*\))+')
                inter = r.findall(i)
                if (len(exp) == 1 and (exp.islower() or exp in string.digits)) or \
                (len(exp) > 1 and (exp[0].islower() or exp[0] in string.digits)): 
                    model.interp[exp] = eval(inter[0])
                else:
                    model.interp[exp] = set([eval(x) for x in inter])
            print('Current variables are {}. Would you like to add additional variables? Type "yes" or "no".'.format(model.all_vars))
            v = input('%')
            if v == 'yes':
                print ('Input new variables, separated by commas.')
                new_vars = input('%')
                if new_vars == '': 
                    pass
                new_vars = new_vars.split(',')
                for var in new_vars: 
                    model.all_vars.add(var)
                #print (model.domain, model.interp, model.all_vars)
            else: 
                pass
        elif e == 'exit':
            break
        elif e == 'evaluate':
            #here we use our parser to determine the appropriate syntax tree and then run its eval method and print 
            #the truth-value of the inputted sentence relative to the model
            print ('Please input the sentence to be evaluated relative to the specified model.')
            s = input('%')
            try:
                print ('%', evaluate(s, model))
            #if the user inputted an improper string, they will get an error message and the program will continue to run
            except AttributeError:
                print ('That is not a well-formed sentence.')
            except UnboundLocalError: 
                print ('Model has not been defined.')

        else: 
            print ('Please input "model", "evaluate", or "exit".')
            pass
                

