# Cambios

Formato por versión. Las versiones anteriores a la 4 no están documentadas en este paquete; solo se sabe que la actualización v3→v4 permite continuar el guardado.

## 5.5 — Más dificultad: niveles, evoluciones, ataques de su tipo y rival por detrás (30 de octubre de 2026)

Siete cambios pedidos tras jugar la 5.4 hasta el evento Rocket de la Torre Radio. **269 comprobaciones agrupadas** ([evidencias/Validacion-v5.5.json](evidencias/Validacion-v5.5.json)): las 222 de la 5.4 más las nuevas de esta versión (rutinas y recorrido de historia, como chico y como chica).

1. **Niveles al mismo nivel que el último líder.** Una vez vences a un líder (o a un as de la Liga), los entrenadores y los Pokémon salvajes que vienen después ya no bajan de **su nivel exacto** (antes, tres niveles menos). Los salvajes también se elevan al pescar y al sacudir árboles, no solo en la hierba. Siguen exentas las rutas 29, 30 y 31 y los encuentros de nivel especial.
2. **MT infinitas.** Usar una MT ya no la gasta.
3. **Curva de dificultad más marcada: sin Pokémon a medio evolucionar.** Al generar un salvaje o un Pokémon de entrenador, evoluciona hasta donde le permite su nivel: las evoluciones por nivel cuando se alcanza el umbral (un Croconaw de nivel 40 pasa a ser Feraligatr) y las de piedra única desde el nivel 32 (Pikachu → Raichu); Eevee y las familias con muchas piedras no cambian. Se comprobaron 795 equipos de entrenador: ninguno conserva un Pokémon que su nivel debiera haber evolucionado.
4. **El otro protagonista te alcanza por detrás.** La primera vez que, con un Pokémon, caminas hacia el oeste para entrar en la Ruta 29, GOLD o CRISTAL aparece corriendo detrás de ti, te llama y empieza el combate. Ya no hace falta hablar con Plata junto al laboratorio (esa vía sigue funcionando; la emboscada solo ocurre una vez).
5. **Movimientos Hada para el Recordador de Tito.** Los Pokémon de tipo Hada pueden recordar Viento Hada, Encanto, Luz Lunar, Brillo Mágico, Carantoña y Fuerza Lunar según su nivel (5, 10, 20, 30, 40 y 50), aunque su tabla original no los tenga (Mr. Mime no aprendía ninguno).
6. **Desde la sexta medalla, todo Pokémon con un ataque de su tipo.** Con seis o más medallas (Johto y Kanto sumadas), cada Pokémon salvaje o de entrenador tiene al menos un ataque de daño de su tipo (el cuarto movimiento se sustituye si no lo tiene).
7. **Más ataques de tipo Veneno.** Cuatro movimientos modernos sustituyen a otros poco útiles en el mismo ID, con su propia animación: Puya Nociva (80, física), Veneno X (70, física), Lanzamugre (120, física, 80 % de precisión) y Onda Tóxica (95, especial), todos con probabilidad de envenenar. Pasan a ser, por ID, los de Agarre, Atadura, Conversión y Conversión2 ([tabla](docs/MOVIMIENTOS-SUSTITUIDOS.md)).

**Límites:** un Pokémon de un guardado anterior que conociera Agarre, Atadura, Conversión o Conversión2 pasa a conocer el movimiento nuevo (se comprobó el ID, no los PP guardados). La dificultad sube de forma notable: los topes de nivel del jugador no cambian.

