# Mecánicas y reglas vigentes (v5.6)

Descripción de la ROM normal. Los datos numéricos se contrastaron con la fuente integrada (`engine/pokemon/v2_balance.asm`, `data/moves/moves.asm`, `data/pokemon/evos_attacks.asm`). Cuando una regla depende del emulador o de la semilla, se indica.

## Nuzlocke

- **Muerte permanente** al llegar a 0 PS, también por veneno fuera del combate y en los contextos que contempla el motor. Los muertos no se curan, no luchan, no se intercambian ni usan MO. Al depositarlos en el PC desaparecen.
- **Captura ordinaria**: solo el primer encuentro ordinario de cada zona con nombre. Huir, debilitarlo o dejarlo escapar consume la oportunidad. En ese primer combate se pueden lanzar varias Balls. Las plantas de una cueva y los distintos métodos de encuentro comparten zona.
- **Excepciones**: regalos, huevos, iniciales, intercambios, tutorial y encuentros de evento. Un evento puede capturarse aunque ya se haya usado la captura ordinaria de la zona. Los Pokémon errantes también cuentan como evento.
- **Tras perder el equipo** se puede continuar si quedan reservas vivas (PC, guardería; los huevos cuentan como reservas futuras). Sin supervivientes, termina la partida.

## Combate y experiencia

- **Categoría por movimiento**: física, especial o de estado, independiente del tipo. Las estadísticas Ataque, Defensa, Ataque Especial, Defensa Especial y Velocidad ya estaban separadas en la segunda generación; lo nuevo es que cada movimiento declara su categoría.
- **Subpanel de combate**: potencia, tipo, categoría y PP del movimiento seleccionado dentro del marco del menú, con los cuatro nombres completos. La potencia también aparece en las pantallas de movimientos. El arreglo fue de distribución del panel; no se cambió la tipografía.
- **Iconos de categoría (4.4)**: el subpanel muestra un icono (estallido, espiral u óvalo) en lugar de texto para físico, especial y estado.
- **Poder Oculto** muestra tipo y potencia reales calculados con los DVs de segunda generación, coherentes con el combate (contrastado con 768 combinaciones de DVs).
- **Reparto de experiencia**: los participantes vivos reciben la recompensa completa; las reservas vivas, la mitad. Huevos y Pokémon muertos no ganan experiencia.
- **Experiencia por captura**: aproximadamente la mitad de derrotarlo. El Pokémon recién capturado no recibe experiencia por su propia captura.
- **Tope de nivel**: al alcanzar el límite vigente se reciben 0 puntos de experiencia (4.4: el límite vigente se ve en la primera página de estado como «TOPE»). Se aplica también a caramelos raros y guardería. Los Pokémon intercambiados obedecen hasta ese límite incluido.
- **Viento Hielo** conserva daño y bajada de Velocidad con una animación simplificada; se retiró una ruta gráfica problemática. Se probaron doce ejecuciones completas sin reinicio. El fallo original, observado en un emulador móvil con un guardado concreto, no se reprodujo con esos mismos elementos.

## Tipos y movimientos

- **Tipo Hada**, con actualización de los tipos de las especies correspondientes y ajustes de efectividades. Hada es inmune a Dragón. Acero resiste Fantasma y Siniestro, como en generaciones modernas.
- **Movimientos nuevos**: Fuerza Lunar, Carantoña y Brillo Mágico, más treinta y cuatro modernos que sustituyen a otros en el mismo ID (cuatro de tipo Veneno y veintiuno de otros tipos, como Acua Jet o Energibola) ([tabla](MOVIMIENTOS-SUSTITUIDOS.md)).
- **Movimientos iniciales aleatorios**: cuatro distintos, con al menos uno de daño directo utilizable. En los hitos de aprendizaje por nivel se ofrecen movimientos aleatorios.
- **Recordador de Tito**: consulta las tablas originales de movimientos hasta el nivel actual y respeta los identificadores sustituidos. Además ofrece los ataques modernos añadidos por este proyecto (de Hada, Veneno, Agua, Planta, Eléctrico…) a cualquier Pokémon con ese tipo y el nivel suficiente: 39 ataques en 18 tipos (p. ej. Hada: Viento Hada 5, Encanto 10, Luz Lunar 20, Brillo Mágico 30, Carantoña 40, Fuerza Lunar 50; Agua: Acua Jet 12, Escaldar 30, Acua Cola 40).
- **MT y MO**: las 50 MT tienen contenidos aleatorios únicos y **no se gastan al usarlas** (desde la 5.5); las siete MO conservan sus movimientos.

