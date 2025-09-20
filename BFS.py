# -*- coding: utf-8 -*-
"""
Torres de Hanoi - Búsqueda No Informada (BFS, DFS, UCS)
Implementación del juego Torres de Hanoi usando búsquedas no informadas
"""

from copy import deepcopy
from heapq import heappush, heappop

class nodo:
    def __init__(self, torres, padre, costo, num_discos=3):
        """
        torres: lista de 3 listas, cada una representa una torre
        cada torre contiene los discos ordenados de mayor a menor (base a tope)
        """
        self.torres = deepcopy(torres)
        self.padre = padre
        self.costo = costo
        self.num_discos = num_discos

    def __lt__(self, otroNodo):
        return self.costo < otroNodo.costo

    def __str__(self):
        """Representa visualmente las torres"""
        resultado = "Torres de Hanoi:\n"
        for i, torre in enumerate(self.torres):
            resultado += f"Torre {i+1}: {torre if torre else '[]'}\n"
        return resultado

    def __eq__(self, otroNodo):
        return self.torres == otroNodo.torres

    def __hash__(self):
        """Permite usar el nodo en conjuntos y diccionarios"""
        return hash(str(self.torres))

    def es_movimiento_valido(self, torre_origen, torre_destino):
        """Verifica si un movimiento es válido según las reglas de Hanoi"""
        if not self.torres[torre_origen]:  # Torre origen vacía
            return False
        if not self.torres[torre_destino]:  # Torre destino vacía
            return True
        # El disco superior de origen debe ser menor que el superior de destino
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

    def sucesores(self, ABIERTOS, CERRADOS):
        """Genera todos los sucesores válidos"""
        listaSucesores = []
        for regla in range(1, 7):  # 6 posibles movimientos
            sucesor = self.aplicaRegla(regla)
            if sucesor is not None and sucesor not in ABIERTOS and sucesor not in CERRADOS:
                listaSucesores.append(sucesor)
        return listaSucesores

    def esMeta(self):
        """El estado meta es tener todos los discos en la torre 3 (índice 2)"""
        return (len(self.torres[2]) == self.num_discos and 
                len(self.torres[0]) == 0 and 
                len(self.torres[1]) == 0)

# ------------fin clase nodo ------------------------

def ingresaLista(lista, nodo, esquema):
    if esquema == "BFS":
        lista.append(nodo)    #BFS: Ingreso al final
    if esquema == "DFS":
        lista.insert(0, nodo)    #DFS: Ingreso al inicio
    if esquema == "UCS":
        heappush(lista, nodo)
    return lista

def Solucion(nodo, inicial):
    solucion = []
    while nodo is not inicial:
        solucion = [str(nodo)] + solucion
        nodo = nodo.padre
    return [str(inicial)] + solucion

def busquedaNoInformada(nodoInicial, esquema):
    ABIERTOS = [nodoInicial]
    CERRADOS = []
    exito = False
    fracaso = False
    cont = 0
    MAX_NODOS = 15000  # Límite para evitar búsquedas infinitas
    
    while not exito and not fracaso and cont < MAX_NODOS:
        cont += 1
        
        if not ABIERTOS:
            fracaso = True
            break
            
        if esquema == "UCS":
            nodoActual = heappop(ABIERTOS)
        else:
            nodoActual = ABIERTOS.pop(0)

        CERRADOS.append(nodoActual)
        
        if nodoActual.esMeta():
            exito = True
        else:
            listaSucesores = nodoActual.sucesores(ABIERTOS, CERRADOS)
            for nodo in listaSucesores:
                ABIERTOS = ingresaLista(ABIERTOS, nodo, esquema)
                
    if exito:
        return Solucion(nodoActual, nodoInicial), len(CERRADOS)
    else:
        return None, len(CERRADOS)

#---- BLOQUE PRINCIPAL:

def main():
    # ESTADOS INICIALES DISPONIBLES PARA PRUEBAS:
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
    
    # CAMBIAR ESTE ÍNDICE (0-4) PARA PROBAR DIFERENTES ESTADOS INICIALES
    estado_elegido = 0
    
    # Cambiar el esquema por "BFS", "DFS", "UCS"
    esquema = "BFS"
    
    torres_iniciales = estados_disponibles[estado_elegido]["torres"]
    nombre_estado = estados_disponibles[estado_elegido]["nombre"]
    
    inicial = nodo(torres_iniciales, None, 0, num_discos=3)
    
    print(f"=== TORRES DE HANOI CON {esquema} ===")
    print(f"Probando: {nombre_estado}")
    print("Estado inicial:")
    print(inicial)
    print("Estado objetivo: Todos los discos en Torre 3")
    print(f"\nEjecutando {esquema}...")
    
    respuesta, nodosRevisados = busquedaNoInformada(inicial, esquema)
    
    if respuesta is None:
        print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
        print("No se encontró solución (o se alcanzó el límite)")
    else:
        print(f"Cantidad de nodos revisados: {nodosRevisados} nodos")
        print(f"Pasos de la solución: {len(respuesta)-1}")
        print(f"\nSolución encontrada por {esquema}:")
        for i, paso in enumerate(respuesta):
            print(f"\n--- Paso {i} ---")
            print(paso)

if __name__ == "__main__":
    main()