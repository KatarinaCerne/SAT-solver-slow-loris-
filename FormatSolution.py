
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
