# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 13:47:07 2020

@author: jasso
"""

class Arbol:
    def __init__(self,elemento):
        self.hijos = []
        self.elemento = elemento
    
def agregarElemento(arbol,elemento,elementoPadre):
    subarbol = buscarSubarbol(arbol,elementoPadre);
    subarbol.hijos.append(Arbol(elemento))
    
def buscarSubarbol(arbol,elemento):
    if arbol.elemento == elemento:
        return arbol
    for subarbol in arbol.hijos:
        arbolBuscado = buscarSubarbol(subarbol, elemento)
        if (arbolBuscado != None):
            return arbolBuscado
    return None        
        
abuela = "Jacqueline Gurney"
marge = "Marge Bouvier"
patty = "Patty Bouvier"
selma = "Selma Bouvier"
bart = "Bart Simpson"
lisa = "Lisa Simpson"
maggie = "Maggie Simpson"
ling = "Ling Bouvier"

arbol = Arbol(abuela)
agregarElemento(arbol, patty, abuela)
agregarElemento(arbol, selma, abuela)
agregarElemento(arbol, ling, selma)
agregarElemento(arbol, marge, abuela)
agregarElemento(arbol, bart, marge)
agregarElemento(arbol, lisa, marge)
agregarElemento(arbol, maggie, marge)
        
def ejecutarProfundidadPrimero(arbol,funcion):
    funcion(arbol.elemento)
    for hijo in arbol.hijos:
        ejecutarProfundidadPrimero(hijo,funcion)
       
def printElement(element):
    print(element)

ejecutarProfundidadPrimero(arbol,printElement)        