ROM de esta versión (reconstruida desde la base española aplicando el parche con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal (`Radical Cristal.gbc`) | `b5530aa12dd945ae99ffb2045d4927c32e9077d9d0dbb899d21cfa3deb5738e8` |
| Sandbox | `ec31d24151faf0a4dc80640d35aa93f426c8ce5277aac907a3b922dca2ddc050` |

## 5.4 — Revisión de los beta testers: sprites, Elegidos y MO (25 de octubre de 2026)

Dos beta testers automáticos (uno jugando como GOLD y otro como CRISTAL) recorrieron los mapas, los PNJ, los ataques y los menús en el emulador. Hallaron seis errores, todos corregidos. **222 comprobaciones agrupadas** ([evidencias/Validacion-v5.4.json](evidencias/Validacion-v5.4.json)): las 217 de la 5.3 más 5 nuevas. Registro completo de causas y soluciones: [docs/ERRORES-Y-SOLUCIONES.md](docs/ERRORES-Y-SOLUCIONES.md); informes de los testers: [pruebas/beta](pruebas/beta).

**Errores corregidos**

1. **Reinicio de la consola al elegir otro ataque con Banda, Gafas o Pañuelo Elegidos.** El aviso «El objeto elegido fija el ataque.» estaba en un banco de ROM distinto del que lee el motor de texto de combate. Es la causa más probable de «Inversión cierra el juego»: ese ataque no falla en ninguna prueba (los 254 ataques, como jugador y como rival). El texto ahora está en `data/text/battle.asm`.
2. **Los PNJ cambiaban de sprite al volver a un mapa o cruzar una zona** (PLATA y el guía de Ciudad Cerezo tras el primer combate, la profesora de la Ruta 29, PNJ de Ciudad Trigal). Al cruzar el borde de un mapa a pie no se reconstruía la lista de gráficos, y la siguiente recarga dejaba a cada PNJ con los gráficos de otro. Nuevo paso `RebuildSpriteList` en el cruce de mapas, antes de crear los objetos. 287 cruces entre mapas sin fallos (antes 32 con fallos).
3. **El PNJ de la Ruta 29 que avisa de Ulex se distorsionaba al andar** al llegar desde Pueblo Primavera a pie, que es el camino de toda partida nueva. Mismo origen que el punto 2.
4. **El otro protagonista no estaba en la lista de gráficos de Pueblo Primavera** al entrar desde las rutas 27 o 29. Mismo origen.
5. **Comillas del campeón de la Superliga:** `«»` se imprimían como símbolos raros; ahora son `“”`.
6. **Los movimientos MO no se podían olvidar.** Los ataques aleatorios pueden ser Corte, Vuelo, Surf, Fuerza, Destello, Torbellino o Cascada (34 de 251 especies tras usar caramelos raros) y el menú de olvidar los rechazaba, aunque las MO ya son herramientas de la mochila. Se quita esa comprobación.

**Límites:** el cruce de mapas apaga la pantalla unos 7 fotogramas mientras recarga los gráficos (como al cerrar un menú); está medido en emulador, no en una consola real. El fallo exacto de «Inversión» no se ha reproducido con el ataque en sí; si vuelve a ocurrir, indica si llevabas equipado un objeto Elegido.

ROM de esta versión (reconstruida desde la base española aplicando el parche con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal (`Radical Cristal.gbc`) | `91845e52c2afee9f0f6e0425f15fc62e7685aff5c116284cceee768ac00e67c1` |
| Sandbox | `4afbf8921e51f9086bbb5412f9d43f7ede1b1271c1aff42d9ff5ec106d9d2020` |

## 5.3 — Revisión de la Superliga, Elm, tiendas y caramelos (23 de octubre de 2026)

Corrige lo que salió al probar la 5.2 con el sandbox y añade tres mejoras. **217 comprobaciones agrupadas** ([evidencias/Validacion-v5.3.json](evidencias/Validacion-v5.3.json)): las 200 de la 5.2, las nuevas de esta versión y el recorrido de historia ampliado, jugado como chico y como chica.

**Errores corregidos**

1. **Reinicio al vencer o perder contra ULEX o TITO en la Superliga.** El texto de victoria o derrota de un entrenador se lee del banco de ROM de su clase: para ULEX y TITO XELUIS el motor suponía los scripts de sus encuentros normales, pero en la Superliga los textos viven en el mapa de cada sala. Se leían de un banco equivocado y la consola se reiniciaba («Este cartucho está diseñado para ser usado únicamente en Game Boy Color»). Ahora la Superliga usa el banco del mapa (`PrintWinLossText`). Comprobado ganando y perdiendo contra los dos.
2. **Elm combatía con la imagen de Oak.** El duelo usaba la clase de entrenador de Oak (que también sale en la introducción). Ahora Elm tiene su propia clase, `ELM_PROF`, y su propia imagen (la de Oak con el pelo castaño y los pantalones marrones).
3. **Los tres regalos de Elm no eran shiny al ir a la caja.** Con el equipo lleno los Pokémon regalados van al PC y esa vía nunca tiraba el dado de shiny (ni el forzado). Ahora lo hace, así que los regalos forzados (Elm, la Superliga) son shiny vayan al equipo o a la caja, y los demás regalos al PC tienen la misma probabilidad que los del equipo.
4. **Sandbox: «Viajar» a la Liga te dejaba dentro de la pared.** La casilla de llegada al Centro Pokémon de la Meseta Añil estaba mal. Se comprobaron los 41 destinos: el resto son transitables (en Ciudad Iris el anciano Bill y en el laboratorio de Elm la escena de llegada te sujetan unos segundos, como en el juego original).
5. **TITO hablaba de sí mismo en tercera persona** al pulsar SUPERLIGA sin haberle vencido. Ahora habla en primera persona. El entrenador de la Meseta conserva su texto.
6. **El guardia que cierra el paso a ROJO no desaparecía** al dejarte pasar. Ahora se aparta para siempre (bandera propia).
7. **Sudowoodo se dibujaba con el sprite de otro PNJ** en partidas que se saltaron el script de partida nueva o que mezclaron sus banderas (el sandbox): su gráfico es un sprite variable. Ahora, mientras el árbol está en el mapa, es Sudowoodo.
8. **Imagen trasera de Dark Lugia más grande**: ahora es el recorte central de 48×48 del arte original (antes se había reducido).

**Mejoras**

9. **Piedras evolutivas en las tiendas.** Las seis piedras se compran en las tiendas normales de Ciudad Trigal en adelante (Trigal, Olivo, Ecruteak, Caoba, Orquídea, Endrino, Azulona…, Viridian, Plateada, Celeste, Lavanda, Carmín, Azafrán, Fucsia, Celadón, Monte Moon y Meseta Añil). Se quitó el vendedor del Centro Pokémon de Trigal, que vuelve a ser el chico de la Game Boy.
10. **Caramelos raros varios a la vez.** Tras elegir el Pokémon sale un selector de cantidad (1 a 99): sube todos los niveles de golpe hasta el tope vigente, muestra una sola ficha de estadísticas, enseña los movimientos de cada nivel y evoluciona al final. Siguen sin consumirse.
11. **Sandbox: OBJETOS también entrega las siete MO** (Corte, Vuelo, Surf, Fuerza, Destello, Torbellino y Cascada).

**Revisión general:** los 394 mapas cargan y ningún objeto se queda sin sprite; humo de 373 mapas; ningún texto nuevo supera las 18 columnas; la Superliga se juega entera (victoria y derrota de Azul, Lance, Rojo, Ulex y Tito) sin reinicios; Pokédex y combates con Dark Lugia.

**Límites:** no he podido reproducir el cambio de sprite de PLATA tras el primer combate (en Ciudad Cerezo se ve igual antes y después en la ROM normal y en la del sandbox, con y sin el estado de partida nueva); si vuelve a verse hacen falta los pasos exactos o la partida. PLATA en Ciudad Olivo es la escena del juego original (aparece al entrar por la ruta del este); en el sandbox se activa al saltar hasta allí. Con el reto terminado, cada intento de combate sigue mostrando el mensaje de fin (diseño).

ROM de esta versión (reconstruida desde la base española aplicando el parche con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal (`Radical Cristal.gbc`) | `aab4601450c38aa762b643033df21af26dd698cb30d44dce50f92780783e6408` |
| Sandbox | `880a161a97ae2321565a751ca58c4284d796263f490c4aba67a1fe5b90f020d6` |

## 5.2 — Mensaje de fin del reto (23 de octubre de 2026)

Corrige el mensaje de «has perdido el reto» que salía cortado y desplazado, y un fallo relacionado que podía dar una medalla sin combatir. **200 comprobaciones agrupadas** ([evidencias/Validacion-v5.2.json](evidencias/Validacion-v5.2.json)): las 198 de la 5.1 con una más en cada recorrido de historia (chico y chica).

1. **Un combate rechazado cuenta como derrota.** Con el reto Nuzlocke terminado (o sin Pokémon aptos) el motor rechaza todo combate nuevo, pero el script de después leía el resultado del combate *anterior*: casi siempre una derrota. El juego repetía entonces la pantalla de «pierdes el conocimiento» y «NUZLOCKE: no quedan #MON vivos. Fin de la partida. Empieza NUEVA PARTIDA» con el mapa a la vista, sin haber anclado la caja de texto: se veía desplazada y cortada por la izquierda y la parte de arriba. Ahora `Script_startbattle` detecta el rechazo, fija la derrota y marca `EVENT_BATTLE_REFUSED`; `Script_BattleWhiteout` en ese caso ancla el mapa y limpia la pantalla como la derrota por veneno, y el texto sale entero. La derrota tras un combate real no cambia.
2. **Un líder de gimnasio ya no da la medalla si el combate se rechaza.** Si el último combate se había ganado, el resultado antiguo valía como victoria y el líder entregaba la medalla sin combatir (con el reto terminado). Nueva prueba: con el reto terminado, un líder no combate, no da medalla y la pantalla de derrota sale completa.
3. **Pruebas.** Una comprobación más en el recorrido de historia (chico y chica).

**Límites:** con el reto terminado, cada intento de combate (encuentro salvaje o entrenador) vuelve a mostrar el mensaje de fin y te devuelve al Centro Pokémon; es la forma que tiene el juego de decir que hay que empezar una partida nueva.

ROM de esta versión (reconstruida desde la base española aplicando el parche con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal (`Radical Cristal.gbc`) | `6861c67987485a36df0e3c4a83906bd68f778a7b649466984dffdeb31ffc590b` |
| Sandbox | `2d39b0abac24322576aa1deaa00e5ed09279958f37db97e5e01d69e2af9bf747` |

## 5.1 — Correcciones y arte propio de Dark Lugia (23 de octubre de 2026)

Corrige los fallos que aparecían al hablar con el rival al principio de la partida y al volver de un combate, y sustituye la imagen trasera de Dark Lugia. **198 comprobaciones agrupadas** ([evidencias/Validacion-v5.1.json](evidencias/Validacion-v5.1.json)): las 173 de la 5.0 con dos más del recorrido de Pueblo Primavera, y el recorrido de historia repetido jugando como chica (22 + 22).

1. **El otro protagonista ya no embosca a quien no tiene Pokémon.** Al hablar con PLATA junto a la ventana antes de recibir el inicial se activaba la emboscada: el combate no podía empezar, pero quedaban guardados en memoria el entrenador y el tipo de combate, y el primer encuentro salvaje de la ruta se dibujaba como un combate contra ella; después aparecían fallos al abrir el menú. Ahora, sin Pokémon, solo ocurre el empujón de Plata y la emboscada espera a la siguiente conversación con equipo (nueva prueba, que además comprueba que no quedan banderas ni objeto).
2. **Imagen trasera de Dark Lugia** nueva: arte de [SageDeoxys](https://www.deviantart.com/sagedeoxys) aportado por el autor del proyecto, convertido a 48×48 y 4 colores y con la marca roja de la barriga eliminada. El frontal sigue siendo el de la 5.0.
3. **Sprites tras un combate.** Con la lista de gráficos ampliada, algunos mapas superaban los 20 sprites de 12 tiles que caben en la VRAM; el sobrante no se descartaba y `GetUsedSprites` leía su tipo como número de tile y escribía encima de los tiles del jugador, que se veía deformado al volver de un combate. Ahora `ArrangeUsedSprites` corta la lista donde ya no cabe nada. Comprobado en los 394 mapas (ningún objeto se queda sin sprite) y con una prueba nueva que compara los tiles del jugador antes y después de la emboscada.
4. **El otro protagonista aparecía lejos.** `MoveObjectToPlayerFront` usaba la constante del script como índice del objeto sin restarle uno, así que en las emboscadas de Pueblo Primavera, Torre Bellsprout y Guarida Dragón movía otro objeto y ella aparecía en su sitio del mapa (detrás del cartel de Pueblo Primavera). Ahora aparece en la casilla frente al jugador (prueba nueva).
5. **Pruebas.** El recorrido de historia se ejecuta ahora dos veces: jugando como chico (la emboscada la hace CRISTAL) y como chica (la hace GOLD), y comprueba además que el otro protagonista aparece delante del jugador y que los tiles de su sprite no cambian tras el combate.

**Revisión general de esta versión:** los 394 mapas cargan y ningún objeto se queda sin sprite; humo de 373 mapas con una caminata aleatoria (se omiten los ascensores y las salas de enlace, que esperan hardware); ningún texto nuevo supera las 18 columnas; las Pokédex nueva, vieja y A-Z muestran a Dark Lugia con su sprite; las cuatro emboscadas y el combate final se completan jugando como chico y como chica (la de la Guarida Dragón con un parche de la ROM que fuerza la presencia del rival).

**Límites:** no pude reproducir tal cual el aviso de «CRISTAL en el mundo y GOLD en el combate» eligiendo a CRISTAL: en esta versión, con jugadora, GOLD se ve igual en el mapa y en el combate en las cuatro escenas; lo más probable es que fuera la lista de sprites desbordada de la 5.0 (punto 3). Si vuelve a verse, ayudará una captura con la partida. Dark Lugia sigue teniendo solo tres fotogramas de animación.

ROM de esta versión (reconstruida desde la base española aplicando el parche con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal (`Radical Cristal.gbc`) | `339f38f5d51b9bd1a4adcd28e1767fbbf32ef4e0e343f4965acbdc9cb4fa00e5` |
| Sandbox | `b060483611e9bb5c1fbc88607e2f5a218ac500bbb268962279725a1cb4702183` |

## 5.0 — Radical Cristal (22 de octubre de 2026)

El juego pasa a llamarse **Radical Cristal** (pantalla de título, Randomizador, README y la Release). Es la versión con más contenido nuevo desde la 4.0: un cambio en la historia (el otro protagonista y el duelo de Elm), una liga extra, un Pokémon nuevo y varios arreglos. Detalle de las partes nuevas en [docs/SUPERLIGA-Y-RIVAL.md](docs/SUPERLIGA-Y-RIVAL.md). **173 comprobaciones agrupadas** ([evidencias/Validacion-v5.0.json](evidencias/Validacion-v5.0.json)): las 140 de la 4.4, 1 nueva de la barra de experiencia y 32 de esta versión.

**Mundo y objetos**

1. **El NPC del tutorial de captura avisa de Ulex.** En lugar de enseñar a capturar, te cuenta que han visto a ULEX más allá de la CUEVA OSCURA, que es un ladrón peligroso y que subas tus Pokémon al nivel 15 antes de llegar (coincide con el nivel del primer Ulex). Ya no hay combate de tutorial.
2. **Bonguri → Baya dorada.** Los siete árboles de bonguri dan BAYA DORADA.
3. **Balls → Máx. Poción.** Las 32 Balls colocadas en mapas (en el suelo, ocultas y regalos de NPC, incluidas las cinco Poké Balls del ayudante de Elm y los regalos de Kurt y Wilton) dan MÁX. POCIÓN. La Master Ball se mantiene. Las tiendas siguen vendiendo Balls.
4. **Enfermeras Joy** en las rutas sin Centro Pokémon cerca: 13, 14, 25, 26, 27 y 46. Curan al equipo (sin muertos). **No hay en la Ruta 17**: es la ciclovía de bajada forzada y no se puede frenar ni girar hacia arriba, así que una enfermera no sería alcanzable.
5. **Objetos de combate infinitos.** Banda Focus, Cinta Elegida, Gafas Elegidas, Pañuelo Elegido y Restos de la partida nueva conservan sus 10 unidades pero no se gastan al equiparlos (devolverlos tampoco aumenta la pila). Ellos, los caramelos raros y la Master Ball **valen 0** en las tiendas.
6. **Huevos:** eclosionan a los **10 pasos** y siempre dan un **Pokémon aleatorio shiny de su primera etapa** (sin legendarios ni Dark Lugia); conservan los cuatro movimientos aleatorios con los que se generaron.
7. **Piedras evolutivas** a la venta en el CENTRO POKÉMON de CIUDAD TRIGAL (Piedra Fuego, Agua, Trueno, Hoja, Lunar y Solar).
8. **Título:** «RADICAL CRISTAL» sobre el logo (`tools/build_title_branding.py`).

**Errores corregidos**

9. **Animación de andar del rival (y de otros PNJ).** En CIUDAD CEREZO (y en 22 mapas más) algunos PNJ que caminan se dibujaban con los fotogramas de pie, porque la lista de gráficos exteriores del grupo tenía más sprites de los que caben con fotogramas de andar. Ahora los sprites de los objetos del propio mapa se cargan primero (`AddOutdoorSprites`). Comprobado en los 394 mapas (`pruebas/simulacion`): ninguno queda con un PNJ andando sin fotogramas.
10. **Barra de experiencia.** Los iconos de categoría de la 4.4 reutilizaban tiles de la barra; al abrir el panel de ataques, la barra mostraba esos símbolos en su extremo. Ahora se restauran al volver a dibujar la barra (`RestoreExpBarTiles`).

**Historia**

11. **Duelo con Elm.** Al darte la Master Ball (y en cada visita posterior hasta que lo hagas), Elm te ofrece un combate con los niveles de DÉBORA; sin muertes. Si ganas te regala un FERALIGATR, un MEGANIUM y un TYPHLOSION shiny al nivel 53 (una vez).
12. **El otro protagonista (GOLD si eres chica, CRISTAL si eres chico).** Emboscadas tras las tres escenas en que Plata solo habla (Pueblo Primavera, Torre Bellsprout, Guarida Dragón): combate, cura a tu equipo, te da una MÁX. POCIÓN y se va. Combate final al entrar al Centro Pokémon de la Meseta Añil con un huevo de recuerdo; después vive en la casa de los vecinos de Pueblo Primavera con un RATTATA y cambia un ZURULLO de Ulex por un Pokémon aleatorio de tercera etapa.
13. **Superliga.** Se abre al vencer a Tito (por su menú MÁS → SUPERLIGA o hablando con el entrenador de la Meseta). Cuatro retadores al nivel 100 con equipos aleatorios fuertes (Azul, Lance, Rojo, Ulex sin robo) y Tito como campeón (Mew, Celebi, Lugia, Ho-Oh, Dragonite, Mewtwo). Sin muertes, 99 RESTAU. TODO al entrar; si caes, los pierdes y hay que vencer otra vez a Tito; si ganas, un CHARIZARD shiny nivel 100 con una carta. Seis mapas nuevos con los gráficos de la Liga.
14. **Dark Lugia** (nº 252, Siniestro/Volador, PS 106, Atq 130, Def 90, Vel 110, At. Esp. 154, Def. Esp. 90). No es capturable: se entrega a nivel 100 la primera vez que vences a Tito. Su sprite frontal es el arte de aficionado de Dark Lugia que aportó el autor (obra de [SageDeoxys](https://www.deviantart.com/sagedeoxys) en DeviantArt; ver [CREDITOS.md](CREDITOS.md)), convertido a 4 colores con tres fotogramas de animación; la imagen trasera es la de Lugia con la paleta oscura.

**Límites y cosas que no se han hecho**

- Dark Lugia usa solo tres fotogramas de animación (el límite de tiles de la animación de Lugia es estricto) y su imagen trasera es la de Lugia recoloreada; su grito es el de Lugia con otro tono.
- El combate del campeón de la Superliga no se juega entero en las pruebas (equipos de leyendas con Recuperación); se comprueba su flujo de recompensa con un atajo y el resto de la sala con el combate de Azul.
- El huevo de Elm (Togepi) también eclosiona en un Pokémon aleatorio: la rama de la historia que reconoce a TOGEPI puede no darse.
- Los textos del juego son los acordados con el autor; no se han revisado todas las líneas del juego original (solo las nuevas se auditaron por anchura).

ROM de esta versión (reconstruida desde la base española aplicando el parche con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal (`Radical Cristal.gbc`) | `5b9fb58edd1742f2de4b6a1bbc9999e05f48c31d3ac28a44200650e2f3133ecd` |
| Sandbox | `ec9dbc978709369f95218bb1afca61927ca27b225b95f2f4fd832cee416a0130` |

### Compatibilidad

No necesita partida nueva respecto a la 4.4: las nuevas banderas de evento usan bits que estaban libres y la tabla de especies llega a la 252, que no cambia el tamaño de los registros del Pokédex. Los objetos de combate y la Master Ball siguen siendo los que ya tuvieras. El randomizador de esta versión solo acepta la ROM 5.0 (cambia la firma de la parte inmutable). Un guardado con una Poké Ball sin recoger la verá convertida en Máx. Poción.

## 4.4 — Interfaz y herramientas (22 de octubre de 2026)

Cinco mejoras de interfaz y herramientas propuestas en el [informe de playtest](docs/INFORME-PLAYTEST-v4.3.md) y aprobadas por el autor, más dos correcciones de texto. La compilación pasa 140 comprobaciones agrupadas ([evidencias/Validacion-v4.4.json](evidencias/Validacion-v4.4.json)): las 137 anteriores y 3 nuevas.

1. **Tope de nivel en la pantalla de estado.** La primera página de estado muestra «TOPE» y el límite vigente (por ejemplo 24 con una medalla) en su fila inferior, con la misma rutina `GetCurrentLevelCap` que usa el combate. El menú de Tito ya consultaba el límite en su propio flujo y no se ha modificado.
2. **Iconos de categoría en el subpanel de ataques.** La categoría física, especial o de estado se dibuja con un icono de un tile en lugar de texto. Los tres iconos (estallido, espiral y óvalo) se generan con `herramientas/fuentes/build_move_icons.py`, viven en una sección ROMX propia y se cargan en un tile de fondo libre al abrir el panel.
3. **Rótulos en toda la mochila.** MT/MO, BALLS y OBJ.CLAVE se redibujan con la misma tipografía que MEDICINA, BAYAS, COMBATE y OTROS; reutilizan los tiles originales de `gfx/pack/pack_menu.png`, sin tiles nuevos.
4. **Tito respira.** En los Centros Pokémon, Tito alterna dos fotogramas cada pocos segundos (hombros y cabeza un píxel más bajos). Usa el fotograma alterno que la hoja ya tenía, un nuevo movimiento de sprite (`SPRITEMOVEDATA_STANDING_IDLE`) y la acción `OBJECT_ACTION_IDLE`; no consume VRAM ni WRAM adicionales.
5. **Randomizador con vista previa.** Tras generar, la página muestra los iniciales, los equipos de los 22 líderes, Alto Mando y rivales principales (nombres de especie) y las 50 MT de la semilla. Solo muestra nombres; no hay sprites.
6. **Dos líneas desbordadas** (la profesora de CIUDAD CEREZO y el santuario del Encinar) detectadas por el playtest. Antes estaban sueltas en `parches/correcciones-v4.3.1.patch`; ahora están integradas en `Cambios-fuente.patch`.
7. **Integración continua** (`.github/workflows/verificacion.yml`; el script que usa está en [`pruebas/ci`](pruebas/ci)): sintaxis de herramientas y pruebas, descarga de la ROM de la Release enlazada en el README, comprobación de su SHA-256 y prueba del randomizador con esa ROM. Su primera ejecución real (23 de octubre de 2026) terminó con éxito.

ROM publicada (reconstruida desde la base española aplicando el parche y compilando con RGBDS 1.0.0):

| | SHA-256 |
|---|---|
| ROM normal | `b4cff3b076988a780d6570653d677b7fecab1cbb4fdfcc6dde8cda5a22c1e3ef` |
| Sandbox | `f77fb27ec0e2365985be7cc7d6045fde364a9e3e6ad484e2a1df5aab74b3706e` |

### Compatibilidad

No necesita partida nueva respecto a la 4.3. El randomizador de esta versión solo acepta la ROM 4.4 (cambia la firma de la parte inmutable). Otra semilla del randomizador sigue requiriendo partida nueva.

## 4.3 — Mejoras de jugabilidad (21 de octubre de 2026)

Ocho cambios pedidos por el autor tras jugar la 4.2. Se validaron con 13 comprobaciones nuevas más las 124 anteriores (137 en total, [evidencias/Validacion-v4.3.json](evidencias/Validacion-v4.3.json)); no equivalen a una campaña completa.

1. **Vuelo desde el menú del Pokémon.** Con la MO Vuelo en la mochila, la medalla de Tormenta y un Pokémon vivo, aparece VUELO en el submenú del Pokémon (igual que Destello). El vuelo desde el mapa exterior del Pokégear se conserva.
2. **El anciano de CIUDAD CEREZO entrega el mapa sin hablarle.** Al entrar en la ciudad le sale una exclamación, se acerca, dice que usó la tarjeta «para limpiarme los mocos» y se la da, y desaparece. Se eliminó la visita guiada. Si el jugador le habla, también se la da.
3. **El primer Ulex (Ruta 31, sin medallas) saca sus Pokémon al nivel 15** en lugar de 19. Solo ese encuentro: los demás Ulex siguen en el límite vigente.
4. **Las tiendas ya no venden objetos curativos.** Se quitaron pociones, revivir, antídotos y demás curas de estado, bebidas curativas y CARAM. FURIA de las 34 tiendas. Tres tiendas que quedaban vacías (Ciudad Orquídea, el primer mostrador de la planta 2 del Gran Almacén de Ciudad Trigal y el herbolario subterráneo) venden ahora Poké Balls, Superrepelentes, repelentes o Cuerdas Huida. Las máquinas expendedoras de Ciudad Trigal y Ciudad Azulona están vacías.
5. **Suministros de la Liga.** El oficial de la Puerta de la CALLE VICTORIA, al comprobar las ocho medallas de Johto, entrega una sola vez 8 MÁX. POCIÓN, 10 HÍPER POCIÓN y 7 RESTAU. TODO.
6. **Diálogo inicial de Tito reescrito.** Sintaxis corregida y reglas Nuzlocke explicadas paso a paso (capturas, excepciones, muerte, fin de la aventura, límite de nivel, intercambios, Ulex).
7. **99 caramelos raros infinitos.** Una partida nueva empieza con un único montón de 99 que no se consume al usarlo (antes 999 finitos en 11 montones). Libera 10 espacios de la mochila. Los guardados existentes conservan sus montones y todos los caramelos pasan a ser infinitos.
8. **Mochila más clara.** El tipo de objeto (MEDICINA, BAYAS, COMBATE, OTROS) se muestra ahora en el recuadro negro de la izquierda, en lugar del rótulo «Objetos» y de la línea superior. La navegación es un círculo: derecha desde OTROS pasa a Balls, Obj.Clave y MT/MO, y vuelve a MEDICINA; izquierda desde MEDICINA llega a MT/MO y, al volver desde Balls, se entra en OTROS.

Notas técnicas: el banco 4 de la ROM está casi lleno, por lo que los gráficos de los rótulos viven en una sección propia y el cálculo del punto de entrada de la mochila está fuera de ese banco. No se añadió WRAM; el nivel blando del primer Ulex usa el bit 7 de `wUlexLocation`. Se añadieron tres flags de evento en el rango antes libre.

### Compatibilidad

No necesita partida nueva. Las curas ya compradas se conservan. Otra semilla del randomizador sigue requiriendo partida nueva, y el randomizador de esta versión solo acepta la ROM 4.3 (cambia la firma de la parte inmutable).
## 4.2 — Sprites y sandbox (20 de octubre de 2026)

Tres correcciones. Las pruebas citadas (124 comprobaciones) se resumieron en evidencias/Validacion-v4.2.json, que se conserva en la etiqueta 4.2 del historial de Git; ninguna equivale a una campaña completa.

### 1. Sprite de Tito: cuadrícula nativa y direcciones

- **Problema.** El sprite de Tito en los centros no tenía la calidad ni la estructura de direcciones que exige el motor: contornos y ojos poco legibles a 16×16 y fotogramas alternos incompletos.
- **Causa.** Según la documentación del generador, reescalar la hoja grande de referencia a 16×16 pierde ojos y contornos, y el motor necesita frente, espalda e izquierda seguidos de fotogramas alternos completos para no leer datos ajenos al gráfico. Esta lectura se basa en la nota del generador y en el registro de cambios 4.2; no se conserva una captura del estado anterior.
- **Solución.** El arte se define ahora en una cuadrícula nativa de 16×16 (contornos, sombreado, ojos separados del bigote, silueta con sombrero y pañuelo). La hoja tiene tres poses (frente, espalda, izquierda) y tres fotogramas alternos completos; la derecha se refleja por hardware. Se compila a 16×96 en 2bpp con `herramientas/fuentes/build_tito_sprite.py`.
- **Validación.** 4 comprobaciones de orientaciones renderizadas (tiles y reflejo reales, no solo la variable de dirección) y 48 de servicios y mapas de Tito.

### 2. Ulex: espacio de gráficos en exteriores

- **Problema.** El sprite variable de Ulex (disfraz y revelación) podía mostrarse con los tiles del jugador.
- **Causa.** Las tablas de gráficos de los mapas exteriores no tenían registro para `SPRITE_COPYCAT`; `GetSpriteVTile` recurría a los tiles del jugador.
- **Solución.** Se reserva un espacio gráfico para el sprite variable reutilizando un espacio exterior sin uso, de la misma capacidad, en lugar de añadir gráficos sin límite (la VRAM es limitada). Los 16 encuentros tienen un disfraz de NPC según la ruta y, tras el giro, cargan siempre el gráfico de recluta Rocket.
- **Validación.** Disfraz y revelación comprobados en las 16 rutas con los bytes reales de VRAM (grupo de 17 comprobaciones junto con Objetos).

### 3. Sandbox: OBJETOS se bloqueaba

- **Problema.** La opción OBJETOS del sandbox colgaba el juego.
- **Causa.** Llamaba directamente a `ReceiveRandomTM`, situada en otro banco de ROM; la dirección se ejecutaba en el banco equivocado.
- **Solución.** Se sustituyó por la llamada que cambia de banco (far call) a `ReceiveRandomTM`, que conserva y restaura el banco. OBJETOS entrega 10 de cada uno de Repelente, Superrepelente, Máximo Repelente, Banda Focus, Poción y Restaurar Todo, y 7 MT aleatorias si hay capacidad; se puede repetir.
- **Validación.** Una prueba entra desde el menú real, usa OBJETOS dos veces, comprueba cantidades y 14 MT en total, y vuelve al mapa.

### Compatibilidad

No necesita partida nueva. Guarda dentro del juego, cierra el emulador y carga el `.sav` con la nueva ROM. No uses estados rápidos de otra compilación. Otra semilla del randomizador sigue requiriendo partida nueva. El retrato de combate de Tito y sus servicios se conservan.

## 4.1 — Interfaz y calidad de vida (19 de octubre de 2026)

1. La potencia, el tipo, la categoría y los PP ocupan un subpanel compacto dentro del marco de combate; los cuatro nombres de ataque conservan todo su ancho.
2. Ulex aparece con el sprite genérico propio de cada ruta antes del giro y revela después su sprite de ladrón.
3. La mochila usa cuatro bolsillos de objetos (MEDICINA, BAYAS, COMBATE, OTROS) navegables con izquierda/derecha junto a MT/MO, Balls y objetos clave. Start deja de alternar filtros y desaparece la vista duplicada TODOS.
4. SUBIR MEDALLAS del sandbox abre un selector de 0 a 16 y recalcula el límite al instante.
5. Una partida nueva recibe 99 Master Balls en un único montón. Los guardados existentes conservan sus cantidades.
6. Todos los intercambios con entrenadores genéricos usan el flujo de Tito: eliges Pokémon, ves la especie exacta y aceptas o cancelas. Solo el primer intercambio completado queda gastado.
7. El sprite de Tito en los centros se sustituye por el nuevo lienzo, con frente, espalda y perfil.

## 4.0 — Sistemas y contenido

1. Tito en los centros: hoja de sprites completa, poses y colores corregidos; los menús muestran su nombre; el retrato de combate se conserva.
2. Recordador: desaparecen los sprites del mapa sobre los menús y se restauran las paletas. Nueva consulta gratuita de evoluciones modificadas.
3. Intercambio: seleccionas, ves la oferta exacta y confirmas. Cancelar no gasta el intercambio de la ciudad.
4. Antes de Oak, Tito explica Nuzlocke, capturas, muertes, límites y Ulex.
5. La madre compra MT aleatorias para su bolsillo. Los revividores encontrados y el regalo de Trigal pasan a MT.
6. Repelentes desde la primera tienda; se renuevan al agotarse con prioridad Máximo, Super, Repelente.
7. Los Pokémon muertos desaparecen al depositarlos en el PC.
8. Mochila de 20 a 50 montones, PC de 50 a 20 (70 combinados), con migración automática comprobada con guardados v3 principal y de respaldo.
9. Ulex el Ladrón: 16 disfraces en Johto y Kanto, giro y revelación, equipo aleatorio shiny al límite de nivel, MT por victoria sin nuevas muertes o robo y ZURULLO (Rattata nivel 5 con Salpicadura) si hay una nueva muerte. Los combates rechazados no consumen el encuentro.
10. El shiny mostrado al encontrarlo se conserva al capturarlo y enviarlo al PC. Eventos salvajes y errantes son shiny garantizado y no consumen la captura ordinaria de la zona.
11. Santuario del Encinar: Misdreavus shiny nivel 25 en la distribución incluida; el randomizador cambia la especie según la semilla.
12. Potencia visible en la selección de combate, estado y detalle de movimientos. Poder Oculto muestra tipo real y potencia calculada con los DVs.
13. Líderes y Alto Mando suben 5 niveles. Rojo tiene seis Pokémon al 95. Límite 95 con 16 medallas y 100 tras Rojo. Salvajes y entrenadores respetan el mínimo del líder anterior menos tres.
14. Los Pokémon intercambiados obedecen hasta el límite vigente incluido.
15. Banda Focus y Cinta-Focus: solo a PS completos, sobreviven con 1 PS ante un golpe directo letal y se consumen; un ataque múltiple puede rematar.
16. Viento Hielo conserva daño y bajada de Velocidad con una animación más simple. Probado con Bayleef en 12 usos completos sin reinicio; el fallo móvil original no se reprodujo.
17. Nueve ataques modernos adicionales con animaciones del motor.
18. Los 254 identificadores estaban ocupados: nueve ataques se sustituyen en su mismo ID ([tabla](docs/MOVIMIENTOS-SUSTITUIDOS.md)).
19. Randomizador portable por semilla, sin instalación ni conexión ([docs](docs/RANDOMIZADOR.md)).
20. Sandbox separado con 41 accesos rápidos y 388 destinos en 26 grupos.

### Validación y límites de 4.0

Se compilaron versiones normal y sandbox con RGBDS 1.0.0 y se ejecutaron rutinas reales en PyBoy, pruebas de interfaz y combate, migración de guardados v3, aleatorización en Node y generación/descarga en navegador. Se mantienen 251 especies. No hay habilidades, megas ni recursos de Prism.
