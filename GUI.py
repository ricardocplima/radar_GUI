import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to animate both graphs
def update_graph(frame=0):
    shift = frame * 0.1
    sin_value = np.sin(shift)
    cos_value = np.cos(shift)

    # Update graph data
    line_sin.set_ydata(np.sin(x + shift))
    line_cos.set_ydata(np.cos(x + shift))

    # Text of each square (Change this ↓ part to a value that gets updated in real time)
    square1_1.config(text=f"sin: {sin_value:.2f}")
    square1_2.config(text=f"cos: {cos_value:.2f}")

    # Redraw graphs
    canvas_sin.draw()
    canvas_cos.draw()

    # Repeat the update.
    root.after(500, update_graph, frame + 1)    # Change the first number to alter the refresh rate


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
left_frame.columnconfigure(0, weight=1)  # Ensure that the graphs occupy all the space (remember the blue and light blue test)

# Squares with the values from the graphs + a third square
square_frame = tk.Frame(left_frame)
square_frame.grid(row=0, column=0, sticky="nsew")

square_frame.columnconfigure([0, 1, 2], weight=1)
square_frame.rowconfigure(0, weight=1)


square1_1 = tk.Label(square_frame, bg="white", font=("Arial", 16), fg="black", borderwidth=4, relief="solid", width=10, height=5)
square1_1.grid(row=0, column=0, padx=10, pady=10)

square1_2 = tk.Label(square_frame, bg="white", font=("Arial", 16), fg="black", borderwidth=4, relief="solid", width=10, height=5)
square1_2.grid(row=0, column=1, padx=10, pady=10)

square1_3 = tk.Label(square_frame, text="Other", bg="white", font=("Arial", 16), fg="black", borderwidth=4, relief="solid", width=10, height=5)
square1_3.grid(row=0, column=2, padx=10, pady=10)


# Bottom area: Two rectangles (for the graphs)
graph_frame = tk.Frame(left_frame)
graph_frame.grid(row=1, column=0, sticky="nsew")

graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)
graph_frame.rowconfigure(1, weight=1)

# Top Graph (sine wave)
fig_sin = Figure(figsize=(5, 2), dpi=100)
ax_sin = fig_sin.add_subplot(111)
ax_sin.axhline(y=0, color='black', linewidth=1, linestyle='--') # 0 line
x = np.linspace(0, 2 * np.pi, 100)
y_sin = np.sin(x)
line_sin, = ax_sin.plot(x, y_sin, 'b')


ax_sin.set_xticks([])
ax_sin.set_yticks([])

canvas_sin = FigureCanvasTkAgg(fig_sin, master=graph_frame)
canvas_sin.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# Bottom Graph (cosine wave)
fig_cos = Figure(figsize=(5, 2), dpi=100)
ax_cos = fig_cos.add_subplot(111)
ax_cos.axhline(y=0, color='black', linewidth=1, linestyle='--') # 0 line
y_cos = np.cos(x)
line_cos, = ax_cos.plot(x, y_cos, 'c')  # 'c' for cyan

ax_cos.set_xticks([])
ax_cos.set_yticks([])

canvas_cos = FigureCanvasTkAgg(fig_cos, master=graph_frame)
canvas_cos.get_tk_widget().grid(row=1, column=0, sticky="nsew")

# Right section: Vertical rectangle
right_rectangle = tk.Canvas(root, bg="green", width=500)
right_rectangle.grid(row=0, column=1, rowspan=2, sticky="nsew")


update_graph()  # Start animation

# Run the main loop
root.mainloop()
