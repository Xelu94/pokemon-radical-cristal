# Arquitectura y decisiones verificadas

## Motor y estado de la partida

Se modifica el motor de Cristal en ensamblador LR35902/SM83. Las tablas de especies,
movimientos, entrenadores, mapas y eventos alimentan los sistemas de combate y mundo.
Las reglas Nuzlocke, topes y excepciones se integran en las rutas correspondientes;
las comprobaciones ejecutan la ROM, en lugar de reimplementar las reglas en Python.
WRAM y flags existentes guardan el estado; la migración del inventario conserva el
total de espacios combinado entre mochila y PC. No se afirma compatibilidad universal
con cualquier ROM externa o estado de emulador.

## Gráficos y memoria

Tito usa una cuadrícula revisada de 16x16 con tres colores visibles más transparencia.
La hoja 16x96 incluye frente, espalda, izquierda y tres fotogramas alternos completos.
El perfil derecho se refleja. Las pruebas observan OAM y los índices de tiles
dibujados, además de comparar la carga en VRAM con el gráfico compilado.

En exteriores el motor reserva gráficos por grupo de mapas. Ulex carecía de una
entrada para su sprite variable y GetSpriteVTile recurría a los tiles del jugador.
La corrección sustituye un espacio exterior sin uso, de la misma capacidad, por
SPRITE_COPYCAT. Los callbacks eligen el disfraz y el giro carga SPRITE_ROCKET.
Se verificaron el disfraz y la revelación en las 16 rutas con los bytes reales de VRAM.

## Llamadas entre bancos

OBJETOS del sandbox llamaba directamente a ReceiveRandomTM, situada en otro banco.
La dirección se ejecutaba en el banco equivocado. La llamada farcall conserva y
restaura el contexto de banco. La prueba de interfaz entrega objetos dos veces,
comprueba catorce MT en total y regresa al mapa sin bloquearse.

## Randomizador portable

El exportador genera un manifiesto a partir de la fuente y los símbolos compilados.
Solo ciertas referencias de especies, tablas de MT y campos relacionados son
mutables. El HTML integra núcleo y manifiesto, valida tamaño y firma de la parte
inmutable y descarga una nueva ROM sin enviarla a un servidor. Misma semilla y base
compatibles producen los mismos bytes; niveles, MO y código permanecen protegidos.

## Restricciones conservadas

Se reutilizan IDs de movimientos existentes; no se ha ampliado la Pokédex a otras
generaciones. Las habilidades y las megas no están implementadas. Los informes
distinguen pruebas ejecutadas, montajes controlados y límites de la validación.

## Rutinas centrales (fuente integrada)

- `GetCurrentLevelCap` (`engine/pokemon/v2_balance.asm`) devuelve el tope de nivel en B y conserva C, DE y HL. Lo reutilizan la experiencia de combate, los caramelos raros, la guardería y Tito. Lee dos tablas de pares `medalla, tope` (`V3JohtoCaps`, `V3KantoCaps`) y consulta los flags de Hall of Fame y de victoria sobre Rojo.
- `RandomizeFourMoves` genera cuatro movimientos distintos al crear un Pokémon sin tocar la tabla de aprendizaje original, con el primero siempre de daño directo repetible. `ChooseRandomLevelMove` y `ChooseRandomMoveAtDE` eligen movimientos desconocidos al subir de nivel y al retirar de la guardería. Las tablas originales (`EvosAttacks`) se conservan para el recordador de Tito.
- Los movimientos modernos reutilizan IDs de un byte con alias `DEF ... EQU ...` en `constants/move_constants.asm` ([tabla](MOVIMIENTOS-SUSTITUIDOS.md)).

## Compatibilidad de guardados

El inventario ocupa 50 montones y el PC 20 (antes 20 y 50): se conservan los 70 espacios combinados y una rutina migra guardados anteriores, principal y de respaldo. Los recursos de inicio solo se otorgan en partidas nuevas. Detalle en [COMPATIBILIDAD-GUARDADOS.md](COMPATIBILIDAD-GUARDADOS.md).

## Qué distingue base y modificación

