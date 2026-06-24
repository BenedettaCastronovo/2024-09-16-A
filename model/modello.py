import copy

from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self.g = nx.Graph()
        self.mappan = {}
        self.best = {}
        self.costo = 0
        pass

    def getLO(self):
        lon = DAO.getLo()
        return min(lon), max(lon)

    def getLA(self):
        lat = DAO.getLa()
        return min(lat), max(lat)

    def getS(self):
        return DAO.getS()

    def creaG(self, s, lat, lon):
        self.g.clear()
        self.n = DAO.getN(s,lat,lon)
        for n in self.n:
            self.mappan[n.id] = n
        self.a = DAO.getA(s,lat,lon, self.mappan)
        for arco in self.a:
            self.g.add_edge(arco.id1, arco.id2, weight=arco.peso)

    def len(self):
        return len(self.g.nodes), len(self.g.edges)


    def stampa(self):
        lista = sorted(self.g.nodes(), key= lambda n: self.g.degree[n], reverse=True)
        pes = sorted(self.g.edges(data=True), key= lambda n: n[2]["weight"], reverse=True)
        return len(self.g.nodes()), len(self.g.edges()), lista[:5], pes[:5]

    def cerca(self):
        self.best = {}
        self.costo = 0
        self.nodi = list(self.g.nodes())
        for n in self.nodi:
            parziale = [n]
            self.ric(parziale, self.nodi)
            #parziale.pop() qua non serve perche al ciclo successivo è gia vuota
        return self.best, self.costo

    def ric(self, parziale, nodi):
        if len(parziale) >= 2 and self.costoC(parziale) > self.costo:
            self.best = copy.deepcopy(parziale)
            self.costo = self.costoC(parziale)
            #return #bloccava i percorsi piu lunghi

        for n in self.g.neighbors(parziale[-1]):
            if n not in parziale and self.is_valid(n, parziale):
              parziale.append(n)
              self.ric(parziale, self.nodi)
              parziale.pop()

    def is_valid(self, n, parziale):
        if len(parziale) == 0:
            return True
        densita = n.Population/n.Area
        if densita > (parziale[-1].Population/parziale[-1].Area):
            return True

        return False

    def costoC(self, parziale):
        somma = 0
        distanza = 0
        for i in range(0, len(parziale)-1):
            somma += self.g[parziale[i]][parziale[i+1]]["weight"]
            distanza += parziale[i].distance_HV(parziale[i+1])
        return float(somma/distanza)



