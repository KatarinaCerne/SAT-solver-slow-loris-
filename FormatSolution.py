import math
from boolean import *

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

def polniGraf(n):
    G = [[] for k in range(n)]
    for i in range(n):
        for j in range(n):
            if j != i:
                G[i].append(j)
    return G

def graphColouring2SATdimacs(G, k, file): 
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
        #print(Or(*((i, j) for j in range(k))), [slovar[(i, j)] for j in range(k)])
        for j in range(k):
            for jj in range(j+1, k):
                conj.append(Or(Not((i, j)), Not((i, jj))))
                if [-slovar[(i, jj)], -slovar[(i, j)]] not in clauses:
                    clauses.append([-slovar[(i, j)], -slovar[(i, jj)]])
                #print(Or(Not((i, j)), Not((i, jj))), [-slovar[(i, j)], -slovar[(i, jj)]])
        for h in G[i]:
            for j in range(k):
                conj.append(Or(Not((h, j)), Not((i, j))))
                if [-slovar[(i, j)], -slovar[(h, j)]] not in clauses:
                    clauses.append([-slovar[(h, j)], -slovar[(i, j)]])
                #print(Or(Not((h, j)), Not((i, j))), [-slovar[(h, j)], -slovar[(i, j)]])
    s = "p cnf " + str(a-1) + " " + str(len(clauses)) + "\n"
    #cl_s = list(clauses)
    for el in clauses:
        s += " ".join(map(str, el))
        s += " 0 \n"
    file = open(file, "w")
    file.write(s)
    file.close()
    #return And(*conj)

def sodoku2SATdimacs(N, con, file):
    conj = []
    slovar = dict()
    clauses = []
    a = 1
    for x in range(N):
        for y in range(N):
            for n in range(N):
                slovar[(x, y, n)] = a
                a += 1
    z = int(math.sqrt(N))
    mini_sq = []
    for i in range(z):
        for j in range(z):
            mini_sq_help = []
            for x in range(z):
                for y in range(z):
                    mini_sq_help.append((x + i*z, y + j*z))
            mini_sq.append(mini_sq_help)
    for x in range(N):
        for y in range(N):
            
            conj.append(Or(*((x, y, n) for n in range(N))))
            clauses.append([slovar[(x, y, n)] for n in range(N)])
            
            conj.append(Or(*((x, n, y) for n in range(N))))
            clauses.append([slovar[(x, n, y)] for n in range(N)])
            
            conj.append(Or(*((n, x, y) for n in range(N))))
            clauses.append([slovar[(n, x, y)] for n in range(N)])
            
            conj.append(Or(*((p, q, y) for (p, q) in mini_sq[x])))
            clauses.append([slovar[(p, q, y)] for (p, q) in mini_sq[x]])
                           
            for m in range(N):
                for n in range(m+1, N):
                           
                    conj.append(Or(Not((x, y, m)), Not((x, y, n))))
                    clauses.append([-slovar[(x, y, m)], -slovar[(x, y, n)]])
                           
                    conj.append(Or(Not((x, m, y)), Not((x, n, y))))
                    clauses.append([-slovar[(x, m, y)], -slovar[(x, n, y)]])
                    
                    conj.append(Or(Not((m, x, y)), Not((n, x, y))))
                    clauses.append([-slovar[(m, x, y)], -slovar[(n, x, y)]])
                    
                    (p, q) = mini_sq[x][m]
                    (pp, qq) = mini_sq[x][n]
                    conj.append(Or(Not((p, q, y)), Not((pp, qq, y))))
                    clauses.append([-slovar[(p, q, y)], -slovar[(pp, qq, y)]])

    conj = conj + con
    for c in con:
        (x, y, z) = c
        clauses.append([slovar[(x-1, y-1, z-1)]])
    
    s = "p cnf " + str(a-1) + " " + str(len(clauses)) + "\n"
    for el in clauses:
        s += " ".join(map(str, el))
        s += " 0 \n"
    file = open(file, "w")
    file.write(s)
    file.close()                          
    #return And(*conj)
                

                                
    














    
