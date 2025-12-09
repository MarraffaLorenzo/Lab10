from dataclasses import dataclass
from model.hub import Hub

@dataclass
class Tratta:
    h1: Hub
    h2: Hub
    valore_totale: float   # somma del valore delle spedizioni
    n_spedizioni: int      # numero di spedizioni tra gli hub

    def get_valore_medio(self):
        return float(self.valore_totale / self.n_spedizioni) if self.n_spedizioni > 0 else 0.0