import networkx as nx
from database.dao import DAO



class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.lista_nodi_creati=[]
        self.dizionario_squadra_year={}
        self.nodi_map={}


    def take_years(self):

        lista_anni=DAO.query_year()
        return lista_anni


    def take_all_team(self,year):

        self.dizionario_squadra_year=DAO.get_all_team(year)
        print(self.dizionario_squadra_year)



    def build_graph(self):

        # TODO

        self.G.clear()

        for squadra1 in self.dizionario_squadra_year.values():
            for squadra2 in self.dizionario_squadra_year.values():

                if squadra1==squadra2:
                    continue

                else:
                    peso=squadra1.salary+squadra2.salary
                    self.G.add_edge(squadra1, squadra2,weight=peso)

        print(self.G.number_of_nodes())
        print(self.G.number_of_edges())

    def trova_miglior_percorso(self, start_nodo):
        self.soluzione_best = []
        self.peso_ottimo = 0
        # Iniziamo la ricorsione
        self._ricorsione([start_nodo], peso_precedente=float('inf'), peso_totale=0)
        return self.soluzione_best

    def _ricorsione(self, percorso_corrente, peso_precedente, peso_totale):
        # Salva il percorso migliore trovato finora
        if peso_totale > self.peso_ottimo:
            self.soluzione_best =percorso_corrente.copy()
            self.peso_ottimo = peso_totale

        nodo_ultimo = percorso_corrente[-1]

        vicini_validi = []
        k = 0

        for v in self.G.neighbors(nodo_ultimo):
            if k==3:
                break

            elif v not in percorso_corrente:
                peso_arco = self.G[nodo_ultimo][v]["weight"]
                if peso_arco < peso_precedente:
                    vicini_validi.append((v, peso_arco))
                    k+=1

        # Strategia K=3
        vicini_validi.sort(key=lambda x: x[1], reverse=True)

        for vicino, peso in vicini_validi:
            if peso<=peso_precedente:

                percorso_corrente.append(vicino)
                self._ricorsione(percorso_corrente, peso, peso_totale + peso)
                print('A')
                percorso_corrente.pop()
'''
    def trova_miglior_percorso(self,start_nodo):

        self.soluzione_best = []
        self.peso_ottimo =0
        self._ricorsione([start_nodo],peso_corrente=float('inf'),peso_totale=0)
        return self.soluzione_best

    def _ricorsione(self,percorso_corrente,peso_corrente,peso_totale):

        if  peso_totale> self.peso_ottimo:
            self.soluzione_best = percorso_corrente.copy()
            self.peso_ottimo = peso_corrente

        nodo_partenza=percorso_corrente[-1]
        lista_nodi_vicini=self.G.neighbors(nodo_partenza)
        lista_vicini_ordinati=[]

        for v in lista_nodi_vicini:
            peso = self.G.edges[(nodo_partenza, v)]["weight"]
            lista_vicini_ordinati.append((v, peso))

        # ordino per peso crescente
        lista_vicini_ordinati.sort(key=lambda x: x[1],reverse=True)
        k=0

        for arco in lista_vicini_ordinati:
            if k==3:
                break
            else:
                if peso_corrente>=float(arco[1]) and arco[0] not in percorso_corrente:
                    k+=1
                    percorso_corrente.append(arco[0])
                    peso_nuovo=arco[1]
                    self._ricorsione(percorso_corrente,peso_nuovo,peso_totale+peso_nuovo)
                    percorso_corrente.pop()

'''

