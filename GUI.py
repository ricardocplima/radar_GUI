import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


update_time = 500   # Time of update in ms
text_update_time = update_time
graph_update_time = update_time


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
    root.after(graph_update_time, update_graph, frame + 1)    # Change the first number to alter the refresh rate


    

# Example: Automatically adding placeholder messages
def update_text():

    # Replace this by the output of the serial port
    message="This is a placeholder message."


    text_log.config(state="normal")     # Enable editing

    # Check if the scrollbar is at the bottom to allow view of the log
    if text_log.yview()[1] == 1.0:  # If at bottom (1.0 means fully scrolled down)
        auto_scroll = True
    else:
        auto_scroll = False
    
    text_log.insert("end", message + "\n")  # Append message
    text_log.config(state="disabled")       # Disable editing
    if auto_scroll:                         # Only keeps the scroll at the end if the scrollbar is at the bottom
        text_log.yview("end")
    root.after(text_update_time, update_text)


# Create the main window
root = tk.Tk()
root.title("Simple GUI Layout")
root.geometry("1400x800")

# Configure the main window's grid
root.columnconfigure(0, weight=2)  # Top side (Graphs)
root.columnconfigure(1, weight=1)  # Right side (Squares)
root.rowconfigure(0, weight=2)  # Upper section (Graphs & Squares)
root.rowconfigure(1, weight=1)  # Bottom section (Text log)

# Top section: Two areas
Top_frame = tk.Frame(root)
Top_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

Top_frame.rowconfigure(0, weight=0)  # Space for squares
Top_frame.rowconfigure(1, weight=1)  # Space for graphs
Top_frame.columnconfigure(0, weight=1)  # Ensure that the graphs occupy all the space (remember the blue and light blue test)

# Squares with the values from the graphs + a third square
square_frame = tk.Frame(Top_frame)
square_frame.grid(row=0, column=1, sticky="nsew")

square_frame.columnconfigure(0, weight=1)
square_frame.rowconfigure([0, 1, 2], weight=0)


square1_1 = tk.Label(square_frame, bg="white", font=("Arial", 16), fg="black", borderwidth=4, relief="solid", width=10, height=5)
square1_1.grid(row=0, column=0, padx=10, pady=10)

square1_2 = tk.Label(square_frame, bg="white", font=("Arial", 16), fg="black", borderwidth=4, relief="solid", width=10, height=5)
square1_2.grid(row=1, column=0, padx=10, pady=10)

square1_3 = tk.Label(square_frame, text="Other", bg="white", font=("Arial", 16), fg="black", borderwidth=4, relief="solid", width=10, height=5)
square1_3.grid(row=2, column=0, padx=10, pady=10)


# Upper-Left area: Two rectangles (for the graphs)
graph_frame = tk.Frame(Top_frame)
graph_frame.grid(row=0, column=0, sticky="nsew")


graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)
graph_frame.rowconfigure(1, weight=1)

# Upper Graph (sine wave)
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


# Right section: Scrollable text log
right_frame = tk.Frame(root)
right_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=0)

# Scrollbar
scrollbar = tk.Scrollbar(right_frame)
scrollbar.grid(row=0, column=1, sticky="ns")

# Text widget for displaying messages
text_log = tk.Text(right_frame, wrap="word", font=("Arial", 12), bg="white", fg="black", state="disabled", height=1)
text_log.grid(row=0, column=0, sticky="nsew")

text_log.config(yscrollcommand=scrollbar.set, height=15)   #   Connects the scrollbar and the text log
scrollbar.config(command=text_log.yview)






update_text()   # Function that updates the text
update_graph()  # Function that updates the graphs

# Run the main loop
root.mainloop()
