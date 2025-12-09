import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        threshold = self._view.guadagno_medio_minimo.value
        try:
            min_value = float(threshold)
        except (ValueError, TypeError):
            self._view.show_alert("Valore numerico non valido per il guadagno medio minimo (€).")
            return

        # Costruisce il grafo filtrando le tratte con guadagno medio >= min_value
        self._model.costruisci_grafo(min_value)

        self._view.lista_visualizzazione.controls.clear()
        self._view.lista_visualizzazione.controls.append(ft.Text("Numero di Hubs: " + str(self._model.get_num_nodes())))
        self._view.lista_visualizzazione.controls.append(
            ft.Text("Numero di Tratte: " + str(self._model.get_num_edges())))

        all_edges = self._model.get_all_edges()
        for i, (u, v, attr) in enumerate(all_edges, start=1):
            weight = attr.get("weight") if attr else None
            if weight is None:
                display_weight = "N/A"
            else:
                display_weight = f"€ {weight:.2f}"
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{i}) [{u} -> {v}] -- guadagno Medio Per Spedizione: {display_weight}")
            )

        self._view.update()