## Límites de nivel y dificultad

Ver [NIVELES-Y-EVOLUCIONES.md](NIVELES-Y-EVOLUCIONES.md) para la tabla completa.

- El límite sigue al **primer líder pendiente** en el orden de progresión, aunque se visiten los gimnasios en otro orden.
- Con ocho medallas de Johto el límite es 65 hasta superar la Liga. Con las dieciséis medallas es 95. **Rojo exige las dieciséis medallas y tiene seis Pokémon al nivel 95.** Al derrotarlo se desbloquea el nivel 100 (el equipo de Rojo no está al 100).
- Salvajes (en hierba, al pescar y en árboles) y entrenadores no bajan del **nivel del último líder derrotado**, con excepciones para rutas iniciales (29, 30 y 31) y encuentros de nivel especial. Desde la 5.5, además, salen evolucionados hasta donde su nivel lo permite, y desde la sexta medalla todos conocen un ataque de daño de su tipo.
- Líderes y Alto Mando suben 5 niveles; progresión revisada entre Johto y Kanto y objetos equipados útiles.
- Una partida actualizada no pierde los niveles que ya tuviera por encima de un nuevo tope.

## Aleatorización

- 251 especies de las dos primeras generaciones. Iniciales, salvajes, entrenadores, regalos, huevos y eventos son aleatorios con restricciones por nivel, línea evolutiva y potencia. No aparecen legendarios antes del nivel 55.
- Otra distribución se genera con el [randomizador sin conexión](RANDOMIZADOR.md). **Cambiar de semilla requiere una partida nueva.**

## Shiny y eventos

- Probabilidad general shiny del 20 %, incluidos los huevos. Los eventos salvajes, los errantes y los equipos de Tito y Ulex son shiny garantizado. Se conserva el sistema de DVs de segunda generación.
- Los DVs shiny se mantienen al capturar, enviar directamente al PC, depositar o retirar. Una actualización no puede reconstruir DVs que ya se perdieron en un guardado anterior.
- **Santuario del Encinar**: se activa sin GS Ball, una vez por partida. El evento original de Celebi está aleatorizado: en la ROM publicada aparece **Misdreavus shiny al nivel 25**. Otra semilla puede cambiar la especie; no es un Celebi fijo.

## Tito Xeluis

- Presente en 22 Centros Pokémon, con nombre, menús, diálogos, retrato de combate y sprite de mapa propios. Antes de empezar, explica las reglas Nuzlocke en un diálogo inicial.
- **Intercambio**: uno completado por ciudad antes de derrotarlo. Eliges libremente un Pokémon vivo y ves la especie exacta ofrecida (potencia comparable, mismo nivel) antes de confirmar. Cancelar no consume el intercambio.
- Servicios gratuitos: consulta de límites de nivel, recordador de movimientos y guía de evoluciones modificadas, y (MÁS → TRUEQUES) una lista de con quién puedes intercambiar aún y dónde: él mismo en sus ciudades (todas tras vencerle) y Mike, Kyle, Tim, Emy, Kim y Forest.
- **Jefe extra** tras vencer a Rojo: Charizard, Tyranitar, Dragonite, Gengar, Scizor y Mewtwo, todos shiny al nivel 100, con movimientos aleatorios y objetos. Se puede repetir el combate; la muerte permanente sigue aplicándose.
- Solo vencer a Tito desbloquea intercambios ilimitados en todos sus centros.
- Los intercambios genéricos de otros NPC usan la misma propuesta y confirmación, pero solo se completa uno por NPC; se puede preguntar y cancelar sin penalización.

## Ulex el Ladrón

- Dieciséis encuentros independientes en las rutas 31, 32, 34, 37, 41, 39, 43, 44, 6, 8, 11, 12, 14, 15, 17 y 25.
- Se presenta con un disfraz de NPC según la ruta (cazabichos, pescador, chica, joven, marinero, motorista…). Tras su giro se muestra siempre como recluta Rocket.
- Equipos aleatorios shiny al límite de nivel vigente, de tres, cuatro o cinco Pokémon según la etapa. **Excepción:** el primer Ulex (Ruta 31, antes de ninguna medalla) saca sus tres Pokémon al nivel 15 en lugar de 19; los demás encuentros no cambian. Desde la 5.6 no hay cerrojo por medallas: cada ubicación se combate **una vez**, en cuanto lo encuentras, en el orden que recorras las rutas.
- **Victoria sin nuevas muertes**: una MT aleatoria. **Si hay una nueva muerte**, roba otro Pokémon vivo y entrega a ZURULLO, un Rattata de nivel 5 que solo conoce Salpicadura; en ese caso no hay MT.
- Los combates rechazados no gastan el encuentro. Los resultados reales se registran antes de recargar el mapa.

