# Errores encontrados y soluciones

Registro único de los errores que se han encontrado en Radical Cristal desde la 5.0, con su causa, su solución y la prueba que lo vigila. El detalle de cada versión sigue en [CHANGELOG.md](../CHANGELOG.md); las causas de motor, en [ARQUITECTURA.md](ARQUITECTURA.md). Los informes anteriores a la 5.0 están en [INFORME-PLAYTEST-v4.3.md](INFORME-PLAYTEST-v4.3.md).

Origen de los errores: la revisión del autor del proyecto (documentos «Arreglos y errores») y, desde la 5.4, dos **beta testers automáticos** que juegan en un emulador sin pantalla (PyBoy): uno como GOLD (jugador chico) y otro como CRISTAL (jugadora chica). Sus informes completos están en [`pruebas/beta/`](../pruebas/beta/).

## Resumen

| Versión | Errores corregidos | Gravedad máxima |
|---|---|---|
| 5.4 | 6 (todos hallados por los beta testers) | Reinicio de consola |
| 5.3 | 8 | Reinicio de consola |
| 5.2 | 2 | Pérdida de reto mal anunciada |
| 5.1 | 4 | Gráficos corruptos |
| 5.0 | 2 | Gráficos |

## 5.4

### E-5.4-1 · Reinicio de consola al elegir otro ataque con un objeto «Elegido»
- **Síntoma:** con Banda, Gafas o Pañuelo Elegidos equipados, tras usar un ataque, elegir otro distinto reiniciaba la consola (pantalla «Este cartucho está diseñado…»). Es la causa más probable del «INVERSIÓN cierra el juego»: el movimiento es inocente (los 254 ataques se probaron como jugador y como rival, sin un solo reinicio) y la partida nueva trae 10 unidades de cada objeto Elegido.
- **Causa:** el texto «El objeto elegido fija el ataque.» estaba definido dentro del bloque de combate, pero `StdBattleTextbox` lo lee siempre del banco `$20`. Leía basura y ejecutaba un código de operación no definido.
- **Solución:** el texto se movió a `data/text/battle.asm` (`BattleText_ChoiceLocked`), junto a los demás avisos de ese menú.
- **Prueba:** `pruebas/` · `test-v54-fixes.py` (los tres objetos).

### E-5.4-2 · Los PNJ cambian de sprite al volver a un mapa o cambiar de zona
- **Síntoma:** PLATA y el guía en Ciudad Cerezo tras el primer combate, la profesora de la Ruta 29, un PNJ de Ciudad Trigal… se dibujaban con los gráficos de otro PNJ después de cruzar un mapa a pie y abrir un menú o pelear.
- **Causa:** desde la 5.0 la lista de gráficos de PNJ de un mapa exterior empieza por los objetos del propio mapa. La disposición en VRAM depende del mapa, no solo del grupo. Al cruzar una conexión a pie el juego **no reconstruía la lista**: los PNJ del mapa nuevo se creaban con la numeración de tiles del mapa anterior y, en la siguiente recarga (menú, combate), cada uno quedaba apuntando al tile de otro PNJ. Con la ROM de la 5.3, 22 de 112 cruces entre mapas tenían el fallo y la base original solo 1.
- **Solución:** nuevo paso `RebuildSpriteList` en `MapSetupScript_Connection`, antes de `LoadMapObjects` (`engine/overworld/map_setup.asm`, `data/maps/setup_scripts.asm`).
- **Comprobación:** 287 cruces entre mapas en ambos sentidos (antes 32 con fallos): 0; 109 llegadas: ningún objeto sin hueco de gráficos y ningún caminante en la zona de sprites quietos.
- **Prueba:** `test-v54-fixes.py` (profesora y bolsa; PLATA y guía tras el combate).

### E-5.4-3 · El PNJ de la Ruta 29 que avisa de Ulex se «distorsiona» al andar
- **Síntoma:** al llegar a la Ruta 29 desde Pueblo Primavera a pie (el camino de toda partida nueva), durante su paseo el PNJ se dibuja como un bloque de tiles del fondo.
- **Causa:** la misma que E-5.4-2. Con la lista de Pueblo Primavera ese PNJ quedaba en la segunda tabla de VRAM, que solo guarda sprites quietos. Al caminar se dibujaba con los tiles `$9C..$9F` del banco 0, que son tiles de fondo. Llegando desde Ciudad Cerezo o con un salto de mapa no ocurría, por eso no se veía en las pruebas con puerta.
- **Solución:** la de E-5.4-2.
- **Prueba:** `test-v54-fixes.py` (0 muestras con tiles de fondo en OAM).

### E-5.4-4 · Comillas del mensaje del campeón de la Superliga
- **Síntoma:** al terminar la Superliga, el texto «Eres el puto amo, cabra!» salía con símbolos raros delante y detrás.
- **Causa:** `«` y `»` no existen en la tabla de caracteres y el ensamblador escribía sus bytes UTF-8.
- **Solución:** se cambian por `“` y `”` (`maps/SuperLeagueTito.asm`).

