import socket
import json

HOST = "localhost"
PUERTO = 5000


def enviar_tarea(cliente, tarea):

    mensaje = json.dumps(tarea) + "\n"

    cliente.sendall(mensaje.encode())

    archivo = cliente.makefile("r")

    respuesta = archivo.readline()

    return json.loads(respuesta)


def iniciar_cliente():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:

        try:
            cliente.connect((HOST, PUERTO))

            print("Conectado al servidor distribuido.")
            print()
            print("Tareas disponibles:")
            print("1 - SUMAR")
            print("2 - MAYUSCULAS")
            print("3 - LONGITUD")
            print("4 - SALIR")

            while True:

                opcion = input("\nSeleccione una opción: ")

                if opcion == "1":

                    numeros = input(
                        "Ingrese números separados por espacios: "
                    )

                    datos = [
                        float(numero)
                        for numero in numeros.split()
                    ]

                    tarea = {
                        "tipo": "SUMAR",
                        "datos": datos
                    }

                elif opcion == "2":

                    texto = input("Ingrese un texto: ")

                    tarea = {
                        "tipo": "MAYUSCULAS",
                        "datos": texto
                    }

                elif opcion == "3":

                    texto = input("Ingrese un texto: ")

                    tarea = {
                        "tipo": "LONGITUD",
                        "datos": texto
                    }

                elif opcion == "4":

                    print("Cliente finalizado.")
                    break

                else:

                    print("Opción incorrecta.")
                    continue

                respuesta = enviar_tarea(
                    cliente,
                    tarea
                )

                if respuesta["estado"] == "ok":

                    print(
                        "Resultado:",
                        respuesta["resultado"]
                    )

                else:

                    print(
                        "Error:",
                        respuesta["mensaje"]
                    )

        except ConnectionRefusedError:

            print(
                "No se pudo conectar con el servidor."
            )

        except Exception as error:

            print(f"Error: {error}")


if __name__ == "__main__":
    iniciar_cliente()