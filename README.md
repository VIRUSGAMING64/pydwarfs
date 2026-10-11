# pydwarfs

Motor de simulación inspirado en *Dwarf Fortress* escrito en Python. El proyecto cuenta con un intérprete de lenguaje de instintos propio, un cargador de datos del mundo y un servidor de visualización basado en WebSockets.

## Módulos

| Módulo | Descripción |
| --- | --- |
| `modules/interpreter/` | Lenguaje de instintos: lexer, AST, parser, memoria e intérprete. |
| `modules/game/` | Carga de datos del mundo (terrains, objetos, mapas) y entidades. |
| `gui/` | Servidor HTTP (Flask) y servidor de WebSockets. |
| `src/` | Frontend compilado (JS, HTML, Tailwind). |

## Requisitos

- Python 3.10+
- Dependencias: `pip install -r requirements.txt`
- Para compilar el frontend (TypeScript): `npm install -g typescript`

## Estructura del repositorio

```text
pydwarfs/
├── main.py                # Punto de entrada / Banco de pruebas
├── requirements.txt       # Dependencias de Python
├── gui/                   # Fuentes del servidor y cliente (TS)
├── src/                   # Cliente frontend servido (JS)
├── modules/               # Lógica del motor y lenguaje
├── gamedata/              # Datos del juego (terrains, mapas, entidades)
└── run.sh                 # Script de compilación frontend y ejecución
```

## Frontend

El frontend consiste en dos partes:
1. **Fuentes:** `gui/src/` contiene los archivos TypeScript.
2. **Servido:** `src/` contiene el JavaScript compilado y los archivos estáticos que el servidor Flask sirve en la raíz.

Para compilar el frontend desde las fuentes:
```bash
./run.sh
```

## Ejecución

`main.py` actúa como banco de pruebas. Asegúrese de haber creado los archivos de datos en `gamedata/` y un `codigotest.txt` antes de ejecutar:

```bash
python main.py
```

## Estado actual
El proyecto se encuentra en una etapa de prototipo. Consulte los comentarios en el código y la estructura para entender las limitaciones actuales de la implementación del intérprete y el servidor.
