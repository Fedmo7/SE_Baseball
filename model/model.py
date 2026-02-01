
from database.dao import DAO
import networkx as nx




class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.lista_archi=[]
        self.dizionario_nodi_creati={}
        self.nodo = None



    def take_years(self):

        self.lista_archi = DAO.query_year()
        return self.lista_archi



    def take_nodi(self,year):

        self.dizionario_nodi_creati = DAO.query_team(year)

        return self.dizionario_nodi_creati


    def crea_grafo(self):

        self.G.clear()


        for n in self.dizionario_nodi_creati.values():
            self.G.add_node(n)


        for n1 in self.dizionario_nodi_creati.values():
            for n2 in self.dizionario_nodi_creati.values():

                peso=n1.salary+n2.salary
                self.G.add_edge(n1,n2,weight=peso)



    def trova_squadre_adiacenti(self,key):

        self.nodo=self.dizionario_nodi_creati[int(key)]

        lista_vicini=self.G.neighbors(self.nodo)
        lista_vicini_con_peso=[]

        for n in lista_vicini:
            peso=self.G[self.nodo][n]['weight']
            lista_vicini_con_peso.append((n,peso))

        return lista_vicini_con_peso

    def get_best_path(self, key):
        self.best_path = []
        self.best_peso_totale = 0

        start_node = self.dizionario_nodi_creati[int(key)]

        self._ricorsione([start_node], 0, float('inf'))

        return self.best_path, self.best_peso_totale


    def _ricorsione(self, parziale, peso_parziale, ultimo_peso_arco):
        # 1. Aggiornamento del Best (Peso massimo)

        if peso_parziale > self.best_peso_totale:
            self.best_path = list(parziale)
            self.best_peso_totale = peso_parziale

        ultimo_nodo = parziale[-1]

        # 2. Recupero vicini con i relativi pesi degli archi
        vicini_pesati = []
        for vicino in self.G.neighbors(ultimo_nodo):
            if vicino not in parziale:
                peso_arco = self.G[ultimo_nodo][vicino]['weight']
                # Vincolo: peso strettamente decrescente rispetto all'arco precedente
                if peso_arco < ultimo_peso_arco:
                    vicini_pesati.append((vicino, peso_arco))

        # 3. Ordinamento decrescente per peso dell'arco
        vicini_pesati.sort(key=lambda x: x[1], reverse=True)

        # 4. Esplorazione limitata ai primi K=3 vicini più pesanti
        K = 3
        for vicino, peso in vicini_pesati[:K]:
            parziale.append(vicino)
            self._ricorsione(parziale, peso_parziale + peso, peso)
            parziale.pop()  # Backtracking