### E-5.4-5 · PNJ del otro protagonista fuera de la lista de gráficos de Pueblo Primavera
- **Síntoma:** entrando a Pueblo Primavera a pie desde la Ruta 27 o 29, el otro protagonista no estaba en la lista de gráficos y se habría dibujado como el jugador.
- **Causa y solución:** la de E-5.4-2.

### E-5.4-6 · Movimientos MO que no se pueden olvidar
- **Síntoma:** los ataques aleatorios al subir de nivel o al recibir un regalo pueden ser Corte, Vuelo, Surf, Fuerza, Destello, Torbellino o Cascada (34 de 251 especies tras usar caramelos raros). Al aprender uno nuevo con los cuatro huecos llenos, el menú de olvidar rechazaba esos ataques con «Los movimientos MO no se pueden olvidar ahora.». Solo el Borrador de movimientos podía quitarlos.
- **Causa:** el menú de olvidar conservaba la comprobación original `IsHMMove`, pensada para cuando las MO eran movimientos imprescindibles. Desde la 4.x las MO son herramientas de la mochila y el Pokémon no necesita el ataque.
- **Solución:** se elimina la comprobación en `engine/pokemon/learn.asm`; cualquier ataque se puede olvidar.
- **Prueba:** `test-v54-fixes.py` (comprobación del código).

### Nota de rendimiento de E-5.4-2
La primera versión del arreglo recargaba los gráficos con la pantalla encendida y congelaba el juego algo más de un segundo (65 fotogramas) en cada cruce de mapa. Ahora la pantalla se apaga durante la carga, igual que al cerrar un menú: el cruce tarda unos 7 fotogramas. Está probado en emulador; el parpadeo en una consola real o en BGB conviene comprobarlo.

## 5.3

| # | Error | Causa | Solución |
|---|---|---|---|
| 1 | Reinicio al ganar o perder contra Ulex o Tito en la Superliga | el texto de victoria/derrota se leía del banco de la clase, no del mapa | `PrintWinLossText` elige el banco según la clase |
| 2 | Elm combatía con la imagen de Oak | usaba la clase `POKEMON_PROF` | nueva clase `ELM_PROF` con su imagen |
| 3 | Regalos de Elm no shiny en la caja | `GivePoke` al PC no tiraba el dado | `BoxGiftRollShiny` |
| 4 | «Viajar» a la Liga (sandbox) te dejaba dentro de la pared | casilla de llegada mal | destino (6, 10) |
| 5 | Tito hablaba de sí mismo en 3.ª persona | texto | reescrito en 1.ª persona |
| 6 | El guardia de Rojo no desaparecía | objeto sin bandera propia | `EVENT_SILVER_CAVE_GUARD_GONE` |
| 7 | Sudowoodo con sprite de otro PNJ | sprite variable sin valor | `Route36SudowoodoSpriteCallback` |
| 8 | Dark Lugia pequeño por detrás | imagen reducida | recorte central 48×48 |

## 5.2

| # | Error | Causa | Solución |
|---|---|---|---|
| 1 | Con el reto terminado, el mensaje de fin salía cortado y se repetía | `Script_startbattle` leía el resultado del combate anterior | `RefusedBattleResult` + anclar el mapa |
| 2 | Un líder daba la medalla sin combatir con el reto terminado | resultado anterior = victoria | mismo arreglo |

## 5.1

| # | Error | Causa | Solución |
|---|---|---|---|
| 1 | Emboscada de PLATA sin Pokémon | variables del combate sucias | comprobación de equipo |
| 2 | Imagen trasera de Dark Lugia con una X roja | arte | arte de SageDeoxys limpio |
| 3 | Sprites corruptos tras un combate | lista de sprites mayor que la VRAM | `ArrangeUsedSprites` descarta el sobrante |
| 4 | El otro protagonista aparecía lejos | falta un `dec a` al indexar el objeto | `MoveObjectToPlayerFront` |

## 5.0

| # | Error | Causa | Solución |
|---|---|---|---|
| 1 | Los PNJ que caminan no tenían animación de andar | lista de sprites más larga que las 10 plazas con fotogramas | los objetos del propio mapa ocupan las primeras plazas |
| 2 | Barra de experiencia con símbolos | tiles de la 4.4 reutilizados | se restauran al redibujar |

## Pendiente y límites

- **Imagen de combate distinta de la del mapa (Gold/Crystal):** reportada, no reproducida. Con jugadora chica se ve Gold en ambos sitios. Posible efecto de la lista desbordada de la 5.0, ya corregida.
- **Campeón de la Superliga:** se prueba perdiendo y con atajos; no se ha jugado entero.
- **Salas de ascensor, enlace e intercambio:** cuelgan el emulador de pruebas (también con la ROM original); no se han podido recorrer.
- **Objetos que no hacen falta documentar aquí:** aparece «Evento de objeto.» al hablar con los objetos de relleno de los otros protagonistas, pero están ocultos en una partida normal.
