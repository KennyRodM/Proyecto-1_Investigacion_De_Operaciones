import sys




#---------------------------------- Open File -------------------------------------------------------#
'''
This function simply opens the file from which we are going the get the information for doing the whole
process of the project.
'''
def open_file(file_name):
    file1 = open(file_name, 'r')
    Lines = file1.readlines()
    i = 0
    while(i<len(Lines)):
        Lines[i] = [int(e) if e.isdigit() else e for e in Lines[i].split(',')]
        i+=1
    return Lines



#----------------------------------Variables -------------------------------------------------------#
extra_solutions = False 
flagDeg = False
if sys.argv[1] == "-h":
    print(" El archivo de código fuente a ejecutarse debe llamarse simplex.py, ejecutando de la forma:\n"+"python simplex.py [-h] archivo.txt")
    Lines = open_file(sys.argv[2])
    out = open("out_"+sys.argv[2], 'w')
else:
    Lines = open_file(sys.argv[1])
    out = open("out_"+sys.argv[1], 'w')
method = Lines[0][0]
optimization = Lines[0][1]
bVariables = Lines[0][2]
restrictions = int(Lines[0][3])
matrix = []
degenerada = 0
divisions = []
dVariables = 0
aVariables = 0   

#---------------------------------- Create Initial Matrix -------------------------------------------------------#
'''
It's simply a function meant to return a list of zeros to add to the matrix.
'''

def zerolistmaker(n): 
    return [0] * n


'''
This functions does the work of adding the aditional variables needed in the different posible cases.
'''
def count_variables():
    global dVariables, aVariables, bVariables
    i = 2
    for i in range(2,len(Lines)):
        if Lines[i][bVariables] == "<=":
            dVariables+=1
        elif Lines[i][bVariables] == ">=":
             dVariables+=1
             aVariables+=1
        else:
            aVariables+=1
'''
This function is used to add the letters that represent the vraibles in the matrix, it's mainly
meant for esthetic.
''' 
def prepare_matrix():
    global dVariables, bVariables, aVariables
    temp = ["VB"]
    count_variables()   
    lenght = dVariables+aVariables+bVariables
    count = 1 
    while(count<lenght+1):
        if count>(bVariables+dVariables):
            temp.append("r"+str(count-(dVariables+bVariables)))
            
        elif count>bVariables:
                temp.append("s"+str(count-bVariables)) 
        else:
            temp.append("x"+str(count))
        count+=1
    temp.append("LD")
    matrix.append(temp)
    len_matrix = restrictions+1
    for i in range(len_matrix):
        temp = zerolistmaker(lenght+2)
        matrix.append(temp)
'''
This function is used to do as it names suggest, it creates the initial matrix from the lines
it reads from the file, it checks the method for the special case scenarios on the first line,
and if not it simply places tha values in its respective spots in the matrix.
'''
def create_initial_matrix():
    global dVariables, bVariables
    prepare_matrix()
    countD = bVariables+1
    countA = bVariables+dVariables+1
    matrix[1][0] = "U"
    i = 1
    while(i<len(Lines)):
        j = 0
        while(j<len(Lines[i])):
              if i == 1 and aVariables>0 and method == 1:
                  matrix[i][j+1] = float(Lines[i][j])
                  k = countA
                  while(k<len(matrix[1])-1):
                        if optimization == "max":
                            matrix[1][k] = -1000
                        else:
                            matrix[1][k] = 1000
                        k+=1
              elif i == 1 and aVariables>0 and method == 2: 
                  matrix[i][j+1] = float(Lines[i][j])
                  k = 1
                  while(k<len(matrix[1])-1):
                        if(k < bVariables + dVariables + 1):
                            matrix[1][k] = 0
                        else:
                            matrix[1][k] = -1
                        k+=1
              elif i == 1:
                  matrix[i][j+1] = -1*float(Lines[i][j])
              elif Lines[i][j] == "<=":
                  matrix[i][0] = matrix[0][countD]
                  matrix[i][countD] = 1
                  countD+=1
              elif Lines[i][j] == ">=":
                  matrix[i][0] = matrix[0][countA]
                  matrix[i][countD] = -1
                  countD+=1
                  matrix[i][countA] = 1
                  countA+=1
              elif Lines[i][j] == "=":
                  matrix[i][0] = matrix[0][countA]
                  matrix[i][countA] = 1
                  countA+=1
              elif j == len(Lines[i])-1 and i != 1:
                 matrix[i][-1] = float(Lines[i][j])
              else:
                 matrix[i][j+1] = float(Lines[i][j])
              j+=1
        i+=1



    
