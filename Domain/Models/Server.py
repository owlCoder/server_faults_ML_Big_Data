import uuid

class Server:
    def __init__(self, naziv, lista_otkaza=None):
        self.id_servera = str(uuid.uuid4())
        self.naziv = naziv
        self.lista_otkaza = lista_otkaza if lista_otkaza is not None else []

    def dodaj_otkaz(self, otkaz_id):
        if isinstance(otkaz_id, int):
            self.lista_otkaza.append(otkaz_id)
        else:
            raise ValueError("ID must be primary key!")

    def __str__(self):
        return ("ID: " + self.id_servera + "\n" + self.naziv
                + "\nFaulty Times: " + len(self.lista_otkaza).__str__() + "\n")