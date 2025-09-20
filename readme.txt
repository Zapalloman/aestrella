Integrantes:
- Javier Farías (NRC: 8062)
- Uriel Navarrete (NRC: 8062)

Nombre del Juego: Torres de Hanoi

Enlace a algún sitio para poder comprender en qué consiste la versión del juego que consideraste:
https://es.wikipedia.org/wiki/Torres_de_Hanoi
https://www.mathsisfun.com/games/towerofhanoi.html

Heurística implementada:
La heurística utilizada en el algoritmo A* combina dos factores:
1. Número de discos que no están en la torre objetivo (Torre 3)
2. Penalización por discos mal ordenados en la torre objetivo
Esta heurística es admisible ya que nunca sobreestima el costo real para llegar al estado meta, 
garantizando que A* encuentre la solución óptima.

Estado inicial 1: [[3, 2, 1], [], []] - Configuración estándar
N° nodos revisados A*: 18
N° nodos revisados BFS: 25

Estado inicial 2: [[3, 2], [1], []] - Un paso avanzado
N° nodos revisados A*: 18
N° nodos revisados BFS: 26

Estado inicial 3: [[3], [2, 1], []] - Configuración intermedia
N° nodos revisados A*: 10
N° nodos revisados BFS: 16

Estado inicial 4: [[1], [], [3, 2]] - Casi completo
N° nodos revisados A*: 2
N° nodos revisados BFS: 3

Estado inicial 5: [[], [3, 2, 1], []] - Configuración compleja
N° nodos revisados A*: 18
N° nodos revisados BFS: 25