#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 14:41:01 2020

@author: nmbice
"""

import string

#parse atomic formulas
def atomic_parser(formula): 

    if type(formula) != str: 
        print ("Input is not an expression.")
        return None
    
    for n in range(len(formula)): 
        if formula[n] == '(': 
            par_ind = n
            pred = formula[:n]
    
    if len(formula) < 4 or '(' not in formula or ')' not in formula: 
        print ("Expression {} is not a well-formed formula.".format(formula))
        return None
    
    args = formula[par_ind+1:-1]
    
    cons = args.split(',')
    
    if pred[0].isupper() == False and pred[0] != '=': 
        print ('That expression is not an appropriate predicate.')
        return None
    
    for con in cons: 
        if con[0].islower() == False and con[0] not in string.digits: 
            print ('That expression is not an appropriate constant.')
            return None
    
    #print (cons)
    
    return [pred, cons]



#evaluate atomic formulas relative to a model
def atomic_evaluator(formula, MOD): 
    
    IN = MOD.interp
    
    #print (MOD.interp)
    #print (formula)

    parsed = atomic_parser(formula)
    
    if type(parsed) == type(None): 
        return None
    
    pred, cons = parsed[0], parsed[1]
    
    if pred not in IN: 
        print ("Model has no interpretation of predicate {}.".format(pred))
        return None
    
    objs = []
    
    for con in cons: 
        
        if con not in IN: 
            print ("Model has no interpretation of constant {}.".format(con))
            return None
        
        objs.append(IN[con])
              
    #TO FIX: arity ignored if no objects satisfy predicate   
    if len(IN[pred]) == 0: 
        return False
        
    rand_elem = next(iter(IN[pred]))
        
    if len(objs) == 1: 
        objs = objs[0]
        if isinstance(rand_elem, tuple): 
            print ("Expression {} is not a well-formed formula.".format(formula))
            return None
    else: 
        objs = tuple(objs)
        if (not isinstance(rand_elem, tuple)) or len(objs) != len(rand_elem): 
            print ("Expression {} is not a well-formed formula.".format(formula))
            return None
    #print (IN[pred])
    if objs in IN[pred]: 
        return True
    else: 
        return False
        
    
    
#test_mod = ({1,2,3}, {'L': {(1,2), (2,1), (3,1)}, 'E': {2}, 'P': {}, 'G': {(2,1), (3,1), (3,2)}, '=': {(1,1), (2,2), (3,3)}, \
#            '1': 1, '2': 2, '3': 3, 'N': {1,2,3}})


            
    
    
