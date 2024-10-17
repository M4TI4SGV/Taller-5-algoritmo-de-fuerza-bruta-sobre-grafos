import itertools
import random

# Generación de grafos aleatorios con las caracteristicas dadas en el enuciado del taller
def generar_grafo_aleatorio(num_vertices, prob_arista=0.5, peso_max=10):
    grafo = {}
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j and random.random() < prob_arista:
                grafo[(i, j)] = random.randint(1, peso_max)
    return grafo

# Implementación del algoritmo de Floyd-Warshall
def floyd_warshall(grafo, num_vertices):
    dist = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        dist[i][i] = 0
    for (u, v), peso in grafo.items():
        dist[u][v] = peso
    
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist

# Obtener el camino más largo entre los más cortos
def obtener_camino_mas_largo(distancias):
    max_dist = 0
    camino = (-1, -1)
    num_vertices = len(distancias)
    for i in range(num_vertices):
        for j in range(num_vertices):
            if distancias[i][j] != float('inf') and distancias[i][j] > max_dist:
                max_dist = distancias[i][j]
                camino = (i, j)
    return camino

# Verifica si una permutación es un camino válido en el grafo
def es_camino_valido(perm, grafo):
    for i in range(len(perm) - 1):
        if (perm[i], perm[i+1]) not in grafo:
            return False
    return True

# Algoritmo de fuerza bruta para calcular todos los caminos posibles y válidos
def calcular_caminos_fuerza_bruta(grafo, inicio, fin, num_vertices):
    vertices = list(range(num_vertices))
    todos_caminos = []
    for perm in itertools.permutations(vertices):
        if perm[0] == inicio and perm[-1] == fin and es_camino_valido(perm, grafo):
            todos_caminos.append(perm)
    return todos_caminos

# Comparar si el camino más corto es el mismo en ambos enfoques
def comparar_caminos(distancias_floyd, caminos_fuerza_bruta, grafo):
    camino_min_fuerza_bruta = min(caminos_fuerza_bruta, key=lambda camino: sum(grafo[(camino[i], camino[i+1])] for i in range(len(camino)-1)))
    camino_min_floyd = obtener_camino_mas_largo(distancias_floyd)
    return camino_min_fuerza_bruta, camino_min_floyd


def ejecutar_y_guardar_resultados_txt(num_grafos=50):
    with open("resultados_floydwarshall_vs_fuerza_bruta.txt", mode='w') as file:
        for i in range(num_grafos):
            num_vertices = random.randint(5, 10)
            grafo = generar_grafo_aleatorio(num_vertices)
            distancias = floyd_warshall(grafo, num_vertices)
            inicio, fin = obtener_camino_mas_largo(distancias)
            caminos = calcular_caminos_fuerza_bruta(grafo, inicio, fin, num_vertices)
            
            if caminos:
                camino_fuerza_bruta, camino_floyd = comparar_caminos(distancias, caminos, grafo)
                file.write(f"Grafo {i+1}:\n")
                file.write(f"Camino más corto (Floyd-Warshall): {camino_floyd}\n")
                file.write(f"Camino más corto (Fuerza Bruta): {camino_fuerza_bruta}\n")
                file.write("\n")
            else:
                file.write(f"Grafo {i+1}:\n")
                file.write(f"No se encontraron caminos válidos entre {inicio} y {fin}\n")
                file.write("\n")

ejecutar_y_guardar_resultados_txt()
