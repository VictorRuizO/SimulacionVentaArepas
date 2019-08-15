
import random
import simpy
import numpy

########################################################################################################################
# Variables en entrada

SEMILLA = 40  # Semilla generador

TIEMPO_SIMULACION = 480  # Tiempo de la simulacion 8 Horas = 480 min

LLEGADA_CLIENTES = 4  # Clientes llegan de acuerdo a una distribucion exponencial con media 4 minutos

ATENCION_CLIENTES_NONE = 15  # Clientes que no realiza ninguna compra son atendidos en una distribucion
                             # exponencial con media 1,5 minutos

ATENCION_CLIENTES_TODO = [5,10]  # Clientes que compran arepas con todoo son atendidos en una distribucion
                                 # uniforme entre 5 y 10 minutos

ATENCION_CLIENTES_BEBE = [3,7]  # Clientes que compran arepas para bebe son atendidos en una distribucion
                                # uniforme entre 3 y 7 minutos

ATENCION_CLIENTES_MORCILLA = 6  # Clientes que compran arepas con morcilla son atendidos en una distribucion
                                # exponencial con media 6 minutos

########################################################################################################################
# Variables desempeño
COLA = 0
MAX_COLA = 0
ESPERA_CLIENTES = numpy.array([])

########################################################################################################################
def llegada(env, numero, contador):
    for i in range(numero):
        c = cliente(env, 'Cliente %02d' % i, contador)
        env.process(c)
        tiempo_llegada = random.uniform(LLEGADA_CLIENTES[0], LLEGADA_CLIENTES[1])
        yield env.timeout(tiempo_llegada)  # Yield retorna un objeto iterable


def cliente(env, nombre, servidor):
    # El cliente llega y se va cuando es atendido
    llegada = env.now
    print('%7.2f' % (env.now), " Llega el cliente ", nombre)
    global COLA
    global MAX_COLA
    global ESPERA_CLIENTES
    # Atendemos a los clientes (retorno del yield)
    # With ejecuta un iterador sin importar si hay excepciones o no
    with servidor.request() as req:
        # Hacemos la espera hasta que sea atendido el cliente
        COLA += 1
        if COLA > MAX_COLA:
            MAX_COLA = COLA

        # print("Tamaño cola", COLA)
        results = yield req
        COLA = COLA - 1
        espera = env.now - llegada
        ESPERA_CLIENTES = numpy.append(ESPERA_CLIENTES, espera)

        print('%7.2f' % (env.now), " El cliente ", nombre, " espera a ser atendido ", espera)

        tiempo_atencion = random.uniform(ATENCION_CLIENTES[0], ATENCION_CLIENTES[1])
        yield env.timeout(tiempo_atencion)

        print('%7.2f' % (env.now), " Sale el cliente ", nombre)


# Inicio de la simulación

print('Sala de cine')
random.seed(SEMILLA)
env = simpy.Environment()

# Inicio del proceso y ejecución
servidor = simpy.Resource(env, capacity=1)
env.process(llegada(env, CLIENTES, servidor))
env.run()

print("Cola máxima ", MAX_COLA)
print("Tiempo promedio de espera ", '%7.2f' % (numpy.mean(ESPERA_CLIENTES)))