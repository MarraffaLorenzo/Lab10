from database.DB_connect import DBConnect
from model.hub import Hub
from model.spedizione import Spedizione
from model.compagnia import Compagnia
from model.tratta import Tratta


class DAO:

    @staticmethod
    def get_all_hubs():
        """
        Restituisce tutti gli hub
        :return: un dizionario di tutti gli hub
        """
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM hub"""

        cursor.execute(query)

        for row in cursor:
            result[row["id"]] = Hub(**row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_spedizioni():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM spedizione"""  # la tabella delle spedizioni

        cursor.execute(query)

        for row in cursor:
            result.append(Spedizione(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_compagnie():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM compagnia"""

        cursor.execute(query)

        for row in cursor:
            result.append(Compagnia(**row))

        cursor.close()
        conn.close()
        return result

    # Tratte V1: aggregazione per direzione (avremo entry A->B e B->A separate)
    @staticmethod
    def get_all_tratte_v1():
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT 
                        id_hub_origine      AS h1,
                        id_hub_destinazione AS h2,
                        SUM(valore_merce)   AS valore_totale,
                        COUNT(*)            AS n_spedizioni
                    FROM spedizione
                    GROUP BY id_hub_origine, id_hub_destinazione
                    """

        cursor.execute(query)

        for row in cursor:
            h1, h2 = sorted([row["h1"], row["h2"]])
            if (h1, h2) in result:
                result[h1, h2].valore_totale += row["valore_totale"]
                result[h1, h2].n_spedizioni += row["n_spedizioni"]
            else:
                result[h1, h2] = Tratta(h1, h2, row["valore_totale"], row["n_spedizioni"])
        cursor.close()
        conn.close()
        return result.values()

    # Tratte V2: aggregazione simmetrica (A<->B unite). Uso LEAST/GREATEST per rendere il grafo non orientato.
    @staticmethod
    def get_all_tratte_v2():

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT
                        LEAST(id_hub_origine, id_hub_destinazione)      AS h1,
                        GREATEST(id_hub_origine, id_hub_destinazione)   AS h2,
                        SUM(valore_merce)                               AS valore_totale,
                        COUNT(*)                                        AS n_spedizioni
                    FROM spedizione
                    GROUP BY h1, h2
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(**row))

        cursor.close()
        conn.close()
        return result