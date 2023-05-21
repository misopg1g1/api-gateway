# Guía para ejecutar el Api Gateway

## Requisitos previos

Asegúrate de tener los siguientes requisitos previos instalados en tu sistema:

- Docker
- Docker Compose (solo para ejecutar con Docker Compose)
- Python 3.9 (solo para ejecución local)
- Tener pip instalado
- Tener en ejecución los microservicios de la capa mas baja (Auth, Sellers, Orders, Inventory, Customer, Product)

## Configuración

Antes de ejecutar la aplicación, asegúrate de realizar la siguiente configuración:

1. Abre el archivo `docker-compose.yml` y encuentra la sección `environment` dentro del servicio `gateway`.
   Define los valores de las variables de entorno requeridas directamente en el archivo `docker-compose.yml`. Por
   ejemplo:
   ```yaml
      - AUTH_URL=http://microservice-url
      - CUSTOMERS_URL=http://microservice-url
      - ENCRYPTION_KEY_SECRET=encryption-key
      - INVENTORY_URL=http://microservice-url
      - ORDERS_URL=http://microservice-url
      - PRODUCTS_URL=http://microservice-url
      - RABBIT_HOST=rabbitmq
      - RABBIT_PASSWORD=your-rabbitmq-password
      - RABBIT_PORT=5672
      - RABBIT_USER=your-rabbitmq-username
      - REDIS_HOST=redis
      - REDIS_PASSWORD=your-redis-password
      - REDIS_PORT=6379
      - SELLERS_URL=http://microservice-url

2. Si tienes dependencias adicionales, agrégalas al archivo `requirements.txt`.

## Ejecución con Docker Compose

Sigue estos pasos para ejecutar la aplicación utilizando Docker Compose:

1. Abre una terminal y navega hasta el directorio que contiene el archivo `docker-compose.yml`.

2. Ejecuta el siguiente comando para construir la imagen y ejecutar los contenedores:

```
  docker-compose up
```

3. Docker Compose construirá la imagen de la aplicación y ejecutará el contenedor del servicio. Podrás acceder a la
   aplicación en `http://localhost:3001`.

4. Si deseas detener la aplicación, presiona `Ctrl + C` en la terminal y ejecuta el siguiente comando:

## Ejecución local

Sigue estos pasos para ejecutar la aplicación de forma local:

1. Abre una terminal y navega hasta el directorio que contiene el archivo `requirements.txt`.

2. Ejecuta el siguiente comando para instalar las dependencias de Python:

```shell
 pip install -r requirements.txt
```

3. Una vez instaladas las dependencias, ejecuta el siguiente comando para iniciar la aplicación:

```
AUTH_URL=... CUSTOMERS_URL=... ENCRYPTION_KEY_SECRET=... INVENTORY_URL=... ORDERS_URL=... PRODUCTS_URL=... RABBIT_HOST=... RABBIT_PASSWORD=... RABBIT_PORT=... RABBIT_USER=... REDIS_HOST=... REDIS_PASSWORD=... REDIS_PORT=... SELLERS_URL=...  python main.py
```

4. La aplicación ahora estará en ejecución y podrás acceder a ella en `http://localhost:3001`.

5. Para detener la aplicación, ve a la terminal y presiona `Ctrl + C`.

## Ejecución de tests con pytest

Sigue estos pasos para ejecutar los tests utilizando pytest:

1. Abre una terminal en la raiz del proyecto.

2. Ejecuta el siguiente comando para instalar las dependencias de Python:

```shell
 pip install -r requirements.txt
```

3. Ejecuta el siguiente comando para ejecutar los tests:

```shell
 PYTHONPATH=.:$PYTHONPATH pytest
```