#----------------------------------Simplex Method-------------------------------------------------------#

'''
Function that initializes the everything needed in order to start the simplex method
'''
def initialize_simplex():
    #Prints the initial matrix
    out.write(""+"\n")
    out.write("Matriz Inicial"+"\n")
    print("")
    print("Matriz Inicial")
    out.write(matrix_to_string()+"\n")
    print(matrix_to_string())
    simplex_method(1)
    

'''
Function that unifies every simplex method steps
'''
def simplex_method(iteration):
    
    mnv = determine_minimum_negative_variable()
    
    #When there is no negative variables, the simplex method ends
    if mnv[0] == None:
        check_extra_solution()
        print_solution()
        return 0
        
    else:
        restriction = determine_restriction(mnv[2],iteration)
        #When there is no elegible restriction, means that there is no solution with simplex
        if restriction[0] == None:
            out.write("El problema no está acotado"+"\n")
            print("El problema no está acotado")
            out.write(str(mnv[0]) + " puede crecer tanto como quiera"+"\n")
            print(str(mnv[0]) + " puede crecer tanto como quiera")
        else:
            #Prints the current iteration and graphs the current state of the matrix
            out.write(""+"\n")
            out.write("Iteración " + str(iteration)+"\n")
            out.write("Variable básica que entra: " + mnv[0]+"\n")
            out.write("Variable básica que sale: " + restriction[0]+"\n")
            out.write("Pivote: " + str(matrix[restriction[2]][mnv[2]])+"\n")
                            
            print("")
            print("Iteración " + str(iteration))
            print("Variable básica que entra: " + mnv[0])
            print("Variable básica que sale: " + restriction[0])
            print("Pivote: " + str(matrix[restriction[2]][mnv[2]]))
            
            matrix[restriction[2]][0] = mnv[0]
            row_operations(mnv[2],restriction[2])
            print("")
            out.write(""+"\n")
            out.write(matrix_to_string()+"\n")
            print(matrix_to_string())
            
            
            return simplex_method(iteration + 1)


'''
Function that determines the minimum negative value of a variable of the matrix.
'''
def determine_minimum_negative_variable():
    answer = [None,0,0] #The answer has the form [variable,value,number of column]
    var_amount = len(matrix[0]) -1 #Gets the amount of variables in the matrix
    i = 1
    
    #Checks every variable to see which one is the minimun negative
    while i < var_amount:
        if matrix[1][i] <= answer[1] and matrix[1][i] != 0:
            answer = [matrix[0][i],matrix[1][i],i]
        i = i + 1
    
    return answer
    
'''
Function that determines the restriction selected according to the minimum negative variable (mnv)
'''
def determine_restriction(mnv,iteration):
    global flagDeg
    divisions = []
    answer = [None,0,0] #The answer has the form [restriction,division with the mnv result,number of row]
    restriction_amount = len(matrix) #Gets the amount of restrictions in the matrix
    i = 1
    #Checks every restriction to see which one divided by de mnv gives the lowest result
    while i < restriction_amount:
        #Checks that the mnv in this row is bigger than 0 (to avoid division by 0)
        if matrix[i][mnv] > 0 and matrix[i][-1] >= 0:
            division_result = matrix[i][-1]/matrix[i][mnv]
            divisions.append(matrix[i][-1]/matrix[i][mnv])
            #If is the first division, just put it as a partial answer
            if answer[0] == None:
                answer = [matrix[i][0],division_result,i]
            
            else:
                #Checks if the current division is lower than the current answer
                if division_result < answer[1]:
                    answer = [matrix[i][0],division_result,i]
        
        i = i + 1
    if divisions!=[] and divisions.count(min(divisions))>1  :
        flagDeg = True
        degenerada = iteration
    return answer

