import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg

# Función para cargar el grafo desde un archivo JSON
def cargar_grafo_desde_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    G = nx.DiGraph()
    
    # Agregar nodos
    for node in data['nodes']:
        G.add_node(node['id'])
    
    # Agregar aristas con pesos
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    return G

# Ruta del archivo JSON
file_path = '/home/andre/Documents/TF_CHIPANA_DELASCASAS/grafo.json'

# Cargar el grafo
G = cargar_grafo_desde_json(file_path)

# Posiciones de los nodos para el gráfico
pos = nx.spring_layout(G)

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(8, 6))

# Inicializar listas para nodos y aristas
nodos_dibujados = []
aristas_dibujadas = []
etiquetas_aristas = nx.get_edge_attributes(G, 'weight')

def init():
    """Inicializar la animación con un grafo vacío."""
    ax.clear()
    ax.set_facecolor('black')

    nx.draw(G, pos, ax=ax, with_labels=True, node_color='blue', node_size=2000, font_size=16, font_weight='bold', edge_color='green', alpha=0)
    return ax,

def update(frame):
    """Actualizar la animación agregando nodos y aristas secuencialmente."""
    ax.clear()
    plt.title('Animación del sistema de tuberia ')
    num_nodos = len(G.nodes)
    num_aristas = len(G.edges)
    
    if frame < num_nodos:
        nodos_a_mostrar = list(G.nodes)[:frame+1]
        aristas_a_mostrar = [edge for i, edge in enumerate(G.edges) if i < frame]
    else:
        nodos_a_mostrar = list(G.nodes)
        aristas_a_mostrar = [edge for i, edge in enumerate(G.edges) if i < frame - num_nodos + 1]
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, nodelist=nodos_a_mostrar, node_color='blue', node_size=2000, ax=ax)
    
    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, edgelist=aristas_a_mostrar, edge_color='green', ax=ax)
    
    # Dibujar etiquetas de los nodos
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=16, font_weight='bold')
    
    # Dibujar etiquetas de las aristas
    edge_labels = {edge: etiquetas_aristas[edge] for edge in aristas_a_mostrar}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=12, ax=ax)
    
    return ax,

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=len(G.nodes) + len(G.edges), init_func=init, blit=False, interval=1000, repeat=True)



# Mostrar la animación
plt.title('Animación del sistema de tuberia ')
plt.show()

