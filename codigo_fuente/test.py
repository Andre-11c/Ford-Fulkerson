import json
import networkx as nx
import tkinter as tk
from tkinter import filedialog, messagebox

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def create_graph(data):
    G = nx.DiGraph()
    for node in data["nodes"]:
        G.add_node(node["id"])
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"], capacity=edge["weight"])
    return G

def ford_fulkerson_max_flow(G, source, target):
    flow_value, flow_dict = nx.maximum_flow(G, source, target)
    return flow_value, flow_dict

def save_max_flow_to_json(data, flow_dict, output_path):
    nodes = data["nodes"]
    edges = []
    for u in flow_dict:
        for v in flow_dict[u]:
            if flow_dict[u][v] > 0:  # Only include edges with flow > 0
                edges.append({"source": u, "target": v, "weight": flow_dict[u][v]})
    
    result = {
        "nodes": nodes,
        "edges": edges
    }
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)

def main(input_file, output_file, source, target):
    data = load_graph_from_json(input_file)
    G = create_graph(data)
    flow_value, flow_dict = ford_fulkerson_max_flow(G, source, target)
    save_max_flow_to_json(data, flow_dict, output_file)
    messagebox.showinfo("Resultado", f"Valor máximo del flujo: {flow_value}")

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    entry_input_file.delete(0, tk.END)
    entry_input_file.insert(0, file_path)

def save_file_dialog():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    entry_output_file.delete(0, tk.END)
    entry_output_file.insert(0, file_path)

def run_algorithm():
    input_file = entry_input_file.get()
    output_file = entry_output_file.get()
    source = int(entry_source.get())
    target = int(entry_target.get())
    main(input_file, output_file, source, target)

# Crear la ventana principal
root = tk.Tk()
root.title("Flujo Máximo - Ford-Fulkerson")

# Etiquetas y entradas para los archivos y nodos
tk.Label(root, text="Archivo JSON de entrada:").grid(row=0, column=0, padx=10, pady=10)
entry_input_file = tk.Entry(root, width=50)
entry_input_file.grid(row=0, column=1, padx=10, pady=10)
btn_browse_input = tk.Button(root, text="Examinar...", command=open_file_dialog)
btn_browse_input.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Archivo JSON de salida:").grid(row=1, column=0, padx=10, pady=10)
entry_output_file = tk.Entry(root, width=50)
entry_output_file.grid(row=1, column=1, padx=10, pady=10)
btn_save_output = tk.Button(root, text="Guardar como...", command=save_file_dialog)
btn_save_output.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Nodo fuente:").grid(row=2, column=0, padx=10, pady=10)
entry_source = tk.Entry(root)
entry_source.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Nodo sumidero:").grid(row=3, column=0, padx=10, pady=10)
entry_target = tk.Entry(root)
entry_target.grid(row=3, column=1, padx=10, pady=10)

# Botón para ejecutar el algoritmo
btn_run = tk.Button(root, text="Ejecutar", command=run_algorithm)
btn_run.grid(row=4, column=1, padx=10, pady=20)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()