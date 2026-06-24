import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.lat = None
        self.lon = None
        self.minLa, self.maxLa = self._model.getLA()
        self.minLo, self.maxLo = self._model.getLO()
        self.shape = None
        self.shapes = None

    def scegliValori(self):
        self.lat = self._view.txt_latitude.value
        self.lon= self._view.txt_longitude.value
        print(f"lat={self.lat}, lon={self.lon}")
        print(f"minLa={self.minLa}, maxLa={self.maxLa}")
        print(f"minLo={self.minLo}, maxLo={self.maxLo}")

        if self.lat is None or self.lon is None:
            print("RETURN: valori None")
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("valori nulli, riprova"))
            self._view.update_page()
            return False

        try:
            self.lat = float(self.lat)
            self.lon = float(self.lon)
        except ValueError:
            print("RETURN: ValueError")
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("valore non numerico"))
            self._view.update_page()
            return False

        if self.lat < self.minLa or self.lat > self.maxLa:
            print("RETURN: lat fuori range")
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("valori di lat fuori dal range"))
            self._view.update_page()
            return False
        if self.lon < self.minLo or self.lon > self.maxLo:
            print("RETURN: lon fuori range")
            #self._view.txt_result1.controls.clear()
            #self._view.txt_result1.controls.append(ft.Text("valori di lo fuori dal range"))
            self._view.create_alert("valori di lo fuori dal range")
            self._view.update_page()
            return False
        print("scegliValori OK")
        self._view.update_page()
        return True

    def fill_ddshape(self):
        self.shapes = self._model.getS()
        print(f"Shapes: {self.shapes}")
        print(f"Lunghezza: {len(self.shapes)}")
        for shape in self.shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(key = str(shape),
                                                                 text = str(shape)))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if not self.scegliValori():
            return
        self.shape = self._view.ddshape.value
        if self.shape is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("scegli shape"))
            return
        self._model.creaG(self.shape, self.lat, self.lon)
        self._view.update_page()
        nodi, archi, lista, pesi = self._model.stampa()
        self._view.txt_result1.controls.append(ft.Text(f"nodi: {nodi}, archi: {archi}"))
        for l in lista:
            self._view.txt_result1.controls.append(ft.Text(f"{l.id}"))
        for p in pesi:
            self._view.txt_result1.controls.append(ft.Text(f"{p[0]} - {p[1]} - {p[2]}"))

        self._view.btn_path.disabled = False
        self._view.update_page()



    def handle_path(self, e):
        best, costo = self._model.cerca()
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"punteggio: {costo}"))
        for s in best:
            densita = s.Population/s.Area
            self._view.txt_result2.controls.append(ft.Text(f"{s.id} - {s.Name} - {densita}"))
        self._view.update_page()