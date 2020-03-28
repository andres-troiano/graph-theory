# Redes Complejas

En este trabajo se analizan distintas redes (redes de interacción proteína-proteína, redes sociales, redes de colaboraciones científicas) utilizando herramientas de Redes Complejas, área de investigación relativamente joven (años 2000) de la que fueron pioneros László Barabási y Mark Newman entre otros.

## Parte 1
En esta sección se estudian 3 redes de interacciones entre proteínas, las cuales están en la carpeta "dataset". Estas 3 redes corresponden al mismo organismo (levadura) pero fueron relevadas de distintas maneras:

* ``yeast_Y2H.txt``: red de interacciones binarias
* ``yeast_AP-MS.txt``: red de copertenencia a complejos proteicos
* ``yeast_LIT.txt``: red relevada de la literatura

En el script ``parte_1.py`` se desarrolla el siguiente análisis:
En primer lugar se grafica cada red representándola con un grafo, donde cada nodo es una proteína y cada vértice representa una interacción. Para mayor claridad sólo se graficó la componente conexa más grande, como se muestra a continuación:

![red Y2H](./images/red_Y2H.png)
![red AP-MS](./images/red_AP-MS.png)
![red LIT](./images/red_LIT.png)
