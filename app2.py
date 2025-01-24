import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("App Responsive")

# Configurar la ventana principal para ser responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Crear un frame principal
frame = ttk.Frame(root, padding=10, relief="solid")
frame.grid(row=0, column=0, sticky="nsew")

# Configurar el frame para ser responsive
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Agregar widgets al frame
button1 = ttk.Button(frame, text="Botón 1")
button1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

button2 = ttk.Button(frame, text="Botón 2")
button2.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

button3 = ttk.Button(frame, text="Botón 3")
button3.grid(row=1, column=0, columnspan=2, sticky="ns", padx=5, pady=5)

# Ejecutar la app
root.mainloop()