La base (motor, mapas, gráficos y textos de Pokémon Cristal en español) procede de MicaelAlighieri/pokecristal y pret/pokecrystal. Las modificaciones están agrupadas en `parches/Cambios-fuente.patch`: 65 archivos de `engine/`, 63 de `maps/`, 57 de `data/`, 16 de `tools/`, 11 de `constants/`, 10 de `gfx/`, 2 de `ram/`, 1 de `home/` y los archivos raíz `.gitattributes` y `main.asm` (227 en total).

## Cambios de la 4.3 con restricciones de memoria

- **Rótulos de la bolsa.** El recuadro negro de la izquierda muestra el bolsillo de objetos con cinco tiles por rótulo (20 tiles, `gfx/pack/pack_categories.png`, generados por `herramientas/fuentes/build_pack_labels.py`). El banco 4 estaba casi lleno y 320 bytes de gráficos lo desbordaban, así que los tiles viven en una sección ROMX propia (`SECTION "Pack category labels"`) y se copian con `FarCopyBytes` a los tiles `$60-$73` de VRAM, libres en esa pantalla. `DrawBagCategoryName` ya no escribe texto en la fila superior: coloca los cinco tiles del rótulo en el recuadro.
- **Círculo de bolsillos.** Al entrar en ITEMS desde BALLS (izquierda) se aterriza en OTROS y desde MT/MO (derecha) en MEDICINA. El cálculo está en `PackSetCategoryOnEntry` (otro banco, vía `farcall`) para ahorrar bytes en el banco 4; antes la categoría se conservaba y desde MT/MO se volvía a entrar en OTROS.
- **Caramelos infinitos.** `RareCandyEffect` termina con `ret` en lugar de `jp UseDisposableItem`: el efecto se aplica y la cantidad no cambia.
- **Nivel blando del primer Ulex.** El área WRAM de `wUlexLocation` y compañía está dimensionada al byte: añadir una variable desplaza la sección alineada siguiente y desborda WRAM0. El nivel 15 se señala con el bit 7 de `wUlexLocation`, que `UlexSelectTeam` activa solo con cero medallas en la Ruta 31 y que `ClampProgressionLevel` consume mientras se lee el equipo; `UlexCommitEncounter` y la rama de combate rechazado lo borran para que ningún combate salvaje posterior se vea afectado.
- **Escena del anciano.** Dos eventos de coordenada en la entrada de Ciudad Cerezo (filas 6 y 7, columna 36), activos solo en la escena inicial, mueven al anciano hasta el jugador; la visita guiada y sus textos se eliminaron.
- **Suministros de la Liga.** Tres flags de evento nuevos (`EVENT_GOT_LEAGUE_*`) en un rango libre de la tabla de eventos permiten reanudar la entrega si la mochila estaba llena.
- **Tiendas.** `data/items/marts.asm` se reescribe sin objetos curativos; los tres casos que quedaban vacíos reciben artículos no curativos. Las máquinas expendedoras (dos mapas) se sustituyen por un texto.

## Cambios de la 4.4

