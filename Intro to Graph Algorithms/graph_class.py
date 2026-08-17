# graph_class.py

class Graph:
    def __init__(self):
        # Dictionary to store Adjacency List: { 'A': ['B', 'C'], 'B': ['A'] }
        self.adj_list = {}
        # List to keep track of nodes to create an ordered Adjacency Matrix
        self.nodes = []

    def add_node(self, node):
        """Adds a new vertex to the graph."""
        if node not in self.adj_list:
            self.adj_list[node] = []
            self.nodes.append(node)

    def add_edge(self, u, v, is_directed=False):
        """Adds an edge between node u and node v."""
        # Ensure both nodes exist in the graph before connecting them
        self.add_node(u)
        self.add_node(v)

        # Add v to u's list
        self.adj_list[u].append(v)
        
        # If undirected, also add u to v's list (two-way street)
        if not is_directed:
            self.adj_list[v].append(u)

    def print_adj_list(self):
        """Prints the Adjacency List representation."""
        print("\n--- Adjacency List ---")
        for node, neighbors in self.adj_list.items():
            print(f"{node} -> {neighbors}")

    def print_adj_matrix(self):
        """Prints the Adjacency Matrix representation."""
        print("\n--- Adjacency Matrix ---")
        size = len(self.nodes)
        
        # Create an empty size x size matrix filled with 0s
        matrix = [[0] * size for _ in range(size)]
        
        # Create a dictionary to map node names to their index in the matrix
        node_to_index = {node: i for i, node in enumerate(self.nodes)}

        # Fill the matrix with 1s where edges exist
        for u, neighbors in self.adj_list.items():
            for v in neighbors:
                row_index = node_to_index[u]
                col_index = node_to_index[v]
                matrix[row_index][col_index] = 1

        # Print the matrix nicely
        # Print column headers
        print("  " + " ".join(str(n) for n in self.nodes))
        
        # Print rows with headers
        for i, row in enumerate(matrix):
            print(f"{self.nodes[i]} {row}")


# ==========================================
# Testing the Graph Class
# ==========================================
if __name__ == "__main__":
    g = Graph()
    
    # Adding edges (nodes will be added automatically)
    # Creating an Undirected Graph
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'D')
    g.add_edge('D', 'E')

    # Print outputs
    g.print_adj_list()
    g.print_adj_matrix()