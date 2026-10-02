# pydwarfs

Motor de simulación tipo *Dwarf Fortress* escrito en Python donde **cada criatura está
controlada por sus propios instintos**, escritos en un lenguaje propio que el proyecto
lexeriza, convierte a AST e interpreta paso a paso.

El repositorio reúne tres piezas independientes (y todavía en crecimiento):

| Módulo | Qué hace |
| --- | --- |
| `modules/interpreter` | El lenguaje de instintos: lexer, AST, parser de expresiones, memoria e intérprete. |
| `modules/game` | Carga de los datos del mundo: terrains, objetos y mapas desde archivos de texto. |
| `gui` | Servidor web (Flask) + WebSockets + cliente Canvas (JS/TS) para visualizar el mundo. |

> **Estado: en desarrollo activo.** El intérprete, el cargador de datos y el renderizado ya
> funcionan de forma independiente. La capa que une las tres (entidades `.ins` ejecutándose
> dentro de un `Game`) todavía está pendiente.

---

## Características

- **Lenguaje de instintos propio** con etiquetas, saltos `goto`, condicionales `if` y bucles
  `while`, con una precedencia de operadores explícita.
- **Intérprete de un solo paso** (`Step()`): permite avanzar la simulación instrucción a
  instrucción, clave para depurar IA y para renderizar el mundo a medida que avanza.
- **AST serializable a JSON** (`ast.json`) para inspeccionar exactamente cómo quedó
  interpretado el código.
- **Memory con direcciones** (`malloc` / `alloc` / `query` / `realloc`) al estilo de un
  gestor de memoria.
- **Carga de mundo por data files** en formatos muy sencillos y legibles: `.te`, `.ob`, `.map`.
- **Errores con número de línea** mediante excepciones propias (`MissingVariable`,
  `SintaxisException`, `ExpresionException`, `ZeroDivisionException`, `MemoryException`).
- **Visualizador web** con Canvas 2D y Tailwind, conectado al backend por WebSockets.
- **Cero dependencias del juego**: solo Python + Flask + `websockets` en el backend.

---

## Requisitos

- **Python 3.9+** (el código usa `str.removeprefix` / `str.removesuffix` y anotaciones
  `list[Token]`).
- Dependencias de Python:

  ```
  flask
  websockets
  ```

El proyecto **no incluye todavía un `requirements.txt`**; instálalas manualmente:

```bash
pip install flask websockets
```

El frontend no tiene build step: usa Tailwind y el cliente tal cual desde
`gui/src/` (los `.ts` son la versión tipada de los `.js`).

---

## Uso rápido

Todo se ejecuta desde la raíz del repositorio (las rutas de `gamedata/` y `gui/src/`
son relativas al CWD):

```bash
# 1. Compila el intérprete de instintos y vuelca el AST a ast.json
# 2. Carga terrains, objetos y mapas, y vuelca gamedump.txt
# 3. Ejecuta codigotest.txt paso a paso e imprime la memoria final
python main.py
```

Salida esperada (con `codigotest.txt` como script):

```
DEBUG:root:[]
{'a': 99999}
```

### Reproducir cada pieza por separado

`main.py` es un pequeño banco de pruebas; comenta las llamadas del final y descomenta
la que quieras (o impórtalas desde tu propio script):

```python
from modules.interpreter import *
from modules.game import Game

# --- Intérprete: ver el AST de un script como JSON ---
tokens = Lexer(open("codigotest.txt").read(), {}).TokenizeSource()
ast = AstBuilder(tokens)
ast.ExtractStructures()
print(ast.__json__())

# --- Intérprete: ejecutar paso a paso ---
iner = Interpreter(open("codigotest.txt").read())
while iner.Step():
    print(iner.line, iner.memory.addrs)

# --- Juego: cargar y volcar el mundo ---
g = Game()
g.LoadTerrains()
g.LoadObjects()
g.LoadMaps()
print(g.__dict__())
```

---

## Arquitectura

