#Ejercicio de laberintos
import numpy as np
import random

#Definir rod con su orientación
class Rod:
    def __init__(self):
        self.orientacion = 'horizontal'
        self.posicion = (0, 1)
        
rod = Rod()

#Función que indique si el rod puede estar en esa ubicación
def pos_valida(orientacion, x, y, labyrinth_np):
    shape = labyrinth_np.shape

    if orientacion == 'horizontal' and 0 <= x < shape[0] and 1 <= y < shape[1] - 1: #Verificar que esté dentro del laberinto
        if '#' not in labyrinth_np[x, y - 1:y + 2]: #Verificar que no haya # en su ubicación
            return True
    if orientacion == 'vertical' and 1 <= x < shape[0] - 1 and 0 <= y < shape[1]: #Verificar que esté dentro del laberinto
        if '#' not in labyrinth_np[x - 1:x + 2, y]: #Verificar que no haya # en su ubicación
            return True
        
    return False

#Función que indique si el rod puede girar
def giro_valido(x, y, labyrinth_np):
    shape = labyrinth_np.shape
    
    if 0 < x < shape[0]-1 and 0 < y < shape[1] - 1 and '#' not in list(labyrinth_np[x - 1:x + 1, y - 1:y + 2].flatten()) + [labyrinth_np[x - 1, y - 1], labyrinth_np[x - 1, y + 1], labyrinth_np[x + 1, y - 1], labyrinth_np[x + 1, y + 1]]:
        return True
    
    return False

#Función para mover el rod
def movimientos( moves, pos_pasadas,x1, y1, orientacion, labyrinth_np, loops):
    x_list = [x1, x1, x1 + 1, x1 - 1, x1]
    y_list = [y1 + 1, y1 - 1, y1, y1, y1]
    giro_list = [False, False, False, False, True]
    
    for x, y, giro in zip (x_list, y_list, giro_list):   
    
        if pos_valida(orientacion, x, y, labyrinth_np) == True and loops != -1:
            if (x, y, orientacion) not in pos_pasadas.keys():
                moves += 1
                pos_pasadas[(x, y, orientacion)] = moves
                loops = -1
        if giro_valido(x, y, labyrinth_np) == True and loops != -1 and giro == True: # Girar
            if orientacion == 'horizontal' and (x, y, 'vertical') not in pos_pasadas.keys():
                moves += 1
                orientacion = 'vertical'
                pos_pasadas[(x, y, orientacion)] = moves
                loops = -1
            elif orientacion == 'vertical' and (x, y, 'horizontal') not in pos_pasadas.keys():
                moves += 1
                orientacion = 'horizontal'
                pos_pasadas[(x, y, orientacion)] = moves
                loops = -1
        if orientacion == 'horizontal' and (x, y, 'vertical') in pos_pasadas.keys() and moves < pos_pasadas[(x, y, 'vertical')] and loops == -1 and giro == True:
            orientacion = 'vertical'
            pos_pasadas[(x, y, orientacion)] = moves
        elif orientacion == 'vertical' and (x, y, 'horizontal') in pos_pasadas.keys() and moves < pos_pasadas[(x, y, 'horizontal')] and loops == -1 and giro == True:
            orientacion = 'horizontal'
            pos_pasadas[(x, y, orientacion)] = moves
        elif (x, y, orientacion) in pos_pasadas.keys() and moves < pos_pasadas[(x, y, orientacion)] and loops == -1 and giro == False: #Si se puede llegar a la posición con menos movimientos
            pos_pasadas[(x, y, orientacion)] = moves
            
    return  moves, pos_pasadas,x, y, orientacion

def solution(labyrinth):
    moves = 0
    pos_pasadas = {(0, 1, 'horizontal'):0} #va a tener la estructura {'posición':'# de movimientos'}
    x, y = rod.posicion
    orientacion = rod.orientacion
    labyrinth_np = np.array(labyrinth)
    shape = labyrinth_np.shape
    
    #Empezar a mover el rod
    for loops in range(0, shape[0] * shape[1]):

        pos_pasadas_init = list(pos_pasadas.keys())
        for x1, y1, orientacion1 in pos_pasadas_init:
            moves, pos_pasadas,x, y, orientacion = movimientos(pos_pasadas[(x1, y1, orientacion1)], pos_pasadas,x1, y1, orientacion1, labyrinth_np, loops)
    
    moves_list = [] #Guardar lista de movimientos en caso de que haya más de una solución
    for x, y, orientacion in list(pos_pasadas.keys()):
        if (x == shape[0] - 1 and y == shape[1] - 2 and orientacion == 'horizontal') or (x == shape[0] - 2 and y == shape[1] - 1 and orientacion == 'vertical'):
            moves_list.append(pos_pasadas[x, y, orientacion])
    if moves_list:
        return min(moves_list)
    else:
        return -1
    

labyrinth = [[".",".",".",".",".",".",".",".","."],
["#",".",".",".","#",".",".",".","."],
[".",".",".",".","#",".",".",".","."],
[".","#",".",".",".",".",".","#","."],
[".","#",".",".",".",".",".","#","."]]

labyrinth1 = [[".",".",".",".",".",".",".",".","."],
["#",".",".",".","#",".",".","#","."],
[".",".",".",".","#",".",".",".","."],
[".","#",".",".",".",".",".","#","."],
[".","#",".",".",".",".",".","#","."]]

labyrinth2 = [[".",".","."],
[".",".","."],
[".",".","."]]


labyrinth3 = [[".",".",".",".",".",".",".",".",".","."],
[".","#",".",".",".",".","#",".",".","."],
[".","#",".",".",".",".",".",".",".","."],
[".",".",".",".",".",".",".",".",".","."],
[".",".",".",".",".",".",".",".",".","."],
[".","#",".",".",".",".",".",".",".","."],
[".","#",".",".",".","#",".",".",".","."],
[".",".",".",".",".",".","#",".",".","."],
[".",".",".",".",".",".",".",".",".","."],
[".",".",".",".",".",".",".",".",".","."]]

c = 0
for i in [labyrinth, labyrinth1, labyrinth2, labyrinth3]:
    solucion = solution(i)
    print('solución del laberinto {}: '.format(c), solucion)
    c += 1