'''
This function is used to apply the necesary operations on the matrix for the current iteration.
'''
def row_operations(mnv,restriction):
    out.write("Operaciones fila realizadas:"+"\n")
    print("Operaciones fila realizadas:")
    row_amount = len(matrix)
    column_amount = len(matrix[0])
    #Calculates the inverse multiplicative of the mnv value in the choosen restriction in order to multiply them and make sure the result is 1
    inverse_multiplicative = 1/matrix[restriction][mnv]
    j = 1
    out.write("f" + str(restriction - 1) + " * " + str(inverse_multiplicative) + " -> f" + str(restriction - 1)+"\n")
    print("f" + str(restriction - 1) + " * " + str(inverse_multiplicative) + " -> f" + str(restriction - 1))
    
    #Multiplies the choosen restriction row by the inverse multiplicative
    while j < column_amount:
        matrix[restriction][j] = matrix[restriction][j] * inverse_multiplicative
        j = j + 1

    i = 1
    
    #Goes trough the matrix, making the mnv column 0 (Except the choosen restriction)
    while i < row_amount:
        
        if i != restriction:
            j = 1
            multiplier = - matrix[i][mnv]
            if multiplier != 0:
                out.write(str(multiplier) + "f" + str(restriction - 1) + " + f" + str(i - 1) + " -> f" + str(i - 1)+"\n")
                print(str(multiplier) + "f" + str(restriction - 1) + " + f" + str(i - 1) + " -> f" + str(i - 1))
            while j < column_amount:
                matrix[i][j] = round(matrix[restriction][j] * multiplier + matrix[i][j], 2)
                j = j + 1
                
        i = i + 1


'''
Function that returns a string with a matrix in form of a table.
'''
def matrix_to_string():
    answer = ""
    
    for line in matrix:
        
        for word in line:
            word_len = len(str(word))
            if word_len > 6:
                word_len = 6
            answer = answer + ('%.6s' % str(word))
            blank_spaces = 8 - word_len
            answer = answer + (" " * blank_spaces)
        answer = answer + "\n"
        
    return answer
    
    
'''
Function that prints the final solution of the matrix, it also checks if the answer is degenerate
and does some simple final changes.
'''
def print_solution():
    if flagDeg:
        out.write(""+"\n")
        print("")
        out.write("Solución Degenerada"+"\n")
        print("Solución Degenerada")
    if extra_solutions:
        out.write(""+"\n")
        print("")
        out.write("Solución Multiple"+"\n")
        print("Solución Multiple")
    if  not extra_solutions and not flagDeg:
        print("")
        out.write(""+"\n")
        out.write("Solución"+"\n")
        print("Solución")
    print("")
    out.write(""+"\n")
    out.write("Valor de las variables:"+"\n")
    print("Valor de las variables:")
    answer = {}
    #Finds every variable
    for column in matrix[0]:
        if column[0] == "x" or column[0] == "s" or column[0] == "r":
            answer[column] = 0
        
    #Finds the value of every value
    for row in matrix[1:]: 
        if row[0][0] in ["x","U","r","s"]:
            answer[row[0]] = row[-1]

    if optimization == "min" and method != 0:
        answer["U"]*=-1
    #Prints every value
    for variable in sorted(answer.keys()):
        out.write(variable + " = " + str(answer[variable])+"\n")
        print(variable + " = " + str(answer[variable]))
    #Prints the optimal value of z
    out.write("Por lo tanto el valor óptimo de U es: "+"\n")
    print("Por lo tanto el valor óptimo de U es: ")
    out.write("U = " + str(answer["U"])+"\n")
    print("U = " + str(answer["U"]))
    if method != 2:
        out.close()
   



#---------------------------------- Big M Method-------------------------------------------------------#

