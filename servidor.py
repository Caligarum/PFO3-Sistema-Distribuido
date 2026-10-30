import socket
import json
from concurrent.futures import ThreadPoolExecutor

HOST = "localhost"
PUERTO = 5000

MAX_CLIENTES = 10
MAX_WORKERS = 4

# Pool encargado de procesar las tareas
worker_pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)


def procesar_tarea(tarea):
    """
    Función ejecutada por los workers.
    Recibe una tarea y devuelve el resultado.
    """

    tipo = tarea.get("tipo")
    datos = tarea.get("datos")

    if tipo == "SUMAR":
        resultado = sum(datos)

    elif tipo == "MAYUSCULAS":
        resultado = str(datos).upper()

    elif tipo == "LONGITUD":
        resultado = len(str(datos))

    else:
        return {
            "estado": "error",
            "mensaje": "Tipo de tarea desconocido"
        }

    return {
        "estado": "ok",
        "resultado": resultado
    }


def manejar_cliente(cliente, direccion):
    print(f"Cliente conectado: {direccion}")

    try:
        # makefile permite trabajar línea por línea
        archivo = cliente.makefile("r")

        while True:
            linea = archivo.readline()

            if not linea:
                break

            tarea = json.loads(linea)

            print(f"Tarea recibida de {direccion}: {tarea}")

            # Se envía la tarea a un worker
            futuro = worker_pool.submit(procesar_tarea, tarea)

            # Esperamos el resultado
            resultado = futuro.result()

            respuesta = json.dumps(resultado) + "\n"

            cliente.sendall(respuesta.encode())

    except json.JSONDecodeError:
        respuesta = {
            "estado": "error",
            "mensaje": "JSON inválido"
        }

        cliente.sendall(
            (json.dumps(respuesta) + "\n").encode()
        )

    except Exception as error:
        print(f"Error con {direccion}: {error}")

    finally:
        cliente.close()
        print(f"Cliente desconectado: {direccion}")


def iniciar_servidor():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:

        servidor.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        servidor.bind((HOST, PUERTO))
        servidor.listen()

        print(f"Servidor escuchando en {HOST}:{PUERTO}")
        print(f"Workers disponibles: {MAX_WORKERS}")

        # Pool para atender varios clientes
        with ThreadPoolExecutor(max_workers=MAX_CLIENTES) as clientes_pool:

            while True:

                cliente, direccion = servidor.accept()

                clientes_pool.submit(
                    manejar_cliente,
                    cliente,
                    direccion
                )


if __name__ == "__main__":
    iniciar_servidor()