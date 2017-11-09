import sys
import ast
import time
from collections import Counter
from copy import deepcopy

from boolean import *

command_line = False
if len(sys.argv) == 3:
    input_doc = sys.argv[1]
    output_doc = sys.argv[2]
    command_line = True


def findUnit(prob):
    formula, variables = prob
    unit_clauses = []
    for clause in formula:
        if len(clause) == 1:
            k=clause[0]
            unit_clauses.append(k)
    return unit_clauses

def simplify_by_unit(prob, var):
    formula, variables = prob
    c_form = []
    for clause in formula:
        if var in clause:
            pass
        elif -var in clause:
            clause.remove(-var)
            c_form.append(clause)
        else:
            c_form.append(clause)
    return c_form, variables

def simplify(prob):
    units = findUnit(prob)
    while len(units) > 0:
        var = units.pop()
        prob = simplify_by_unit(prob, var)
        formula, variables = prob
        variables[abs(var)] = var > 0
        units = findUnit((formula, variables))
        prob = formula, variables
    return prob


def solveSAT(prob):
    prob = simplify(prob) 
    formula, variables = prob
    states = {}
    st = 0
    
    if formula == []:
        return True, variables
    elif [] in formula:
        return False, variables
    else:
        flat_formula = [abs(item) for sublist in formula for item in sublist]
        pojavitve = Counter(flat_formula)

        p = [k for k, v in pojavitve.items() if v == max(pojavitve.values())][0]
        
        states[st] = [formula, variables, p]
        while True:
            for_n, var_n, p_n = states[st]
            
            copy_form = deepcopy(for_n)
            copy_var = dict(var_n)
            #copy_poj = dict(poj_n)

            copy_form.append([p_n])
            copy_form, copy_var = simplify((copy_form, copy_var))

            if copy_form == []:
                return True, copy_var
            elif [] in copy_form:
                if st == 0:
                    if states[st][2]>0:
                        states[st][2] = -p_n
                    elif states[st][2]<0:
                        return False, copy_var
                elif st > 0:
                    if states[st][2]>0:
                        states[st][2] = -p_n
                    elif states[st][2]<0:
                        while states[st][2]<0:
                            if st == 0:
                                return False, states[st][1]
                            else:
                                st-=1
                        states[st][2] = -states[st][2]
            else:
                st += 1
                                           
                copy_flat_form = [abs(item) for sublist in copy_form for item in sublist]
                copy_poj = Counter(copy_flat_form)
                                           
                p = [k for k, v in copy_poj.items() if v == max(copy_poj.values())][0]
                                           
                states[st] = [copy_form, copy_var, p]

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

def formatOutput(slovar):
    formatted_output = ""
    for k, v in slovar.items():
        if v:
            formatted_output += str(k) + " "
        else:
            formatted_output += str(-k) + " "
    return formatted_output


def main(input_file, output_file):
    start_time = time.time()
    formula, variables = readDimacs(input_file)
    formula_copy = formula[:]
    sat, var = solveSAT((formula, variables))

    file = open(output_file,"w")
    if sat:
        formatted_output = formatOutput(var)
        file.write(str(formatted_output))
        #file.write(str(var))
        s = checkOutput(formula_copy, var)
    else:
        file.write("0")
        s = checkOutput(formula_copy, var)
    file.close()
    return "Finished " + str(s) + " " + str(time.time()-start_time)
    
if command_line:
    print(main(input_doc, output_doc))
                
