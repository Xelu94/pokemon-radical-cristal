# Compilación, herramientas y pruebas

## Qué contiene este repositorio y qué no

Este repositorio **no incluye el árbol completo del código fuente** (miles de archivos de la base española), sino las modificaciones como [`parches/Cambios-fuente.patch`](../parches/Cambios-fuente.patch) (formato `git diff --binary`, acumulado: lleva la base española a la versión 4.3) más los recursos, herramientas y pruebas propios. La fuente integrada se obtiene aplicando el parche sobre la instantánea base española.

- La instantánea base verificada (`base-espanola-verificada.zip`, SHA-256 `99e659b91677e822b2ed31c12e1695ac730b426a7ef79d0bbb4352a07ac0e74b`) se conserva en el material de trabajo local del autor; no se publica aquí.
- El parche vigente tiene SHA-256 `5a0d232457e55de031a75def8b416d5ebdf0c8d794d74570f7e8b8037b3569a7`.
- El identificador de revisión de informes anteriores pertenecía al historial local y **no es un commit descargable** del repositorio upstream.
- La base española procede de [MicaelAlighieri/pokecristal](https://github.com/MicaelAlighieri/pokecristal). Hasta que se compruebe un commit concreto de ese repositorio con el mismo hash de árbol, la reconstrucción exclusivamente desde GitHub no está garantizada.

Las ROM sin parche no se publican. Los parches BPS históricos (normal y sandbox) de 4.2 y anteriores son material de trabajo local; se aplicaron a la ROM española de referencia con SHA-1 `889a06fc0bb863666865aa69def0adf97945ac2a` y no se adjuntan.

## Herramientas

| Herramienta | Uso |
|---|---|
| RGBDS 1.0.0 | `rgbasm`, `rgblink`, `rgbfix`, `rgbgfx` |
| make y GCC | Construcción y utilidades en C de la fuente |
| Git | Aplicar el parche (`git apply`) |
| Python 3 | Generación de recursos, manifiestos, hashes, pruebas |
| Pillow | Compilar y verificar gráficos |
| PyBoy 2.8.1 | Ejecutar la ROM en pruebas (`pruebas/requirements.txt`) |
| Node.js | Núcleo del randomizador y Playwright |
| Playwright 1.62.1 | Prueba del randomizador en navegador (`pruebas/package.json`) |
| mGBA 0.10.5 | Emulador del portable de desarrollo; no se distribuye |

Las herramientas se resuelven por `PATH` (y `PLAYWRIGHT_CHANNEL`/`NODE_BINARY` si se desea otro navegador o Node); no hay rutas absolutas. En Windows, la reconstrucción se comprobó con RGBDS 1.0.0 (zip oficial de Windows), GCC y make de WinLibs (`mingw32-make`) y las utilidades `sh` de Git for Windows en el `PATH`.

## Reconstruir la fuente y compilar

Desde la raíz del repositorio:

```sh
mkdir pruebas/work/source
# Extrae base-espanola-verificada.zip en pruebas/work/source (instantánea base)
cd pruebas/work/source
git init
git apply --check ../../../parches/Cambios-fuente.patch
git apply ../../../parches/Cambios-fuente.patch
make -j4 cristal cristal_debug      # en Windows con WinLibs: mingw32-make -j4 cristal cristal_debug
```

Salidas: `pokecristal.gbc` (ROM normal) y `pokecristal_debug.gbc` (sandbox), con sus `.sym`.

> **Verificado en la preparación de la v4.3 (21 de octubre de 2026):** el parche aplica sin conflictos (solo un aviso de línea en blanco al final de un archivo) y los 4660 archivos resultantes son idénticos, byte a byte, a la fuente con la que se compiló. Una compilación limpia sobre ese árbol produjo exactamente:
>
> - ROM normal: `a6a232589e9ff8859bc9307c3593707c753dcaf8b6be65a8ba835faafe949b1e`
> - Sandbox: `d6a7449506680bdbb215e3aabeb4f6772585516e55eefe07c396f9543cc401f2`
>
> La compilación de la fuente de la 4.2 sin cambios reprodujo también los hashes publicados de la 4.2.

> **Verificado para la 5.4 (25 de octubre de 2026):** el parche acumulado (317 archivos) aplicado sobre `base-espanola-verificada` y compilado desde cero con RGBDS 1.0.0 produjo exactamente:
>
> - ROM normal: `91845e52c2afee9f0f6e0425f15fc62e7685aff5c116284cceee768ac00e67c1`
> - Sandbox: `4afbf8921e51f9086bbb5412f9d43f7ede1b1271c1aff42d9ff5ec106d9d2020`

> **Verificado para la 5.3 (23 de octubre de 2026):** ROM normal `aab4601450c38aa762b643033df21af26dd698cb30d44dce50f92780783e6408`; sandbox `880a161a97ae2321565a751ca58c4284d796263f490c4aba67a1fe5b90f020d6`.

> **Verificado para la 5.2 (23 de octubre de 2026):** ROM normal `6861c67987485a36df0e3c4a83906bd68f778a7b649466984dffdeb31ffc590b`; sandbox `2d39b0abac24322576aa1deaa00e5ed09279958f37db97e5e01d69e2af9bf747`.

> **Verificado para la 5.1 (23 de octubre de 2026):** ROM normal `339f38f5d51b9bd1a4adcd28e1767fbbf32ef4e0e343f4965acbdc9cb4fa00e5`; sandbox `b060483611e9bb5c1fbc88607e2f5a218ac500bbb268962279725a1cb4702183`.

> **Verificado para la 5.0 (22 de octubre de 2026, ROM publicada primero; ver el CHANGELOG):** el parche acumulado (302 archivos) aplicado sobre `base-espanola-verificada` y compilado desde cero con RGBDS 1.0.0 produjo exactamente:
>
> - ROM normal: `5b9fb58edd1742f2de4b6a1bbc9999e05f48c31d3ac28a44200650e2f3133ecd`
> - Sandbox: `ec9dbc978709369f95218bb1afca61927ca27b225b95f2f4fd832cee416a0130`

> **Verificado para la 4.4 (22 de octubre de 2026):** el parche acumulado (227 archivos) aplicado sobre `base-espanola-verificada` y compilado desde cero con RGBDS 1.0.0 produjo exactamente:
>
> - ROM normal: `b4cff3b076988a780d6570653d677b7fecab1cbb4fdfcc6dde8cda5a22c1e3ef`
> - Sandbox: `f77fb27ec0e2365985be7cc7d6045fde364a9e3e6ad484e2a1df5aab74b3706e`

### Generación del sprite de Tito, de los rótulos y de los iconos

```sh
python herramientas/fuentes/build_tito_sprite.py   # desde la raíz de la fuente integrada
python herramientas/fuentes/build_pack_labels.py   # rótulos de la mochila (40x32) y rótulos nativos MT/MO, BALLS, OBJ.CLAVE
python herramientas/fuentes/build_move_icons.py    # iconos de categoría de ataque (24x8)
python herramientas/fuentes/build_title_branding.py # línea «RADICAL CRISTAL» de la pantalla de título
```

El primero lee `gfx/sprites/tito_xeluis.pixels` y escribe `gfx/sprites/tito_xeluis.png` (16×96; la segunda mitad lleva el fotograma de «respiración»). El segundo escribe `gfx/pack/pack_categories.png` y redibuja los rótulos nativos en `gfx/pack/pack_menu.png`. El tercero escribe `gfx/battle/move_categories.png`. El Makefile convierte los PNG a 2bpp.

### Randomizador

```sh
cd pruebas/work/source
python tools/export_portable_randomizer.py ../v4-randomizer
```

Requiere los símbolos de la ROM recién compilada. **No ejecutes `tools/balanced_randomizer.py`**: pertenece al flujo histórico y restauraría tablas anteriores sobre la fuente vigente.

## Pruebas

Los scripts de [`pruebas/`](../pruebas) conservan la estructura relativa que esperan (`work/…`).

```sh
cd pruebas
python -m pip install -r requirements.txt
npm install
npx playwright install chromium
python work/validate-v50-release.py
```

`validate-v50-release.py` ejecuta todos los grupos, comprueba el número esperado de comprobaciones de cada uno y genera `work/v50-validation.json`. Las pruebas de PyBoy usan la ROM compilada y sus símbolos; las de navegador usan el randomizador y no envían la ROM a ningún servidor.

### Resultados de 5.4

222 comprobaciones agrupadas, ejecutadas el 25 de octubre de 2026 sobre las ROM de 5.4 (informes en [`evidencias/`](../evidencias); los ficheros `v4-*` y `v41-*` se regeneraron con esta compilación, y [`Validacion-v4.3.json`](../evidencias/Validacion-v4.3.json) conserva el resumen de la 4.3): (informes en [`evidencias/`](../evidencias)):

| Grupo | Informe | Comprobaciones |
|---|---|---|
| Servicios y mapas de Tito | `v4-tito-tests.json` | 48 |
| Orientaciones renderizadas de Tito | `v42-tito-directions-tests.json` | 4 |
| Rutas de Ulex y Objetos del sandbox | `v42-fixes-tests.json` | 17 |
| Combates de Ulex (incluido el primer Ulex al nivel 15) y menú sandbox | `v41-root-ui-tests.json` | 27 |
| Cálculos de combate y almacenamiento | `v4-battle-tests.json` | 11 |
| Interfaz real de combate y captura | `v41-battle-ui-tests.json` | 4 |
| Núcleo del randomizador | `v4-randomizer-tests.json` | 9 |
| Randomizador en navegador sin conexión | `v4-randomizer-ui-tests.json` | 4 |
| Cambios de la 4.3 (Vuelo, anciano del mapa, tiendas, Liga, caramelos, bolsa) | `v43-changes-tests.json` | 14 |
| Cambios de la 4.4 (tope en estado, iconos de ataque, barra de experiencia, respiración de Tito) | `v44-changes-tests.json` | 4 |
| Rutinas de la 5.0 (objetos infinitos, eclosión, selector de la Superliga, huevos de 10 pasos) | `v45-routines-tests.json` | 14 |
| Historia y mundo de la 5.0 (aviso de Ulex, Joy, Elm, otro protagonista, Superliga, datos) | `v45-story-tests.json` | 28 |
| Mochila del sandbox (MO) y tiendas con piedras (datos y rutinas) | `v53-routines-tests.json` | 5 |
| Arreglos de los beta testers (texto de objeto Elegido, sprites al cruzar mapas, ataques MO) | `v54-fixes-tests.json` | 5 |
| Los mismos recorridos jugando como chica (Gold embosca; Cristal no) | `v45-story-girl-tests.json` | 28 |

Las comprobaciones nuevas de la 4.3: la partida nueva empieza con un montón de 99 caramelos y 6 montones en total, usar un caramelo sube el nivel sin gastarlo, el recuadro negro muestra los cuatro rótulos, la navegación derecha e izquierda recorre el círculo de bolsillos, VUELO aparece en el submenú solo con la MO, el anciano entrega el mapa por las dos filas de entrada, ninguna de las 34 tiendas vende curas ni queda vacía, y el oficial entrega 8/10/7 con ocho medallas.

Las comprobaciones de la 4.4: la primera página de estado imprime TOPE y el límite (24 con una medalla); el subpanel de ataques muestra tres iconos distintos para un ataque físico, uno especial y uno de estado, con los bytes de VRAM iguales a los de la ROM; y Tito muestra exactamente dos fotogramas distintos en reposo. La prueba de orientaciones de Tito fija el contador de cuadros para medir siempre la pose de reposo, y la prueba del navegador comprueba que la vista previa coincide con las elecciones del núcleo. Los rótulos nativos de la mochila se verifican visualmente en la captura [bolsa-rotulos.png](../capturas/bolsa-rotulos.png), no con una comprobación automática propia.

Las comprobaciones de la 5.0 ejecutan las rutinas nuevas con el arnés de CPU (`pruebas/work/cpu_harness.py`) y los recorridos con el emulador: ver el aviso de Ulex en la Ruta 29, curar con la enfermera de la Ruta 13, el duelo de Elm completo, la emboscada de Pueblo Primavera y la de Torre Bellsprout, el combate final en la Meseta Añil con el huevo, el canje de ZURULLO, el vestíbulo y la sala de Azul de la Superliga (victoria y derrota), y la recompensa del campeón. La sala del campeón se comprueba con un atajo (se marca el combate como ganado); la Guarida Dragón se comprobó a mano con un parche de la ROM y no está en la suite. Además se ejecutó el humo de los 394 mapas (todos cargan, salvo los dos ascensores y la sala móvil del Torre Batalla que dependen de su contexto) y el recorrido de sprites que comprueba que ningún PNJ queda sin fotogramas de andar.

Los informes de 4.2 y anteriores pertenecen a otras compilaciones y no se suman a este recuento.

### Cómo leer los resultados

- No es un porcentaje de cobertura. Un grupo puede contener muchos casos (p. ej. Poder Oculto con 768 combinaciones de DVs).
- Los montajes omiten la introducción; algunos combates de Ulex aumentan el daño para recorrer los equipos; en Ruta 17 se desactiva la gravedad solo en el montaje de prueba.
- No se ha completado una campaña entera ni queda demostrado el equilibrio global.
- Los informes no contienen rutas del equipo: las ROM aparecen por nombre de archivo o ruta relativa.

## Integración continua

El flujo de GitHub Actions `verificacion.yml` está subido al repositorio y se ejecuta en cada `push`, `pull_request` y a demanda, con dos trabajos, ambos sin compilar la ROM:

- **herramientas**: sintaxis de los scripts de Python y JavaScript, validez de los JSON de `evidencias/` y sintaxis de los scripts incrustados en `Randomizador.html`.
- **release**: descarga el `.gbc` de la Release que enlaza el README, comprueba que su SHA-256 coincide con el del README y ejecuta [`pruebas/ci/verificar-randomizador.cjs`](../pruebas/ci/verificar-randomizador.cjs) con esa ROM y el `Randomizador.html` del repositorio (firma de la parte inmutable, determinismo por semilla, solo cambian bytes mutables, reaplicación sobre una ROM ya generada).

La compilación completa y las pruebas con emulador **no** están en la CI: necesitan RGBDS, WinLibs/GCC y PyBoy y siguen siendo ejecuciones locales. No se muestra ninguna insignia de estado. Sus scripts se probaron en local antes de subirlo; el resultado de su primera ejecución real se consulta en la pestaña Actions del repositorio.
