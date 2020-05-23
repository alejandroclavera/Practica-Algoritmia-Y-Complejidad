# Documentación Práctica ALGORITMIA Y COMPLEJIDAD

## Índice 
1. Introducción 
2. Módulo Preprocesamiento
3. Módulo Alineamiento
4. Módulo Clustering

## 1. Introducción 
El objetivo de esta práctica es, dada una lista de muestras del COVID-19 de diferentes paises, agrupar a estas segun su similitud.

A lo largo de este documento, se iran comentando y analizando los costes de los principales alogritmos de los diferentes modulos de la práctica.

La practica ha sido dividida en los siguientes modulos:
1. Preprocesamiento
2. Alineamiento (alineamiento de secuencias)
3. Clustering (clasificación)

## 2. Modulo Preprocesamiento
La función de este modulo es leer una lista de muestras de un fichero csv y obtener la muestra mediana de cada pais.

Para realizar esta operación, se han implementado principalmente las siguientes funciónes:

* **load_regions**: Esta función lee el fichero de las muestras y obtiene los diferentes paises en forma de un dicciónario, donde cada clave es una pais.

* **load_samples_of_csv**: La tarea de esta función es la de obtener las muestras de cada pais, esta a igual que la función anterior devuelve un diccionario donde cada clave en un pais y el valor es un diccionario con las muestras del pais.

* **get_median_samples_of_csv**: El objetivo de esta función obtener la muestra mediana de cada pais leido del csv.

* **median**: Esta función calcula la mediana de un pais.

La función load_regions, ha sido implementada para mejorar el coste computacional de la función load_samples_of_csv. Como se nombrado anterior mente ha decidido que las muestras estaran estructuradas en un diccionario con todos los paises y cada pais tendra un subdiccionario con sus muestras. Para hacer esto antes de añadir una muestra a cada pais se ha de estar seguro que el subdicionario esta creado, el hecho de implementar load_regions nos permite olvidarnos de eso ya que este en monento que lee los paises esta ya crea sus subdiccionarios. Realizado de esta forma obtenemos un coste en el peor de los casos de O(n * max(m)), siendo n el número de paises y m el número de muestra de cada pais.

Otra forma de implementarlo seria mirando antes si ya se ha leido una muestra del pais, si no es asi primero se crea el subdicionario y a continuación se añade la muestra. Aunque esta solición es menor eficiente que la anterior, donde su coste es O((n^2) * max(m)) ya que se esta buscando si el pais ya esta en el diccionario.

## 3. Modulo Alineamiento
La tarea principal de este modulo, es alinear cada secuncia con todas la demas.

Las principales funciones que encontramos en este modulo son:
* **calc_needleman_score**: Función encargada de obtener la alineación optima de dos secuencias, para esto se utiliza el algoritmo de Needleman–Wunsch.
* **get_scores**: Esta función se encarga de alinear cada secuncia con todas la demas.

### 3.1 calc_needleman_score
Para implementar esta función cabe destacar el uso del lenguaje C, ya ejecución en python del algoritmo resulta costosa.

Cuando el algoritmo comienza, calcula las puntuaciones de la primera columna y de la primera fila de la matriz de puntuaciones, esto tiene un coste de m + n + 1, ya que la matriz es de tamaño (m + 1) x (n + 1). 

A la hora de la implementación se ha tenido en cuenta que la primera puntuacion de la primera fila no se ha de calcular ya que se ha calculado con anterioridad  en la primera columna.

Una vez calcula la primera fila y columna, se calcula las m * n puntuaciones restantes.

Con toda la información comentada anteriormente podemos llegar a la conclusión de que el coste es (m * n) + m + n + 1. 

### 3.2 get_scores
Esta función se encarga de realizar el aliniamiento de todas la cadenas ARN. 

Para realiar esta operación se utiliza una matriz de k * k elementos donde k es el numero de cadenas de arn. 

En cada posición de la matriz se almacena la puntuacion del aliniamiento optimo de dos secuencias. Los indices de cada posición representan la muestra

El algoritmo consiste 


coste_comparaciones =  (k(k-1)/2)*(n*m n + m)











