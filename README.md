# TP LU - Métodos Numéricos
UNSAM - 1er Cuatrimestre 2023

## Integrantes
- Tobías Riccone
- Franco Nicotra

## Breve descripción de la solución planteada
Este programa ofrece al usuario obtener, por medio de LU, el vector incógnita dada una matriz y su vector resultado. La dimensión de la matriz cuadrada a calcular va de 1 a 4 inclusive. Al calcular la incógnita se mostraran datos extras sobre la operación realizada, como las operaciones elementales, la cantidad de pasos de eliminación Gaussiana y las matrices L, U e Y.
El programa incluye las validaciones fundamentales como la obligatoriedad de los campos, los tipos de datos aceptados (Enteros y Flotantes, Positivos y Negativos) y si la matriz a descomponer cumple con los requisitos (determinantes de submatrices != 0)

## Aclaraciones extra
Para el desarrollo del programa se utilizaron las librerías Numpy y Tkinter.

El programa solo admite matrices de dimensión de 1 a 4 inclusive debido a la dimensión de la ventana. Esto se puede modificar aumentando la dimensión de la pantalla (línea 157) y actualizando las teclas que admiten los inputs con expresión regular (línea 169). Por fines prácticos se dejó de esta forma.
