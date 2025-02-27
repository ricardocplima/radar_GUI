import tkinter as tk
from tkinter import ttk
import threading
import struct
import serial
import numpy as np
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
update_time = 100  # Time of update in ms
decimal_round = 5
running = True
flag = 0
buffer_size = 100
serialPort = serial.Serial("COM3", baudrate=1382400, timeout=2)

# Buffers for graphs
heart_phase_values = np.zeros(buffer_size)
breath_phase_values = np.zeros(buffer_size)
time_values = np.arange(-buffer_size + 1, 1, 1)


def initialize_serial():
    """Initialize the serial port."""
    global serialPort
    try:
        serialPort = serial.Serial(
            port="COM3", baudrate=1382400, bytesize=8, timeout=2, stopbits=serial.STOPBITS_TWO
        )
        print("Serial port initialized successfully.")
    except Exception as e:
        print(f"Error initializing serial port: {e}")


class SerialReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Data Reader")
        self.queue = queue.Queue()

        # Create the main frame
        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Left side: Graphs
        graph_frame = ttk.Frame(main_frame)
        graph_frame.grid(row=0, column=0, sticky="nsew")

        # Create the graphs
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(5, 4), sharex=True)
        self.ax1.set_title("Heart Phase")
        self.ax1.set_ylim(-8, 8)
        self.ax2.set_title("Breath Phase")
        self.ax2.set_ylim(-8, 8)
        self.ax2.set_xlabel("Time")
        self.line1, = self.ax1.plot(time_values, heart_phase_values, "r-")
        self.line2, = self.ax2.plot(time_values, breath_phase_values, "b-")
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Right side: Labels (Squares)
        square_frame = ttk.Frame(main_frame)
        square_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        self.square1_1 = tk.Label(square_frame, bg="white", font=("Arial", 14), fg="black",
                                  borderwidth=2, relief="solid", width=20, height=3)
        self.square1_1.pack(pady=5)

        self.square1_2 = tk.Label(square_frame, bg="white", font=("Arial", 14), fg="black",
                                  borderwidth=2, relief="solid", width=20, height=3)
        self.square1_2.pack(pady=5)

        self.square1_3 = tk.Label(square_frame, bg="white", font=("Arial", 14), fg="black",
                                  borderwidth=2, relief="solid", width=20, height=3)
        self.square1_3.pack(pady=5)

        self.square1_4 = tk.Label(square_frame, bg="white", font=("Arial", 14), fg="black",
                                  borderwidth=2, relief="solid", width=20, height=3)
        self.square1_4.pack(pady=5)

        # Log area
        log_frame = ttk.Frame(root)
        log_frame.grid(row=1, column=0, sticky="nsew")
        self.text_log = tk.Text(log_frame, height=6, width=50, state=tk.DISABLED)
        self.text_log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, command=self.text_log.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_log.config(yscrollcommand=scrollbar.set)

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=3)
        root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)

        # Start the serial reading thread
        self.thread = threading.Thread(target=self.read_serial_thread, daemon=True)
        self.thread.start()

        # Start the UI update loop
        self.update_ui()

    def read_serial_thread(self):
        """Read data from the serial port in a separate thread."""
        global flag, heart_phase_values, breath_phase_values
        while running:
            try:
                byte = serialPort.read(1)
                if byte == b'\x0A':
                    next_byte = serialPort.read(1)
                    if next_byte == b'\x14':
                        flag = 0
                    elif next_byte == b'\x13':
                        data = serialPort.read(13)
                        TotalPhase = struct.unpack('<f', data[1:5])[0]
                        BreathPhase = struct.unpack('<f', data[5:9])[0]
                        HeartPhase = struct.unpack('<f', data[9:13])[0]
                        self.queue.put({
                            "type": "data",
                            "message": f"Breath: {BreathPhase}, Heart: {HeartPhase}, Total: {TotalPhase}\n",
                            "HeartPhase": HeartPhase,
                            "BreathPhase": BreathPhase,
                            "TotalPhase": TotalPhase
                        })
                        # Update the buffers for the graphs
                        heart_phase_values[:-1] = heart_phase_values[1:]
                        heart_phase_values[-1] = HeartPhase
                        breath_phase_values[:-1] = breath_phase_values[1:]
                        breath_phase_values[-1] = BreathPhase
                        flag = 1
                    elif next_byte == b'\x16' and flag == 1:
                        data = serialPort.read(9)
                        Distance = struct.unpack('<f', data[5:9])[0]
                        self.queue.put({
                            "type": "distance",
                            "message": f"Distance: {Distance}\n",
                            "Distance": Distance
                        })
            except Exception as e:
                self.queue.put({"type": "error", "message": f"Error reading serial data: {e}\n"})

    def update_ui(self):
        """Update the UI with new data from the queue."""
        while not self.queue.empty():
            item = self.queue.get()
            if item["type"] == "data":
                # Update labels
                self.update_square_labels(
                    item["HeartPhase"], item["BreathPhase"], item["TotalPhase"], 0
                )
            elif item["type"] == "distance":
                # Update only the distance label
                self.square1_4.config(text=f"Distance:\n{round(item['Distance'], decimal_round)}")

            # Log message
            self.text_log.config(state=tk.NORMAL)
            self.text_log.insert(tk.END, item["message"])
            self.text_log.config(state=tk.DISABLED)
            self.text_log.yview(tk.END)

        # Update the graphs
        self.line1.set_ydata(heart_phase_values)
        self.line2.set_ydata(breath_phase_values)
        self.canvas.draw()

        if running:
            self.root.after(update_time, self.update_ui)

    def update_square_labels(self, HeartPhase, BreathPhase, TotalPhase, Distance):
        """Update the square labels with the latest values."""
        self.square1_1.config(text=f"Heart:\n{round(HeartPhase, decimal_round)}")
        self.square1_2.config(text=f"Breath:\n{round(BreathPhase, decimal_round)}")
        self.square1_3.config(text=f"Total:\n{round(TotalPhase, decimal_round)}")
        self.square1_4.config(text=f"Distance:\n{round(Distance, decimal_round)}")

    def on_close(self):
        """Handle application shutdown."""
        global running
        running = False
        if serialPort and serialPort.is_open:
            serialPort.close()
        self.root.destroy()


def create_gui():
    """Create and configure the GUI."""
    global root
    root = tk.Tk()
    root.geometry("1600x1000")
    app = SerialReaderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    return root


def main():
    """Main function to initialize and run the application."""
    initialize_serial()
    root = create_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
