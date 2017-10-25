def simplify(prob):
    formula , variables = prob
    i=0
    while i<len(formula):
        if  len(formula[i])==1:
            k=formula[i][0] 
            if k > 0:
                variables[abs(k)] = True
            else:
                variables[abs(k)] = False
            formula.remove(formula[i])
            copy_formula = formula
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

def readDimacs(file):
    formula = []
    file = open(file,"r")
    for line in file:
        line = line.strip()
        if line[0] == "c":
            continue
        elif line[0:5] == "p cnf":
            num_var = int(line[6])
            num_clauses = int(line[8])
            variables = dict((i,None) for i in range(1, num_var + 1))
        else:
            line = line.split()
            line = list(map(int, line))
            if line[-1]==0:
                formula.append(line[:-1])
    file.close()
    return formula, variables
                
