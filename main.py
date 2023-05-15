import numpy as np


def descomposicionLUCorrecta(a, l, u):
    return np.array_equal(np.matmul(l, u), a)


def validarOperacionLU(a, l, u):
    if not descomposicionLUCorrecta(a, l, u):
        raise Exception("Se produjo un error al decomponer la matríz")


def descomposicionLU(a):
    dim = a.shape[0]
    l = np.zeros((dim, dim))
    u = np.copy(a)
    for fil in range(dim):
        l[fil, fil] = 1
        for col in range(fil + 1, dim):
            coef = u[col, fil] / u[fil, fil]
            l[col, fil] = coef
            u[col, :] -= coef * u[fil, :]
    validarOperacionLU(a, l, u)
    return l, u


def matrizValidaParaLU(a):
    n = len(a)
    for i in range(n):
        submatriz = a[0:i + 1, 0:i + 1]
        if np.linalg.det(submatriz) == 0:
            return False
    return True


def validarMatrizIngresada(a):
    if not matrizValidaParaLU(a):
        raise Exception("Matríz ingresada inválida")


if __name__ == '__main__':
    print("\nTP LU - Métodos Numéricos"
          "\nGrupo 8 conformado por Tobías Riccone, Franco Nicotra y Facundo Díaz"
          "\nEn este TP vamos a resolver un sistema de ecuaciones utilizando el Método de LU")
    print("\nA continuación se le va a solicitar los parámetros del sistema de ecuaciones")
    dim = int(input("Dimension de la matríz cuadrada: "))
    a = np.zeros((dim, dim))
    vector = np.zeros((dim, 1))
    print("Elementos de la matríz")
    for fil in range(dim):
        for col in range(dim):
            a[fil, col] = float(input(f"Posición {fil + 1}{col + 1}: "))
    validarMatrizIngresada(a)
    print("Elementos del vector")
    for fil in range(dim):
        vector[fil, 0] = float(input(f"Posición {fil + 1}1: "))
    l, u = descomposicionLU(a)
    print(a)
    print(l)
    print(u)
