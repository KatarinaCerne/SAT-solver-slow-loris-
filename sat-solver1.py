import sys
import ast
import time
from collections import Counter

from boolean import *

#input_doc = sys.argv[1]
#output_doc = sys.argv[2]
    
    
def simplify(prob):
    formula, variables = prob
    i = 0
    while i<len(formula):
        if  len(formula[i])==1:
            k = formula[i][0] 
            if k > 0:
                variables[abs(k)] = True
            else:
                variables[abs(k)] = False
            formula.remove(formula[i])
            # copy_formula = formula
            j=0
            while j<len(formula):
                if k in formula[j]:
                    formula.remove(formula[j])
                    j=0
                elif -k in formula[j]:
                    formula[j].remove(-k)
                    j+=1
                else:
                    j+=1
            i=0
        else:
            i+=1
    return formula, variables

def solveSAT(prob):
    prob = simplify(prob)
    formula, variables = prob
    if formula == []:
        return True, variables
    elif [] in formula:
        return False, variables
    else:
        #kljuci = [k for k, v in variables.items() if v == None]
        #pojavitve = [0]*len(kljuci)
        flat_formula = [abs(item) for sublist in formula for item in sublist]
        pojavitve = Counter(flat_formula)
        #for k in kljuci:
        #    pojavitve[k] = flat_formula.count(k)
        #print(pojavitve)
        p = [k for k, v in pojavitve.items() if v == max(pojavitve.values())][0]
##        p = random.choice(random.choice(formula))

##še ena hevristika, ki ne izboljša 
##        pojavitve = dict()
##        binarni = 0
##        for cl in formula:
##            if len(cl)==2:
##                binarni+=1
##                for var in cl:
##                    if var<0:
##                        pojavitve[-var]=[pojavitve.get(-var,[0,0])[0],pojavitve.get(-var,[0,0])[1]+1]
##                    else:
##                        pojavitve[var]=[pojavitve.get(var,[0,0])[0]+1,pojavitve.get(var,[0,0])[1]]
##        if binarni >0:
##            maks = 0
##            for k, v in pojavitve.items():
##                if 1024*v[0]*v[1]+v[0]+v[1] > maks:
##                    p = k
##        else:
##            p = random.choice(random.choice(formula))

##        pojavitve = dict()
##        izbr_cl = min(formula, key=len)
##        for clause in formula:
##            for var in clause:
##                pojavitve[abs(var)] = pojavitve.get(abs(var),0)+1
##        v = list(pojavitve.values())
##        k = list(pojavitve.keys())
##        p = k[v.index(max(v))]
##            
            
        
        copy_form = formula[:]
        copy_var = dict(variables)
        copy_form.append([p])
        sat, var = solveSAT((copy_form, copy_var))
        if sat:
            return sat, var
        else:
            copy_form = formula[:]
            copy_var = dict(variables)
            copy_form.append([-p])
            sat, var = solveSAT((copy_form, copy_var))
            return sat, var

def solveSAT_slaba(prob):
    prob = simplify(prob)
    formula, variables = prob
    if formula == []:
        return True, variables
    elif [] in formula:
        return False, variables
    else:
        for p, r in variables.items():
            if r == None:
                copy_form = formula[:]
                copy_var = dict(variables)
                copy_form.append([p])
                sat, var = solveSAT_slaba((copy_form, copy_var))
                if sat:
                    return sat, var
                else:
                    copy_form = formula[:]
                    copy_var = dict(variables)
                    copy_form.append([-p])
                    sat, var = solveSAT_slaba((copy_form, copy_var))
                    return sat, var

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
                
