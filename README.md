# CTEDA - 2020 - TrabajoFinal

Este trabajo tiene como objetivo implementar un juego del estilo "**Zero-Sum Games**".

El mismo consiste en que 2 jugadores (máximo permitido) reciben la **mitad** de cartas de un **mazo** con largo especifico.

Los jugadores deberán ir **descartando** una de las cartas por **cada turno** de manera obligatoria.

Un jugador pierde cuando descarta una carta que hace que el **monto** de cartas descartadas (suma de las cartas que se fueron descartando durante la partida) sobrepasa un cierto **limite**.

## ¿Cómo uso esta aplicación?

Primero y antes que nada, se deben instalar las dependencias de la librería utilizando el comando:

````bash
$ <prev_path>\<virtual_env_folder>\Scripts>activate  # Use virtual environment
$ pip install -r requirements.txt
````

---------

El uso del juego se compone por 2 piezas importantes:

- La primera es setear una variable de entorno llamada **GAME_CONFIG**, la misma contendrá el path hasta el archivo de configuración (YAML)
  - Dicha ruta puede ser relativa o absoluta
- La segunda condición es tener un archivo de configuración en formato YAML. El mismo deberá contar con la siguiente estructura

````yaml
game_config:
    players_info:
        p1: 
            type: 'human'
            alias: 'Joe Doe'
            dump_location: '<path_to_settings.yml>'
        p2: 
            type: 'cpu'
            alias: 'Skynet'
            dump_location: '<path_to_settings.yml>'
    limit: <max_limit (int)>
    deck_size: <q_of_cards (int)>
    lower_threshold_limit: <porcentual (int/float)>
    higher_threshold_limit: <porcentual (int/float)>
````

---------

Para ejecutar la aplicación se debe utilizar un comando como el siguiente:

````bash
$ <prev_path>\<virtual_env_folder>\Scripts>activate  # Use virtual environment
$ (env) python main.py
# Ejecución...
````

--------

Para utilizar el backend se debe utilizar el siguiente comando (una vez estemos utilizando el virtual environment):

````bash
$ (env) python app.py
````

Esto levantará un servidor web de desarrollo para testear el aplicativo.

Las rutas importantes serán:

- **/p1**: Dump del player con id **p1**
- **/p2**: Dump del player con id **p2**

## Features requeridas

El proyecto implica el implementar una IA (CPU Player) el cual haga uso del algoritmo de creación de árboles **MiniMax**. Este algoritmo busca maximizar o minimizar las posibilidades de victoria por medio de evaluaciones heurísticas basadas en cada instante/momento/turno/movimiento (análogo a nodo del árbol) de una partida.

El segundo requerimiento es que el "cerebro" de/los jugador/es CPU sean accesibles.

> En esta implementación se opto por hacer un muestreo en "tiempo real" sobre el estado de cada CPU player por medio del uso de un backend sencillo (Flask + JQUERY/AJAX)

### Checklist

**Requerimientos bases**:

- [x] Controlador de jugadores CPU
- [x] Controlador para jugadores humanos
- [x] Handler para las partidas
- [x] Documentación del proyecto

**Adicionales** (Propuestos):

- [x] Configuración de los jugadores
- [x] Soporte para CPU vs. CPU
- [x] Configuración via YAML
- [ ] Optimizaciones sobre la lógica de armado MiniMax
- [ ] Backend para mostrar el estado de los jugadores CPU
- [ ] Backend para métricas de partidas
- [ ] Visualización gráfica del árbol para los jugadores CPU

## ¿Cómo funciona esta implementación?

El detalle y paso a paso de las funcionalidades mas grandes e importantes (**CPUController** y **GameController**) se encuentran en detalle sobre la documentación del código.

A su vez, la documentación del código será provista en cada release/tag en el repositorio.

### ¿Cómo se encaró el desarrollo?

El desarrollo fue encarado primero realizando un spike de pruebas para comprender la lógica de los árboles MiniMax, comprender los datos necesarios para ejecutar una partida y posibles mejoras e implementaciones no imposibles que podían entrar dentro de las funcionalidades.

Luego se procedio a documentar y pasar a limpio el spike antes trabajado.

Se trató de mantener una visión de partida y jugadores customizables, para brindar un mayor abanico de posibilidades a futuras mejoras.

Por desgracia, por cuestiones de tiempo no se pudo implementar una suite de testing que soporte la solución que se esta entregando, para mantener un trackeo mas robusto sobre el funcionamiento, prioritariamente, de la simulación de posibles movimientos para los controladores de CPU.

### ¿Tiempo invertido?

El tiempo invertido puede ser seguido desde este link (app **Clockify**):

- [Time Sheet for project](https://clockify.me/shared/5f1bd7322f10102b0002b22b)

