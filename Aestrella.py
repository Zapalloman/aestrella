# -*- coding: utf-8 -*-
"""
Torres de Hanoi - Algoritmo A*
Implementación del juego Torres de Hanoi usando búsqueda informada con heurística
"""

from copy import deepcopy
from heapq import heappush, heappop

class nodo:
    def __init__(self, torres, padre, costo, num_discos=3):
        """
        Torres: lista de 3 listas, cada una representa una torre
        cada torre contiene los discos ordenados de mayor a menor y de abajo hacia arriba
        """
        self.torres = deepcopy(torres)
        self.padre = padre
        self.costo = costo
        self.num_discos = num_discos
        self.f = self.costo + self.heuristica()

    def __lt__(self, otroNodo):
        return self.f < otroNodo.f

    def __str__(self):
        """Representacion de las torres"""
        resultado = "Torres de Hanoi:\n"
        for i, torre in enumerate(self.torres):
            resultado += f"Torre {i+1}: {torre if torre else '[]'}\n"
        return resultado

    def __eq__(self, otroNodo):
        return self.torres == otroNodo.torres

    def __hash__(self):
        return hash(str(self.torres))

    def heuristica(self):
        """
        Heuristica: Suma de discos que no están en la torre objetivo (torre 3)
        + penalización por discos mal ordenados en la torre objetivo
        """
        objetivo_torre = 2  # Torre 3 (índice 2)
        h = 0
        
        # Contar discos que no están en la torre objetivo, la torre 3
        total_discos_objetivo = len(self.torres[objetivo_torre])
        discos_faltantes = self.num_discos - total_discos_objetivo
        h += discos_faltantes

        # Penalizar si los discos en la torre objetivo no están en el orden correcto
        torre_objetivo = self.torres[objetivo_torre]
        for i in range(len(torre_objetivo) - 1):
            if torre_objetivo[i] < torre_objetivo[i + 1]:  # Debe estar ordenado de mayor a menor
                h += 1
                
        return h

    def es_movimiento_valido(self, torre_origen, torre_destino):
        """Verifica si un movimiento es válido según las reglas de Hanoi"""
        if not self.torres[torre_origen]:  # Torre origen vacía
            return False
        if not self.torres[torre_destino]:  # Torre destino vacía
            return True
        # El disco superior de origen debe ser menor que el superior de destino, grande abajo chico arriba
        return self.torres[torre_origen][-1] < self.torres[torre_destino][-1]

    def aplicaRegla(self, regla):
        """
        Aplica un movimiento específico:
        regla 1: Torre 1 -> Torre 2
        regla 2: Torre 1 -> Torre 3  
        regla 3: Torre 2 -> Torre 1
        regla 4: Torre 2 -> Torre 3
        regla 5: Torre 3 -> Torre 1
        regla 6: Torre 3 -> Torre 2
        """
        movimientos = {
            1: (0, 1),  # Torre 1 -> Torre 2
            2: (0, 2),  # Torre 1 -> Torre 3
            3: (1, 0),  # Torre 2 -> Torre 1
            4: (1, 2),  # Torre 2 -> Torre 3
            5: (2, 0),  # Torre 3 -> Torre 1
            6: (2, 1)   # Torre 3 -> Torre 2
        }
        
        if regla not in movimientos:
            return None
            
        origen, destino = movimientos[regla]
        
        if not self.es_movimiento_valido(origen, destino):
            return None
            
        # Crear nuevo estado
        nuevas_torres = deepcopy(self.torres)
        disco = nuevas_torres[origen].pop()  # Quitar disco de torre origen
        nuevas_torres[destino].append(disco)  # Añadir disco a torre destino
        
        return nodo(nuevas_torres, self, self.costo + 1, self.num_discos)

    def esMeta(self):
        """El estado meta es tener todos los discos en la torre 3 (índice 2)"""
        return (len(self.torres[2]) == self.num_discos and 
                len(self.torres[0]) == 0 and 
                len(self.torres[1]) == 0)

    def sucesores(self, ABIERTOS, CERRADOS):
        """Genera todos los sucesores válidos"""
        listaSucesores = []
        for regla in range(1, 7): 
            sucesor = self.aplicaRegla(regla)
            if sucesor is not None and sucesor not in ABIERTOS and sucesor not in CERRADOS:
                listaSucesores.append(sucesor)
        return listaSucesores

# ------------fin clase nodo ------------------------

def ingresaLista(lista, nodo):
    heappush(lista, nodo)
    return lista

def Solucion(nodo, inicial):
    solucion = []
    while nodo is not inicial:
        solucion = [str(nodo)] + solucion
        nodo = nodo.padre
    return [str(inicial)] + solucion

def Aestrella(nodoInicial):
    ABIERTOS = []
    heappush(ABIERTOS, nodoInicial)
    CERRADOS = []
    éxito = False
    fracaso = False
    cont = 0
    MAX = 10000  # Límite aumentado para Torres de Hanoi
    
    while not éxito and not fracaso and cont <= MAX:
        if not ABIERTOS:
            fracaso = True
            break
            
        nodoActual = heappop(ABIERTOS)
        CERRADOS.append(nodoActual)

        if nodoActual.esMeta():
            éxito = True
        else:
            listaSucesores = nodoActual.sucesores(ABIERTOS, CERRADOS)
            for nodo in listaSucesores:
                heappush(ABIERTOS, nodo)
        cont += 1
        
    if éxito:
        return Solucion(nodoActual, nodoInicial), cont
    else:
        return None, cont

#---- BLOQUE PRINCIPAL:

def main():
    # Estados iniciales para hacer pruebas:
    estados_disponibles = [
        {
            "nombre": "Estado 1 - Estándar",
            "torres": [[3, 2, 1], [], []]
        },
        {
            "nombre": "Estado 2 - Un paso avanzado", 
            "torres": [[3, 2], [1], []]
        },
        {
            "nombre": "Estado 3 - Configuración intermedia",
            "torres": [[3], [2, 1], []]
        },
        {
            "nombre": "Estado 4 - Casi completo",
            "torres": [[1], [], [3, 2]]
        },
        {
            "nombre": "Estado 5 - Configuración compleja",
            "torres": [[], [3, 2, 1], []]
        }
    ]
    
    # Elegir entre un indice entre 0-4 para probar los estados iniciales
    estado_elegido = 0
    
    torres_iniciales = estados_disponibles[estado_elegido]["torres"]
    nombre_estado = estados_disponibles[estado_elegido]["nombre"]
    
    inicial = nodo(torres_iniciales, None, 0, num_discos=3)
    
    print("=== TORRES DE HANOI CON A* ===")
    print(f"Probando: {nombre_estado}")
    print("Estado inicial:")
    print(inicial) #ver*
    print("Estado objetivo: Todos los discos en Torre 3")
    print("\nEjecutando A*...")
    
    respuesta, nodosRevisados = Aestrella(inicial)
    
    if respuesta is None:
        print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
        print("No se encontró solución")
    else:
        print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
        print(f"Pasos de la solución: {len(respuesta)-1}")
        print("\nSolución paso a paso:")
        for i, paso in enumerate(respuesta):
            print(f"\n--- Paso {i} ---")
            print(paso)

if __name__ == "__main__":
    main()