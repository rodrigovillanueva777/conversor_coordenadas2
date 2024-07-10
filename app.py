import tkinter as tk
from tkinter import ttk, messagebox
from pyproj import Proj
import re

class CoordenadasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Coordenadas")
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

        self.convert_to_latlong_btn = ttk.Button(root, text="Convertir UTM", command=self.convert_from_utm)
        self.convert_to_latlong_btn.grid(row=4, column=0, columnspan=4, pady=10)

        ttk.Label(root, text="Latitud (DMS):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.lat_dms_entry = ttk.Entry(root, textvariable=self.lat_dms_var)
        self.lat_dms_entry.grid(row=5, column=1, padx=10, pady=5)
        self.paste_lat_dms_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.lat_dms_var))
        self.paste_lat_dms_button.grid(row=5, column=2, padx=5, pady=5)
        self.copy_lat_dms_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.lat_dms_var))
        self.copy_lat_dms_button.grid(row=5, column=3, padx=5, pady=5)

        ttk.Label(root, text="Longitud (DMS):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.long_dms_entry = ttk.Entry(root, textvariable=self.long_dms_var)
        self.long_dms_entry.grid(row=6, column=1, padx=10, pady=5)
        self.paste_long_dms_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.long_dms_var))
        self.paste_long_dms_button.grid(row=6, column=2, padx=5, pady=5)
        self.copy_long_dms_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.long_dms_var))
        self.copy_long_dms_button.grid(row=6, column=3, padx=5, pady=5)

        self.convert_from_dms_btn = ttk.Button(root, text="Convertir DMS", command=self.convert_from_dms)
        self.convert_from_dms_btn.grid(row=7, column=0, columnspan=4, pady=10)

        ttk.Label(root, text="Latitud (Decimal):").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.latitude_entry = ttk.Entry(root, textvariable=self.latitude_var)
        self.latitude_entry.grid(row=8, column=1, padx=10, pady=5)
        self.paste_lat_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.latitude_var))
        self.paste_lat_button.grid(row=8, column=2, padx=5, pady=5)
        self.copy_lat_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.latitude_var))
        self.copy_lat_button.grid(row=8, column=3, padx=5, pady=5)

        ttk.Label(root, text="Longitud (Decimal):").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.longitude_entry = ttk.Entry(root, textvariable=self.longitude_var)
        self.longitude_entry.grid(row=9, column=1, padx=10, pady=5)
        self.paste_long_button = ttk.Button(root, text="Pegar", command=lambda: self.paste_from_clipboard(self.longitude_var))
        self.paste_long_button.grid(row=9, column=2, padx=5, pady=5)
        self.copy_long_button = ttk.Button(root, text="Copiar", command=lambda: self.copy_to_clipboard(self.longitude_var))
        self.copy_long_button.grid(row=9, column=3, padx=5, pady=5)

        self.convert_to_dms_btn = ttk.Button(root, text="Convertir Decimal", command=self.convert_from_latlong)
        self.convert_to_dms_btn.grid(row=10, column=0, columnspan=4, pady=10)

    def convert_from_utm(self):
        zone = self.zone_var.get()
        easting = self.easting_var.get()
        northing = self.northing_var.get()
        north_or_south = self.north_or_south_var.get()

        if zone and easting and northing and north_or_south:
            try:
                latitude, longitude = self.utm_to_latlong(zone, easting, northing, north_or_south)
                self.latitude_var.set(f"{latitude:.6f}°")
                self.longitude_var.set(f"{longitude:.6f}°")
                self.lat_dms_var.set(self.decimal_to_dms(latitude, is_latitude=True))
                self.long_dms_var.set(self.decimal_to_dms(longitude, is_latitude=False))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")

    def convert_from_dms(self):
        try:
            lat_dms = self.lat_dms_var.get()
            long_dms = self.long_dms_var.get()
            if lat_dms and long_dms:
                latitude = self.dms_to_decimal(lat_dms)
                longitude = self.dms_to_decimal(long_dms)
                self.latitude_var.set(f"{latitude:.6f}º")
                self.longitude_var.set(f"{longitude:.6f}º")
                zone, easting, northing, north_or_south = self.latlong_to_utm(latitude, longitude)
                self.zone_var.set(zone)
                self.easting_var.set(f"{easting:.4f}")
                self.northing_var.set(f"{northing:.4f}")
                self.north_or_south_var.set(north_or_south)
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def convert_from_latlong(self):
        try:
            lat_decimal = self.latitude_var.get().rstrip('º')
            long_decimal = self.longitude_var.get().rstrip('º')
            lat_dms = self.decimal_to_dms(float(lat_decimal), is_latitude=True)
            long_dms = self.decimal_to_dms(float(long_decimal), is_latitude=False)
            self.lat_dms_var.set(lat_dms)
            self.long_dms_var.set(long_dms)
            zone, easting, northing, north_or_south = self.latlong_to_utm(float(lat_decimal), float(long_decimal))
            self.zone_var.set(zone)
            self.easting_var.set(f"{easting:.4f}")
            self.northing_var.set(f"{northing:.4f}")
            self.north_or_south_var.set(north_or_south)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Resto del código


    def utm_to_latlong(self, zone, easting, northing, north_or_south):
        p = Proj(proj="utm", zone=zone, south=True if north_or_south == "Sur" else False)
        longitude, latitude = p(easting, northing, inverse=True)
        return latitude, longitude

    def latlong_to_utm(self, latitude, longitude):
        p = Proj(proj="utm", zone=self.zone_var.get(), south=True if self.north_or_south_var.get() == "Sur" else False)
        easting, northing = p(longitude, latitude)
        return self.zone_var.get(), easting, northing, self.north_or_south_var.get()

    def decimal_to_dms(self, decimal_degrees, is_latitude=True):
        degrees = int(decimal_degrees)
        minutes_float = (decimal_degrees - degrees) * 60
        minutes = int(minutes_float)
        seconds = (minutes_float - minutes) * 60

        if is_latitude:
            direction = "N" if degrees >= 0 else "S"
        else:
            direction = "E" if degrees >= 0 else "O"

        return f"{abs(degrees)}°{minutes}'{seconds:.2f}\"{direction}"

    def dms_to_decimal(self, dms_string):
        pattern = re.compile(r'''(\d+)°\s*(\d+)'\s*([\d\.]+)"\s*([NSOE])''', re.IGNORECASE)
        match = pattern.match(dms_string)
        if match:
            degrees = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3))
            direction = match.group(4).upper()

            decimal_degrees = degrees + minutes / 60 + seconds / 3600
            if direction in ['S', 'O']:
                decimal_degrees = -decimal_degrees

            return decimal_degrees
        else:
            raise ValueError("Formato DMS inválido")

    def paste_from_clipboard(self, var):
        try:
            clipboard_text = self.root.clipboard_get()
            var.set(clipboard_text)
        except tk.TclError:
            pass  # No se pudo obtener el texto del portapapeles

    def copy_to_clipboard(self, var):
        self.root.clipboard_clear()
        self.root.clipboard_append(var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordenadasApp(root)
    root.mainloop()
