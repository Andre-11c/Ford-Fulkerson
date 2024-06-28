import json
import networkx as nx

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

def save_max_flow_and_redundant_pipes_to_json(data, flow_dict, max_flow_output_path, redundant_output_path):
    nodes = data["nodes"]
    max_flow_edges = []
    all_edges = {(edge["source"], edge["target"]): edge for edge in data["edges"]}
    redundant_edges = []

    for u in flow_dict:
        for v in flow_dict[u]:
            if flow_dict[u][v] > 0:  # Only include edges with flow > 0
                max_flow_edges.append({"source": u, "target": v, "weight": flow_dict[u][v]})
                if (u, v) in all_edges:
                    del all_edges[(u, v)]

    redundant_edges = [{"source": u, "target": v, "weight": all_edges[(u, v)]["weight"]} for u, v in all_edges]

    max_flow_result = {
        "nodes": nodes,
        "edges": max_flow_edges
    }
    
    redundant_result = {
        "nodes": nodes,
        "edges": redundant_edges,
        "title": "Tuberías a retirar"
    }
    
    with open(max_flow_output_path, 'w') as f:
        json.dump(max_flow_result, f, indent=4)
        
    with open(redundant_output_path, 'w') as f:
        json.dump(redundant_result, f, indent=4)

def main(input_file, max_flow_output_file, redundant_output_file, source, target):
    data = load_graph_from_json(input_file)
    G = create_graph(data)
    flow_value, flow_dict = ford_fulkerson_max_flow(G, source, target)
    save_max_flow_and_redundant_pipes_to_json(data, flow_dict, max_flow_output_file, redundant_output_file)
    print(f"Max flow value: {flow_value}")

if __name__ == "__main__":
    input_file = '/home/andre/Documents/TF_CHIPANA_DELASCASAS/dataset/dataset.json'  # Archivo JSON de entrada
    max_flow_output_file = 'max_flow_output.json'  # Archivo JSON de salida para el flujo máximo
    redundant_output_file = 'redundant_output.json'  # Archivo JSON de salida para las tuberías a retirar
    source = 0  # Nodo fuente
    target = 3  # Nodo sumidero

    main(input_file, max_flow_output_file, redundant_output_file, source, target)
