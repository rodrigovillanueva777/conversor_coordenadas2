import tkinter as tk
from tkinter import ttk, messagebox
from pyproj import Proj
import re

class CoordenadasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Coordenadas UTM <-> Latitud/Longitud")
        self.root.attributes('-topmost', True)  # Mantener ventana sobre las demás

        # Variables para almacenar entradas del usuario
        self.zone_var = tk.IntVar()
        self.easting_var = tk.DoubleVar()
        self.northing_var = tk.DoubleVar()
        self.latitude_var = tk.DoubleVar()
        self.longitude_var = tk.DoubleVar()
        self.north_or_south_var = tk.StringVar(value="Norte")  # Valor inicial
        self.lat_dms_var = tk.StringVar()
        self.long_dms_var = tk.StringVar()

        # Crear etiquetas y campos de entrada
        ttk.Label(root, text="Zona UTM (1-60):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.zone_entry = ttk.Entry(root, textvariable=self.zone_var)
        self.zone_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Norte/Sur:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.north_or_south_combobox = ttk.Combobox(root, textvariable=self.north_or_south_var, values=["Norte", "Sur"])
        self.north_or_south_combobox.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(root, text="Este (m):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.easting_entry = ttk.Entry(root, textvariable=self.easting_var)
        self.easting_entry.grid(row=2, column=1, padx=10, pady=5)
        self.paste_easting_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.easting_var))
        self.paste_easting_button.grid(row=2, column=2, padx=5, pady=5)
        self.copy_easting_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.easting_var))
        self.copy_easting_button.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(root, text="Norte (m):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.northing_entry = ttk.Entry(root, textvariable=self.northing_var)
        self.northing_entry.grid(row=3, column=1, padx=10, pady=5)
        self.paste_northing_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.northing_var))
        self.paste_northing_button.grid(row=3, column=2, padx=5, pady=5)
        self.copy_northing_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.northing_var))
        self.copy_northing_button.grid(row=3, column=3, padx=5, pady=5)

        ttk.Label(root, text="Latitud (DMS):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.lat_dms_entry = ttk.Entry(root, textvariable=self.lat_dms_var)
        self.lat_dms_entry.grid(row=4, column=1, padx=10, pady=5)
        self.paste_lat_dms_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.lat_dms_var))
        self.paste_lat_dms_button.grid(row=4, column=2, padx=5, pady=5)
        self.copy_lat_dms_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.lat_dms_var))
        self.copy_lat_dms_button.grid(row=4, column=3, padx=5, pady=5)

        ttk.Label(root, text="Longitud (DMS):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.long_dms_entry = ttk.Entry(root, textvariable=self.long_dms_var)
        self.long_dms_entry.grid(row=5, column=1, padx=10, pady=5)
        self.paste_long_dms_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.long_dms_var))
        self.paste_long_dms_button.grid(row=5, column=2, padx=5, pady=5)
        self.copy_long_dms_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.long_dms_var))
        self.copy_long_dms_button.grid(row=5, column=3, padx=5, pady=5)

        ttk.Label(root, text="Latitud (Decimal):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.latitude_entry = ttk.Entry(root, textvariable=self.latitude_var)
        self.latitude_entry.grid(row=6, column=1, padx=10, pady=5)
        self.paste_lat_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.latitude_var))
        self.paste_lat_button.grid(row=6, column=2, padx=5, pady=5)
        self.copy_lat_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.latitude_var))
        self.copy_lat_button.grid(row=6, column=3, padx=5, pady=5)

        ttk.Label(root, text="Longitud (Decimal):").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.longitude_entry = ttk.Entry(root, textvariable=self.longitude_var)
        self.longitude_entry.grid(row=7, column=1, padx=10, pady=5)
        self.paste_long_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.longitude_var))
        self.paste_long_button.grid(row=7, column=2, padx=5, pady=5)
        self.copy_long_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.longitude_var))
        self.copy_long_button.grid(row=7, column=3, padx=5, pady=5)

        # Botones de conversión en una sola fila
        self.convert_to_latlong_btn = ttk.Button(root, text="UTM -> Lat/Long", command=self.convert_from_utm)
        self.convert_to_latlong_btn.grid(row=8, column=0, columnspan=1, pady=10)
        self.convert_to_utm_btn = ttk.Button(root, text="Lat/Long -> UTM", command=self.convert_from_latlong)
        self.convert_to_utm_btn.grid(row=8, column=1, columnspan=1, pady=10)
        self.convert_to_dms_btn = ttk.Button(root, text="Decimal -> DMS", command=self.convert_from_decimal)
        self.convert_to_dms_btn.grid(row=8, column=2, columnspan=1, pady=10)
        self.convert_from_dms_btn = ttk.Button(root, text="DMS -> Decimal", command=self.convert_from_dms)
        self.convert_from_dms_btn.grid(row=8, column=3, columnspan=1, pady=10)

    def convert_from_utm(self):
        zone = self.zone_var.get()
        easting = self.easting_var.get()
        northing = self.northing_var.get()
        north_or_south = self.north_or_south_var.get()

        if zone and easting and northing and north_or_south:
            try:
                latitude, longitude = self.utm_to_latlong(zone, easting, northing, north_or_south)
                self.latitude_var.set(f"{latitude:.6f}")
                self.longitude_var.set(f"{longitude:.6f}")
                self.convert_from_decimal()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")

    def convert_from_latlong(self):
        latitude = self.latitude_var.get()
        longitude = self.longitude_var.get()

        if latitude and longitude:
            try:
                zone, easting, northing, north_or_south = self.latlong_to_utm(latitude, longitude)
                self.zone_var.set(zone)
                self.easting_var.set(f"{easting:.4f}")
                self.northing_var.set(f"{northing:.4f}")
                self.north_or_south_var.set(north_or_south)
                self.convert_from_decimal()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")

    def utm_to_latlong(self, zone, easting, northing, north_or_south):
        # Definir el sistema de coordenadas UTM para la zona correspondiente
        projstring = "+proj=utm +zone={}".format(zone)
        if north_or_south == "Sur":
            projstring += " +south"
        projstring += " +ellps=WGS84 +datum=WGS84 +units=m +no_defs"

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

    def dms_to_decimal(self, dms_str):
        dms_str = dms_str.strip()
        degrees, minutes, seconds, direction = re.split('[°\'"]', dms_str)
        degrees = float(degrees)
        minutes = float(minutes)
        seconds = float(seconds)
        decimal = degrees + minutes/60 + seconds/3600
        if direction in ['S', 'O']:
            decimal = -decimal
        return decimal

    def decimal_to_dms(self, decimal, is_latitude=True):
        direction = 'N' if is_latitude else 'E'
        if decimal < 0:
            direction = 'S' if is_latitude else 'O'
            decimal = -decimal
        degrees = int(decimal)
        minutes = int((decimal - degrees) * 60)
        seconds = (decimal - degrees - minutes/60) * 3600
        return f"{degrees}°{minutes}'{seconds:.2f}\"{direction}"

    def convert_from_decimal(self):
        try:
            latitude = self.latitude_var.get()
            longitude = self.longitude_var.get()
            self.lat_dms_var.set(self.decimal_to_dms(latitude, is_latitude=True))
            self.long_dms_var.set(self.decimal_to_dms(longitude, is_latitude=False))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def convert_from_dms(self):
        try:
            lat_dms = self.lat_dms_var.get()
            long_dms = self.long_dms_var.get()
            lat_decimal = self.dms_to_decimal(lat_dms)
            long_decimal = self.dms_to_decimal(long_dms)
            self.latitude_var.set(f"{lat_decimal:.6f}")
            self.longitude_var.set(f"{long_decimal:.6f}")
            self.convert_from_latlong()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def paste_from_clipboard(self, var):
        try:
            clipboard_text = self.root.clipboard_get()
            var.set(clipboard_text)
        except tk.TclError:
            pass  # No se pudo obtener datos del portapapeles o no es un número

    def copy_to_clipboard(self, var):
        self.root.clipboard_clear()
        self.root.clipboard_append(var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordenadasApp(root)
    root.mainloop()