- **Tope de nivel en la pantalla de estado.** `LoadPinkPage` termina imprimiendo «TOPE» en la fila 17 y el nivel con `PrintLevel`. `GetCurrentLevelCap` devuelve el límite en `b`; como `PrintLevel` lee `wTempMonLevel`, se guarda ese byte, se sustituye por el límite y se restaura. No se añade WRAM.
- **Iconos de categoría de ataque.** Tres tiles 2bpp (`gfx/battle/move_categories.png`, generados por `herramientas/fuentes/build_move_icons.py`) en una sección ROMX propia (`SECTION "Move category icons"`), porque el banco del combate (`Battle Core`) está casi lleno. `DrawMoveCategoryIcon` se llama con `farcall` al final del dibujo del recuadro de información del movimiento: lee los dos bits altos del tipo del movimiento (la categoría), copia los tres tiles al identificador de fondo 89 (`MOVE_CATEGORY_ICON_TILE`, libre en la pantalla de combate) con `Get2bpp` y coloca el índice correspondiente en la columna de la categoría.
- **Rótulos nativos de la mochila.** `build_pack_labels.py` redibuja en `gfx/pack/pack_menu.png` los tres rótulos originales (OBJ.CLAVE, MT/MO y BALLS) con la misma tipografía de cinco píxeles que los cuatro propios. Es arte, no código: ocupan los mismos tiles que antes.
- **Animación de reposo.** Nuevo movimiento de sprite `SPRITEMOVEDATA_STANDING_IDLE` (función `MovementFunction_StandingIdle`, acción `OBJECT_ACTION_IDLE`) con la rutina `SetFacingIdle`, que fija el fotograma «paso 0» de la dirección actual y, durante 16 de cada 128 cuadros (según `hVBlankCounter`), el «paso 1». La hoja de Tito (16×96) ya tenía una segunda mitad de fotogramas alternos; `build_tito_sprite.py` la genera ahora como la misma pose con cabeza y tronco un píxel más abajo. Los 22 Tito de los Centros Pokémon usan el nuevo movimiento. Sin VRAM ni WRAM nuevas: los sprites de pie y de paso ya se cargan en dos copias de tiles (`$3c` y `$bc`), por lo que las pruebas aceptan Tito en cualquiera de las dos copias.
- **Vista previa del randomizador.** El exportador añade al manifiesto `speciesNames`, `moveNames`, `leaders` (22 grupos de entrenador, con las claves `.__RZ` de sus ranuras de `parties.asm`) y `starterKeys`; `randomize` devuelve ahora `chosen` con las elecciones por clave. Es solo lectura y no cambia los bytes generados.

## Cambios de la 5.0

- **Más de 300 archivos en el parche** (`parches/Cambios-fuente.patch`, 302 archivos): mapas nuevos, tablas de entrenadores, una especie, datos de tiendas y el motor.
- **Una especie nueva sin romper tablas.** `DARK_LUGIA` ocupa el id `$fc`, que estaba libre entre Celebi y el huevo, de modo que `NUM_POKEMON` pasa a 252 y todas las tablas indexadas por especie (nombres, estadísticas, evoluciones, gritos, iconos, imágenes y animaciones, paletas, Pokédex, intercambios) ganan una fila. Los sprites frontal (arte aportado, 3 fotogramas de animación; los tiles de la animación están limitados por la carga de la imagen) y trasero (arte aportado desde la 5.1) son propios. Las imágenes viven en la sección `Pics 18`, porque `FixPicBank` solo conoce las secciones `Pics N` del enlazador. Los generadores de huevos, la tabla de la Superliga y el randomizador excluyen la especie.
- **Entrenadores sin tocar los existentes.** Elm usa la clase `POKEMON_PROF` (que no tenía equipos); el otro protagonista añade dos clases al final (`OTHER_BOY`, `OTHER_GIRL`, con imagen de Chris y Kris y las paletas de Cal y Falkner); la Superliga añade un id por clase (`LANCE_SUPER`, `RED_SUPER`, `BLUE_SUPER`, `ULEX_SUPER`, `TITO_XELUIS_SUPER`). Las cuatro primeras elijen sus especies en `SuperLeagueRandomizeSpecies`, llamada desde `TrainerType1`.
- **Seis mapas nuevos sin escenas.** `SUPER_LEAGUE_LOBBY`, `_AZUL`, `_LANCE`, `_ROJO`, `_ULEX` y `_TITO` se añaden al final del grupo de la Meseta Añil con los bloques de las salas de Mento y del campeón. No tienen escenas (cada escena reserva un byte de WRAM, que sigue sin hueco): el progreso de cada sala es un evento y la puerta se abre con `changeblock` en una callback de tiles.
- **Banderas y WRAM.** Ninguna variable nueva en WRAM. Las banderas de evento nuevas se asignaron en el rango que quedaba libre hasta el evento 599. Los objetos GOLD/CRISTAL/RATTATA se ocultan con banderas compartidas por varios mapas (`EVENT_OTHER_*_HIDDEN`): una bandera solo oculta al objeto al cargar su mapa, así que se pueden reutilizar. Las callbacks `MAPCALLBACK_OBJECTS` ejecutan solo la primera de su tipo en cada mapa; si ya hay una del mismo tipo se usa otro (`NEWMAP` y `OBJECTS`).
- **Textos de combate en el banco del script.** `winlosstext` toma sus punteros sin banco: los textos de victoria y derrota de cada escena viven en el archivo del mapa, no en una sección común.
- **Resultado del combate tras `reloadmap`.** Las callbacks de tiles de la sala pisan `wScriptVar` (`checkevent`); las escenas leen el resultado con `readmem wBattleResult`, que no se toca.
- **Gráficos de sprites.** `AddOutdoorSprites` llama primero a `AddIndoorSprites`: los sprites de los objetos del propio mapa ocupan los primeros huecos. Sin ello, en mapas con más de diez sprites de 12 tiles con fotogramas de andar en la lista del grupo (22 mapas), los últimos se cargaban en el bloque de la banco 0 sin fotogramas de andar y se veían deformados al moverse.
- **VRAM.** Los iconos de categoría reutilizan tres tiles de la barra de experiencia; `RestoreExpBarTiles` los devuelve al dibujar la barra (`FillInExpBar` y `AnimateExpBar`).
- **Eclosión.** `DoEggStep` se ejecuta en cada paso y recorta el contador del huevo a 10; `RerollHatchedEgg` sustituye la especie, los DVs shiny y la experiencia del nivel 5 justo antes de la eclosión.
- **Sin muertes en los duelos de exhibición.** `NuzlockeMarkPartyMonDead` sale sin marcar nada mientras está activa `EVENT_EXHIBITION_BATTLE` (duelo de Elm y Superliga).

