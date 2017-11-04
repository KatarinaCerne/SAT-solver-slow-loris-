import sys
import ast
import time
from collections import Counter
from random import uniform

from boolean import *

#input_doc = sys.argv[1]
#output_doc = sys.argv[2]

def bcp(prob):
    # sets the free literal of a unit clause true until there exists no unit clause in formula
    formula, variables = prob
    new_true = []
    for el in formula:
        list_unit = []
        for i in el:
            if variables[abs(i)] == None:
                list_unit.append(i)
            else:
                if i < 0:
                    list_unit.append(not variables[abs(i)])
                else:
                    list_unit.append(variables[abs(i)])
        num_occ = Counter(list_unit)
        if num_occ.get(True, 0) != 0:
            pass
        elif num_occ.get(False, 0) != len(list_unit) - 1:
            pass
        else:
            keys = list(num_occ.keys())
            if False in keys:
                keys.remove(False)
            a = keys[0]
            if a < 0:
                variables[abs(keys[0])] = False
            else:
                variables[abs(keys[0])] = True
            new_true.append((a, el))
    return variables, new_true

def checkFalseClause(formula, variables):
    false_clauses = []
    for el in formula:
        clause = []
        for i in el:
            if i < 0:
                clause.append(not variables[abs(i)])
            else:
                clause.append(variables[abs(i)])
        occ = Counter(clause)
        false_occ = occ.get(False, 0)
        if false_occ == len(el):
            false_clauses.append(el)
    if len(false_clauses) != 0:
        return True, false_clauses
    return False, None
    

def derivingConflictImplicates(formula, variables, dl, false_clause_list):
    a = []
    i = formula.index(false_clause_list[0])
    m = 0
    p = len(dl) - 1
    v = dl[-1][0]
    y = len(dl) - 1
    U = [False] * len(dl)
    U[0] = True
    dl_help = [x[0] for x in dl]
    while True:
        for literal in formula[i]: # notri sami false-i => literal > 0 => v dl_help je -literal? 
            v = -(literal)
            i_v = dl_help.index(v)
            if not U[i_v]: 
                U[i_v] = True 
                if i_v < y:
                    a.append(literal)
                else:
                    m += 1
        v = dl[p][0]
        i_v = dl_help.index(v)
        while not U[i_v]: 
            p = p - 1
            v = dl[p][0]
            i_v = dl_help.index(v)
        if m == 1:
           a.append(-dl[p][0])
           return a
        else:
            p = p - 1
        m = m - 1
        el = dl[p][1]
        while (el not in false_clause_list) and (p > 0):
            p = p - 1
            el = dl[p][1]
        if p == 0:
            return a
        i = formula.index(el)
        
        
def findY(dl, a):
    for j in range(len(dl)-1):
        for k in a:
            if k == abs(dl[j][0]):
                return j
    return 0

def unassignVariables(dl, variables, y2):
    new_dl = dl[:y2] + [dl[-1]] 
    for i in range(y2, len(dl) - 1):
        variables[abs(dl[i][0])] = None
    return new_dl, variables
                        
def solveSAT(prob):
    formula, variables = prob
    if formula.count([]) != 0:
        return False, variables
    y = 0
    dl = []
    free_variables = [k for k, v in variables.items() if v == None]
    while len(free_variables) != 0:
        variables, new_true = bcp((formula, variables))
        dl += new_true
        free_variables = [k for k, v in variables.items() if v == None]
        false_clause, false_clause_list = checkFalseClause(formula, variables)
        if false_clause:
            if y == 0:
                return False, variables
            a = derivingConflictImplicates(formula, variables, dl, false_clause_list)
            formula.append(a)
            if len(a) == 1:
                y2 = 0
            else:
                y2 = findY(dl, a)
            dl, variables = unassignVariables(dl, variables, y2)
        else:
            if len(free_variables) == 0:
                return True, variables
            y += 1
            p = free_variables[int(uniform(0, len(free_variables)))]
            variables[p] = True
            #formula.append([p])
            dl.append((p, [p])) 
            continue
    return True, variables
                        
    

def readDimacs(file):
    formula = []
    file = open(file,"r")
    for line in file:
        line = line.strip()
        line = line.split()
        if line[0] == "c":
            continue
        elif line[0] == "p" and line[1] == "cnf":
            num_var = int(line[2])
            num_clauses = int(line[3])
            variables = dict((i,None) for i in range(1, num_var + 1))
        else:
            line = list(map(int, line))
            if line[-1]==0:
                formula.append(line[:-1])
    file.close()
    return formula, variables

def checkOutput(formula, solution):
    conj = []
    for dis in formula:
        for i in range(0, len(dis)):
            if dis[i] < 0:
                dis[i] = Not(abs(dis[i]))
        conj.append(Or(dis))
    cnf = And(*conj)
    return cnf.evaluate(solution)


def main(input_file, output_file):
    start_time = time.time()
    formula, variables = readDimacs(input_file)
    formula_copy = formula[:]
    #formula = list(set(formula))
    sat, var = solveSAT((formula, variables))

    file = open(output_file,"w")
    if sat:
        file.write(str(var)) # prav format?
        s = checkOutput(formula_copy, var)
        
    else:
        file.write("0")
        s = ""
    file.close()
    return "Finished \n" + str(s) + str(time.time()-start_time)
    

#print(main(input_doc, output_doc))
                
