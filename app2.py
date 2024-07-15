import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        root.title("UTM Converter")
        root.geometry("600x400")
        
        # Configurar la primera columna para que no se redimensione
        root.grid_columnconfigure(0, weight=0)  # Fijo
        root.grid_columnconfigure(1, weight=1)  # Redimensionable
        root.grid_columnconfigure(2, weight=1)  # Redimensionable para botones
        root.grid_rowconfigure(5, weight=1)  # Espacio dinámico en la parte inferior

        self.zone_var = tk.StringVar()
        self.north_or_south_var = tk.StringVar()
        self.easting_var = tk.StringVar()
        self.northing_var = tk.StringVar()

        # Etiqueta y combobox: Zona UTM
        ttk.Label(root, text="Zona UTM (1-60):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.zone_entry = ttk.Combobox(root, textvariable=self.zone_var, values=[str(i) for i in range(1, 61)], width=15)
        self.zone_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Etiqueta y combobox: Norte/Sur
        ttk.Label(root, text="Norte/Sur:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.north_or_south_combobox = ttk.Combobox(root, textvariable=self.north_or_south_var, values=["Norte", "Sur"], width=15)
        self.north_or_south_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Etiqueta, entrada y botones: Este (X)
        ttk.Label(root, text="Este (X):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.easting_entry = ttk.Entry(root, textvariable=self.easting_var, width=15)
        self.easting_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.create_buttons(root, row=2, column=2, var=self.easting_var, entry=self.easting_entry)

        # Etiqueta, entrada y botones: Norte (Y)
        ttk.Label(root, text="Norte (Y):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.northing_entry = ttk.Entry(root, textvariable=self.northing_var, width=15)
        self.northing_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.create_buttons(root, row=3, column=2, var=self.northing_var, entry=self.northing_entry)

        # Botón de conversión
        self.convert_to_latlong_btn = ttk.Button(root, text="Convertir", command=self.convert_from_utm)
        self.convert_to_latlong_btn.grid(row=4, column=0, columnspan=3, padx=5, pady=15, sticky="ew")

    def create_buttons(self, root, row, column, var, entry):
        """Crea los botones para Copiar, Pegar y Cortar."""
        frame = ttk.Frame(root)  # Frame para los botones
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        frame.grid_columnconfigure((0, 1, 2), weight=1)  # Ajuste uniforme

        ttk.Button(frame, text="Pegar", command=lambda: self.paste_from_clipboard(var)).grid(row=0, column=0, sticky="ew")
        ttk.Button(frame, text="Copiar", command=lambda: self.copy_to_clipboard(var)).grid(row=0, column=1, sticky="ew")
        ttk.Button(frame, text="Cortar", command=lambda: self.cut_to_clipboard(var, entry)).grid(row=0, column=2, sticky="ew")

    def paste_from_clipboard(self, var):
        # Lógica para pegar
        pass

    def copy_to_clipboard(self, var):
        # Lógica para copiar
        pass

    def cut_to_clipboard(self, var, entry):
        # Lógica para cortar
        pass

    def convert_from_utm(self):
        # Lógica de conversión
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
