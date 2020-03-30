# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pylab as plt
import numpy as np
import scipy.stats as st
import os

basepath = 'C:\\Users\\username\\python_scripts\\Redes-Complejas'
os.chdir(basepath)

import modulo_redes as mr

files = ["./dataset/as-22july06.gml", "./dataset/netscience.gml"]

for f in files:
    tag = mr.split(f, ("/", "."))[3] # para identificar la red
    print(tag)

    G = nx.read_gml(f)
    
    k_dv = G.degree() # esto es un DegreeView
    k_dict = dict(k_dv)
    k_array = np.array(list(k_dv)) # al usar un array, las dos cosas (etiqueta y grado) tienen que ser del mismo tipo. En este caso quedan como str. Cuando necesite los grados voy a tener que usar int
    
    # %%
    
    # esta lista tiene en la 1er columna la cantidad de vecinos de un nodo, y en la columna 2 el grado medio de esos vecinos
    k_medio_vecinos = np.zeros(k_array.shape)
    
    for i in range(k_array.shape[0]):
        nodo = k_array[i] # [etiqueta del nodo, grado del nodo]
        
        vecinos = list(G.neighbors(nodo[0]))
        
        N = len(vecinos)
        # ojo: hay nodos aislados, para los que N=0
        if N == 0:
            continue
        grado_acumulado = 0
        for v in vecinos:
            # calculo el promedio de los grados de los vecinos de este nodo
            grado_acumulado = grado_acumulado + k_dict.get(v)
        k_medio = grado_acumulado/N
        k_medio_vecinos[i] = (k_dict.get(nodo[0]), k_medio)
        
    # %%
    
    k_max = k_dict[max(k_dict, key=k_dict.get)] # grado máximo
    
    # éste es el promedio de los k_medio_vecinos
    k_medio_vecinos_medio = np.zeros(k_max)
    
    for k in range(1,k_max+1):
        # el primer grado es k=1, y va en el índice 0
        k_medio_vecinos_medio[k-1] = np.mean(k_medio_vecinos[k_medio_vecinos[:, 0] == k, 1])
        
    ind = np.logical_not(np.isnan(k_medio_vecinos_medio))
    arange_k = np.arange(1,k_max+1) # todos los grados entre 1 y el máximo, existan o no en el grafo
    
    ax = plt.gca()
    plt.grid('on')
    ax.set_axisbelow(True)
    ax.scatter(k_medio_vecinos[:,0], k_medio_vecinos[:,1], marker='o', s=20, edgecolor='black')
    ax.scatter(arange_k[ind], k_medio_vecinos_medio[ind], marker='o', s=20, c='r', edgecolor='black')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel('grado')
    plt.ylabel('grado medio de los vecinos')
    plt.suptitle(tag)
    plt.savefig('./images/grado_medio_vecinos_' + tag + '.png')
    plt.show()
    plt.close()
    
    # ahora aplicamos log a los datos y volvemos a escala lineal para hacer un ajuste lineal
    arange_k_log = np.log10(arange_k[ind])
    k_medio_vecinos_medio_log = np.log10(k_medio_vecinos_medio[ind])
    
    # %%
    
    slope, intercept, r_value, p_value, std_err = st.linregress(arange_k_log, k_medio_vecinos_medio_log)
    fit = slope*arange_k_log + intercept
    
    plt.figure(1)
    plt.plot(arange_k_log, k_medio_vecinos_medio_log, '.r')
    plt.plot(arange_k_log, fit, 'b--')
    plt.xlabel('log(grado)')
    plt.ylabel('log(grado medio de los vecinos)')
    plt.suptitle(tag)
    plt.grid('on')
    plt.savefig('./images/grado_medio_vecinos_ajuste_' + tag + '.png')
    plt.show()
    plt.close()
    
    # %% calculo es estimador de Newman (ecs. 8.26 - 8.29 de su libro)
    
    # la documentación dice que esto devuelve un EdgeView, sin embargo esto es una lista (?)
    edges = G.edges()
    
    s = 0
    for e in edges:
        # pido el grado de cada nodo. Esto no lo puedo vectorizar
        s = s + G.degree(e[0])*G.degree(e[1])
    
    Se = 2*s
    
    # armo una lista que tiene todos los grados (en int), sin los labels de los nodos
    grado = np.array([int(numeric_string) for numeric_string in k_array[:,1]],dtype='int64')
    
    S1 = sum(grado)
    S2 = sum(grado**2)
    S3 = sum(grado**3)
    
    # estimador de Newman
    r = (S1*Se - S2**2)/(S1*S3 - S2**2)
    print('Estimador de Newman: %.2f' % (r))
    print('Pendiente ajuste: %.2f' % (slope))