```
código de instintos (.ins / .txt)
            │
            ▼
    ┌───────────────┐
    │     Lexer     │  texto  →  lista de Token por línea
    └───────┬───────┘
            ▼
    ┌───────────────┐
    │  AstBuilder   │  tokens  →  árbol de estructuras
    └───────┬───────┘  (Label / SingleLine / Condition / Loop / Goto)
            ▼
    ┌───────────────┐   ┌──────────────┐
    │  Interpreter  ├──►│    Memory    │  variables por dirección
    │  Step()       │◄──┤ query/alloc  │
    └───────┬───────┘   └──────────────┘
            │
            │  código de salida: NORMAL / FINDING / CONTINUE / RETURING
            ▼
      estado del mundo  ──►  Game (terrains, objetos, mapas)
                                  │
                                  ▼
                    gui/server  (Flask + WebSockets)
                                  │
                                  ▼
                        gui/src  (Canvas 2D + Tailwind)
```

El intérprete es **estructural, no recursivo en el bucle principal**: `Step()` ejecuta
exactamente una instrucción y devuelve `True`/`False`, de modo que el bucle de simulación
externa decide cuántas instrucciones avanzan por tick.

---

## Estructura del proyecto

```
pydwarfs/
├── main.py                       # Banco de pruebas: AST, carga de juego, intérprete, servidor
│
├── modules/
│   ├── game/                     # Carga de datos del mundo
│   │   ├── __init__.py
│   │   ├── basegame.py           # Clase Game: LoadTerrains/LoadObjects/LoadMaps
│   │   ├── initializer.py        # Carga genérica "atributo valor" de los data files
│   │   ├── terrains.py           # GameTerrain / GameTerrainBuilder
│   │   ├── objects.py            # GameObject / GameObjectBuilder
│   │   ├── map.py                # GameMap: resuelve caracteres a tiles
│   │   ├── typesutil.py          # GameJson: serialización a dict
│   │   └── static.py             # OBJECT = 1, TERRAIN = 2
│   │
│   └── interpreter/              # Lenguaje de instintos
│       ├── __init__.py
│       ├── lexer.py              # Texto → tokens por línea (comentarios, comillas, tabs)
│       ├── ast.py                # Tokens → árbol de estructuras
│       ├── interpreter.py        # Clase Interpreter: header, búsqueda de labels, Step()
│       ├── statics.py            # Tipos de token, operadores por precedencia, keywords
│       ├── exceptions.py         # Jerarquía de errores con número de línea
│       ├── tokens/
│       │   ├── token.py          # Token + Parser (shunting-yard) + Memory re-export
│       │   └── tokens_utils.py   # Detectores: ValidLoop, ValidLabel, validGoto...
│       ├── parser/
│       │   ├── parser.py         # (reservado)
│       │   └── parserutils.py    # Tabla de operaciones, asignaciones, unarios
│       ├── structures/
│       │   ├── structure.py      # Clase base + códigos de salida
│       │   ├── label.py          # Label
│       │   ├── SimpleLine.py     # Una línea simple (asignación / expresión)
│       │   ├── condition.py      # if ... end
│       │   ├── loop.py           # while ... end
│       │   └── goto.py           # goto etiqueta
│       └── memory/
│           └── memory.py         # Memory: malloc / alloc / query / realloc
│
├── gamedata/                     # (ignorado por git) Data files del mundo
│   ├── terrains/*.te             #   terreno
│   ├── objets/*.ob               #   objeto
│   ├── maps/*.map                #   mapa
│   └── entity/*.ins              #   instintos de una criatura
│
├── gui/
│   ├── server/
│   │   ├── server.py             # Server (Flask) + WebSockServer
│   │   └── routes.py             # Servidor de estáticos y mime types
│   └── src/                      # Frontend servido en /
│       ├── index.html            # Layout + Tailwind
│       ├── main.js / main.ts     # Canvas 2D: dibuja la grilla y escucha el mouse
│       ├── com.js  / com.ts      # Cliente WebSocket con cola de mensajes
│       └── tailwind.js
│
├── codigotest.txt                # Script de prueba (bucle while + goto)
├── codigotest1.txt               # Script de prueba (instintos completos de Uruk)
├── codigotest2.txt               # Script de prueba (flujo con labels)
├── ast.json                      # Volcado del AST (generado)
└── gamedump.txt                  # Volcado del mundo (generado)
```