## Cambios de la 5.1

- **`ArrangeUsedSprites` corta la lista de sprites donde ya no hay VRAM.** Cuando los sprites no cabían en las dos tablas de tiles (20 de 12 tiles), el sobrante conservaba en el byte del tile el *tipo* del sprite; `GetUsedSprites` lo leía como número de tile (3) y copiaba esos gráficos encima de los del jugador, que se veía deformado tras volver de un combate (la recarga tras `reloadmap` los dibujaba). Ahora el primer sprite que no cabe se descarta junto con el resto de la lista. Los sprites de los objetos del mapa entran primero (`AddOutdoorSprites`), de modo que lo que se descarta son los de la lista del grupo que ese mapa no usa.
- **`MoveObjectToPlayerFront` resta uno a la constante del script.** Las constantes de objeto de los scripts son el índice del objeto más uno (`GetScriptObject`); usarlas tal cual movía otro objeto.
- **Emboscada sin equipo.** `NewBarkTownRivalScript` comprueba `wPartyCount` antes de la emboscada. Un `startbattle` que no llega a empezar deja `wOtherTrainerClass`, `wOtherTrainerID` y `wBattleType` rellenos, y el siguiente encuentro salvaje se dibuja con ellos.
- **Dark Lugia:** `gfx/pokemon/dark_lugia/back.png` es la imagen trasera de Lugia (mismos índices de color) pintada con los cuatro colores de Dark Lugia (desde la 5.7); `front.png` se genera con `tools/build_dark_lugia_sprite.py` a partir del vídeo del frontal.
- **Pruebas por género.** `test-v43-changes.py` acepta `PLAYER_GENDER=1`: parchea `OakSpeech` para que guarde chica y así los recorridos se juegan como chica sin pasar por la introducción.

## Cambios de la 5.2

- **Combates rechazados.** `StartBattle` devuelve acarreo solo si hubo combate. `Script_startbattle` (que lo llama con `predef`, que conserva los flags) trata la ausencia de acarreo como una derrota: escribe `LOSE` en `wBattleResult` y activa `EVENT_BATTLE_REFUSED`. Antes el script leía el resultado del combate anterior (derrota repetida, o victoria y medalla gratis). `StartBattle` no se tocó: el bloque `Battle Core` está completo.
- **Pantalla de derrota.** `Script_BattleWhiteout` mira `EVENT_BATTLE_REFUSED`: si está activo (nunca se dibujó la pantalla de combate) hace `reanchormap` + `OverworldBGMap`, como el desmayo por veneno, y borra la bandera; si no, conserva el aspecto de la derrota tras un combate real. El texto de fin de reto ya no se dibuja sin `opentext` ni ancla sobre el mapa.

