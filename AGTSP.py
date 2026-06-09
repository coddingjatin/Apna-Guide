import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

VALID_CITIES = ['Mumbai', 'Pune', 'Thane', 'Delhi']


class WelcomeWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.config(background='black')
        self.master.title("Apna Guide Using TSP")

        # Load the background image with error handling
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fl.jpg")
        try:
            self.bg_image = ImageTk.PhotoImage(Image.open(image_path))
        except FileNotFoundError:
            messagebox.showerror(
                "Missing Resource",
                f"Background image not found: {image_path}\n"
                "Please ensure 'fl.jpg' is in the same directory as AGTSP.py."
            )
            sys.exit(1)
        except Exception as e:
            messagebox.showerror(
                "Image Load Error",
                f"Failed to load background image: {e}"
            )
            sys.exit(1)

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

        # Connected to show_path method instead of destroying the window
        self.close_button = tk.Button(self.master, text="Show Path", command=self.show_path, font=("Algerian", 14))
        self.close_button.pack(side="top", padx=10, pady=10)

    def _build_graph(self):
        """Build and return the city graph with nodes and weighted edges."""
        G = nx.Graph()

        G.add_node('Mumbai', pos=(0, 0), node_color='red')
        G.add_node('Pune', pos=(1, 2))
        G.add_node('Thane', pos=(3, 1))
        G.add_node('Delhi', pos=(2, 3))

        G.add_edge('Mumbai', 'Pune', weight=120)
        G.add_edge('Mumbai', 'Thane', weight=15)
        G.add_edge('Mumbai', 'Delhi', weight=400)
        G.add_edge('Pune', 'Thane', weight=90)
        G.add_edge('Pune', 'Delhi', weight=250)
        G.add_edge('Thane', 'Delhi', weight=305)

        return G

    def _compute_tsp_path(self, G, start_node):
        """Compute an approximate TSP path using nearest-neighbor heuristic.

        Returns the computed path list, or raises ValueError if a dead-end
        is reached before all nodes are visited.
        """
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

            if next_node is None:
                raise ValueError(
                    f"Dead-end reached at '{current_node}': no unvisited neighbor is reachable. "
                    f"Visited so far: {path}"
                )

            path.append(next_node)
            visited[next_node] = True

        path.append(start_node)
        return path

    # Handles Show Path button click - will display TSP path on graph
    def show_path(self):
        name = self.name_entry.get().strip()

        if not name:
            self.label.config(text="Please enter a city name.")
            return

        if name not in VALID_CITIES:
            self.label.config(
                text=f"Invalid city! Choose from: {', '.join(VALID_CITIES)}"
            )
            return

        try:
            G = self._build_graph()

            # Draw the graph
            pos = nx.get_node_attributes(G, 'pos')
            nx.draw(G, pos, with_labels=True, node_size=5000, font_size=15, font_color='white')

            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)

            # Find approximate solution using nearest neighbor heuristic
            start_node = 'Mumbai'
            path = self._compute_tsp_path(G, start_node)

            # Trim path to stop at the destination city
            try:
                dest_index = path.index(name)
            except ValueError:
                self.label.config(
                    text=f"Error: destination '{name}' was not reached in the computed path."
                )
                return

            trimmed_path = path[:dest_index + 1]

            # Calculate total distance of the path
            total_distance = sum(
                G[trimmed_path[i]][trimmed_path[i + 1]]['weight']
                for i in range(len(trimmed_path) - 1)
            )

            # Show the plot
            path_edges = list(zip(trimmed_path[:-1], trimmed_path[1:]))

            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
            plt.suptitle(
                f"Path: {' → '.join(trimmed_path)} | Distance: {total_distance} km",
                fontsize=10, y=0.98, x=0.02, ha='left'
            )
            plt.subplots_adjust(top=0.75)
            plt.tight_layout()
            plt.show()

        except ValueError as e:
            self.label.config(text=f"Path error: {e}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred while computing the path:\n{e}")

    def greet_user(self):
        name = self.name_entry.get().strip()
        if not name:
            self.label.config(text="Please enter a destination city.")
            return

        if name not in VALID_CITIES:
            self.label.config(
                text=f"Invalid city! Choose from: {', '.join(VALID_CITIES)}"
            )
            return

        greeting = (
            f"Hello From Mumbai To {name} This is The Shortest and Minimum cost path.\n"
            "*Click On Show Path To View Shortest Path or Enter Another Destination*"
        )
        self.label.config(text=greeting)


def main():
    """Application entry point with top-level error handling."""
    try:
        root = tk.Tk()
    except tk.TclError as e:
        print(f"Error: Unable to initialize the GUI. Is a display available?\n{e}", file=sys.stderr)
        sys.exit(1)

    root.geometry("600x400+400+200")

    try:
        app = WelcomeWindow(master=root)
        app.mainloop()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        messagebox.showerror("Fatal Error", f"The application encountered a fatal error:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
