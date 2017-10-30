
def solutionToDict(input_file, output_file):
    input_file = open(input_file, "r")
    dictionary = dict()
    for line in input_file:
        line = line.split()
        for number in line:
            number = int(number)
            if number < 0:
                dictionary[abs(number)] = False
            elif number > 0:
                dictionary[abs(number)] = True
            else:
                dictionary[abs(number)] = None
    input_file.close()
    
    output_file = open(output_file, "w")
    output_file.write(str(dictionary))
    output_file.close()


def graphColouring2SATdisc(G, k, file): 
    conj = []
    slovar = dict()
    clauses = []
    a = 1
    for i in range(len(G)):
        for j in range(k):
            slovar[(i, j)] = a
            a += 1
    for i in range(len(G)):
        conj.append(Or(*((i, j) for j in range(k))))
        clauses.append([slovar[(i, j)] for j in range(k)])
        for j in range(k):
            for jj in range(j+1, k):
                conj.append(Or(Not((i, j)), Not((i, jj))))
                clauses.append([-slovar[(i, j)], -slovar[(i, jj)]])
        for h in G[i]:
            for j in range(k):
                conj.append(Or(Not((h, j)), Not((i, j))))
                clauses.append([-slovar[(h, j)], -slovar[(i, j)]])
    s = "p cnf " + str(a-1) + " " + str(len(clauses)) + "\n"
    for el in clauses:
        s += " ".join(map(str, el))
        s += " 0 \n"
    file = open(file, "w")
    file.write(s)
    file.close()
    return And(*conj)