> Nota: `gui/` y sus subcarpetas no tienen `__init__.py`; el import funciona gracias a los
> *namespace packages* de Python 3.3+.

---

## El lenguaje de instintos

### Anatomía de un archivo

Un script tiene tres zonas: **cabecera** (atributos de la criatura), **punto de entrada
obligatorio `start:`** y **cuerpo** con labels y saltos.

```python
# Instintos de un Uruk-hai
creature Uruk

faction isengard

health 80

vision 6

lifespan 400

start:
    if health < 20 goto flee
    if enemy_dist == 1 goto bite
    if enemy_dist > 0 goto hunt

wander:
    move(random % 3 - 1, random % 3 - 1, 1)
    goto start

flee:
    move(-enemy_dx, -enemy_dy, 3)
    goto start
```

**Reglas de la cabecera** (`modules/interpreter/interpreter.py:17`):

- Solo se admiten estos cinco atributos: `creature`, `faction`, `health`, `vision`, `lifespan`.
- Cada línea debe tener exactamente `atributo valor`; cualquier otro nombre lanza
  `Invalid header`.
- Todas van **antes** de `start:`. Si falta el label `start`, el intérprete lanza
  `Entry point unknow`.

### Etiquetas y saltos

```python
start:                 # label — identificador que termina en ":"
    a = 0
    goto start         # Goto salta a la etiqueta; devuelve FINDING
```

- Las etiquetas se declaran como una línea que consiste **solo** en `nombre:`.
- No se permiten dos labels con el mismo nombre (`Two labels with same name`).
- `goto` por sí solo es una estructura; `goto` precedido de un `if` genera un
  `Condition` + `Goto` fusionados.

### Condicionales

Dos formas, ambas sin paréntesis obligatorios:

```python
# 1. Salto condicional (una línea)
if health < 20 goto flee
if allies_near > 3 goto celebrate

# 2. Bloque con end
if a == 1
    b = 10
    goto start
end
```

`Condition` se re-evalúa en cada entrada (`self.ip == 0`), ejecuta su cuerpo línea a línea
y devuelve `CONTINUE` para que el intérprete vuelva a entrar en la siguiente instrucción.

### Bucles

```python
a = 0

while a < 100
    a = a + 1
    if a == 99 goto er
end

er:
```

- La condición del `while` se evalúa al entrar (`ip == 0`); si es falsa, devuelve `NORMAL`
  y el bucle se salta.
- `end` cierra el bloque; un `while` sin `end` lanza `Not closed strucure`.

### Expresiones y operadores

El parser es un *shunting-yard* con precedencia definida en
`modules/interpreter/statics.py`. De mayor a menor prioridad:

| Nivel | Precedence | Operadores | Notas |
| --- | --- | --- | --- |
| P3 | 3 (máxima) | `**` | Potencia |
| — | unario (3) | `-` `+` `!` | `neg`, `plus`, `_not` |
| P2 | 2 | `%` `*` `/` `!` `&` `\|` `^` | `!` en su forma binaria también está mapeada |
| P1 | 1 | `+` `-` | |
| P0 | 0 (mínima) | `==` `<=>` `=>` `!=` `<=` `>=` `<` `>` `<<` `>>` `=` | `=` es la asignación |

Extra: los delimitadores `= ( ) [ ] ,` y el marcador de comentario `#` también son tokens
de operador. `!` es tanto unario (`not`) como binario según el contexto. `/` usa división
entera (`//`); `/ 0` lanza `ZeroDivisionException`.

### Tipos de token

| Constante | Valor | Significado |
| --- | --- | --- |
| `NIL` | 0 | Sin clasificar / inválido |
| `NUMBER` | 1 | Entero |
| `STRING` | 2 | `"..."` o `'...'` |
| `OPERATOR` | 8 | Operador o delimitador |
| `VARIABLE` | 16 | Identificador |
| `KEYWORD` | 32 | `goto` `if` `func` `var` `for` `end` |
| `LINE` | 64 | Línea simple |
| `COMMENT` | 256 | Resto de la línea tras `#` |
| `CONDITION` | 512 | Bloque `if` |
| `LOOP` | 1024 | Bloque `while` |
| `LABEL` | 2048 | Etiqueta |
| `GOTO` | 4096 | Salto |