## Historia y mundo (v5.0)

- **Aviso de Ulex.** El NPC de la Ruta 29 que enseñaba a capturar avisa ahora de que ULEX anda por la CUEVA OSCURA y recomienda el nivel 15.
- **Duelo de Elm, otro protagonista y Superliga:** ver [SUPERLIGA-Y-RIVAL.md](SUPERLIGA-Y-RIVAL.md).
- **Huevos.** Eclosionan a los 10 pasos en un Pokémon aleatorio shiny de su primera etapa (sin legendarios).
- **Enfermeras Joy** (rutas 13, 14, 25, 26, 27 y 46), **piedras evolutivas** a la venta (desde la 5.3) en las tiendas normales de Ciudad Trigal en adelante, **BAYA DORADA** en los árboles de bonguri y **MÁX. POCIÓN** en lugar de cualquier Ball del mapa o de regalo (la Master Ball se mantiene).
- **Objetos de combate infinitos y precio 0.** Banda Focus, Cinta Elegida, Gafas Elegidas, Pañuelo Elegido y Restos de la partida nueva no se consumen al equipar o devolver; ellos, los caramelos raros y la Master Ball se venden por 0.
- **Dark Lugia:** especie 252, no capturable; se entrega a nivel 100 al vencer a Tito por primera vez.

## Calidad de vida e inventario

- **MO como herramientas**: requieren la MO en la mochila, la medalla y un Pokémon vivo, sin aprender el ataque. Vuelo y Destello aparecen como acciones en el submenú de cualquier Pokémon (VUELO y DESTELLO) mientras se tenga la MO; Vuelo también se usa desde el mapa exterior del Pokégear hacia ciudades visitadas.
- **Mochila de 50 montones y PC de 20**, conservando los 70 espacios combinados. Bolsillos MEDICINA, BAYAS, COMBATE y OTROS, además de MT/MO, Balls y objetos clave. El nombre del bolsillo de objetos se muestra en el recuadro negro de la izquierda y los bolsillos forman un círculo con izquierda/derecha: MEDICINA, BAYAS, COMBATE, OTROS, BALLS, OBJ. CLAVE, MT/MO y de nuevo MEDICINA (el filtro TODOS con Start se retiró).
- **Partida nueva**: 99 Master Balls, un montón de 99 caramelos raros **infinitos** (usar uno no lo consume; el tope de nivel sigue frenándolos) y diez unidades de Banda Focus, Cinta Elegida, Gafas Elegidas, Pañuelo Elegido y Restos. Los recursos gastados no se regeneran al actualizar.
- **Objetos equipados**: los elegidos multiplican por 1,5 y bloquean el movimiento hasta cambiar de Pokémon. Restos recupera 1/16 de los PS. Banda Focus (y la variante antigua adaptada) actúa a PS completos ante un golpe directo letal, deja 1 PS y se consume; los ataques múltiples pueden rematar después.
- **Tiendas sin curas.** Ninguna tienda vende pociones, revivir, antídotos y demás curas de estado, bebidas curativas ni CARAM. FURIA, y las máquinas expendedoras están vacías. Los repelentes siguen en la primera tienda con renovación al agotarse. La madre y los revividores encontrados entregan MT aleatorias en su bolsillo.
- **Suministros de la Liga.** Con las ocho medallas de Johto, el oficial de la Puerta de la CALLE VICTORIA entrega una sola vez 8 MÁX. POCIÓN, 10 HÍPER POCIÓN y 7 RESTAU. TODO (si la mochila está llena, se completa al volver a hablar con él).
- **El mapa del Pokégear.** Al entrar por primera vez en CIUDAD CEREZO, el anciano se acerca solo y entrega la TARJ. MAPA; ya no hay visita guiada.
- **Evoluciones** por intercambio o amistad sustituidas por nivel o piedra ([tabla](NIVELES-Y-EVOLUCIONES.md)).

## Diferencias entre ROM normal y sandbox

Ver [SANDBOX.md](SANDBOX.md). Resumen: el sandbox es otra compilación con su propio guardado y un menú de pruebas; la descarga pública es solo la ROM normal.
