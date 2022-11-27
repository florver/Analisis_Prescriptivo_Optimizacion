# -*- coding: utf-8 -*-
"""4. Práctica Programación Lineal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q3GzkW0jzNT7lGiXZtq2AWX5hN2DItuE

##Link para acceder al código en colab

https://colab.research.google.com/drive/1q3GzkW0jzNT7lGiXZtq2AWX5hN2DItuE?usp=sharing

# Práctica Programación Lineal
"""

#pip install --upgrade --user ortools
!pip install ortools

import numpy as np
import time
import ortools
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit
import networkx as nx
from networkx.algorithms import bipartite

"""## Punto 1 
**Crear diversas instancias con varios depósitos y locales para experimentar.**

Llamaremos $D_{1}$, $D_{2}$, ..., $D_{n}$ al listado de posibles depósitos de los cuales puede partir la mercadería a transportar. En cada uno habra un determinado stock de los productos $A$, $B$ y $C$. Los productos deberán ser transportados a los locales $L_{1}$, $L_{2}$, ... $L_{N}$ de acuerdo a su demanda.

Para empezar el problema podemos pensar un ejemplo en donde tengamos dos depósitos y dos posibles locales. La representación sería la siguiente:
"""

B = nx.Graph()
B.add_nodes_from(["A_D0", "A_D1","B_D0", "B_D1","C_D0", "C_D1"], bipartite=0)
B.add_nodes_from(["L0", "L1"], bipartite=1)

B.add_edges_from([("A_D0", "L0"), ("A_D0", "L1"), ("A_D1", "L0"), ("A_D1", "L1"),("B_D0", "L0"), ("B_D0", "L1"), ("B_D1", "L0"), ("B_D1", "L1"),("C_D0", "L0"), ("C_D0", "L1"), ("C_D1", "L0"), ("C_D1", "L1")])
RB_top = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
RB_bottom = set(B) - RB_top

val_map = {'A_D0': 1.0,
           'A_D1': 1.0,
           'B_D0': 0.5714285714285714,
           'B_D1': 0.5714285714285714,
           'C_D0': 0.3,
           'C_D1': 0.3,}

values = [val_map.get(node, 0.25) for node in B.nodes()]

nx.draw_networkx(B,pos = nx.drawing.layout.bipartite_layout(B, RB_top), node_color=values)

