import simpy # Libreria para realizar simulaciones
import random # Libreria numeros aleatorios python
import numpy as np # Libreria para trabajar con listas
import matplotlib.pyplot as pp # Libreria para graficar

# TIEMPO_TRAMITE = [720, 60, 60, 240, 30, 60, 240, 30, 600, 1200, 480, 240] 
# El siguiente listado es un diccionario cuya clave son lon nombres de los trámites y el valor es el tiempo de duracion de los mismos 
#la libreria trabaja los valores en minutos  simpy
TIEMPO_TRAMITE = {
    'Capacitacion temas tributarios': 720, # 12hrs
    'Determinar necesidades del contribuyente': 60, # 1hrs
    'Ingreso de contribuyentes a la base de datos': 60, # 1hrs
    'Asesoramiento individual sobre derechos y oblicgaciones tributarias': 240, # 4hrs
    'Recepcion de documentos tributarios': 30, # 0.3hrs
    'Analisis de documentos tributarios': 60, # 1hrs
    'Llenado de formularios en el sri': 240, # 4hrs
    'Entrega de declaraciones y documentacion al contribuyente': 30, # 0.5hrs
    'Determinar los grupos vulnerables': 600, # 10hrs
    'Preparacion de talleres de capacitacion': 1200, # 20hrs
    'Ejecucion de talleres de capacitacion': 480, # 8hrs
    'Promocion de servicios tributarios': 240, # 4hrs
}

INTERVALO_LLEGADA = 96 # Frecuencia de llegada de clientes a la oficia tributaria

tramites = {} # Clasifica por nombre de tramite y cuenta cuantos trámites de ese tipo han hecho 

total_tiempo_tramites = 0 # Es el total global de todas las pasantias que se han realizado 

contador_de_tramites = 0 # cuenta el total de trámites que se han realizado en una  simulación de la pasantía  


# Es una representación de la oficina tributaria como objeto entro de la simulacón 
class OficinaTributariaUC(object):

    # init :Inicia las variables de la oficina tributaria 
    def __init__(self, environment, max_estudiantes, tiempo_tramite):
        self.env = environment # Entorno de ejecucion de la simulación 
        self.estudiantes = simpy.Resource(environment, max_estudiantes) # Pasantes trabajando en la oficina
        self.tiempo_tramite = tiempo_tramite # Duracion de pasantia(160/96)

    # Se cuenta, se acumula y se clasifican los trámites de cliente que llega que se efectúan en la simulación 
    def atendiendo_tramite(self, cliente):
        global total_tiempo_tramites
        global contador_de_tramites
        
        tramite = np.random.choice(list(TIEMPO_TRAMITE.keys()), 1)[0] # Escogemos un tramite al azar
        duracion = TIEMPO_TRAMITE[tramite]/60
        print(
            f'{cliente} entra a realizar: {tramite} y tomara un tiempo de {duracion}hrs.')

        total_tiempo_tramites += duracion # acumula la duración en el total global de todos los estudiantes 
        contador_de_tramites += 1 # va a contar todos los trámites que han hecho los estudiantes 


        yield self.env.timeout(int(TIEMPO_TRAMITE[tramite])) # Estudiante realizar el tramite solicitado
        
        # Clasificas y contar por duracion los trámites    
        k = duracion
        if k in tramites:
            tramites[k] = tramites[k]+1
        else:
            tramites[k] = 1

# Asigna un cliente a un estudiante que esté libre
# env: entorno de ejecuión
# cliente: persona que requiere el servicio
# oficina: lugar de gestion de trámites 
def llegada_cliente(env, cliente, oficina):
    with oficina.estudiantes.request() as estudiante: # Solicita estudiante libre
        yield estudiante # Designa un estudiate
        yield env.process(oficina.atendiendo_tramite(cliente)) # Asigna estudiante al tramite

# Inicia con el proceso de la oficina
def ejecutar_simulacion(env, max_estudiantes, max_clientes, tiempo_tramite, intervalo):
    oficina = OficinaTributariaUC(env, max_estudiantes, tiempo_tramite) # Apertura oficina
    for i in range(max_clientes):
        env.process(llegada_cliente(env, 'Cliente-%d' % (i+1), oficina))

    # Este bucle va a permitir que los clientes sigan llegando a la oficina mientras no se cumpla la meta de 800 clientes
    while True:
        yield env.timeout(random.randint(intervalo-10, intervalo+10)) # Frecuencia de llegada de los clientes
        i += 1
        env.process(llegada_cliente(env, 'Cliente-%d' % (i+1), oficina))

# Establece las variables para iniciar con la simulacion, muestra resultados 
def run(max_estudiantes, tiempo_pasantia, max_clientes):
    # Variables globales utilizadas para recopilar informacion de la simulacion
    global tramites
    global total_tiempo_tramites
    global contador_de_tramites

    env = simpy.Environment() # Se crea el entorno de ejecucion de simpy
    # Hace que simpy ejecute la simulación 
    env.process(ejecutar_simulacion(env, max_estudiantes,
                max_clientes, TIEMPO_TRAMITE, INTERVALO_LLEGADA))

    print('*'*50)
    print(f'Tiempo de pasantia: {tiempo_pasantia/60}'.upper())
    env.run(until=tiempo_pasantia)

    # Generamos la grafica
    datos = sorted(tramites.items())
    x, y = zip(*datos)
    print(f'Cantidad de alumnos: {max_estudiantes}\n')
    # total horas, total clientes
    print(f'Cantidad de clientes que deberia atender: {max_clientes}\n')
    # total horas, total clientes
    promedio_duracion_tramite = total_tiempo_tramites / contador_de_tramites
    print(f'Cantidad de tramites realizados: {contador_de_tramites}\n')
    print(
        f'Duracion promedio por tramite: {promedio_duracion_tramite:.2f} horas')
    print(f'Horas cumplidas: {total_tiempo_tramites}\n'.upper())

    pp.bar(x, y, width=1, linewidth=2, color='red')
    pp.grid(True)
    pp.show()

    aux_tramites = contador_de_tramites

    tramites = {}
    total_tiempo_tramites = 0
    contador_de_tramites = 0

    return max_clientes, aux_tramites
