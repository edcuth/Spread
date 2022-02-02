# Proyecto Spread de Futuros

## Objetivo

El objetivo de este proyecto es hacer un mini bot que se conecte a la plataforma remarkets de
MatbaRofex utilizando la librería pyRofex y obtenga además los precios de futuros y busque
oportunidades de arbitraje entre los siguientes pares de instrumentos:

* SOJ.ROS/MAY22 – SOJ.MIN/MAY22
* MAI.ROS/ABR22 – MAI.MIN/ ABR22
* TRI.ROS/JUL22 – TRI.MIN/JUL22


## Instalación

Es recomendable crear un virtual environment en donde instalar las dependencias del proyecto.

1. Crear un virtual environment usando el comando `py -m venv venv`

2. Activar el virtual environment `venv\scripts\activate`

3. Instalar dependencias usando `pip install -r requirements.txt`

4. Es necesario configurar el ambiente, a traves de un arcihvo `.env` o con environment variables:

    - USER
    - PASSWORD
    - ACCOUNT

5. Correr la aplicación usando el comando `py main.py`

6. Es posible configurar el costo de las trasnacciones creando un archivo `.config` usando `COST`, por default, la aplicación usa el valor 0 para el costo.

Es posible configurar la lista de instrumentos en el archivo main.py, siempre y cuando sean pares de contratos standard y mini. Los pares de instrumentos deben tener `ROS` y `MIN` en los nombres respectivamente.

## Testing

El proyecto usa pytest, para correr las mismas, se debe usar el comando `pytest`, es posible testear cada modulo por separado usando `pytest tests\[nombre del modulo]`