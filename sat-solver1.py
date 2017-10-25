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
            for cl in formula:
                if k in cl:
                    formula.remove(cl)
                elif -k in cl:
                    cl.remove(-k)
                else:
                    pass
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
                