## Cambios de la 5.3

- **Banco de los textos de combate.** `PrintWinLossText` lee el texto de victoria o derrota del banco del script de la clase de entrenador (Ulex y Tito tienen el suyo) o, si no, del banco del mapa. En la Superliga las clases `ULEX` y `TITO_XELUIS` se usan con los identificadores `ULEX_SUPER` y `TITO_XELUIS_SUPER`, cuyos textos están en el mapa de la sala: ahora esos dos identificadores usan el banco del mapa. Con el banco equivocado la consola leía basura y se reiniciaba.
- **Clase de Elm.** `ELM_PROF` (al final de las tablas de clases) con `ElmPic` (`gfx/trainers/elm.png`, derivada de la de Oak: se rellena el pelo y se cambia la paleta); `POKEMON_PROF` vuelve a ser solo Oak, que usan la introducción y la radio.
- **Regalos al PC.** `LoadEnemyMon` solo tira el dado de shiny en combates salvajes. `GivePoke` llama a `BoxGiftRollShiny` (`engine/pokemon/custom_shiny.asm`) tras `LoadEnemyMon` cuando el equipo está lleno, de modo que el regalo al PC recibe la misma tirada y respeta `EVENT_FORCE_SHINY_GIFT`.
- **Caramelos raros por tandas.** `RareCandyEffect` pregunta la cantidad con `SelectQuantityToToss` y llama `RareCandy_LevelUpOnce` en bucle (se detiene en el tope vigente); la ficha de estadísticas sale una vez, `LearnLevelMoves` se llama por cada nivel ganado y `EvolvePokemon` una vez al final. El texto de la pregunta es un texto lejano (`_RareCandyHowManyText`): un texto local sin `done` colgaba la consola.
- **Tiendas.** Se eliminó la tienda `MART_GOLDENROD_STONES`; las seis piedras están en las tiendas generales de Trigal en adelante (`data/items/marts.asm`).
- **Sprite variable de Sudowoodo.** `Route36SudowoodoSpriteCallback` (`MAPCALLBACK_SPRITES`) fija `SPRITE_WEIRD_TREE` a `SPRITE_SUDOWOODO` mientras el árbol está en el mapa.
- **Guardia de Rojo.** El objeto usa la bandera `EVENT_SILVER_CAVE_GUARD_GONE`; `disappear` la activa. Los objetos con bandera -1 no se pueden ocultar de forma permanente.
- **Sandbox.** El destino de la Meseta Añil sale en (6, 10); OBJETOS recorre una lista `.HMs` y llama a `ReceiveItem` con cantidad 1.

## Cambios de la 5.4

- **Lista de gráficos de PNJ al cruzar mapas.** Desde la 5.0 `AddOutdoorSprites` añade primero los objetos del propio mapa, así que la disposición de VRAM (`wUsedSprites`) depende del mapa y no solo de su grupo. `MapSetupScript_Connection` ahora ejecuta `RebuildSpriteList` (`engine/overworld/map_setup.asm`, comando `$2e` de `data/maps/setup_script_pointers.asm`) antes de `LoadMapObjects`, para que los objetos nuevos cacheen sus tiles (`OBJECT_SPRITE_TILE`) con la disposición correcta. La rutina apaga la LCD mientras carga: con la pantalla encendida la copia de unos 300 tiles tardaba 65 fotogramas.
- **Texto de bloqueo de objeto Elegido.** `StdBattleTextbox` lee siempre del banco `$20`; los textos que se le pasan deben estar en `data/text/battle.asm`, no dentro del bloque `Battle Core`.
- **Olvidar MO.** `engine/pokemon/learn.asm` ya no llama a `IsHMMove`: las MO son herramientas de la mochila.

## Cambios de la 5.5

