import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from pyproj import Proj
from PIL import Image, ImageTk
import re
import webbrowser
import os

class CoordenadasApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Coordenadas")
        self.root.attributes('-topmost', True)  # Mantener ventana sobre las demás
        self.root.configure(background='#394351')  # Fondo azul claro

        # Estilos personalizados
        style = ttk.Style()
        style.configure('TLabel', background='#394351', font=('Roboto Bold', 9), foreground='white')
        style.configure('TButton', background='#394351', font=('Roboto', 9),)
        style.configure('TCombobox', background='#394351')
        style.configure('TEntry', background='#394351')

        # Variables para almacenar entradas del usuario
        self.zone_var = tk.IntVar()
        self.easting_var = tk.DoubleVar()
        self.northing_var = tk.DoubleVar()
        self.latitude_var = tk.StringVar()
        self.longitude_var = tk.StringVar()
        self.north_or_south_var = tk.StringVar(value="Norte")  # Valor inicial
        self.lat_dms_var = tk.StringVar()
        self.long_dms_var = tk.StringVar()

        # Crear etiquetas y campos de entrada
        ttk.Label(root, text="Zona UTM (1-60):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.zone_entry = ttk.Combobox(root, textvariable=self.zone_var, values=[str(i) for i in range(1, 61)])
        self.zone_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Norte/Sur:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.north_or_south_combobox = ttk.Combobox(root, textvariable=self.north_or_south_var, values=["Norte", "Sur"])
        self.north_or_south_combobox.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(root, text="Este (X):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.easting_entry = ttk.Entry(root, textvariable=self.easting_var)
        self.easting_entry.grid(row=2, column=1, padx=10, pady=5)
        self.paste_easting_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.easting_var))
        self.paste_easting_button.grid(row=2, column=2, padx=5, pady=5)
        self.copy_easting_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.easting_var))
        self.copy_easting_button.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(root, text="Norte (Y):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.northing_entry = ttk.Entry(root, textvariable=self.northing_var)
        self.northing_entry.grid(row=3, column=1, padx=10, pady=5)
        self.paste_northing_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.northing_var))
        self.paste_northing_button.grid(row=3, column=2, padx=5, pady=5)
        self.copy_northing_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.northing_var))
        self.copy_northing_button.grid(row=3, column=3, padx=5, pady=5)

        # Boton de conversión UTM
        self.convert_to_latlong_btn = ttk.Button(root, text="Convertir UTM", command=self.convert_from_utm)
        self.convert_to_latlong_btn.grid(row=4, column=0, columnspan=1, pady=10)

        ttk.Label(root, text="Latitud (Decimal):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.latitude_entry = ttk.Entry(root, textvariable=self.latitude_var)
        self.latitude_entry.grid(row=5, column=1, padx=10, pady=5)
        self.paste_lat_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.latitude_var))
        self.paste_lat_button.grid(row=5, column=2, padx=5, pady=5)
        self.copy_lat_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.latitude_var))
        self.copy_lat_button.grid(row=5, column=3, padx=5, pady=5)

        ttk.Label(root, text="Longitud (Decimal):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.longitude_entry = ttk.Entry(root, textvariable=self.longitude_var)
        self.longitude_entry.grid(row=6, column=1, padx=10, pady=5)
        self.paste_long_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.longitude_var))
        self.paste_long_button.grid(row=6, column=2, padx=5, pady=5)
        self.copy_long_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.longitude_var))
        self.copy_long_button.grid(row=6, column=3, padx=5, pady=5)

        # Boton de conversión Decimal
        self.convert_to_utm_btn = ttk.Button(root, text="Convertir Lat/Lon", command=self.convert_from_latlong)
        self.convert_to_utm_btn.grid(row=7, column=0, columnspan=1, pady=10)

        ttk.Label(root, text="Latitud (DMS):").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.lat_dms_entry = ttk.Entry(root, textvariable=self.lat_dms_var)
        self.lat_dms_entry.grid(row=8, column=1, padx=10, pady=5)
        self.paste_lat_dms_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.lat_dms_var))
        self.paste_lat_dms_button.grid(row=8, column=2, padx=5, pady=5)
        self.copy_lat_dms_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.lat_dms_var))
        self.copy_lat_dms_button.grid(row=8, column=3, padx=5, pady=5)

        ttk.Label(root, text="Longitud (DMS):").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.long_dms_entry = ttk.Entry(root, textvariable=self.long_dms_var)
        self.long_dms_entry.grid(row=9, column=1, padx=10, pady=5)
        self.paste_long_dms_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.long_dms_var))
        self.paste_long_dms_button.grid(row=9, column=2, padx=5, pady=5)
        self.copy_long_dms_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.long_dms_var))
        self.copy_long_dms_button.grid(row=9, column=3, padx=5, pady=5)

        # Boton de conversión DMS
        self.convert_from_dms_btn = ttk.Button(root, text="Convertir DMS", command=self.convert_from_dms)
        self.convert_from_dms_btn.grid(row=10, column=0, columnspan=1, pady=10)

        # Botón para abrir en Google Maps (anteriormente Google Earth)
        self.open_in_google_maps_button = ttk.Button(root, text="Abrir en Google Maps", command=self.open_in_google_maps)
        self.open_in_google_maps_button.grid(row=11, column=0, columnspan=4, pady=10)

        # Botón para crear archivo KML y abrir en Google Earth
        self.open_in_google_earth_button = ttk.Button(root, text="Abrir en Google Earth", command=self.create_kml_and_open_in_google_earth)
        self.open_in_google_earth_button.grid(row=12, column=0, columnspan=4, pady=10)

    def convert_from_utm(self):
        zone = self.zone_var.get()
        easting = self.easting_var.get()
        northing = self.northing_var.get()
        north_or_south = self.north_or_south_var.get()

        if zone and easting and northing:
            try:
                latitude, longitude = self.utm_to_latlong(zone, easting, northing, north_or_south)
                self.latitude_var.set(f"{latitude:.6f}")
                self.longitude_var.set(f"{longitude:.6f}")
                self.convert_from_decimal()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")

    def limpiar_entrada(self, coordenada):
        # Mantiene solo números, signo de menos y punto decimal, elimina espacios y signos "º" y "°"
        coordenada_limpia = coordenada.replace(" ", "").replace("º", "").replace("°", "")
    
        # Asegurarse de que solo haya un signo de menos y esté al principio
        if coordenada_limpia.count('-') > 1:
            partes = coordenada_limpia.split('-')
            coordenada_limpia = '-' + ''.join(partes)
    
        # Asegurarse de que solo haya un punto decimal
        if coordenada_limpia.count('.') > 1:
            partes = coordenada_limpia.split('.')
            coordenada_limpia = partes[0] + '.' + ''.join(partes[1:])
    
        return coordenada_limpia

    def convert_from_latlong(self):
        latitude_str = self.limpiar_entrada(self.latitude_var.get())
        longitude_str = self.limpiar_entrada(self.longitude_var.get())

        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except ValueError:
            messagebox.showerror("Error", "Las coordenadas deben ser números válidos.")
            return

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
    
    def decimal_to_dms(decimal):
        degrees = int(decimal)
        minutes = int((abs(decimal) - abs(degrees)) * 60)
        seconds = (abs(decimal) - abs(degrees) - minutes / 60) * 3600
        return f"{degrees}°{minutes}'{seconds:.2f}\""

    def dms_to_decimal(dms):
        match = re.match(r"(-?\d+)°(\d+)'([\d.]+)\"", dms)
        if match:
            degrees, minutes, seconds = map(float, match.groups())
            decimal = degrees + (minutes / 60) + (seconds / 3600)
        return -decimal if degrees < 0 else decimal

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
            latitude_str = self.limpiar_entrada(self.latitude_var.get())
            longitude_str = self.limpiar_entrada(self.longitude_var.get())
            latitude = float(latitude_str)
            longitude = float(longitude_str)
            self.lat_dms_var.set(self.decimal_to_dms(latitude, is_latitude=True))
            self.long_dms_var.set(self.decimal_to_dms(longitude, is_latitude=False))
        except ValueError:
            messagebox.showerror("Error", "Las coordenadas deben ser números válidos.")
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

    def open_in_google_maps(self):
        latitude = self.latitude_var.get()
        longitude = self.longitude_var.get()
        if latitude and longitude:
            url = f"https://www.google.com/maps/place/{latitude},{longitude}/@{latitude},{longitude},18.75z/"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Advertencia", "Por favor convierta las coordenadas primero.")

    def create_kml_and_open_in_google_earth(self):
        latitude = self.latitude_var.get()
        longitude = self.longitude_var.get()

        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>Coordenadas Convertidas</name>
    <Point>
      <coordinates>{longitude},{latitude},0</coordinates>
    </Point>
  </Placemark>
</kml>"""

                kml_file_path = "coordinates.kml"
                with open(kml_file_path, "w") as kml_file:
                    kml_file.write(kml_content)

                # Abrir el archivo KML con la aplicación predeterminada (Google Earth)
                os.startfile(kml_file_path)
            except ValueError:
                messagebox.showerror("Error", "Latitud y Longitud deben ser valores numéricos.")
        else:
            messagebox.showerror("Error", "Por favor, convierta las coordenadas primero.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordenadasApp(root)
    root.mainloop()