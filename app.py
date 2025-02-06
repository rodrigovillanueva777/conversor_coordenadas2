import tkinter as tk
from tkinter import ttk, messagebox
from pyproj import Proj
from PIL import Image, ImageTk
from ttkbootstrap import Style
import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS, LIGHT, SECONDARY
import re
import webbrowser
import os
import json

class CoordenadasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ConverCoor.v2")
        self.root.attributes('-topmost', False)  # Mantener ventana sobre las demás
        self.theme_window = None

        # Configurar el comportamiento de las filas y columnas para que se ajusten
        self.root.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)  # Fila para las etiquetas
        self.root.grid_columnconfigure((1), weight=1)  # Columna para los campos de entrada (centrado)
        self.root.grid_columnconfigure((0,2,3,4), weight=0)  
        
        # Estilos personalizados
        self.theme_file = "theme_config.json"
        self.style = tb.Style()
        self.current_theme = self.load_theme()
        self.style.theme_use(self.current_theme)

        # Variables para almacenar entradas del usuario
        self.zone_var = tk.IntVar()
        self.easting_var = tk.DoubleVar()
        self.northing_var = tk.DoubleVar()
        self.latitude_var = tk.StringVar()
        self.longitude_var = tk.StringVar()
        self.north_or_south_var = tk.StringVar(value="Norte")  # Valor inicial
        self.lat_dms_var = tk.StringVar()
        self.long_dms_var = tk.StringVar()

        # Título de la aplicación
        title_label = ttk.Label(
            root, 
            text="ConverCoor", 
            font=("Arial", 20, "bold"), 
            anchor="center"
            )
        title_label.grid(row=0, column=0, columnspan=5, pady=(10, 0), sticky="n")

        # Subtítulo
        subtitle_label = ttk.Label(
            root, 
            text="Conversor de Coordenadas", 
            font=("Arial", 10), 
            anchor="center"
        )
        subtitle_label.grid(row=1, column=0, columnspan=5, pady=(0, 5), sticky="n")

        # Línea adicional: UTM Estándar
        utmost_label = ttk.Label(
            root, 
            text="UTM Estándar", 
            font=("Arial", 10, "bold")
        )
        utmost_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Crear etiquetas y campos de entrada
        self.pin_icon = ImageTk.PhotoImage(Image.open("icon/pin_icon.png").resize((20, 20)))
        self.config_icon = ImageTk.PhotoImage(Image.open("icon/config_icon.png").resize((20, 20)))

        # Estado de anclaje
        self.is_pinned = False


        # Botón de anclaje
        self.pin_button = tb.Button(root, image=self.pin_icon, command=self.toggle_pin, bootstyle = SECONDARY)
        self.pin_button.grid(row=0, column=3, padx=5, pady=5)

        self.config_button = tb.Button(root, image=self.config_icon, command=self.open_theme_selector, bootstyle = SECONDARY)
        self.config_button.grid(row=0, column=4, padx=5, pady=5)

        ToolTip(self.pin_button, "Anclar sobre otras Apps")
        ToolTip(self.config_button, "Configurar Tema")

        ttk.Label(root, text="Zona:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.zone_entry = ttk.Combobox(root, textvariable=self.zone_var, values=[str(i) for i in range(1, 61)], width=10)
        self.zone_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(root, text="Hemisferio:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.north_or_south_combobox = ttk.Combobox(root, textvariable=self.north_or_south_var, values=["Norte", "Sur"], width=10)
        self.north_or_south_combobox.grid(row=4, column=1, padx=10, pady=5)

        self.paste_icon = ImageTk.PhotoImage(Image.open("icon/paste_icon.png").resize((20, 20)))
        self.copy_icon = ImageTk.PhotoImage(Image.open("icon/copy_icon.png").resize((20, 20)))
        self.cut_icon = ImageTk.PhotoImage(Image.open("icon/cut_icon.png").resize((20, 20)))
        self.convert_icon = ImageTk.PhotoImage(Image.open("icon/convert_icon.png").resize((25, 25)))

        ttk.Label(root, text="Este (X):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.easting_entry = ttk.Entry(root, textvariable=self.easting_var)
        self.easting_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        self.paste_easting_button = ttk.Button(root, image=self.paste_icon, command=lambda: self.paste_from_clipboard(self.easting_var))
        self.paste_easting_button.grid(row=5, column=2, padx=5, pady=5)
        self.copy_easting_button = ttk.Button(root, image=self.copy_icon, command=lambda: self.copy_to_clipboard(self.easting_var))
        self.copy_easting_button.grid(row=5, column=3, padx=5, pady=5)
        self.cut_easting_button = ttk.Button(root, image=self.cut_icon, command=lambda: self.cut_to_clipboard(self.easting_var, self.easting_entry))
        self.cut_easting_button.grid(row=5, column=4, padx=5, pady=5)

        ToolTip(self.copy_easting_button, "Copiar")
        ToolTip(self.paste_easting_button, "Pegar")
        ToolTip(self.cut_easting_button, "Cortar")

        ttk.Label(root, text="Norte (Y):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.northing_entry = ttk.Entry(root, textvariable=self.northing_var)
        self.northing_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
        self.paste_northing_button = ttk.Button(root, image=self.paste_icon, command=lambda: self.paste_from_clipboard(self.northing_var))
        self.paste_northing_button.grid(row=6, column=2, padx=5, pady=5)
        self.copy_northing_button = ttk.Button(root, image=self.copy_icon, command=lambda: self.copy_to_clipboard(self.northing_var))
        self.copy_northing_button.grid(row=6, column=3, padx=5, pady=5)
        self.cut_northing_button = ttk.Button(root, image=self.cut_icon, command=lambda: self.cut_to_clipboard(self.northing_var, self.northing_entry))
        self.cut_northing_button.grid(row=6, column=4, padx=5, pady=5)

        ToolTip(self.copy_northing_button, "Copiar")
        ToolTip(self.paste_northing_button, "Pegar")
        ToolTip(self.cut_northing_button, "Cortar")

        # Boton de conversión UTM

        self.convert_to_latlong_btn = tb.Button(root, image=self.convert_icon, command=self.convert_from_utm, bootstyle=SUCCESS)
        self.convert_to_latlong_btn.grid(row=7, column=1, columnspan=1, padx=30, pady=5, sticky="ew")

        ToolTip(self.convert_to_latlong_btn, "Convertir de UTM")

        utmost_label = ttk.Label(
            root, 
            text="Decimal", 
            font=("Arial", 10, "bold")
        )
        utmost_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        ttk.Label(root, text="Latitud (Y):").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.latitude_entry = ttk.Entry(root, textvariable=self.latitude_var)
        self.latitude_entry.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
        self.paste_lat_button = ttk.Button(root, image=self.paste_icon, command=lambda: self.paste_from_clipboard(self.latitude_var))
        self.paste_lat_button.grid(row=9, column=2, padx=5, pady=5)
        self.copy_lat_button = ttk.Button(root, image=self.copy_icon, command=lambda: self.copy_to_clipboard(self.latitude_var))
        self.copy_lat_button.grid(row=9, column=3, padx=5, pady=5)
        self.cut_lat_button = ttk.Button(root, image=self.cut_icon, command=lambda: self.cut_to_clipboard(self.latitude_var, self.latitude_entry))
        self.cut_lat_button.grid(row=9, column=4, padx=5, pady=5)

        ToolTip(self.copy_lat_button, "Copiar")
        ToolTip(self.paste_lat_button, "Pegar")
        ToolTip(self.cut_lat_button, "Cortar")

        ttk.Label(root, text="Longitud (X):").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.longitude_entry = ttk.Entry(root, textvariable=self.longitude_var)
        self.longitude_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
        self.paste_long_button = ttk.Button(root, image=self.paste_icon, command=lambda: self.paste_from_clipboard(self.longitude_var))
        self.paste_long_button.grid(row=10, column=2, padx=5, pady=5)
        self.copy_long_button = ttk.Button(root, image=self.copy_icon, command=lambda: self.copy_to_clipboard(self.longitude_var))
        self.copy_long_button.grid(row=10, column=3, padx=5, pady=5)
        self.cut_long_button = ttk.Button(root, image=self.cut_icon, command=lambda: self.cut_to_clipboard(self.longitude_var, self.longitude_entry))
        self.cut_long_button.grid(row=10, column=4, padx=5, pady=5)

        ToolTip(self.copy_long_button, "Copiar")
        ToolTip(self.paste_long_button, "Pegar")
        ToolTip(self.cut_long_button, "Cortar")

        # Boton de conversión Decimal
        self.convert_to_utm_btn = tb.Button(root, image=self.convert_icon, command=self.convert_from_latlong, bootstyle=SUCCESS)
        self.convert_to_utm_btn.grid(row=11, column=1, columnspan=1, padx=30, pady=5, sticky="ew")

        ToolTip(self.convert_to_utm_btn, "Convertir de Decimal")

        utmost_label = ttk.Label(
            root, 
            text="Grados, Minutos, Segundos", 
            font=("Arial", 10, "bold"), 
        )
        utmost_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")

        ttk.Label(root, text="Latitud:").grid(row=13, column=0, padx=10, pady=5, sticky="w")
        self.lat_dms_entry = ttk.Entry(root, textvariable=self.lat_dms_var)
        self.lat_dms_entry.grid(row=13, column=1, padx=10, pady=5, sticky="ew")
        self.paste_lat_dms_button = ttk.Button(root, image=self.paste_icon, command=lambda: self.paste_from_clipboard(self.lat_dms_var))
        self.paste_lat_dms_button.grid(row=13, column=2, padx=5, pady=5)
        self.copy_lat_dms_button = ttk.Button(root, image=self.copy_icon, command=lambda: self.copy_to_clipboard(self.lat_dms_var))
        self.copy_lat_dms_button.grid(row=13, column=3, padx=5, pady=5)
        self.cut_lat_dms_button = ttk.Button(root, image=self.cut_icon, command=lambda: self.cut_to_clipboard(self.lat_dms_var, self.lat_dms_entry))
        self.cut_lat_dms_button.grid(row=13, column=4, padx=5, pady=5)

        ToolTip(self.copy_lat_dms_button, "Copiar")
        ToolTip(self.paste_lat_dms_button, "Pegar")
        ToolTip(self.cut_lat_dms_button, "Cortar")

        ttk.Label(root, text="Longitud:").grid(row=14, column=0, padx=10, pady=5, sticky="w")
        self.long_dms_entry = ttk.Entry(root, textvariable=self.long_dms_var)
        self.long_dms_entry.grid(row=14, column=1, padx=10, pady=5, sticky="ew")
        self.paste_long_dms_button = ttk.Button(root, image=self.paste_icon, command=lambda: self.paste_from_clipboard(self.long_dms_var))
        self.paste_long_dms_button.grid(row=14, column=2, padx=5, pady=5)
        self.copy_long_dms_button = ttk.Button(root, image=self.copy_icon, command=lambda: self.copy_to_clipboard(self.long_dms_var))
        self.copy_long_dms_button.grid(row=14, column=3, padx=5, pady=5)
        self.cut_long_dms_button = ttk.Button(root, image=self.cut_icon, command=lambda: self.cut_to_clipboard(self.long_dms_var, self.long_dms_entry))
        self.cut_long_dms_button.grid(row=14, column=4, padx=5, pady=5)

        ToolTip(self.copy_long_dms_button, "Copiar")
        ToolTip(self.paste_long_dms_button, "Pegar")
        ToolTip(self.cut_long_dms_button, "Cortar")

        # Boton de conversión DMS
        self.convert_from_dms_btn = tb.Button(root, image=self.convert_icon, command=self.convert_from_dms, bootstyle=SUCCESS)
        self.convert_from_dms_btn.grid(row=15, column=1, columnspan=1, padx=30, pady=5, sticky="ew")

        ToolTip(self.convert_from_dms_btn, "Convertir de DMS")

        self.maps_icon = ImageTk.PhotoImage(Image.open("icon/maps_icon.png").resize((25, 25)))
        self.earth_icon = ImageTk.PhotoImage(Image.open("icon/earth_icon.png").resize((25, 25)))
        
        # Botón para abrir en Google Maps
        self.open_in_google_maps_button = tb.Button(root, image=self.maps_icon, command=self.open_in_google_maps, bootstyle=LIGHT)
        self.open_in_google_maps_button.grid(row=16, column=1, columnspan=1, padx=10, pady=10, sticky="ew")

        # Botón para crear archivo KML y abrir en Google Earth
        self.open_in_google_earth_button = tb.Button(root, image=self.earth_icon, command=self.create_kml_and_open_in_google_earth, bootstyle=LIGHT)
        self.open_in_google_earth_button.grid(row=17, column=1, columnspan=1, padx=10, pady=10, sticky="ew")

        ToolTip(self.open_in_google_maps_button, "Abrir en Google Maps")
        ToolTip(self.open_in_google_earth_button, "Crear Pin en Google Earth")
        
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
        except ValueError:
            messagebox.showerror("Error", "Las coordenadas deben ser números válidos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self, var):
        self.root.clipboard_clear()
        self.root.clipboard_append(var.get())

    def paste_from_clipboard(self, var):
        try:
            clipboard_text = self.root.clipboard_get()
            var.set(clipboard_text)
        except tk.TclError:
            pass  # No se pudo obtener datos del portapapeles o no es un número

    def cut_to_clipboard(self, var, entry_widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(var.get())
        # Limpiar el campo
        var.set("")
        entry_widget.delete(0, "end")

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

    def toggle_pin(self):
        """Alterna el estado de anclaje de la ventana."""
        self.is_pinned = not self.is_pinned
        self.root.attributes("-topmost", self.is_pinned)
        estado = "sobre otras apps" if self.is_pinned else "menor"
        messagebox.showinfo("Anclar", f"ConverCoor tendrá prioridad {estado}.")

    def open_theme_selector(self):
        # Abrir la ventana de configuración
        theme_window = tk.Toplevel(self.root)
        ThemedApp(theme_window)
        theme_window.geometry("200x150")
        center_window(theme_window) # type: ignore

    def load_theme(self):
        # Cargar el tema inicial
        if os.path.exists(self.theme_file):
            with open(self.theme_file, "r") as f:
                data = json.load(f)
                return data.get("theme", "cosmo")  # Tema predeterminado
        return "cosmo"

class ThemedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selector de Tema")
        self.theme_file = "theme_config.json"  # Archivo para guardar el tema

        # Carga o define un tema inicial
        self.style = tb.Style()
        self.current_theme = self.load_theme()
        self.style.theme_use(self.current_theme)

        # Combobox para seleccionar el tema
        ttk.Label(root, text="Elige un tema:").pack(pady=10)
        self.theme_combobox = ttk.Combobox(
            root,
            values=self.style.theme_names(),
            state="readonly"
        )
        self.theme_combobox.set(self.current_theme)  # Tema actual
        self.theme_combobox.pack(pady=10)

        # Botón para guardar tema
        save_button = ttk.Button(root, text="Guardar Tema", command=self.save_selected_theme)
        save_button.pack(pady=10)

    def save_selected_theme(self):
        # Guarda el tema seleccionado
        selected_theme = self.theme_combobox.get()
        self.style.theme_use(selected_theme)
        self.save_theme(selected_theme)
        tk.messagebox.showinfo("Configuración", f"Tema '{selected_theme}' guardado correctamente.")

    def save_theme(self, theme):
        # Guarda el tema en un archivo JSON
        with open(self.theme_file, "w") as f:
            json.dump({"theme": theme}, f)

    def load_theme(self):
        # Carga el tema desde el archivo JSON
        if os.path.exists(self.theme_file):
            with open(self.theme_file, "r") as f:
                data = json.load(f)
                return data.get("theme", "superhero")  # Tema predeterminado
        return "superhero"  # Si no existe archivo, usa un tema predeterminado

class ToolTip:
    """Clase para mostrar tooltips al pasar el ratón sobre un widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = self.widget.winfo_rootx() + x + 25
        y = self.widget.winfo_rooty() + y + 20
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)  # Mantener siempre arriba
        label = tk.Label(tw, text=self.text, background="white", relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack(ipadx=5, ipady=2)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def center_window(window, width=None, height=None):
    """Función para centrar cualquier ventana."""
    window.update_idletasks()  # Actualiza la geometría de la ventana
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordenadasApp(root)

    # Configurar tamaño inicial y centrar la ventana principal
    root.geometry("500x730")  # Tamaño inicial de la ventana principal
    center_window(root)  # Centrar la ventana principal

    root.mainloop()