"""## Punto 2
**Modelar mediante Programación Lineal el problema de transporte propuesto.**

La siguiente modelación representa el problema de transporte: 

***Funcion objetivo:*** $Min \sum_{i = 0}^n \sum_{j = 0}^m A_{ij} * x_{ij} + B_{ij} * x_{ij} + C_{ij} * x_{ij}$

Siendo $A_{ij}$ , $B_{ij}$ y $C_{ij}$ la cantidad transportada de cada producto del depósito $i$ al local $j$. 
Siendo $x_{ij}$ el costo asociado a transportar una unidad de producto del depósito $i$ al local $j$. 

***Restricciones:*** 
\begin{align*}
A_{ij} \le S_{A} \\
B_{ij} \le S_{B} \\
C_{ij} \le S_{C} \\
\end{align*}
</center>
- Restricciones de Demanda:
\begin{align*}
\sum_{i = 0}^n A_{ij} \ge Dem_{A_j} \\
\sum_{i = 0}^n B_{ij} \ge Dem_{B_j} \\
\sum_{i = 0}^n C_{ij} \ge Dem_{C_j} \\
\end{align*}
</center>
- Restricciones de Stock:
\begin{align*}
\sum_{j = 0}^m A_{ij} \ge S_{A_i} \\
\sum_{j = 0}^m B_{ij} \ge S_{B_i} \\
\sum_{j = 0}^m C_{ij} \ge S_{C_i} \\
\end{align*}
</center>

## Punto 3
**Modelar mediante Programación Lineal el problema de transporte propuesto.**

En primera instancia modelamos el problema con Google Or Tools para el caso de tener solamente dos depósitos con dos locales posibles:
"""

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    # Creación de variables
    a_d1_l1 = solver.NumVar(0, 15, 'a_d1_l1')
    a_d2_l1 = solver.NumVar(0, 15, 'a_d2_l1')
    a_d1_l2 = solver.NumVar(0, 15, 'a_d1_l2')
    a_d2_l2 = solver.NumVar(0, 15, 'a_d2_l2')
    b_d1_l1 = solver.NumVar(0, 24, 'b_d1_l1')
    b_d2_l1 = solver.NumVar(0, 18, 'b_d2_l1')
    b_d1_l2 = solver.NumVar(0, 24, 'b_d1_l2')
    b_d2_l2 = solver.NumVar(0, 18, 'b_d2_l2')
    c_d1_l1 = solver.NumVar(0, 12, 'c_d1_l1')
    c_d2_l1 = solver.NumVar(0, 16, 'c_d2_l1')
    c_d1_l2 = solver.NumVar(0, 12, 'c_d1_l2')
    c_d2_l2 = solver.NumVar(0, 16, 'c_d2_l2')


    print('Number of variables =', solver.NumVariables())

    # Restricción de demanda: a_d1_l1 + a_d2_l1 >= demanda_a_l1
    
    demanda_a_l1 = solver.Constraint(10, solver.infinity(), 'demanda_a_l1')
    demanda_a_l1.SetCoefficient(a_d1_l1, 1)
    demanda_a_l1.SetCoefficient(a_d2_l1, 1)
    
    demanda_b_l1 = solver.Constraint(14, solver.infinity(), 'demanda_b_l1')
    demanda_b_l1.SetCoefficient(b_d1_l1, 1)
    demanda_b_l1.SetCoefficient(b_d2_l1, 1)

    demanda_c_l1 = solver.Constraint(9, solver.infinity(), 'demanda_c_l1')
    demanda_c_l1.SetCoefficient(c_d1_l1, 1)
    demanda_c_l1.SetCoefficient(c_d2_l1, 1)
    
    demanda_a_l2 = solver.Constraint(18, solver.infinity(), 'demanda_a_l2')
    demanda_a_l2.SetCoefficient(a_d1_l2, 1)
    demanda_a_l2.SetCoefficient(a_d2_l2, 1)

    demanda_b_l2 = solver.Constraint(16, solver.infinity(), 'demanda_b_l2')
    demanda_b_l2.SetCoefficient(b_d1_l2, 1)
    demanda_b_l2.SetCoefficient(b_d2_l2, 1)

    demanda_c_l2 = solver.Constraint(12, solver.infinity(), 'demanda_c_l2')
    demanda_c_l2.SetCoefficient(c_d1_l2, 1)
    demanda_c_l2.SetCoefficient(c_d2_l2, 1)

    # Restricción de stock: 0 =< a_d1_l1 + a_d1_l2 <= stock_a_d1

    stock_a_d1 = solver.Constraint(0, 15, 'stock_a_d1')
    stock_a_d1.SetCoefficient(a_d1_l1, 1)
    stock_a_d1.SetCoefficient(a_d1_l2, 1)

    stock_b_d1 = solver.Constraint(0, 24, 'stock_b_d1')
    stock_b_d1.SetCoefficient(b_d1_l1, 1)
    stock_b_d1.SetCoefficient(b_d1_l2, 1)

    stock_c_d1 = solver.Constraint(0, 12, 'stock_c_d1')
    stock_c_d1.SetCoefficient(c_d1_l1, 1)
    stock_c_d1.SetCoefficient(c_d1_l2, 1)    

    
    stock_a_d2 = solver.Constraint(0, 15, 'stock_a_d2')
    stock_a_d2.SetCoefficient(a_d2_l1, 1)
    stock_a_d2.SetCoefficient(a_d2_l2, 1)

    stock_b_d2 = solver.Constraint(0, 18, 'stock_b_d2')
    stock_b_d2.SetCoefficient(b_d2_l1, 1)
    stock_b_d2.SetCoefficient(b_d2_l2, 1)

    stock_c_d2 = solver.Constraint(0, 16, 'stock_c_d2')
    stock_c_d2.SetCoefficient(c_d2_l1, 1)
    stock_c_d2.SetCoefficient(c_d2_l2, 1)


    print('Number of constraints =', solver.NumConstraints())

    # Creación de función objetivo
    objective = solver.Objective()
    objective.SetCoefficient(a_d1_l1, 5)
    objective.SetCoefficient(a_d2_l1, 7)
    objective.SetCoefficient(b_d1_l1, 5)
    objective.SetCoefficient(b_d2_l1, 7)
    objective.SetCoefficient(c_d1_l1, 5)
    objective.SetCoefficient(c_d2_l1, 7)
    objective.SetCoefficient(a_d1_l2, 6)
    objective.SetCoefficient(a_d2_l2, 8)
    objective.SetCoefficient(b_d1_l2, 6)
    objective.SetCoefficient(b_d2_l2, 8)
    objective.SetCoefficient(c_d1_l2, 6)
    objective.SetCoefficient(c_d2_l2, 8)
    objective.SetMinimization()

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    print('a_d1_l1 =', a_d1_l1.solution_value())
    print('a_d2_l1 =', a_d2_l1.solution_value())
    print('a_d1_l2 =', a_d1_l2.solution_value())
    print('a_d2_l2 =', a_d2_l2.solution_value())
    print('b_d1_l1 =', b_d1_l1.solution_value())
    print('b_d2_l1 =', b_d2_l1.solution_value())
    print('b_d1_l2 =', b_d1_l2.solution_value())
    print('b_d2_l2 =', b_d2_l2.solution_value())
    print('c_d1_l1 =', c_d1_l1.solution_value())
    print('c_d2_l1 =', c_d2_l1.solution_value())
    print('c_d1_l2 =', c_d1_l2.solution_value())
    print('c_d2_l2 =', c_d2_l2.solution_value())
    
    

