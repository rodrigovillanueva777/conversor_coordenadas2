import ttkbootstrap as tb
from ttkbootstrap.constants import SUCCESS

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ejemplo de Botones Success")

        # Iconos (asegúrate de tener los archivos "maps_icon.png" y "earth_icon.png")
        self.maps_icon = tb.PhotoImage(file="maps_icon.png")
        self.earth_icon = tb.PhotoImage(file="earth_icon.png")

        # Botón para abrir en Google Maps
        self.open_in_google_maps_button = tb.Button(
            root, 
            image=self.maps_icon, 
            command=self.open_in_google_maps, 
            bootstyle=SUCCESS
        )
        self.open_in_google_maps_button.grid(row=11, column=1, columnspan=1, padx=10, pady=10)

        # Botón para crear archivo KML y abrir en Google Earth
        self.open_in_google_earth_button = tb.Button(
            root, 
            image=self.earth_icon, 
            command=self.create_kml_and_open_in_google_earth, 
            bootstyle=SUCCESS
        )
        self.open_in_google_earth_button.grid(row=11, column=2, columnspan=2, padx=10, pady=10)

    def open_in_google_maps(self):
        print("Abrir en Google Maps")

    def create_kml_and_open_in_google_earth(self):
        print("Crear archivo KML y abrir en Google Earth")

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")  # Cambia el tema si prefieres otro
    app = App(root)
    root.mainloop()
