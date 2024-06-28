import matplotlib.pyplot as plt 
import numpy as np 
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Número de nodos en el grafo
nodos = 4

# Inicializa la matriz de adyacencia con infinito (indica sin conexión)
matriz_adyacencia = np.full((nodos, nodos), np.inf)

# Rellenar la matriz con los pesos de las aristas
# Ejemplo: agregar aristas (0 -> 1, peso 2), (1 -> 2, peso 3), (2 -> 3, peso 4), (3 -> 0, peso 5)
matriz_adyacencia[0, 1] = 2
matriz_adyacencia[1, 2] = 3
matriz_adyacencia[2, 3] = 4
matriz_adyacencia[3, 0] = 5

# Opcional: para no tener pesos infinitos en la diagonal principal (sin bucles), puedes poner ceros
np.fill_diagonal(matriz_adyacencia, 0)

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos
for i in range(nodos):
    G.add_node(i)

# Agregar aristas con pesos
for i in range(nodos):
    for j in range(nodos):
        if matriz_adyacencia[i, j] != np.inf and i != j:
            G.add_edge(i, j, weight=matriz_adyacencia[i, j])

# Posiciones de los nodos para el gráfico
pos = nx.spring_layout(G)

# Dibujar el grafo
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=16, font_weight='bold', edge_color='gray')

# Dibujar etiquetas de los pesos
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', font_size=12)

# Mostrar el gráfico
plt.title('Grafo Dirigido con Pesos')
plt.show()