if __name__ == '__main__':
    pywrapinit.CppBridge.InitLogging('basic_example.py')
    cpp_flags = pywrapinit.CppFlags()
    cpp_flags.logtostderr = True
    cpp_flags.log_prefix = False
    pywrapinit.CppBridge.SetFlags(cpp_flags)
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

"""Generalizamos el problema para que dependa del input de una matriz de costos, los valores de demanda y de stock de cada deposito y local por producto: """

costs = np.array([
    [5, 6], #d1_l1, d1_l2
    [7, 8]  #d2_l1, d2_l2
])

end_nodes_unraveled, start_nodes_unraveled = np.meshgrid(np.arange(costs.shape[1]),np.arange(costs.shape[0]))
start_nodes = start_nodes_unraveled.ravel()
end_nodes = end_nodes_unraveled.ravel()
arc_costs = costs.ravel()

lista_productos = ['a','b','c']
stock = [15,15,24,18,12,16] #[a_d1, a_d2, ..., a_dn, b_d1, b_d2, ..., b_dn]
stock_repeated = np.repeat(stock, len(list(set(end_nodes)))).tolist()
demanda = [10,18,14,16,9,12] # [a_l1, a_l2, ..., a_ln, b_l1, b_l2, ..., b_ln]

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    # Creación de las variables
    s = 0

    for producto in lista_productos: 
      for i in range(len(start_nodes)):
        exec(producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + '= solver.NumVar(0,' + str(stock_repeated[s]) + ',"' + producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + '")')
        s = s + 1 


    print('Number of variables =', solver.NumVariables())

    # Restricción de demanda, a_d1_l1 + a_d2_l1 >= demanda_a_l1.
    i = 0
    for producto in lista_productos: 
      for locales in list(set(end_nodes)): 
        exec('demanda_' + producto + '_'+ str(locales) + '= solver.Constraint(' +  str(demanda[i]) + ', solver.infinity(), "demanda_' + producto + '_' + str(locales) + '")')
        i = i + 1
        for deposito in list(set(start_nodes)): 
          exec('demanda_' + producto + '_'+ str(locales) + '.SetCoefficient(' + producto +'_' + str(deposito) + '_' + str(locales) + ',1)')


    # Restricción de stock, 0 =< a_d1_l1 + a_d1_l2 <= stock_a_d1.

    i = 0
    for producto in lista_productos: 
      for deposito in list(set(start_nodes)): 
        exec('stock_' + producto + '_'+ str(deposito) + ' = solver.Constraint(' +  '0,' + str(stock[i]) +',"stock_' + producto + '_' + str(deposito) + '")')
        i = i + 1
        for locales in list(set(end_nodes)): 
          exec('stock_' + producto + '_'+ str(deposito) + '.SetCoefficient(' + producto +'_' + str(deposito) + '_' + str(locales) + ',1)') 


    print('Number of constraints =', solver.NumConstraints())

    # Creación de la funcion objetivo
    objective = solver.Objective()
    for producto in lista_productos:
      for i in range(len(start_nodes)):
        exec('objective.SetCoefficient(' + producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + ',' + str(arc_costs[i]) + ')')
    objective.SetMinimization()

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    for producto in lista_productos: 
      for i in range(len(start_nodes)):
        exec('print("'+producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + ' =", ' + producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + '.solution_value())')
        s = s + 1 
    
    

