from model.modello import Model
mymdl = Model()

mymdl.creaG("light", 28, -132)
print(mymdl.creaG("light", 28, -132))

nodi, archi, s, v = mymdl.stampa()
print(f"Grafo creato! Il grafo ha {nodi} nodi e {archi} archi.")
