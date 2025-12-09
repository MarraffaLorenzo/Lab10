from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        self.G.clear()
        self._nodes = DAO.get_all_hubs()  # dizionario di Hub

        # lista di Tratte aggregate con valore_totale, n_spedizioni, valore_medio
        # self._edges = DAO.get_all_tratte_v1() # aggregazione usando Python ***
        self._edges = DAO.get_all_tratte_v2()  # aggregazione usando SQL ***

        self.G.add_nodes_from(self._nodes.values())  # Aggiunge tutti i nodi disponibili

        for edge in self._edges:  # un edge è una tratta
            w = edge.get_valore_medio()  # peso = guadagno medio per spedizione)
            h1_object = self._nodes[edge.h1]
            h2_object = self._nodes[edge.h2]
            if w >= threshold:
                self.G.add_edge(h1_object, h2_object, weight=w)
                print("Edge Aggiunto", edge)

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return self.G.edges(data=True)
