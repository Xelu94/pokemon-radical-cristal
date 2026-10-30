# Pruebas portables

Scripts de validación de la versión 5.5. Conservan la estructura relativa que esperan: se ejecutan **desde esta carpeta** y buscan la fuente compilada en `work/source`.

Preparación y comandos completos: [docs/COMPILACION-Y-PRUEBAS.md](../docs/COMPILACION-Y-PRUEBAS.md).

```sh
python -m pip install -r requirements.txt
npm install
npx playwright install chromium
python work/validate-v50-release.py
```

Requisitos previos: la fuente integrada y compilada (`work/source/pokecristal.gbc`, `pokecristal_debug.gbc` y sus `.sym`) y los archivos del randomizador exportados. Las ROM no están en el repositorio.

| Script | Grupo | Comprobaciones |
|---|---|---|
| `work/test-v4-tito.py` | Servicios y mapas de Tito | 48 |
| `work/test-v42-tito-directions.py` | Orientaciones renderizadas | 4 |
| `work/test-v42-fixes.py` | Rutas de Ulex y Objetos | 17 |
| `work/test-v4-root-ui.py` | Combates de Ulex y menú sandbox | 27 |
| `work/test-v4-battle.py` | Cálculos de combate y almacenamiento | 11 |
| `work/test-v4-battle-ui.py` | Interfaz real de combate y captura | 4 |
| `work/test-v4-randomizer.cjs` | Núcleo del randomizador | 9 |
| `work/test-v4-randomizer-ui.cjs` | Randomizador en navegador | 4 |
| `work/test-v43-changes.py` | Cambios de la 4.3 (Vuelo, anciano del mapa, tiendas, Liga, caramelos, bolsa) | 13 |
| `work/test-v44-changes.py` | Cambios de la 4.4 (tope en estado, iconos de ataque, barra de experiencia, respiración de Tito) | 4 |
| `work/test-v45-routines.py` | Rutinas de la 5.0 con el arnés de CPU (objetos infinitos, eclosión, selector de la Superliga, huevos de 10 pasos) | 13 |
| `work/test-v53-routines.py` | Mochila del sandbox (MO) y tiendas con piedras (datos y rutinas) | 5 |
| `work/test-v55-routines.py` | Rutinas de la 5.5 (evolución por nivel, suelo de nivel, ataque de su tipo, Hada de Tito, Veneno, MT) | 35 |
| `work/test-v55-story.py` | Historia de la 5.5 con el emulador (el otro protagonista por detrás, MT infinitas; también con `PLAYER_GENDER=1`) | 6 |
| `work/test-v54-fixes.py` | Arreglos de los beta testers (usa los scripts de `work/beta54`) | 5 |
| `work/test-v45-story.py` | Historia y mundo de la 5.0 con el emulador (aviso de Ulex, Joy, Elm, otro protagonista, Superliga, datos; se ejecuta también con `PLAYER_GENDER=1` para jugar como chica) | 28 |
| `work/story_helper.py` | Ayudante: banderas de evento, mochila, equipo y lectura estable de memoria | |
| `ci/verificar-randomizador.cjs` | Usado por la integración continua: randomizador contra una ROM dada | 4–5 |

`work/cpu_harness.py` es el montaje común para ejecutar rutinas reales de la ROM con PyBoy; `work/test-v2-tito-ui.py` es la base de las pruebas de interfaz. `PLAYWRIGHT_CHANNEL` permite usar un navegador ya instalado y `NODE_BINARY` otra ruta de Node.

Los scripts escriben informes JSON y capturas en `work/`; esos resultados no se versionan salvo los de [`evidencias/`](../evidencias).
