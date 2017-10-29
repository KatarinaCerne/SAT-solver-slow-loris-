import sys
import ast

input_doc = sys.argv[1]
output_doc = sys.argv[2]

solution_doc = None
if len(sys.argv) == 4:
    solution_doc = sys.argv[3] # podana kot slovar!


def simplify(prob):
    formula, variables = prob
    i=0
    while i<len(formula):
        if  len(formula[i])==1:
            k=formula[i][0] 
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
        for p, r in variables.items():
            if r == None:
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

def checkSolution(output_file, solution_file):
    if solution_file == None:
        return "Resitev ni podana"

    output_file = open(output_file, "r")
    solution_file = open(solution_file, "r")

    output = output_file.readline()
    solution = solution_file.readline()
    
    output_file.close()
    solution_file.close()

    if ast.literal_eval(output) == ast.literal_eval(solution):
        return "Resitev je OK"
    return "Resitev ni OK"

def main(input_file, output_file, solution_file):
    sat, var = solveSAT(readDimacs(input_file))

    file = open(output_file,"w")
    if sat:
        file.write(str(var)) # prav format?
    else:
        file.write("0")
    file.close()

    s = checkSolution(output_file, solution_file)
    
    return "Finished \n " + s


print(main(input_doc, output_doc, solution_doc))
                