Los tipos son **bit flags**, lo que permite combinar checks (`type & LABEL`).

### Memoria

```python
mem = Memory()
mem.alloc("a", 42)       # asigna
mem.query("a")           # → 42
addr = mem.malloc(16)    # reserva un bloque de 16 None
mem.realloc(addr, 32)    # cambia el tamaño -> nueva dirección (el anterior queda en None)
```

Usar una variable no declarada lanza `MissingVariable`. El único atajo es la asignación
(`x = ...`), donde el valor todavía puede ser `None`.

### Códigos de salida de `Execute`

| Código | Significado |
| --- | --- |
| `NORMAL` | Terminó la instrucción; el intérprete avanza a la siguiente. |
| `FINDING` | Es un `goto`; el intérprete busca la etiqueta indicada. |
| `CONTINUE` | Siguiente instrucción *dentro* de la misma estructura. |
| `RETURING` | Reservado para el futuro (funciones). |

### Comentarios

```python
# bred in the pits of Isengard
```

`#` y todo lo que sigue en la línea se convierte en un único token `COMMENT`, que el parser
ignora.

---

## Formatos de datos del mundo

Todos los data files comparten el mismo formato: **una línea por atributo, `atributo valor`,
separados por un espacio**. El cargador (`modules/game/initializer.py`) rechaza el archivo
completo si alguna línea no tiene exactamente 2 campos o si el atributo no existe en la clase
destino.

### Terreno — `gamedata/terrains/*.te`

```
terrain Grass
char .
resource_max 100
regen 2
```

| Atributo | Significado |
| --- | --- |
| `terrain` | Nombre del terreno. |
| `char` | Carácter con el que se dibuja en el mapa. |
| `resource_max` | Recursos iniciales y máximos (`Count` / `Max`). |
| `regen` | Regeneración por tick. |

### Objeto — `gamedata/objets/*.ob`

```
object Rock
char #
resource_max 100
```

### Mapa — `gamedata/maps/*.map`

La **primera línea es el nombre**; el resto es la grilla. Todas las filas deben tener la
misma longitud (si no, el mapa se descarta) y cada carácter debe corresponder a un terreno u
objeto ya cargado.

```
Plain with rocks
....................
...##...............
...##**...#.........
....****..#....###..
```

→ `GameMap` resuelve cada carácter contra terrains + objetos y guarda una **copia**
independiente por celda, de modo que cada tile tiene su propio `Count`.

### Instintos de entidad — `gamedata/entity/*.ins`

Contiene el mismo lenguaje de la sección anterior. `uruk.ins` es el ejemplo completo
creado durante el desarrollo.

---

## Cargar el mundo desde Python

```python
from modules.game import Game

g = Game()                      # crea gamedata/{terrains,objets,maps} si no existen
g.LoadTerrains()
g.LoadObjects()
g.LoadMaps()

print(len(g.Terrains), len(g.Objects), len(g.Maps))
print(g.__dict__())             # paths + objects + terrains + maps, listo para JSON
```

Se puede apuntar a otros directorios:

```python
g = Game(
    m_path="mi_juego/maps",
    t_path="mi_juego/terrains",
    o_path="mi_juego/objects",
)
```

Los errores de lectura se registran con `logging.error` y no cortan la carga; un `.map` con
un carácter desconocido se descarta silenciosamente (queda pendiente reportar ese error con
más detalle).

---

## GUI y WebSockets

`gui/server/server.py` levanta dos servicios:

1. **Servidor estático Flask** — publica `gui/src/` en `http://127.0.0.1:1200`.
2. **Servidor WebSockets** en `ws://127.0.0.1:9090` — para consultar y avanzar la simulación.

