from sim import * # Invocando a la simulacion, main es el que llama a la simulación 
import random # Libreria numeros aleatorios python

MAX_CLIENTES = 800 # Meta de clientes por atender
MAX_ESTUDIANTES = 31 # Grupo de estudiantes (pasantes)
TIEMPO_PASANTIA = [9600, 5760] # Duracion de pasantias en minutos (160hrs y 96hrs)
# r: coeficiente de asignación basado en el tiempo de duracion de las pasantias, y a signa en porcentaje el maximo de clientes 
#y determina el porcentaje del total de estudiantes 
r = 0.65
#r = random.random()
# c1 y c2 diferencia el porcentaje de clientes que corresponde en base al coeficiente r 
c1 = int(MAX_CLIENTES*r)
c2 = MAX_CLIENTES - c1

if c1 > c2:
    clientes = [c1, c2]
else:
    clientes = [c2, c1]
# e1 y e2 diferencia el porcentaje de clientes que corresponde en base al coeficiente r 
e1 = int(MAX_ESTUDIANTES*r)
e2 = MAX_ESTUDIANTES - e1

if e1 > e2:
    estudiantes = [e1, e2]
else:
    estudiantes = [e2, e1]

# idx = random.randint(0, 1)
# index = [idx, 0 if idx == 1 else 1]

# Acumula los totalizados de cada tipo de pasantía , luego de que se ejecutan las simulaciones de 160 y 96
acum_clientes = 0
acum_horas = 0

# Primero va a ejecutar las pasantias de : 160 h y luego la de 96 h  
for i in range(2):
    # print(index[i])
    max_clientes, horas = run(
        estudiantes[i], TIEMPO_PASANTIA[i], clientes[i])
    acum_clientes += max_clientes
    acum_horas += horas

print('\n')
print('-'*50)
print(f'Meta de clientes a atender: {acum_clientes}')
print(f'Total de clientes atendidos: {acum_horas}')
print('-'*50)
