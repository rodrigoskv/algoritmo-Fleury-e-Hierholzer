import networkx as nx
import matplotlib.pyplot as plt
import copy

# Create graph and add nodes
G = nx.Graph()

names = ["A", "B", "C", "D", "E", "F"]

for letter in names:
    G.add_node(letter)

# Add edges to create the graph structure
G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("B", "C")
G.add_edge("B", "D")
G.add_edge("C", "D")
G.add_edge("C", "E")
G.add_edge("D", "E")
G.add_edge("D", "F")
G.add_edge("E", "F")

# Display basic graph properties
print("Chain:", list(G.nodes))
print("Path:", list(nx.dfs_edges(G)))

try:
    cycle = nx.find_cycle(G)
    print("Cycle:", cycle)
except nx.NetworkXNoCycle:
    print("Cycle: There is no cycle in the graph")

incidence = nx.incidence_matrix(G).todense()
print("Incidence Matrix:\n", incidence)

print("Graph Order:", G.number_of_nodes())

degrees = dict(G.degree())
print("Vertex Degrees:", degrees)

graph_degree = max(degrees.values())
print("Graph Degree:", graph_degree)

# Eulerian path utility functions
def has_eulerian_path(graph):
    """
    Check if the graph has an Eulerian path.
    Returns True if the graph is connected and has 0 or 2 odd-degree vertices.
    """
    if not nx.is_connected(graph):
        return False
    odd_vertices = [v for v, d in graph.degree() if d % 2 == 1]
    return len(odd_vertices) == 0 or len(odd_vertices) == 2


def is_bridge(graph, u, v):
    """
    Check if the edge (u,v) is a bridge in the graph.
    A bridge is an edge whose removal increases the number of connected components.
    """
    n_components = nx.number_connected_components(graph)
    graph_copy = graph.copy()
    graph_copy.remove_edge(u, v)
    return nx.number_connected_components(graph_copy) > n_components


def fleury(graph):
    """
    Implement Fleury's algorithm to find an Eulerian path or circuit.
    """
    graph_copy = graph.copy()
    odd_vertices = [v for v, d in graph_copy.degree() if d % 2 == 1]
    
    # Select starting vertex: odd degree vertex if available, otherwise any vertex
    if odd_vertices:
        current = odd_vertices[0]
    else:
        current = list(graph_copy.nodes)[0]
    
    path = [current]
    while graph_copy.edges:
        for v in list(graph_copy.neighbors(current)):
            if not is_bridge(graph_copy, current, v) or graph_copy.degree(current) == 1:
                path.append(v)
                graph_copy.remove_edge(current, v)
                if graph_copy.degree(current) == 0:
                    graph_copy.remove_node(current)
                current = v
                break
    
    return path

def hierholzer(graph):
    """
    Implement Hierholzer's algorithm to find an Eulerian path or circuit.
    """
    if not has_eulerian_path(graph):
        return "The graph does not have an Eulerian path."
    graph_copy = graph.copy()
    odd_vertices = [v for v, d in graph_copy.degree() if d % 2 == 1]
    if odd_vertices:
        start = odd_vertices[0]
    else:
        start = list(graph_copy.nodes)[0]
    
    stack = [start]
    current_circuit = []
    
    while stack:
        current = stack[-1] 
        if graph_copy.degree(current) > 0:
            next_vertex = list(graph_copy.neighbors(current))[0]
            graph_copy.remove_edge(current, next_vertex)
            stack.append(next_vertex)
        else:
            current_circuit.append(stack.pop())
    
    final_path = current_circuit[::-1]  # Reverse to get correct order
    return final_path


# Main program execution
print("\n--- Eulerian Path Verification ---")
if has_eulerian_path(G):
    print("The original graph already has an Eulerian path.")
    
    # Apply algorithms to the original graph
    print("\n--- Fleury's Algorithm ---")
    fleury_path = fleury(G)
    print("Eulerian Path (Fleury):", fleury_path)
    
    print("\n--- Hierholzer's Algorithm ---")
    hierholzer_path = hierholzer(G)
    print("Eulerian Path (Hierholzer):", hierholzer_path)
    
    # Visualization
    plt.figure(figsize=(10, 6))
    nx.draw(G, with_labels=True, node_color='lightblue', 
            node_size=500, font_weight='bold')
    plt.title("Graph with Eulerian Path")
    plt.show()