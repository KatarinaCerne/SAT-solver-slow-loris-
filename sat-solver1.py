import sys
import ast
import time
from collections import Counter

from boolean import *

#input_doc = sys.argv[1]
#output_doc = sys.argv[2]


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
    formula_old = []
    i = 0
    while True:
        i += 1
        if i > 10000000:
            return False, variables
        
        prob = simplify(prob)
        formula, variables = prob
        formula_old = formula
        if formula == []:
            return True, variables
        elif [] in formula and len(formula) == 1:
            return False, variables
        elif [] in formula:
            sat, var = False, variables
            copy_form = formula_old[:]
            copy_var = dict(variables)
            copy_form.append([-p])
            prob = (copy_form, copy_var)
            continue
        else:
            flat_formula = [abs(item) for sublist in formula for item in sublist]
            pojavitve = Counter(flat_formula)
            p = [k for k, v in pojavitve.items() if v == max(pojavitve.values())][0]
            copy_form = formula[:]
            copy_var = dict(variables)
            formula_old = copy_form[:]
            copy_form.append([p])
            prob = (copy_form, copy_var)

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
    print(slovar)
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
        file.write(str(formatted_output)) # prav format?
        s = checkOutput(formula_copy, var)
        
    else:
        file.write("0")
        s = ""
    file.close()
    return "Finished \n" + str(s) + str(time.time()-start_time)
    

#print(main(input_doc, output_doc))
                
