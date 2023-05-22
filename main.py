import re
import numpy as np
from tkinter import *

def descomposicionLUCorrecta(a, l, u):
    return np.array_equal(np.matmul(l, u), a)

def validarOperacionLU(matriz, l, u):
    if not descomposicionLUCorrecta(matriz, l, u):
        raise Exception("Se produjo un error al decomponer la matríz")

def descomposicionLU(matriz):
    dim = matriz.shape[0]
    l = np.zeros((dim, dim))
    u = np.copy(matriz)
    pasosL = 0
    pasosU = 0
    for fil in range(dim):
        l[fil, fil] = 1
        for col in range(fil + 1, dim):
            pasosL += 1
            coef = u[col, fil] / u[fil, fil]
            l[col, fil] = coef
            u[col, :] -= coef * u[fil, :]
            pasosU += 1
    validarOperacionLU(matriz, l, u)
    return l, u, pasosL, pasosU

def matrizValidaParaLU(matriz):
    for i in range(len(matriz)):
        submatriz = matriz[0:i + 1, 0:i + 1]
        if np.linalg.det(submatriz) == 0:
            return False
    return True

def validarMatrizIngresada(matriz, alturaCartel):
    if not matrizValidaParaLU(matriz):
        cartelError_MatrizInvalida.place(x=10, y=alturaCartel)
        raise Exception("La matríz no cumple los requisitos para descomponerla en LU")
    else:
        cartelOk_Matriz.place(x=10, y=alturaCartel)

def obtenerMatrizDesdeInputs(listaFilasMatriz, alturaCartel):
    cantFilas = len(listaFilasMatriz)
    cantColumnas = len(listaFilasMatriz[0])
    matriz = np.zeros((cantFilas, cantColumnas))
    i = 0
    j = 0
    for fila in listaFilasMatriz:
        for elemento in fila:
            valorIngresado = elemento.get()
            if valorIngresado == "" or valorIngresado == "-" or valorIngresado.startswith("."):
                cartelError_MatrizIncompleta.place(x=10, y=alturaCartel)
                raise Exception("La matríz ingresada no es válida")
            matriz[i][j] = valorIngresado
            j += 1
        j = 0
        i += 1
    return matriz

def obtenerElementoPorTexto(tipoElemento, texto):
    for widget in root.winfo_children():
        if isinstance(widget, tipoElemento) and widget["text"] == texto:
            return widget
    raise Exception(f"No se encontró el botón {texto}")

def deshabilitarElementosPorListaDeListas(listaDeListasDeElementos):
    for widget in root.winfo_children():
        if isinstance(widget, Entry):
            for lista in listaDeListasDeElementos:
                for elemento in lista:
                    if elemento == widget:
                        widget.config(state=DISABLED)

def imprimirMatriz(matriz, x, y):
    xInicial = x
    for fila in matriz:
        for elemento in fila:
            Label(root, text=int(elemento), font=("Arial", 11)).place(x=x, y=y)
            x += 20
        ultimoX = x
        x = xInicial
        y += 20
    return ultimoX

def verDetalle(l, u, y, pasosL, pasosU, altura):
    obtenerElementoPorTexto(Button, "Más detalles").config(state=DISABLED)
    Label(root, text=f"Se realizaron {pasosL} pasos para L y {pasosU} pasos para U al aplicar la Eliminación Gaussiana",font=("Arial", 11)).place(x=10, y=altura)
    Label(root, text=f"Matríz L - U - Y:", font=("Arial", 11)).place(x=10, y=altura+25)
    ultimoX = imprimirMatriz(l, 10, altura + 50)
    ultimoX = imprimirMatriz(u, ultimoX + 20, altura + 50)
    imprimirMatriz(y, ultimoX + 30, altura + 50)

def mostrarRespuesta(vectorSolucion, alturaCartel):
    dim = int(cajaDimension.get())
    opElementales = int(dim*(dim+1)/2)
    vectorString = ""
    for lista in vectorSolucion:
        for elemento in lista:
            vectorString += f"{int(elemento)}   "
    Label(root, text=f"Vector X obtenido por LU:   {vectorString}", font=("Arial", 11)).place(x=10, y=alturaCartel)
    Label(root, text=f"Se realizaron {opElementales} operaciones elementales para obtener el vector Y, y {opElementales} para obtener el vector X", font=("Arial", 11)).place(x=10, y=alturaCartel+25)
    Label(root, text=f"Se realizo un total de {opElementales*2} operaciones elementales", font=("Arial", 11)).place(x=10, y=alturaCartel + 50)

