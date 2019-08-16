# -*- coding: utf-8 -*-
import random
from builtins import print

import simpy
import numpy

########################################################################################################################
# Variables en entrada

SEMILLA = 40                    # Semilla generador
TIEMPO_SIMULACION = 480         # Tiempo de la simulacion 8 Horas = 480 min
LLEGADA_CLIENTES = 4            # Clientes llegan de acuerdo a una distribucion exponencial con media 4 minutos

ATENCION_CLIENTES_NONE = 15     # Clientes que no realiza ninguna compra son atendidos en una distribucion
                                # exponencial con media 1,5 minutos

ATENCION_CLIENTES_TODO = [5,10] # Clientes que compran arepas con todoo son atendidos en una distribucion
                                # uniforme entre 5 y 10 minutos

ATENCION_CLIENTES_BEBE = [3,7]  # Clientes que compran arepas para bebe son atendidos en una distribucion
                                # uniforme entre 3 y 7 minutos

ATENCION_CLIENTES_MORCILLA = 6  # Clientes que compran arepas con morcilla son atendidos en una distribucion
                                # exponencial con media 6 minutos

UTILIDAD_AREPAS_TODO = 750.0    # Utilidad que tiene las arepas con todoo
UTILIDAD_AREPAS_BEBE = 550.0    # Utilidad que tiene las arepas para el bebe
UTILIDAD_AREPAS_MORCILLA = 750.0# Utilidad que tiene las arepas con morcilla

########################################################################################################################
# Variables estado
COLA = 0
ESPERA_CLIENTES = numpy.array([])

########################################################################################################################
# Variables desempeño
MAX_COLA = 0
PROMEDIO_ESPERA = 0.0

########################################################################################################################
# Funciones utlizadas
def llegadaCliente(env,servidor):
    i=1
    while env.now<60:
        print('%7.2f'%env.now,"Llega el cliente ",i)
        process = accionCliente(env,servidor,i)
        env.process(process)
        nextCliente = numpy.random.exponential(scale=LLEGADA_CLIENTES)
        yield env.timeout(5)
        i+=1



def accionCliente(env,servidor,numero):
    global COLA
    with servidor.request() as req:
        COLA+=1
        r = yield req

        COLA-=1

        yield env.timeout(8)
        print('%7.2f' % (env.now), " Sale el cliente ", numero)


########################################################################################################################
# Inicio de la simulacion

print('Venta de Arepas')
random.seed(SEMILLA)
env = simpy.Environment()

# Inicio del proceso y ejecución
servidor = simpy.Resource(env, capacity=1)
env.process(llegadaCliente(env, servidor))
env.run()

#print("Cola máxima ", MAX_COLA)
#print("Tiempo promedio de espera ", '%7.2f' % (numpy.mean(ESPERA_CLIENTES)))