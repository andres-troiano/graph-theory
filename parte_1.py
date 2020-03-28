import networkx as nx # librería de redes y grafos
import matplotlib.pylab as plt
from modulo_redes import *

# Tengo 3 redes de interacciones de proteínas, pero relevadas de diferentes maneras.

# datos
basepath = "./dataset/"
files = ["yeast_Y2H.txt", "yeast_LIT.txt", "yeast_AP-MS.txt"]

resultados = ("FILE", "N", "L", "k_medio", "k_max", "k_min", "densidad", "C_global", "C_local", "diametro")
print("%-10s "*len(resultados) % resultados)
print(len(resultados)*11*"=")

for f in files:

    datos = ldata(basepath + f)
    G = nx.Graph()
    G.add_edges_from(datos)
    
    tag = split(f, ("_", "."))[1]

    # calculo N
    N = G.number_of_nodes()

    # calculo L
    L = G.number_of_edges()

    # k medio
    k_medio = 2*L/N

    # k max y min
    grado = G.degree()
    grado_2 = [grados[1] for grados in grado]
    k_max = max(grado_2)
    k_min = min(grado_2)

    # densidad
    densidad = nx.density(G)

    # coeficientes de clustering.
    c_global = nx.transitivity(G)
    c_local = nx.average_clustering(G)
    
    # diametro
    # componente gigante
    lcc = max(nx.connected_components(G), key=len)
    # grafo inducido
    lcc_g = G.subgraph(lcc).copy()
    diametro = nx.diameter(lcc_g)
    
    # grafico la componente gigante
    nx.draw(lcc_g, node_size=10)
    #plt.show()
    plt.savefig("./figura_" + tag)
    plt.close()
    
    # imprimo las variables
    print("%-10s %-10d %-10d %-10.1f %-10d %-10d %-10.3f %-10.2f %-10.2f %-10d" % (tag, N, L, k_medio, k_max, k_min, densidad, c_global, c_local, diametro))