def calcular(listaFilasMatriz, listaFilasVector, alturaCartel):
    cartelError_MatrizIncompleta.place_forget()
    cartelError_MatrizInvalida.place_forget()
    cartelOk_Matriz.place_forget()
    matrizA = obtenerMatrizDesdeInputs(listaFilasMatriz, alturaCartel)
    vector = obtenerMatrizDesdeInputs(listaFilasVector, alturaCartel)
    validarMatrizIngresada(matrizA, alturaCartel)
    obtenerElementoPorTexto(Button, "Calcular X").config(state=DISABLED)
    deshabilitarElementosPorListaDeListas(listaFilasMatriz)
    deshabilitarElementosPorListaDeListas(listaFilasVector)
    l, u, pasosL, pasosU = descomposicionLU(matrizA)
    y = np.linalg.solve(l, vector)
    vectorSolucion = np.linalg.solve(u, y)
    mostrarRespuesta(vectorSolucion, alturaCartel+30)
    Button(root, text="Más detalles", command=lambda: verDetalle(l, u, y, pasosL, pasosU, alturaCartel+140)).place(x=10, y=alturaCartel+110)

def crearInputsMatriz(filas, columnas, posXInicial, posYInicial):
    listaFilas = []
    x = posXInicial
    y = posYInicial
    for fila in range(filas):
        listaElementos = []
        for columna in range(columnas):
            input = Entry(root, validate="key", validatecommand=(validacionInputs, '%P'))
            input.place(x=x, y=y, width=30, height=25)
            listaElementos.append(input)
            x += 40
        listaFilas.append(listaElementos)
        ultimoX = x
        x = posXInicial
        y += 40
    return listaFilas, ultimoX, y

def ingresarMatrizYVector(dimension):
    cartelError_Dimension.place_forget()
    cajaDimension.config(state=DISABLED)
    botonSiguiente.config(state=DISABLED)
    Label(root, text="Ingrese la Matríz A y su Vector b:", font=("Arial", 11)).place(x=10, y=140)
    listaFilasMatriz, ultimoXUsado, ultimaYUsada = crearInputsMatriz(dimension, dimension, 12, 180)
    listaFilasVector, ultimoXUsado, ultimaYUsada = crearInputsMatriz(dimension, 1, ultimoXUsado + 50, 180)
    botonCalcular = Button(root, text="Calcular X", command=lambda: calcular(listaFilasMatriz, listaFilasVector, ultimaYUsada))
    botonCalcular.place(x=230, y=140)

def validarDimEIngresarMatrizYVector():
    dimensionIngresada = cajaDimension.get()
    if dimensionIngresada != "" and dimensionIngresada != "-" and 5 > int(dimensionIngresada) > 0:
        ingresarMatrizYVector(int(dimensionIngresada))
    else:
        cartelError_Dimension.place(x=10, y=140)
        raise Exception("Dimension inválida, reintente")

def inicio():
    root.geometry("800x600")
    root.resizable(False, False)
    root.title("Método LU")
    Label(root, text="TP LU - Métodos Numéricos", font=("Arial", 16, "bold")).place(x=10, y=10)
    Label(root, text="Grupo 08 conformado por Riccone, Nicotra y Díaz", font=("Arial", 12, "bold")).place(x=10, y=45)
    Label(root, text="------------------------------------", font=("Arial", 11)).place(x=10, y=75)
    Label(root, text="Ingrese la dimensión de la Matriz cuadrada a resolver (1-4):", font=("Arial", 11)).place(x=10, y=105)
    cajaDimension.place(x=405, y=105, width=30, height=25)
    botonSiguiente.place(x=445, y=103)
    root.mainloop()

def teclaValida(input):
    return re.match(r"^(?:-)?\d*(?:\.\d*)?$", input) is not None

root = Tk()
validacionInputs = root.register(teclaValida)
cajaDimension = Entry(root, validate="key", validatecommand=(validacionInputs, '%P'))
botonSiguiente = Button(root, text="Siguiente", command=validarDimEIngresarMatrizYVector)
Button(root, text="Salir", command=root.destroy, bg="red", fg="white").place(x=750, y=10)
cartelError_MatrizInvalida = Label(root, text="La matríz no cumple los requisitos para descomponerla en LU, modifiquela y calcule nuevamente", font=("Arial", 11), fg="red")
cartelError_MatrizIncompleta = Label(root, text="La matríz esta incompleta, modifiquela y calcule nuevamente", font=("Arial", 11), fg="red")
cartelError_Dimension = Label(root, text="Dimension inválida, ingrese una dimension menor a 5", font=("Arial", 11), fg="red")
cartelOk_Matriz = Label(root, text="La matríz cumple los requisitos para descomponerla en LU", font=("Arial", 11), fg="green")
inicio()