'''
This function is used to find the number 1 in the same column of M to make M 0.
'''
def find_row(column):
    i = 0
    while(i<len(matrix)):
        if matrix[i][column] == 1:
            break
        i+=1
    return i 


'''
This function is used to show the operations for making the Ms 0.
'''
def make_m_zero():
      if optimization == "max":
          j = 1
          while(j<len(matrix[1])):
              matrix[1][j]*=-1
              j+=1
      out.write(""+"\n")
      out.write(matrix_to_string()+"\n")
      print("")
      print(matrix_to_string())
      countA = bVariables+dVariables+1
      while(countA<len(matrix[0])-1):
            row = find_row(countA)
            multiplier = -matrix[1][countA]
            i = 1
            while(i < len(matrix[0])):
                matrix[1][i] = matrix[row][i] * multiplier + matrix[1][i]
                i = i + 1
            out.write(""+"\n")
            out.write(matrix_to_string()+"\n")
            out.write(str(multiplier) + "f" + str(row) + " + f" + str(0) + " -> f" + str(0)+"\n")
            print("")
            print(matrix_to_string())
            print(str(multiplier) + "f" + str(row) + " + f" + str(0) + " -> f" + str(0))
            countA+=1
      initialize_simplex()
      
            
    
    
#---------------------------------- two-phase method -------------------------------------------------------#
'''
This function is used to work over the first phase of the two-phase-method, it fixes the first
row turning to zero the necesary values and then applies simpex and checks the final result
of the phase to check if it can continue or not to the second phase.
'''
def double_phase_method_first_phase():
    global dVariables
    make_r_zero()
    j = 1
    while(j<len(matrix[1])):
        matrix[1][j]*=-1
        j+=1
    initialize_simplex()
    if matrix[1][-1] == 0:
              double_phase_method_second_phase()
    else:
              out.write("No es posible solucionar este problema.")
              print("No es posible solucionar este problema.")
    

'''
This function is used to find the artificial variables and add the rows in which they are in to
the first row of the answer, this is necesary for the second phase of the two-phase-method.
'''
def make_r_zero():
    i = 2
    while(i < len(matrix)):
        if(matrix[i][0][0] == 'r'):
            j = 1
            while(j < len(matrix[0])):
                  matrix[1][j] = matrix[1][j] + matrix[i][j]
                  j += 1
        i += 1

'''
This function is used to work over the second phase of the two-phase-method, it transforms the
matrix by eliminating the artifial variables and putting the original first line in the matrix.
Later it looks for the values it has to turn to zero and applies simplex to obtain the final
answer.
'''
def double_phase_method_second_phase():
    global dVariables, bVariables
    i = 0
    while(i < len(matrix)):
        j = 0
        while(j < dVariables):
            matrix[i].pop(bVariables + dVariables + 1)
            j += 1
        i += 1

    i = 1
    while(i <= bVariables):
        matrix[1][i] = -1*float(Lines[1][i-1])
        i += 1

    i = 2
    while(i < len(matrix)):
        j = 1
        multiplier = abs(matrix[1][matrix[i].index(1)])
        while(j < len(matrix[1])):
            matrix[1][j] = round(round(matrix[i][j] * multiplier, 2) + matrix[1][j], 2)
            j += 1
        i += 1
    j = 1
    while(j<len(matrix[1])):
        matrix[1][j]*=-1
        j+=1
    #print(matrix_to_string())
    initialize_simplex()



#---------------------------------- Extra Solution -------------------------------------------------------#
'''
This function is used to check if there is a 0 in the artificial variables or in the slack variables.
'''
def check_extra_solution():
    global extra_solutions
    for i in range(bVariables+1,len(matrix[1])):
                   if matrix[1][i] == 0:
                       extra_solutions = True 
#---------------------------------- Main -------------------------------------------------------#



if method == 0:
    create_initial_matrix()
    initialize_simplex()
elif method == 1:
    create_initial_matrix()
    make_m_zero()
else:
    create_initial_matrix()
    double_phase_method_first_phase()



