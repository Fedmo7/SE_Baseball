import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.squadra=None




    def take_year(self):
        lista_anni=self._model.take_years()
        self._view.dd_anno.options=[ft.dropdown.Option(a) for a in lista_anni]
        self._view.dd_anno.update()

    def get_year_selected(self,e):

        year=e.control.value
        self._model.take_all_team(year)
        self.squadre_for_year()

    def squadre_for_year(self):

        self.squadre_anno=self._model.dizionario_squadra_year.copy()
        self._view.txt_out_squadre.controls.clear()
        for squadra in self.squadre_anno.values():
            self._view.txt_out_squadre.controls.append(ft.Text(f'{squadra}'))

        self._view.page.update()


    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO

        self._model.build_graph()
        self._view.dd_squadra.options.clear()
        self._view.dd_squadra.options=[ft.dropdown.Option(key=str(s.id), text=s) for s in self._model.dizionario_squadra_year.values()]
        self._view.dd_squadra.update()





    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO

        squadra_id = int(self._view.dd_squadra.value)
        self.squadra=self.squadre_anno[squadra_id]


        lista_vicini=list(self._model.G.neighbors(self.squadra))
        vicini_pesati=[]
        for v in lista_vicini:
            peso = self._model.G.edges[(self.squadra, v)]["weight"]
            vicini_pesati.append((v, peso))

        # ordino per peso crescente
        vicini_pesati.sort(key=lambda x: x[1],reverse=True)

        self._view.txt_risultato.controls.clear()
        for vicino, peso in vicini_pesati:
            self._view.txt_risultato.controls.append(ft.Text(f"{vicino} - peso {peso}"))

        self._view.txt_risultato.update()

    def handle_percorso(self, e):
        id_selezionato = self._view.dd_squadra.value

        if id_selezionato is None:
            self._view.show_alert("Seleziona prima una squadra dal menu!")
            return

        # Trasformo l'ID della UI in oggetto Team
        squadra_partenza = self._model.dizionario_squadra_year.get(int(id_selezionato))

        if squadra_partenza is None:
            print("Errore: Squadra non trovata nel dizionario")
            return

        # Chiamo la ricorsione nel modello
        percorso = self._model.trova_miglior_percorso(squadra_partenza)

        # Pulizia e visualizzazione
        self._view.txt_risultato.controls.clear()

        if not percorso:
            self._view.txt_risultato.controls.append(ft.Text("Nessun percorso trovato."))
        else:
            self._view.txt_risultato.controls.append(
                ft.Text(f"Percorso trovato! Peso totale: {self._model.peso_ottimo}")
            )
            for s in percorso:
                self._view.txt_risultato.controls.append(ft.Text(f"{s}"))

        self._view.page.update()