- **Ajustes de dificultad en una sección propia** (`engine/pokemon/progression_tuning.asm`, "Progression tuning"): `EvolveSpeciesForLevel` recorre `EvosAttacksPointers` y devuelve la especie final posible; `ProgressWildEncounter` (hierba, llamada desde `ChooseWildEncounter`) y `ProgressTempWildMon` (pesca y árboles) aplican `ClampProgressionLevel` y la evolución; `ProgressTrainerSpecies` hace lo mismo con la especie del equipo de un entrenador (`EvolveCurPartySpecies` en `read_trainer_party.asm`). Una llamada lejana (`farcall`) **no devuelve A**: el resultado va en B/C o se escribe en memoria.
- **Suelo de nivel.** `GetProgressionLevelFloor` ya no resta 3 al nivel del último líder derrotado.
- **Ataque de su tipo.** `StabForWild` (al final de `RandomizeFourMoves`, solo con `wBattleMode` salvaje) y `StabForTrainer` (en `RandomizeTrainerMon`) llaman a `EnsureStabMove`, que con seis medallas o más sustituye el cuarto movimiento por uno aleatorio de daño de los tipos del Pokémon. Los movimientos que exigen una situación especial (Autodestrucción, Come Sueños, Contador, golpes de un solo golpe…) no se eligen.
- **MT infinitas.** Se elimina `ConsumeTM` (`engine/items/tmhm.asm`).
- **Hada en el Recordador.** `TitoOfferFairyMoves` añade seis movimientos por nivel a la lista de `TitoBuildReminderMoves` (la lógica de «no repetir ni ofrecer lo conocido» pasó a `TitoOfferReminderMove`).
- **Veneno.** Cuatro IDs reutilizados (`POISON_JAB` = Agarre, `CROSS_POISON` = Atadura, `GUNK_SHOT` = Conversión, `SLUDGE_WAVE` = Conversión2) con animaciones reutilizadas de `BattleAnimations`; se quitó Conversión de las listas de la IA.
- **Emboscada por detrás.** Dos eventos de coordenadas en Pueblo Primavera (1, 8) y (1, 9) para la escena `SCENE_NEWBARKTOWN_NOOP`; el objeto del otro protagonista se coloca con `moveobject` a la derecha del jugador, corre con `big_step` y entra en el guion de emboscada existente.

## Cambios de la 5.6

- **Ulex.** `UlexCanBattle` solo calcula `wUlexBadgeCount` (lo usa el nivel blando del primer Ulex) y devuelve siempre «puede combatir»; se quitan `.WaitForBadge` y su texto.
- **Ataques modernos.** `newmoves` (21 IDs reutilizados, constantes alias `DEF AQUA_JET EQU LOVELY_KISS`…) en `constants/move_constants.asm`, `data/moves/{moves,names,descriptions,animations}.asm`; las listas de la IA (`data/battle/ai`) pierden los nombres antiguos y `engine/battle_anims/core.asm` pierde el caso especial de Kinético. `MIMIC`, `SKETCH`, `SWEET_SCENT`, `SPLASH`, `MINIMIZE`, `TELEPORT` y `FLASH` no se tocaron porque el motor depende de su ID.
- **MT.** `data/moves/tmhm_moves.asm` apunta a IDs nuevos en diez MT.
- **Recordador.** `TitoOfferModernMoves` sustituye a `TitoOfferFairyMoves`: una tabla `nivel, ataque, tipo` de 39 filas.
- **Trueques.** `TitoTradePartners` / `TitoBuildTradeList` (`engine/events/tito_xeluis.asm`): lista de códigos 1-22 (ciudades de Tito, con `GetWorldMapLocation` sobre `TitoTradeCityMaps`) y 23-28 (los seis PNJ, con `wTradeFlags`). Los nombres de ciudad salen de `GetLandmarkName`, que **debe llamarse con `farcall`** porque lee de su propio banco. Un menú que empiece en la columna 0 no se dibuja: se usa `menu_coords 1, 1, 19, 11`.
- **Emboscada.** `NewBarkTownOtherAmbushScript` se parte en la parte común (`NewBarkTownOtherAmbushGirl` / `…Boy`), a la que entra también la emboscada «por detrás» sin repetir `appear`; los saltos locales pasan a etiquetas globales.

