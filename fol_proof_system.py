#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 10:28:04 2020

@author: nmbice
"""

from fol_syntax_semantics import parse, tokenize, TruthValue, And, Or, Not, Implies, Bicond, \
Universal, Existential, atomicTok
from fol_atomic import atomic_parser
import re
import string




#function to flatten nested lists, which will be used to check for particular constants in proof system
def remove_nestings(l, output=[]): 
    for i in l: 
        if type(i) == list: 
            remove_nestings(i, output)
        else: 
            output.append(i)
            
    return output



#function to check whether input is an assumption and output the actual formula
def assum(formula): 
    if type(formula) == list: 
        return formula[0]
    else: 
        return formula
    


#function to ensure user isn't trying to reference a line in a different subproof
def hyp_space_rel(prem, proof, line, exit_lines, sub=False): 
    emb = 0
    emb_thresh = 0
    for n in range(len(proof)): 
        if line == n + len(prem):
            if sub == False: 
                emb_thresh = emb
            else: 
                emb_thresh = emb - 1
        elif type(proof[n]) == list: 
            emb +=1
        elif n + len(prem) in exit_lines: 
            emb -= 1
        if emb_thresh > emb: 
            return False
    return True



#function to make sure the user isn't trying to exit the base proof
def end_checker(prem,proof,exit_lines): 
    emb = 0
    for n in range(len(proof)): 
        if type(proof[n]) == list: 
            emb += 1
        elif n + len(prem) in exit_lines: 
            emb -= 1
    if emb <= 0: 
        return False
    else: 
        return True
    
    

#function to output bound variables in formula
def bound_var(formula, var_set=set()): 
    if type(formula) == Universal or type(formula) == Existential: 
        var_set.add(formula.var)
        var_set = var_set.union(bound_var(formula.formula, var_set))
        return var_set
    elif type(formula) == And or type(formula) == Or or type(formula) == Implies or type(formula) == Bicond: 
        left_form = formula.left
        right_form = formula.right
        left_vars = bound_var(left_form, var_set)
        right_vars = bound_var(right_form, var_set)
        var_set = var_set.union(left_vars, right_vars)
        return var_set
    elif type(formula) == Not: 
        sub_vars = bound_var(formula.formula,var_set)
        var_set = var_set.union(sub_vars)
        return var_set
    else: 
        return var_set


#function to replace specified bound variable by dummy variable (*)
def bound_fix(formula, var): 
    formula_str = str(formula)
    tok = tokenize(formula_str)
    for n in range(len(tok)): 
        if (tok[n] == 'U' or tok[n] == 'X') and tok[n+1] == var: 
            tok[n+1] = '*'
            if atomicTok(tok[n+2]): 
                tok[n+2] = tok[n+2].replace(var,'*')
            else: 
                par_lev = 0
                scope_end = 0
                for m in range(n+2,len(tok)): 
                    if tok[m] == '(': 
                        par_lev += 1
                    elif tok[m] == ')': 
                        par_lev -= 1
                        if m == len(tok) - 1: 
                            scope_end = m
                    elif par_lev == 0: 
                        scope_end = m
                        break
                for l in range(n+2,scope_end): 
                    tok[l] = tok[l].replace(var,'*')
    final = parse(tok)
    return final


#function to output active assumptions
def active_assum(prem,proof,exit_lines): 
    active = []
    for n in range(len(proof)): 
        if type(proof[n]) == list: 
            active.append(proof[n][0])
        elif n + len(prem) in exit_lines: 
            active.pop()
    return active



#function to create display of proof
def proof_display(prem, proof, exit_lines): 
    print (' ')
    count = 0
    for pr in prem: 
        print (str(count) + (' ' * (6 - len(str(count)))) + str(pr))
        count += 1
    print ('_________________')
    print (' ')
    emb = 0
    for line in proof: 
        if type(line) == list: 
            emb += 1
            print (str(count) + (' ' * (6 - len(str(count)))) + ('|' * emb) + ' ' + str(line[0]))
            count += 1
        elif count in exit_lines: 
            emb -= 1
            print (str(count) + (' ' * (6 - len(str(count)))) + ('|' * emb) + ' ' + str(line))
            count += 1
        else: 
            print (str(count) + (' ' * (6 - len(str(count)))) + ('|' * emb) + ' ' + str(line))
            count += 1
    print (' ')
        
    

#this is the main function for constructing and validating proofs
#see Readme file for command descriptions
def prover():
    proof = []
    prem = []
    print('Please state the premises, separated by commas.')
    e = input('%')
    if e == 'Exit': 
        return None
    else: 
        r = re.compile(r'(?:[^,(]|\([^)]*\))+')
        prems = r.findall(e)
        for pr in prems: 
            if parse(tokenize(pr)) == None: 
                prover()
                return None
            else: 
                prem.append(parse(tokenize(pr)))
        count = 0
        exit_lines = []
        print (' ')
        for pr in prem: 
            print (str(count) + (' ' * (6 - len(str(count)))) + str(pr))
            count += 1
        print ('_________________')
        print (' ')
        
        while True: 
            print ('Please state an inference rule. Separate line numbers with commas. Type "Exit" to exit.')
            e = input('%')
            if e == 'Exit': 
                break
            else: 
                rule = r.findall(e)
                
                if rule[0] == 'Assume': 
                    try: 
                        a = rule[1]
                        assumption = parse(tokenize(a))
                        if assumption == None: 
                            pass
                        else: 
                            proof.append([assumption])
                        proof_display(prem, proof, exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a formula to assume.')
                    
                elif rule[0] == 'Delete': 
                    proof = proof[:-1]
                    proof_display(prem, proof, exit_lines)
                
                elif rule[0] == 'TI': 
                    proof.append(TruthValue(True))
                    proof_display(prem, proof, exit_lines)
                    
                elif rule[0] == '^EL': 
                    try:
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use that formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                line = int(rule[1])
                                if type(prem[line]) != And: 
                                    print ('That formula is not a conjunction.')
                                else: 
                                    new = prem[line].left
                                    proof.append(new)
                                    proof_display(prem, proof, exit_lines)
                            else: 
                                line = int(rule[1]) - len(prem)
                                if type(proof[line]) == list: 
                                    if type(proof[line][0]) != And: 
                                        print ('That formula is not a conjunction.')
                                    else: 
                                        new = proof[line][0].left
                                        proof.append(new)
                                        proof_display(prem, proof, exit_lines)
                                elif type(proof[line]) != And: 
                                    print ('That formula is not a conjunction.')
                                else: 
                                    new = proof[line].left
                                    proof.append(new)
                                    proof_display(prem, proof, exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a line number.')
                        pass
                        
                elif rule[0] == '^ER': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use that formula.')
                        else:                         
                            if int(rule[1]) < len(prem): 
                                line = int(rule[1])
                                if type(prem[line]) != And: 
                                    print ('That formula is not a conjunction.')
                                else: 
                                    new = prem[line].right
                                    proof.append(new)
                                    proof_display(prem, proof, exit_lines)
                            else: 
                                line = int(rule[1]) - len(prem)
                                if type(proof[line]) == list: 
                                    if type(proof[line][0]) != And: 
                                        print ('That formula is not a conjunction.')
                                    else: 
                                        new = proof[line][0].right
                                        proof.append(new)
                                        proof_display(prem, proof, exit_lines)
                                elif type(proof[line]) != And: 
                                    print ('That formula is not a conjunction.')
                                else: 
                                    new = proof[line].right
                                    proof.append(new)
                                    proof_display(prem, proof, exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a line number.')
                        pass
                elif rule[0] == '^I':
                    try:
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False \
                        or hyp_space_rel(prem,proof,int(rule[2]),exit_lines) == False: 
                            print ('You can no longer use that formula.')
                        else: 
                            if int(rule[1]) < len(prem) and int(rule[2]) < len(prem): 
                                line1 = int(rule[1])
                                line2 = int(rule[2])
                                new = And(assum(prem[line1]), assum(prem[line2]))
                                proof.append(new)
                                proof_display(prem,proof,exit_lines)
                            elif int(rule[1]) < len(prem) and int(rule[2]) >= len(prem): 
                                line1 = int(rule[1])
                                line2 = int(rule[2]) - len(prem)
                                new = And(assum(prem[line1]), assum(proof[line2]))
                                proof.append(new)
                                proof_display(prem,proof,exit_lines)
                            elif int(rule[1]) >= len(prem) and int(rule[2]) < len(prem): 
                                line1 = int(rule[1]) - len(prem)
                                line2 = int(rule[2])
                                new = And(assum(proof[line1]), assum(prem[line2]))
                                proof.append(new)
                                proof_display(prem,proof,exit_lines)
                            else: 
                                line1 = int(rule[1]) - len(prem)
                                line2 = int(rule[2]) - len(prem)
                                print (proof[line1])
                                new = And(assum(proof[line1]),assum(proof[line2]))
                                proof.append(new)
                                proof_display(prem, proof, exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify two line numbers.')
                        pass
                elif rule[0] == 'vIR':
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use that formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                line = int(rule[1])
                                new = Or(assum(prem[line]),parse(tokenize(rule[2])))
                                proof.append(new)
                                proof_display(prem, proof, exit_lines)
                            else: 
                                line = int(rule[1]) - len(prem)
                                new = Or(assum(proof[line]),parse(tokenize(rule[2])))
                                proof.append(new)
                                proof_display(prem, proof, exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a line number and a formula.')
                        pass
                elif rule[0] == 'vIL':
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use that formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                line = int(rule[1])
                                new = Or(parse(tokenize(rule[2])),assum(prem[line]))
                                proof.append(new)
                                proof_display(prem, proof, exit_lines)
                            else: 
                                line = int(rule[1]) - len(prem)
                                new = Or(parse(tokenize(rule[2])),assum(proof[line]))
                                proof.append(new)
                                proof_display(prem, proof, exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a line number and a formula.')
                        pass
                elif rule[0] == 'End': 
                    if end_checker(prem,proof,exit_lines) == False:
                        print ('There are no more assumptions.')
                    else: 
                        line = len(prem) + len(proof)
                        exit_lines.append(line)
                        proof.append(' ')
                        proof_display(prem, proof, exit_lines)
                elif rule[0] == 'vE': 
                    try: 

                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use the specified formula.')
                        else: 
                            a1 = rule[2].split('-')
                            a2 = rule[3].split('-')
                            proof_test = proof.copy()
                            proof_test.append(' ')
                            exit_test = exit_lines.copy()
                            exit_test.append(len(proof))
                            if int(a1[0]) > int(a1[1]) or int(a2[0]) > int(a2[1]): 
                                print ('That is not an appropriate range of line numbers.')
                            elif end_checker(prem,proof,exit_lines) == True and (hyp_space_rel(prem,proof_test,int(a1[0]),exit_test) == False \
                            or hyp_space_rel(prem,proof_test,int(a2[0]),exit_test) == False): 
                                print ('You are still in that subproof.')
                            elif int(a1[0]) < len(prem) or int(a2[0]) < len(prem) or \
                            type(proof[int(a1[0]) - len(prem)]) != list or type(proof[int(a2[0]) - len(prem)]) != list: 
                                print ('Formulas at beginning of line number ranges must be assumptions.')
                            else: 
                                if hyp_space_rel(prem,proof,int(a1[0]),exit_lines,True) == False or \
                                hyp_space_rel(prem,proof,int(a1[1]),exit_lines,True) == False or \
                                hyp_space_rel(prem,proof,int(a2[0]),exit_lines,True) == False or \
                                hyp_space_rel(prem,proof,int(a2[1]),exit_lines,True) == False: 
                                    print ('You can no longer use a specified formula.')
                                elif str(assum(proof[int(a1[1]) - len(prem)])) != str(assum(proof[int(a2[1]) - len(prem)])): 
                                    print ('The two final formulas must be identical.')
                                elif (int(rule[1]) < len(prem) and type(assum(prem[int(rule[1])])) != Or) or \
                                (int(rule[1]) >= len(prem) and type(assum(proof[int(rule[1]) - len(prem)])) != Or): 
                                    print ('That formula is not a disjunction.')
                                elif (int(rule[1]) < len(prem) and str(assum(proof[int(a1[0]) - len(prem)])) != str(assum(prem[int(rule[1])]).left)) or \
                                (int(rule[1]) >= len(prem) and str(assum(proof[int(a1[0]) - len(prem)])) != str(assum(proof[int(rule[1]) - len(prem)]).left)): 
                                    print ('The first assumption must be the left disjunct of the disjunction.')
                                elif (int(rule[1]) < len(prem) and str(assum(proof[int(a2[0]) - len(prem)])) != str(assum(prem[int(rule[1])]).right)) or \
                                (int(rule[1]) >= len(prem) and str(assum(proof[int(a2[0]) - len(prem)])) != str(assum(proof[int(rule[1]) - len(prem)]).right)): 
                                    print ('The second assumption must be the right disjunct of the disjunction.')
                                else: 
                                    new_form = proof[int(a2[1]) - len(prem)]
                                    proof.append(new_form)
                                    proof_display(prem,proof,exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify line numbers.')
                        pass
                elif rule[0] == '~E': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use the specified formula.')
                        elif (int(rule[1]) < len(prem) and type(prem[int(rule[1])]) != Not) or \
                        (int(rule[1]) >= len(prem) and type(proof[int(rule[1]) - len(prem)]) != Not) or \
                        (int(rule[1]) < len(prem) and type(prem[int(rule[1])].formula) != Not) or \
                        (int(rule[1]) >= len(prem) and type(proof[int(rule[1]) - len(prem)].formula) != Not): 
                            print ('That formula is not a double negation.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                new_form = prem[int(rule[1])].formula.formula
                            else: 
                                new_form = proof[int(rule[1]) - len(prem)].formula.formula
                            proof.append(new_form)
                            proof_display(prem,proof,exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a line number.')
                elif rule[0] == '~I': 
                    try: 
                        a = rule[1].split('-')[0]
                        f = rule[1].split('-')[1]
                        proof_test = proof.copy()
                        proof_test.append(' ')
                        exit_test = exit_lines.copy()
                        exit_test.append(len(proof))
                        if int(a) > int(f): 
                            print ('That is not an appropriate range of line numbers.')
                        elif int(a) < len(prem) or type(proof[int(a) - len(prem)]) != list: 
                            print ('Formula at the beginning of the line number range must be an assumption.')    
                        elif end_checker(prem,proof,exit_lines) == True and hyp_space_rel(prem,proof_test,int(a),exit_test) == False: 
                            print ('You are still in that subproof.')                        
                        else: 
                            if hyp_space_rel(prem,proof,int(a),exit_lines,True) == False or \
                            hyp_space_rel(prem,proof,int(f),exit_lines,True) == False: 
                                print ('You can no longer use a specified formula.')
                            elif type(assum(proof[int(f) - len(prem)])) != TruthValue or \
                            assum(proof[int(f) - len(prem)]).value != False: 
                                print ('The final formula must be F.')
                            else: 
                                new_form = Not(assum(proof[int(a) - len(prem)]))
                                proof.append(new_form)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == 'FE': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                           print ('You can no longer use the specified formula.')
                        else:
                            if (int(rule[1]) < len(prem) and (type(prem[int(rule[1])]) != TruthValue or \
                                    prem[int(rule[1])].value != False)) or (int(rule[1]) >= len(prem) and \
    (type(proof[int(rule[1]) - len(prem)]) != TruthValue or proof[int(rule[1]) - len(prem)].value != False)): 
                                        print ('The formula must be F.')
                            else: 
                                new_form = parse(tokenize(rule[2]))
                                proof.append(new_form)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError, ValueError): 
                        print ('You must specify a line number.')
                elif rule[0] == 'FI': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False or \
                        hyp_space_rel(prem,proof,int(rule[2]),exit_lines) == False: 
                            print ('You can no longer use a specified formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                form1 = assum(prem[int(rule[1])])
                            else: 
                                form1 = assum(proof[int(rule[1]) - len(prem)])
                            if int(rule[2]) < len(prem): 
                                form2 = assum(prem[int(rule[2])])
                            else: 
                                form2 = assum(proof[int(rule[2]) - len(prem)])
                            if type(form2) != Not or str(form2.formula) != str(form1): 
                                print ('The second formula must be the negation of the first.')
                            else: 
                                proof.append(TruthValue(False))
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == 'R': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use the specified formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                proof.append(assum(prem[int(rule[1])]))
                            else: 
                                proof.append(assum(proof[int(rule[1]) - len(prem)]))
                            proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify a line number.')
                elif rule[0] == '>E': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False or \
                        hyp_space_rel(prem,proof,int(rule[2]),exit_lines) == False: 
                            print ('You can no longer use a specified formula.')       
                        else: 
                            if int(rule[1]) < len(prem): 
                                form1 = assum(prem[int(rule[1])])
                            else: 
                                form1 = assum(proof[int(rule[1]) - len(prem)])
                            if int(rule[2]) < len(prem): 
                                form2 = assum(prem[int(rule[2])])
                            else: 
                                form2 = assum(proof[int(rule[2]) - len(prem)])
                            if type(form2) != Implies or str(form2.left) != str(form1): 
                                print ('The first formula must be the antecendent of the second formula and the second formula must be a conditional.')
                            else: 
                                proof.append(form2.right)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == '>I': 
                    try: 
                        a = rule[1].split('-')
                        proof_test = proof.copy()
                        proof_test.append(' ')
                        exit_test = exit_lines.copy()
                        exit_test.append(len(proof))
                        if int(a[0]) > int(a[1]): 
                            print ('That is not an appropriate range of line numbers.')
                        elif int(a[0]) < len(prem) or type(proof[int(a[0]) - len(prem)]) != list: 
                            print ('Formula at the beginning of the line number range must be an assumption.')
                        elif end_checker(prem,proof,exit_lines) == True and hyp_space_rel(prem,proof_test,int(a),exit_test) == False: 
                            print ('You are still in that subproof.')                               
                        else: 
                            a_form = assum(proof[int(a[0]) - len(prem)])
                            c_form = assum(proof[int(a[1]) - len(prem)])
                            if hyp_space_rel(prem,proof,int(a[0]),exit_lines, True) == False or \
                            hyp_space_rel(prem,proof,int(a[1]),exit_lines, True) == False: 
                                print('You can no longer use a specified formula.')
                            else: 
                                new_form = Implies(a_form, c_form)
                                proof.append(new_form)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == '-ER': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False or \
                        hyp_space_rel(prem,proof,int(rule[2]),exit_lines) == False: 
                            print ('You can no longer use a specified formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                form1 = assum(prem[int(rule[1])])
                            else: 
                                form1 = assum(proof[int(rule[1]) - len(prem)])
                            if int(rule[2]) < len(prem): 
                                form2 = assum(prem[int(rule[2])])
                            else: 
                                form2 = assum(proof[int(rule[2]) - len(prem)])
                            if type(form1) != Bicond or str(form1.left) != str(form2): 
                                print ('That is not a biconditional with the second formula as its left subformula.')
                            else: 
                                proof.append(form1.right)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == '-EL': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False or \
                        hyp_space_rel(prem,proof,int(rule[2]),exit_lines) == False: 
                            print ('You can no longer use a specified formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                form1 = assum(prem[int(rule[1])])
                            else: 
                                form1 = assum(proof[int(rule[1]) - len(prem)])
                            if int(rule[2]) < len(prem): 
                                form2 = assum(prem[int(rule[2])])
                            else: 
                                form2 = assum(proof[int(rule[2]) - len(prem)])
                            if type(form1) != Bicond or str(form1.right) != str(form2): 
                                print ('That is not a biconditional with the second formula as its right subformula.')
                            else: 
                                proof.append(form1.left)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == '-I': 
                    try: 
                        a1 = rule[1].split('-')
                        a2 = rule[2].split('-')
                        proof_test = proof.copy()
                        proof_test.append(' ')
                        exit_test = exit_lines.copy()
                        exit_test.append(len(proof))
                        if int(a1[0]) > int(a1[1]) or int(a2[0]) > int(a2[1]): 
                            print ('That is not an appropriate range of line numbers.')
                        elif int(a1[0]) < len(prem) or int(a2[0]) < len(prem) or type(proof[int(a1[0]) - len(prem)]) != list or \
                        type(proof[int(a2[0]) - len(prem)]) != list: 
                            print ('Formulas at the beginning of line number ranges must be assumptions.')
                        elif end_checker(prem,proof,exit_lines) == True and (hyp_space_rel(prem,proof_test,int(a1[0]),exit_test) == False \
                                         or hyp_space_rel(prem,proof_test,int(a2[0]),exit_test) == False): 
                            print ('You are still in that subproof.') 
                        else: 
                            if hyp_space_rel(prem,proof,int(a1[0]),exit_lines,True) == False or \
                            hyp_space_rel(prem,proof,int(a1[1]),exit_lines,True) == False or \
                            hyp_space_rel(prem,proof,int(a2[0]),exit_lines,True) == False or \
                            hyp_space_rel(prem,proof,int(a2[1]),exit_lines,True) == False: 
                                print ('You can no longer use a specified formula.')
                            else: 
                                form1 = assum(proof[int(a1[0]) - len(prem)])
                                form2 = proof[int(a1[1]) - len(prem)]
                                form3 = assum(proof[int(a2[0]) - len(prem)])
                                form4 = proof[int(a2[1]) - len(prem)]
                                if str(form1) != str(form4) or str(form2) != str(form3): 
                                    print ('One must derive the second formula from the first and the first formula from the second.')
                                else: 
                                    new_form = Bicond(form1,form2)
                                    proof.append(new_form)
                                    proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == '=I': 
                    try: 
                        cons = rule[1]
                        if cons[0].islower() == False and cons[0] not in string.digits: 
                            print ('That is not an appropriate constant.')
                        else: 
                            form_str = '=(' + cons + ',' + cons + ')'
                            form = parse(tokenize(form_str))
                            if form == None: 
                                print ('That is not an appropriate constant.')
                            else:
                                proof.append(form)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print('You must specify a constant.')
                elif rule[0] == '=E': 
                    try:
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False or \
                        hyp_space_rel(prem,proof,int(rule[2]),exit_lines) == False: 
                            print ('You can no longer use a specified formula.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                idform = prem[int(rule[1])]
                            else: 
                                idform = assum(proof[int(rule[1]) - len(prem)])
                            if int(rule[2]) < len(prem): 
                                form = prem[int(rule[2])]
                            else: 
                                form = assum(proof[int(rule[2]) - len(prem)])
                            if str(idform)[0] != '=' or str(idform)[1] != '(': 
                                print ('The first formula specified must be an identity.')
                            else: 
                                parsed_idform = atomic_parser(str(idform))
                                if len(parsed_idform[1]) != 2: 
                                    print ('An identity formula must only include two terms.')
                                else: 
                                    con1 = parsed_idform[1][0]
                                    con2 = parsed_idform[1][1]
                                    var_set = set()
                                    bound_vars = bound_var(form, var_set)
                                    var_set = set()
                                    if con1 in bound_vars or con2 in bound_vars: 
                                        print ('A term cannot be both a constant and a variable.')
                                    else: 
                                        form_str = str(form)
                                        new_form_str = form_str.replace(con1,con2)
                                        print (new_form_str)
                                        new_form = parse(tokenize(new_form_str))
                                        proof.append(new_form)
                                        proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers.')
                elif rule[0] == 'XI': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use the specified formula.')
                        elif (rule[2][0].islower() == False and rule[2][0] not in string.digits) \
                        or rule[3][0].islower() == False: 
                            print ('That is not an appropriate term.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                form = prem[int(rule[1])]
                            else: 
                                form = assum(proof[int(rule[1]) - len(prem)])
                            var_set = set()
                            bound_vars = bound_var(form, var_set)
                            var_set = set()
                            if rule[2] in bound_vars or rule[3] in bound_vars: 
                                print ('That term is already used as a variable.')
                            else: 
                                form_str = str(form)
                                new_form_str = form_str.replace(rule[2],rule[3])
                                subform = parse(tokenize(new_form_str))
                                new_form = Existential(rule[3],subform)
                                proof.append(new_form)
                                proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify a line number, a constant, and a variable.')
                elif rule[0] == 'UE': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use the specified formula.')
                        if int(rule[1]) < len(prem): 
                            form = prem[int(rule[1])]
                        else: 
                            form = assum(proof[int(rule[1]) - len(prem)])
                        if type(form) != Universal: 
                            print ('That is not a univerally-quantified formula.')
                        elif rule[2][0].islower() == False and rule[2][0] not in string.digits(): 
                            print ('That is not an appropriate constant.')
                        else: 
                            subform = form.formula
                            var = form.var
                            mod_form = bound_fix(subform, var)
                            rep_form_str = str(mod_form).replace(var,rule[2])
                            final_form_str = rep_form_str.replace('*',var)
                            final_form = parse(tokenize(final_form_str))
                            proof.append(final_form)
                            proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify a line number.')
                elif rule[0] == 'UI': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False: 
                            print ('You can no longer use the specified formula.')
                        elif (rule[2][0].islower() == False and rule[2][0] not in string.digits()) or \
                        rule[3][0].islower() == False:
                            print ('That is not an appropriate constant or variable.')
                        else: 
                            prem_strs = [str(pr) for pr in prem]
                            assum_strs = str(active_assum(prem,proof,exit_lines))
                            if rule[2] in str(prem_strs): 
                                print ('That constant appears in a premise.')
                            elif rule[2] in str(assum_strs): 
                                print ('That constant appears in an active assumption.')
                            else: 
                                if int(rule[1]) < len(prem): 
                                    print ('You cannot generalize from a premise.')
                                else: 
                                    form = proof[int(rule[1]) - len(prem)]
                                    form_str = str(form)
                                    form_rep = form_str.replace(rule[2],rule[3])
                                    new_form = Universal(rule[3],parse(tokenize(form_rep)))
                                    proof.append(new_form)
                                    proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify a line number, a constant, and a variable.')
                elif rule[0] == 'XE': 
                    try: 
                        if hyp_space_rel(prem,proof,int(rule[1]),exit_lines) == False or \
                        hyp_space_rel(prem,proof,int(rule[2]),exit_lines,True) == False or \
                        hyp_space_rel(prem,proof,int(rule[3]),exit_lines,True) == False: 
                            print ('You can no longer use the specified formula.')
                        elif rule[4][0].islower() == False and rule[4][0] not in string.digits(): 
                            print ('That is not an appropriate constant.')
                        else: 
                            if int(rule[1]) < len(prem): 
                                form1 = assum(prem[int(rule[1])])
                            else: 
                                form1 = assum(proof[int(rule[1]) - len(prem)])
                            if int(rule[2]) < len(prem): 
                                print('The second formula must be an assumption, not a premise.')
                            else: 
                                form2 = proof[int(rule[2]) - len(prem)]
                                if int(rule[3]) < len(prem): 
                                    print ('The final formula cannot be a premise.')
                                else: 
                                    form3 = proof[int(rule[3]) - len(prem)]
                                    prem_str = str([str(pr) for pr in prem])
                                    prev_pr_str = str([str(pro) for pro in proof[:int(rule[2])-len(prem)]])
                                    subform = form1.formula
                                    var = form1.var
                                    mod_form = bound_fix(subform, var)
                                    rep_form_str = str(mod_form).replace(var,rule[4])
                                    final_form_str = rep_form_str.replace('*',var)
                                    final_form = parse(tokenize(final_form_str))
                                    if type(form1) != Existential: 
                                        print('That formula is not existentially quantified.')
                                    elif rule[4] in prem_str or rule[4] in prev_pr_str or rule[4] in str(form3): 
                                        print ('You cannot use a constant that appears earlier in the proof or appears in the conclusion.')
                                    elif type(form2) != list: 
                                        print ('The second formula must be an assumption.')
                                    elif str(assum(form2)) != str(final_form): 
                                        print ('The second formula must be the subformula of the first, with the variable replaced by the specified constant.')
                                    else: 
                                        new_form = form3
                                        proof.append(new_form)
                                        proof_display(prem,proof,exit_lines)
                    except (IndexError,ValueError): 
                        print ('You must specify line numbers and a constant.')
                elif rule[0] == 'Finish': 
                    if len(proof) == 0: 
                        print ('You have not begun a proof.')
                    elif len(prem) == 0: 
                        if len(active_assum(prem,proof,exit_lines)) > 0: 
                            print ('You still have an active assumption.')
                        else: 
                            print ('Theorem: {}.'.format(str(proof[-1])))
                            break
                    else: 
                        prem_str = ''
                        if len(prem) == 1: 
                            prem_str = str(prem[0])
                        elif len(prem) == 2: 
                            prem_str = str(prem[0]) + ' and ' + str(prem[1])
                        else: 
                            for pr in prem[:-1]: 
                                prem_str = prem_str + str(pr) + ', '
                            prem_str = prem_str + 'and ' + str(prem[-1])
                        if len(active_assum(prem,proof,exit_lines)) > 0: 
                            print ('You still have an active assumption.')
                        else: 
                            print ('Theorem: If {0} then {1}.'.format(prem_str,str(proof[-1])))
                            break
#                elif rule[0] == 'Restart': 
#                    prover()
                else: 
                    print ('That is not an inference rule.')



                
if __name__ == '__main__': 
    prover()
    
    