if __name__ == '__main__':
    pywrapinit.CppBridge.InitLogging('basic_example.py')
    cpp_flags = pywrapinit.CppFlags()
    cpp_flags.logtostderr = True
    cpp_flags.log_prefix = False
    pywrapinit.CppBridge.SetFlags(cpp_flags)
    # get the start time
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

"""## Punto 4
**Experimentar con las instancias para analizar los tiempos de cómputo
requeridos para resolver el problema con diferentes cantidades de depósitos y
locales.**

Creamos una instancia donde se corra con 3 depósitos y 4 locales para ver como se modifica el tiempo de ejecución:
"""

costs = np.array([
    [5, 6, 7, 3],  #d1_l1, d1_l2, d1_l3, d1_l4
    [7, 8, 8, 4],  #d2_l1, d2_l2, d2_l3, d2_l4
    [9, 4, 9, 5]   #d3_l1, d3_l2, d3_l3, d3_l4
])

end_nodes_unraveled, start_nodes_unraveled = np.meshgrid(np.arange(costs.shape[1]),np.arange(costs.shape[0]))
start_nodes = start_nodes_unraveled.ravel()
end_nodes = end_nodes_unraveled.ravel()
arc_costs = costs.ravel()

lista_productos = ['a','b','c']
stock = [20, 10, 20, 24, 18, 12, 12, 16, 15] #[a_d1, a_d2, ..., a_dn, b_d1, b_d2, ..., b_dn]
stock_repeated = np.repeat(stock, len(list(set(end_nodes)))).tolist()
demanda = [10, 18, 8, 9, 14, 16, 10, 12, 9, 12 , 4, 15] # [a_l1, a_l2, ..., a_ln, b_l1, b_l2, ..., b_ln]

start_nodes

end_nodes

stock_repeated

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    # Creación de las variables
    s = 0

    for producto in lista_productos: 
      for i in range(len(start_nodes)):
        exec(producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + '= solver.NumVar(0,' + str(stock_repeated[s]) + ',"' + producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + '")')
        s = s + 1 


    print('Number of variables =', solver.NumVariables())

    # Restricción de demanda, a_d1_l1 + a_d2_l1 >= demanda_a_l1.
    i = 0
    for producto in lista_productos: 
      for locales in list(set(end_nodes)): 
        exec('demanda_' + producto + '_'+ str(locales) + '= solver.Constraint(' +  str(demanda[i]) + ', solver.infinity(), "demanda_' + producto + '_' + str(locales) + '")')
        i = i + 1
        for deposito in list(set(start_nodes)): 
          exec('demanda_' + producto + '_'+ str(locales) + '.SetCoefficient(' + producto +'_' + str(deposito) + '_' + str(locales) + ',1)')


    # Restricción de stock, 0 =< a_d1_l1 + a_d1_l2 <= stock_a_d1.

    i = 0
    for producto in lista_productos: 
      for deposito in list(set(start_nodes)): 
        exec('stock_' + producto + '_'+ str(deposito) + ' = solver.Constraint(' +  '0,' + str(stock[i]) +',"stock_' + producto + '_' + str(deposito) + '")')
        i = i + 1
        for locales in list(set(end_nodes)): 
          exec('stock_' + producto + '_'+ str(deposito) + '.SetCoefficient(' + producto +'_' + str(deposito) + '_' + str(locales) + ',1)') 


    print('Number of constraints =', solver.NumConstraints())

    # Creación de la funcion objetivo
    objective = solver.Objective()
    for producto in lista_productos:
      for i in range(len(start_nodes)):
        exec('objective.SetCoefficient(' + producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + ',' + str(arc_costs[i]) + ')')
    objective.SetMinimization()

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    for producto in lista_productos: 
      for i in range(len(start_nodes)):
        exec('print("'+producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + ' =", ' + producto + '_' + str(start_nodes[i]) + '_' +str(end_nodes[i]) + '.solution_value())')
        s = s + 1 
    
    

if __name__ == '__main__':
    pywrapinit.CppBridge.InitLogging('basic_example.py')
    cpp_flags = pywrapinit.CppFlags()
    cpp_flags.logtostderr = True
    cpp_flags.log_prefix = False
    pywrapinit.CppBridge.SetFlags(cpp_flags)
    # get the start time
    st = time.time()
    main()
    et = time.time()
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')