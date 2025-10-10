import random 

def generarMapa(): #O(n*m)
    M = []
    for i in range(10):       
        N = []
        for j in range(10):   
            N.append(0)       
        M.append(N)          
    return M

def generarCaminos(M): #O(40)
    for h in range(40):
        i = random.randint(0, 9)  # de 0 a 8
        j = random.randint(0, 9)
        M[i][j] = 1  # marcamos camino con un 1

def mostrarMatriz(M): #O(n)
    for i in range(10):
        print(i, " : ", M[i])  

def empezarJuego(): #O(n*m)
    M = generarMapa()
    generarCaminos(M)
    mostrarMatriz(M)

empezarJuego()
