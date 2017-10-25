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
                
