import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.dizionario_team={}




    def get_all_years(self):

        lista_anni=self._model.take_years()
        return lista_anni


    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO

        year = self._view.dd_anno.value

        if year is None:
            self._view.show_alert("Errore: selezionare un anno.")
            return

        self.dizionario_team = self._model.take_nodi(year)
        print(self.dizionario_team)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f'Numero squadre: {len(self.dizionario_team.values())}'))
        for team in self.dizionario_team:
            squadra=self.dizionario_team[team]
            self._view.txt_out_squadre.controls.append(
                ft.Text(f'{squadra.team_code} ({squadra.team_name})'))

        self._view.update()


        self._model.crea_grafo()


        self._view.dd_squadra.options = [ft.dropdown.Option(key=t.id, text=t.team_name) for t in self.dizionario_team.values()]
        self._view.update()



    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO

        key=self._view.dd_squadra.value

        if key is None:
            self._view.show_alert("Errore: selezionare una squadra.")
            return

        lista_team_peso=self._model.trova_squadre_adiacenti(key)

        for tupla in lista_team_peso:

            self._view.txt_risultato.controls.append(ft.Text(f'{tupla[0].team_code}({tupla[0].team_name})-peso({tupla[1]})'))

        self._view.page.update()

    def handle_percorso(self, e):

        id_partenza = self._view.dd_squadra.value

        if id_partenza is None:
            self._view.show_alert("Errore: selezionare un elemento di partenza.")
            return


        path, peso_totale = self._model.get_best_path(id_partenza)

        self._view.txt_risultato.controls.clear()

        if not path or len(path) < 2:
            self._view.txt_risultato.controls.append(ft.Text("Nessun percorso trovato."))
        else:

            for i in range(len(path) - 1):
                nodo_u = path[i]
                nodo_v = path[i + 1]

                # Recupero il peso dell'arco dal grafo G
                peso_arco = self._model.G[nodo_u][nodo_v]['weight']

                # Formattazione stringa: Squadra1 -> Squadra2 (peso XXX)
                riga = f"{nodo_u.team_name} -> {nodo_v.team_name} (peso {peso_arco})"
                self._view.txt_risultato.controls.append(ft.Text(riga))

            # 4. Aggiungo il peso totale in fondo
                self._view.txt_risultato.controls.append(ft.Text(f"Peso totale: {peso_totale}"))

        self._view.page.update()
