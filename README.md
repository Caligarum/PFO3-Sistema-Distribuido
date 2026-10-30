# PFO 3 - Sistema Distribuido Cliente-Servidor

## Descripción

Implementación de un sistema distribuido cliente-servidor utilizando **sockets TCP en Python**.

El cliente envía tareas al servidor, el servidor las recibe y las distribuye entre distintos workers mediante un `ThreadPoolExecutor`.

## Archivos

```text
servidor.py
cliente.py
README.md
```

## Funcionamiento

El sistema permite ejecutar las siguientes tareas:

- `SUMAR`: suma una lista de números.
- `MAYUSCULAS`: convierte un texto a mayúsculas.
- `LONGITUD`: devuelve la cantidad de caracteres de un texto.

La comunicación entre cliente y servidor se realiza utilizando mensajes en formato **JSON**.

## Ejecución

Primero iniciar el servidor:

```powershell
py servidor.py
```

Luego, desde otra terminal:

```powershell
py cliente.py
```

## Arquitectura

El diagrama propuesto incluye:

- Clientes web y móviles.
- Balanceador de carga Nginx / HAProxy.
- Servidores workers con pool de hilos.
- Cola de mensajes RabbitMQ.
- Almacenamiento distribuido con PostgreSQL / S3.

## Conclusión

El sistema permite que distintos clientes envíen tareas a un servidor, que las distribuye entre workers y devuelve el resultado correspondiente.