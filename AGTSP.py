import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageTk, Image

class WelcomeWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.config(background='black')
        self.master.title("Apna Guide Using TSP")
        

        # Load the background image
        self.bg_image = ImageTk.PhotoImage(Image.open("fl.jpg"))
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the widgets
        self.create_widgets()

    def create_widgets(self):
        # Create the label, entry widget, and buttons
        self.label = tk.Label(self.master, text="Welcome to Apna Guide !", font=("Inter", 20))
        self.label.pack(side="bottom", pady=25)

        self.name_label = tk.Label(self.master, text="Please Enter Your Destination :", font=("Inter Bold", 14))
        self.name_label.pack(side="top", pady=15)

        self.name_entry = tk.Entry(self.master, width=30, font=("Arial", 14))
        self.name_entry.pack(side="top", pady=10)

        self.greet_button = tk.Button(self.master, text="Guide", command=self.greet_user, font=("Algerian", 14))
        self.greet_button.pack(side="top", pady=10)

        self.close_button = tk.Button(self.master, text="Show Path", command=self.master.destroy, font=("Algerian", 14))
        self.close_button.pack(side="top", padx=10, pady=10)

    def greet_user(self):
        name = self.name_entry.get()
        if name:
            greeting = f'''Hello From Mumbai To {name} This is The Shortest and Minimum cost path.
*Click On Show Path To View Shortest Path or Enter Another Destination*'''
        else:
            greeting = "Hello! Welcome to my app."
        self.label.config(text=greeting)

# Create a new instance of Tkinter
root = tk.Tk()

# Set the size of the main window and center it on the screen
root.geometry("600x400+400+200")

# Create the welcome window
app = WelcomeWindow(master=root)

# Run the main loop
app.mainloop()

# Create a graph
G = nx.Graph()

# Add nodes with coordinates as attributes
G.add_node('Mumbai', pos=(0, 0),node_color='red')
G.add_node('Pune', pos=(1, 2))
G.add_node('Thane', pos=(3, 1))
G.add_node('Delhi', pos=(2, 3))

# Add edges with weights as attributes
G.add_edge('Mumbai', 'Pune', weight=120)
G.add_edge('Mumbai', 'Thane', weight=15)
G.add_edge('Mumbai', 'Delhi', weight=400)
G.add_edge('Pune', 'Thane', weight=90)
G.add_edge('Pune', 'Delhi', weight=250)
G.add_edge('Thane', 'Delhi', weight=305)

# Draw the graph
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=5000, font_size=15, font_color='white')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)

# Find approximate solution using nearest neighbor heuristic
start_node = 'Mumbai'
path = [start_node]
visited = {node: False for node in G.nodes}
visited[start_node] = True

while len(path) < G.number_of_nodes():
    current_node = path[-1]
    min_dist = float('inf')
    next_node = None
    for neighbor in G.neighbors(current_node):
        if not visited[neighbor] and G[current_node][neighbor]['weight'] < min_dist:
            min_dist = G[current_node][neighbor]['weight']
            next_node = neighbor
    path.append(next_node)
    visited[next_node] = True

path.append(start_node)

# Calculate total distance of the path
total_distance = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1))

# Print the approximate solution
print("Approximate TSP solution using nearest neighbor:")
print("Path: ", path)
print("Total Distance: ", total_distance)

# Show the plot
plt.title("Traveling Salesperson Problem")
plt.show()