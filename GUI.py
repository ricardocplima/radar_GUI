import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple GUI Layout")
root.geometry("1400x800")

# Configure the main window's grid
root.columnconfigure(0, weight=4)
root.columnconfigure(1, weight=0)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Left section: Two areas
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

left_frame.rowconfigure(0, weight=1)  # Space for squares
left_frame.rowconfigure(1, weight=3)  # Space for graphs
left_frame.columnconfigure(0, weight=1)  # Ensure full width usage

# Top area: Three small squares within a fixed-size container
square_frame = tk.Frame(left_frame)
square_frame.grid(row=0, column=0, sticky="nsew")

square_frame.columnconfigure([0, 1, 2], weight=1)
square_frame.rowconfigure(0, weight=1)

square1_1 = tk.Canvas(square_frame, bg="red", width=100, height=100)
square1_1.grid(row=0, column=0, padx=10, pady=10)

square1_2 = tk.Canvas(square_frame, bg="red", width=100, height=100)
square1_2.grid(row=0, column=1, padx=10, pady=10)

square1_3 = tk.Canvas(square_frame, bg="red", width=100, height=100)
square1_3.grid(row=0, column=2, padx=10, pady=10)

# Bottom area: Two rectangles
graph_frame = tk.Frame(left_frame)
graph_frame.grid(row=1, column=0, sticky="nsew")

graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)
graph_frame.rowconfigure(1, weight=1)

rectangle1 = tk.Canvas(graph_frame, bg="blue")
rectangle1.grid(row=0, column=0, sticky="nsew")

rectangle2 = tk.Canvas(graph_frame, bg="lightblue")
rectangle2.grid(row=1, column=0, sticky="nsew")

# Right section: Vertical rectangle
right_rectangle = tk.Canvas(root, bg="green", width=500)
right_rectangle.grid(row=0, column=1, rowspan=2, sticky="nsew")

# Run the main loop
root.mainloop()