```python
from gui.server.server import Server, WebSockServer
from gui.server.routes import Routes
from threading import Thread
import asyncio

ser = Server("127.0.0.1", 1200, "./gui/src")
routes = Routes("./gui/src")
ser.AddEndpoint("/", routes.hola)
ser.AddEndpoint("/<path>", routes.getfile)
Thread(target=ser.Run, daemon=True).start()

asyncio.run(WebSockServer(game).RunWebsocks())
```

### Protocolo

Mensajes de texto simples, uno por mensaje:

| Enviar | Respuesta | Efecto |
| --- | --- | --- |
| `SHOW` | JSON con el estado completo del juego | `game.__dict__()` serializado |
| `STEP` | `"unknowaction"` | Avanza un tick de la simulación |
| `SIGKILL` | `"KILLED"` | Detiene la simulación |

Cliente (ya implementado en `gui/src/com.js`):

```javascript
import Communication from "./com.js";

const com = new Communication("ws://127.0.0.1:9090");
com.Send("SHOW");

setInterval(() => {
    com.Send("SHOW");
    const data = com.Recive();
    console.log(data);
}, 1000);
```

`Recive()` consume una cola de mensajes de a uno y la compacta cada 30 elementos para no
crecer sin límite.

### Renderizado

`gui/src/main.js` crea un `canvas` del tamaño de la ventana, calcula el tamaño de píxel a
partir de `mapsize = 30` y dibuja la grilla con `FillMatrix()`. Los clics se convierten a
coordenadas de celda con `GetPos()`, que es la base donde se pintarán las entidades.

---

## Puntos de entrada de `main.py`

| Función | Qué verifica |
| --- | --- |
| `TestAstBuild()` | Lexea `codigotest.txt`, construye el AST y escribe `ast.json`. |
| `TestGameLoading()` | Carga el mundo completo y escribe `gamedump.txt`. |
| `TestExprParser()` | Evalúa línea por línea con `Parser.EvalExpr`. |
| `TestServer()` | Levanta Flask + WebSockets sin juego (solo estático). |
| `TestServerCom()` | Igual, pero pasando el `Game` al servidor WebSockets. |
| `InterTest()` | Ejecuta el script paso a paso con un tope de 2000 pasos anti-bucle infinito. |

---

## Limitaciones conocidas

- **Las llamadas a funciones nativas todavía no existen.** `move(...)`, `consume(...)`,
  `reproduce(...)`, `say(...)`, `roar(...)` y `see(...)` aparecen en los scripts de ejemplo
  (`codigotest1.txt`, `uruk.ins`) pero el intérprete aún no las resuelve: hoy `move` se
  tokeniza como variable y falla con `MissingVariable`. La keyword `func` está declarada en
  `statics.py` pero sin implementar.
- **No existe el bucle de simulación.** No hay un tick que instancie criaturas, ejecute sus
  instintos y aplique los efectos sobre el mapa; `Game` solo carga datos.
- **`gui/server/server.py` llama a `self.game.step()` / `.kill()`**, métodos que la clase
  `Game` aún no expone.
- **Los valores de los data files son strings.** `Initialize` no convierte tipos, así que
  `Count`, `Max` y `Regen` llegan como `"100"` en lugar de `100` (visible en `gamedump.txt`).
- `Game.Terrains` / `Objects` / `Maps` son atributos de **clase**, no de instancia: dos
  objetos `Game` compartirían las mismas listas.
- `realloc` deja la dirección anterior en `None` y devuelve una nueva, sin liberar nada.
- No hay suite de tests automatizados; la verificación es manual vía `main.py`.
- El repositorio todavía no incluye un archivo de licencia.

## Hoja de ruta

- [ ] Implementar llamadas a funciones /-effects del mundo (`move`, `consume`, `reproduce`, `say`, `roar`, `see`).
- [ ] Conectar `Entity` + `Interpreter` con `Game` en un `step()` de simulación.
- [ ] Cargar entidades `.ins` desde `gamedata/entity/` y colocarlas en el mapa.
- [ ] Tipado de valores en el cargador de data files.
- [ ] Envío del estado por WebSockets y renderizado real de tiles y entidades en el canvas.
- [ ] `requirements.txt` y tests automatizados.
