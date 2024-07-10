import tkinter as tk
from tkinter import ttk, messagebox
from pyproj import Proj, transform

class CoordenadasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Coordenadas UTM <-> Latitud/Longitud")
        
        # Variables para almacenar entradas del usuario
        self.zone_var = tk.StringVar()
        self.easting_var = tk.DoubleVar()
        self.northing_var = tk.DoubleVar()
        self.latitude_var = tk.DoubleVar()
        self.longitude_var = tk.DoubleVar()
        self.north_or_south_var = tk.StringVar(value="Norte")  # Valor inicial
        
        # Crear etiquetas y campos de entrada
        ttk.Label(root, text="Zona UTM:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.zone_entry = ttk.Entry(root, textvariable=self.zone_var)
        self.zone_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(root, text="Este (m):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.easting_entry = ttk.Entry(root, textvariable=self.easting_var)
        self.easting_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(root, text="Norte (m):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.northing_entry = ttk.Entry(root, textvariable=self.northing_var)
        self.northing_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(root, text="Latitud:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.latitude_entry = ttk.Entry(root, textvariable=self.latitude_var)
        self.latitude_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(root, text="Longitud:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.longitude_entry = ttk.Entry(root, textvariable=self.longitude_var)
        self.longitude_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Selección Norte/Sur
        ttk.Label(root, text="Norte/Sur:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.north_or_south_combobox = ttk.Combobox(root, textvariable=self.north_or_south_var, values=["Norte", "Sur"])
        self.north_or_south_combobox.grid(row=5, column=1, padx=10, pady=5)
        
        # Botones de conversión
        self.convert_to_latlong_btn = ttk.Button(root, text="UTM -> Lat/Long", command=self.convert_to_latlong)
        self.convert_to_latlong_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.convert_to_utm_btn = ttk.Button(root, text="Lat/Long -> UTM", command=self.convert_to_utm)
        self.convert_to_utm_btn.grid(row=7, column=0, columnspan=2, pady=10)
        
    def convert_to_latlong(self):
        zone = self.zone_var.get()
        easting = self.easting_var.get()
        northing = self.northing_var.get()
        north_or_south = self.north_or_south_var.get()
        
        if zone and easting and northing and north_or_south:
            try:
                # Convertir UTM a latitud/longitud
                latitude, longitude = self.utm_to_latlong(int(zone), easting, northing, north_or_south)
                self.latitude_var.set(latitude)
                self.longitude_var.set(longitude)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
    
    def convert_to_utm(self):
        latitude = self.latitude_var.get()
        longitude = self.longitude_var.get()
        
        if latitude and longitude:
            try:
                # Convertir latitud/longitud a UTM
                zone, easting, northing, north_or_south = self.latlong_to_utm(latitude, longitude)
                self.zone_var.set(zone)
                self.easting_var.set(easting)
                self.northing_var.set(northing)
                self.north_or_south_var.set(north_or_south)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
    
    def utm_to_latlong(self, zone, easting, northing, north_or_south):
        # Definir el sistema de coordenadas UTM
        if north_or_south == "Norte":
            projstring = "+proj=utm +zone={} +ellps=WGS84 +datum=WGS84 +units=m +no_defs".format(zone)
        else:
            projstring = "+proj=utm +zone={} +ellps=WGS84 +datum=WGS84 +units=m +no_defs +south".format(zone)
        
        # Crear el objeto de proyección UTM
        utm_proj = Proj(projstring)
        
        # Convertir UTM a latitud y longitud
        longitude, latitude = utm_proj(easting, northing, inverse=True)
        return latitude, longitude
    
    def latlong_to_utm(self, latitude, longitude):
        # Definir el sistema de coordenadas UTM para la zona correspondiente
        zone = int((longitude + 180) // 6) + 1  # Calcular la zona UTM basada en la longitud
        
        # Definir el sistema de coordenadas UTM y Norte/Sur
        if latitude >= 0:
            north_or_south = "Norte"
            projstring = "+proj=utm +zone={} +ellps=WGS84 +datum=WGS84 +units=m +no_defs".format(zone)
        else:
            north_or_south = "Sur"
            projstring = "+proj=utm +zone={} +ellps=WGS84 +datum=WGS84 +units=m +no_defs +south".format(zone)
        
        # Crear el objeto de proyección UTM
        utm_proj = Proj(projstring)
        
        # Convertir latitud y longitud a UTM
        easting, northing = utm_proj(longitude, latitude)
        return zone, easting, northing, north_or_south

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordenadasApp(root)
    root.mainloop()
