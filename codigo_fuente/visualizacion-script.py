import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Función para cargar un grafo desde un archivo JSON
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

# Rutas de los archivos JSON para los tres grafos
file_path_1 = '/home/andre/Documents/TF_CHIPANA_DELASCASAS/dataset/dataset.json'
file_path_2 = '/home/andre/Documents/TF_CHIPANA_DELASCASAS/max_flow_output.json'
file_path_3 = '/home/andre/Documents/TF_CHIPANA_DELASCASAS/redundant_output.json'

# Cargar los tres grafos
G1 = cargar_grafo_desde_json(file_path_1)
G2 = cargar_grafo_desde_json(file_path_2)
G3 = cargar_grafo_desde_json(file_path_3)

# Posiciones de los nodos para los gráficos
pos1 = nx.spring_layout(G1, scale=2)  # Escalar el layout para separar los nodos más
pos2 = nx.spring_layout(G2, scale=2)
pos3 = nx.spring_layout(G3, scale=2)

# Crear la figura y los ejes con una cuadrícula de 1x3
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Inicializar listas para nodos y aristas
nodos_dibujados = []
aristas_dibujadas = []
etiquetas_aristas1 = nx.get_edge_attributes(G1, 'weight')
etiquetas_aristas2 = nx.get_edge_attributes(G2, 'weight')
etiquetas_aristas3 = nx.get_edge_attributes(G3, 'weight')

def init():
    """Inicializar la animación con los grafos vacíos."""
    ax1.clear()
    ax2.clear()
    ax3.clear()
    return ax1, ax2, ax3,

def update(frame):
    """Actualizar la animación agregando nodos y aristas de los tres grafos secuencialmente."""
    ax1.clear()
    ax2.clear()
    ax3.clear()
    
    num_nodos1 = len(G1.nodes)
    num_aristas1 = len(G1.edges)
    num_nodos2 = len(G2.nodes)
    num_aristas2 = len(G2.edges)
    num_nodos3 = len(G3.nodes)
    num_aristas3 = len(G3.edges)
    
    if frame < num_nodos1:
        nodos_a_mostrar1 = list(G1.nodes)[:frame+1]
        aristas_a_mostrar1 = [edge for i, edge in enumerate(G1.edges) if i < frame]
    else:
        nodos_a_mostrar1 = list(G1.nodes)
        aristas_a_mostrar1 = [edge for i, edge in enumerate(G1.edges) if i < frame - num_nodos1 + 1]
    
    if frame < num_nodos2:
        nodos_a_mostrar2 = list(G2.nodes)[:frame+1]
        aristas_a_mostrar2 = [edge for i, edge in enumerate(G2.edges) if i < frame]
    else:
        nodos_a_mostrar2 = list(G2.nodes)
        aristas_a_mostrar2 = [edge for i, edge in enumerate(G2.edges) if i < frame - num_nodos2 + 1]

    if frame < num_nodos3:
        nodos_a_mostrar3 = list(G3.nodes)[:frame+1]
        aristas_a_mostrar3 = [edge for i, edge in enumerate(G3.edges) if i < frame]
    else:
        nodos_a_mostrar3 = list(G3.nodes)
        aristas_a_mostrar3 = [edge for i, edge in enumerate(G3.edges) if i < frame - num_nodos3 + 1]
    
    # Dibujar nodos y aristas del primer grafo en el primer subplot
    nx.draw_networkx_nodes(G1, pos1, nodelist=nodos_a_mostrar1, node_color='skyblue', node_size=2000, ax=ax1)
    nx.draw_networkx_edges(G1, pos1, edgelist=aristas_a_mostrar1, edge_color='gray', ax=ax1)
    nx.draw_networkx_labels(G1, pos1, ax=ax1, font_size=16, font_weight='bold')
    edge_labels1 = {edge: etiquetas_aristas1[edge] for edge in aristas_a_mostrar1}
    nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1, font_color='red', font_size=12, ax=ax1)
    
    # Dibujar nodos y aristas del segundo grafo en el segundo subplot
    nx.draw_networkx_nodes(G2, pos2, nodelist=nodos_a_mostrar2, node_color='lightgreen', node_size=2000, ax=ax2)
    nx.draw_networkx_edges(G2, pos2, edgelist=aristas_a_mostrar2, edge_color='gray', ax=ax2)
    nx.draw_networkx_labels(G2, pos2, ax=ax2, font_size=16, font_weight='bold')
    edge_labels2 = {edge: etiquetas_aristas2[edge] for edge in aristas_a_mostrar2}
    nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_color='blue', font_size=12, ax=ax2)

    # Dibujar nodos y aristas del tercer grafo en el tercer subplot
    nx.draw_networkx_nodes(G3, pos3, nodelist=nodos_a_mostrar3, node_color='lightcoral', node_size=2000, ax=ax3)
    nx.draw_networkx_edges(G3, pos3, edgelist=aristas_a_mostrar3, edge_color='gray', ax=ax3)
    nx.draw_networkx_labels(G3, pos3, ax=ax3, font_size=16, font_weight='bold')
    edge_labels3 = {edge: etiquetas_aristas3[edge] for edge in aristas_a_mostrar3}
    nx.draw_networkx_edge_labels(G3, pos3, edge_labels=edge_labels3, font_color='purple', font_size=12, ax=ax3)
    
    # Agregar títulos a cada subplot
    ax1.set_title('Sistema de Tuberías Completo', fontsize=14)
    ax2.set_title('Tuberías a Reforzar', fontsize=14)
    ax3.set_title('Tuberías a Retirar', fontsize=14)
    
    return ax1, ax2, ax3

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=max(len(G1.nodes) + len(G1.edges), len(G2.nodes) + len(G2.edges), len(G3.nodes) + len(G3.edges)),
                              init_func=init, blit=False, interval=1000, repeat=False)

# Mostrar la animación
plt.suptitle('Animación de Tres Grafos Dirigidos con Pesos en Mosaico', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
