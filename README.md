# Radical Cristal — Tito Xeluis

Modificación personal de **Pokémon Cristal** (antes «Cristal Nuzlocke») para Game Boy Color con un Nuzlocke integrado en el motor, combate modernizado, aleatorización por niveles, una liga extra y personajes propios. Versión **5.7**. Autor: **Tito Xeluis** (apodo de YouTube; [@Xelu94](https://github.com/Xelu94) en GitHub). El NPC Tito Xeluis del juego lleva el nombre del autor.

> *English summary:* **Radical Cristal** is a personal ROM hack of Pokémon Crystal (Game Boy Color, SM83 assembly) built on the Spanish source tree of [MicaelAlighieri/pokecristal](https://github.com/MicaelAlighieri/pokecristal) and the [pret/pokecrystal](https://github.com/pret/pokecrystal) disassembly. It adds built-in Nuzlocke rules, per-move physical/special split, a Fairy type, level caps, a custom NPC (Tito Xeluis), a roaming thief (Ulex), the other protagonist as a rival, a 5-fight Super League at level 100, a new Dark Lugia, a sandbox build for testing and an offline seed-based randomizer. It is **not** a game written from scratch and **not** an official Pokémon product. Spanish only. Download the single `.gbc` from [Releases](https://github.com/Xelu94/pokemon-radical-cristal/releases) and open it in a Game Boy Color emulator.

![Pantalla de título de Radical Cristal](capturas/titulo-radical-cristal.png)

![Selección de ataques con potencia, tipo, categoría y PP](capturas/combate-panel.png)

## Descarga y cómo jugar

**[⬇ Descargar Radical Cristal.gbc (v5.7)](https://github.com/Xelu94/pokemon-radical-cristal/releases/download/v5.7/Radical.Cristal.gbc)** — enlace directo al asset de la [Release v5.7](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.7). GitHub sustituye los espacios del nombre por puntos en la URL; el archivo es el mismo.

Versiones anteriores publicadas: [v5.6](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.6), [v5.5](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.5), [v5.4](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.4), [v5.3](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.3), [v5.2](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.2), [v5.1](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.1), [v5.0](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v5.0), [v4.4](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v4.4), [v4.3](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v4.3) y [v4.2](https://github.com/Xelu94/pokemon-radical-cristal/releases/tag/v4.2).

| | |
|---|---|
| Archivo | `Radical Cristal.gbc` (2 MiB) |
| Versión | 5.7 |
| SHA-256 | `d7f6d1067171632c2f24c2c40520c2c7a66b9c75672d13f31dd4215a14eb46e0` |
1. Descarga el único archivo `.gbc` de la Release. No hay ZIP, parches ni instalador: no necesitas una ROM base ni aplicar nada.
2. Ábrelo con un emulador compatible con Game Boy Color (por ejemplo mGBA). El emulador se obtiene por separado y no forma parte de este proyecto.
3. Guarda dentro del juego. Las actualizaciones de esta familia continúan el guardado interno (`.sav`); no uses estados rápidos de otra compilación. Detalles en [compatibilidad de guardados](docs/COMPATIBILIDAD-GUARDADOS.md).

El modo de velocidad ×2 depende de las opciones del emulador de cada jugador; no es una aceleración añadida al motor.

Comprueba la descarga (PowerShell): `Get-FileHash "Radical Cristal.gbc" -Algorithm SHA256`.

## Qué aporta al jugador

- **Nuzlocke dentro del juego.** Muerte permanente (también por veneno fuera de combate), una captura ordinaria por zona con nombre, excepciones para regalos, huevos, iniciales, intercambios y eventos. Sin supervivientes, termina la partida.
- **Combate modernizado.** Categoría física/especial/estado por movimiento, tipo Hada con resistencias actualizadas y 12 movimientos nuevos. Potencia, tipo, categoría y PP aparecen en un subpanel del menú de combate.
- **Límites de nivel progresivos** ligados a los líderes de Johto y Kanto, que también frenan la experiencia, los caramelos raros y la guardería.
- **Aleatorización por restricciones**: iniciales, salvajes, entrenadores, regalos, huevos y eventos, con topes por nivel, línea evolutiva y potencia. Sin legendarios antes del nivel 55.
- **Experiencia repartida**: participantes vivos, mitad para reservas vivas y experiencia por captura.
- **Mochila y objetos**: el tipo de objeto (MEDICINA, BAYAS, COMBATE, OTROS) se lee en el recuadro negro de la bolsa y los bolsillos forman un círculo; 99 caramelos raros infinitos; MO como herramientas (Vuelo también desde el menú del Pokémon); objetos equipados útiles; evoluciones por intercambio o amistad sustituidas por nivel o piedra.
- **Sin curas en las tiendas.** Ninguna tienda vende pociones, revivir ni curas de estado; en la LIGA, el oficial de la CALLE VICTORIA entrega una vez 8 MÁX. POCIÓN, 10 HÍPER POCIÓN y 7 RESTAU. TODO.
- **Tito Xeluis** en 22 Centros Pokémon: intercambios, recordador de movimientos, guía de evoluciones y un jefe extra tras vencer a Rojo.
- **Ulex el Ladrón**: 16 encuentros disfrazados en rutas de Johto y Kanto.
- **Superliga y otro protagonista**: una liga extra tras vencer a Tito y un rival nuevo (GOLD o CRISTAL) con tres emboscadas, un combate final y un canje.
- **Sandbox** (compilación aparte, no se distribuye como descarga): viajes, medallas, equipo y objetos para probar; incluye los mapas de la Superliga.

![Bolsa con el tipo de objeto en el recuadro negro](capturas/bolsa-medicina.png) ![Menú del Pokémon con VUELO](capturas/menu-vuelo.png)
![Reglas Nuzlocke explicadas por Tito](capturas/tito-reglas.png) ![El anciano entrega el mapa](capturas/anciano-mapa.png)

![Cuatro orientaciones del sprite de Tito](capturas/tito-direcciones.png)

Reglas completas: [docs/MECANICAS.md](docs/MECANICAS.md).

## Retos de ingeniería

El proyecto evoluciona una base existente de ensamblador SM83 con límites estrictos de memoria e identificadores.

- **Movimientos sin ampliar la tabla.** Los 254 identificadores de movimiento ya estaban usados; treinta y cuatro movimientos modernos (cuatro de tipo Veneno y veintiuno de otros tipos) sustituyen a otros en el mismo ID para no romper guardados ([tabla](docs/MOVIMIENTOS-SUSTITUIDOS.md)).
- **Nuevo reparto de experiencia, capturas y topes** integrados en las rutas de combate, caramelos y guardería, con una única rutina de límite (`GetCurrentLevelCap`).
- **Compatibilidad de guardados.** El inventario se amplía de 20 a 50 montones y el PC se reduce de 50 a 20 conservando los 70 espacios combinados, con migración automática de guardados anteriores.
- **Límites de memoria.** El banco 4 de la ROM está casi lleno y la WRAM sin hueco: los rótulos de la bolsa viven en una sección propia y el nivel blando del primer Ulex reutiliza un bit existente en vez de reservar una variable ([detalle](docs/ARQUITECTURA.md)).
- **Gráficos en VRAM.** El sprite de Tito se define en una cuadrícula nativa de 16×16 y se compila a una hoja de 16×96 en 2bpp con tres colores visibles más transparencia. Ulex necesitó reservar un espacio gráfico para su sprite variable en las tablas de mapas exteriores.
- **Llamadas entre bancos.** Un fallo del sandbox venía de llamar directamente a una rutina de otro banco de ROM ([explicación](docs/ARQUITECTURA.md)).
- **Randomizador sin conexión** en HTML/CSS/JavaScript sin framework: semilla repetible, manifiesto de posiciones mutables y firma de la parte inmutable de la ROM. Genera la ROM en el navegador sin enviar datos a ningún servidor ([documentación](docs/RANDOMIZADOR.md)).
- **Pruebas que ejecutan la ROM** con PyBoy (rutinas reales y recorridos de interfaz con montajes controlados) y Playwright (randomizador en navegador sin solicitudes de red) ([pruebas](docs/COMPILACION-Y-PRUEBAS.md)).

![Randomizador sin conexión](capturas/randomizador.png)

### Novedades de la versión 5.7

- **Superliga:** el premio de TITO (CHARIZARD SHINY) ya no deja encerrado a nadie con el equipo lleno: va al PC y, si tampoco cabe, te saca de la sala y el premio te espera.
- **Dark Lugia** usa por detrás los gráficos de Lugia con su propia paleta.

### Novedades de la versión 5.6

- **Ulex sin cerrojo:** ya no te pide otra medalla; lo combates cuando lo encuentras (una vez por ubicación).
- **El otro protagonista** corre hacia la Ruta 29 y desaparece tras la primera pelea (antes se quedaba su sprite).
- **21 ataques modernos** (Acua Jet, Energibola, Chispazo, Esfera Aural, Roca Afilada…) en lugar de ataques inservibles, también en las MT.
- **Tito recuerda esos ataques** según el tipo del Pokémon y tiene una opción **TRUEQUES** que dice con quién puedes intercambiar aún y dónde.

### Novedades de la versión 5.5

- **Más dificultad.** Tras vencer a un líder, entrenadores y salvajes se igualan a **su nivel** (antes, tres menos), también al pescar y sacudir árboles.
- **Sin Pokémon a medio evolucionar:** al generarse, evolucionan hasta donde su nivel lo permite (un Croconaw al 40 ya es Feraligatr).
- **Desde la sexta medalla**, todo Pokémon salvaje o de entrenador conoce un ataque de su tipo.
- **MT infinitas**, **ataques Hada** en el Recordador de Tito para los Pokémon Hada y **cuatro ataques Veneno nuevos** (Puya Nociva, Veneno X, Lanzamugre y Onda Tóxica).
- **El otro protagonista te alcanza por detrás** al dirigirte a la Ruta 29 con tu primer Pokémon.

### Novedades de la versión 5.4

- **Revisión de dos beta testers automáticos** (uno como GOLD y otro como CRISTAL). Registro de errores y soluciones: [docs/ERRORES-Y-SOLUCIONES.md](docs/ERRORES-Y-SOLUCIONES.md).
- **Ya no se reinicia la consola** al elegir otro ataque con Banda, Gafas o Pañuelo Elegidos (probable causa de «Inversión cierra el juego»).
- **Los PNJ ya no cambian de sprite** al cruzar un mapa a pie y volver; el PNJ de la Ruta 29 que avisa de Ulex ya no se distorsiona al andar.
- Los movimientos MO que salen al azar **se pueden olvidar**, y las comillas del campeón de la Superliga se ven bien.

### Novedades de la versión 5.3

- **La Superliga ya no reinicia la consola** al vencer o perder contra Ulex o Tito.
- **Elm** pelea con su propia imagen, y sus tres regalos son shiny también cuando van a la caja.
- **Piedras evolutivas en todas las tiendas** de Ciudad Trigal en adelante, y **caramelos raros por tandas** (selector de cantidad).
- Sandbox: la Meseta Añil ya no te deja en la pared y OBJETOS da las siete MO. Además: el guardia de Rojo se aparta, Sudowoodo se ve bien, Dark Lugia tiene la imagen trasera más grande y Tito habla en primera persona.

![Elm con su propia imagen](capturas/elm-duelo-imagen.png)

### Novedades de la versión 5.2

- El mensaje de «fin del reto» sale entero y en su sitio (antes salía cortado y desplazado sobre el mapa), y un combate rechazado ya no puede dar una medalla.

![Mensaje de fin del reto, completo y sobre pantalla limpia](capturas/fin-del-reto.png)

### Novedades de la versión 5.1

- Sin Pokémon, hablar con Plata ya no activa la emboscada del otro protagonista (dejaba un combate a medias que rompía el menú).
- GOLD/CRISTAL aparece delante del jugador, y el sprite del jugador ya no se deforma tras el combate.
- Imagen trasera de Dark Lugia: la de Lugia con la paleta de Dark Lugia (el frontal sigue siendo arte de SageDeoxys).

![Dark Lugia, de frente y de espaldas](capturas/dark-lugia.png)
![Gold, el otro protagonista si juegas con ella](capturas/otro-protagonista-gold.png)

### Novedades de la versión 5.0

- **Superliga** al vencer a Tito: cuatro retadores y un campeón al nivel 100, sin muertes, con 99 RESTAU. TODO y la carta final ([detalle y diálogos](docs/SUPERLIGA-Y-RIVAL.md)).
- **El otro protagonista** (GOLD o CRISTAL) te embosca tras las escenas en que Plata solo habla, te da un último combate en la Meseta Añil y vive después en Pueblo Primavera.
- **Duelo con Elm** y tres starters shiny.
- **Dark Lugia** (Siniestro/Volador, estadísticas ofensivas) al vencer por primera vez a Tito.
- **Enfermeras Joy** en las rutas lejos de un Centro Pokémon, **piedras evolutivas** (desde la 5.3, en las tiendas), **bayas doradas** en vez de bonguri, **Máx. Poción** en lugar de Balls y huevos que eclosionan en 10 pasos en un shiny aleatorio.
- El aviso sobre Ulex en lugar del tutorial de captura, objetos de combate infinitos, y los arreglos de la animación de andar y de la barra de experiencia.

![Duelo con Elm](capturas/duelo-elm.png)
![El otro protagonista](capturas/otro-protagonista.png)
![Superliga](capturas/superliga.png)
![Dark Lugia](capturas/dark-lugia.png)
![Enfermera Joy en una ruta](capturas/enfermera-joy.png)

Novedades de la 4.4: tope de nivel en la pantalla de estado, iconos de categoría en el panel de ataques, rótulos en toda la mochila, Tito respira y vista previa de la semilla en el randomizador.

![Tope de nivel](capturas/estadisticas-tope.png) ![Iconos de categoría](capturas/iconos-categoria-ataque.png)
![Rótulos de la mochila](capturas/bolsa-rotulos.png) ![Tito respira](capturas/tito-reposo.png)


## Tecnología

Ensamblador LR35902/SM83 · RGBDS 1.0.0 (rgbasm, rgblink, rgbfix, rgbgfx) · Make y utilidades C/GCC · Python y Pillow (recursos, manifiestos, hashes) · PyBoy 2.8.1 (pruebas) · HTML, CSS y JavaScript sin framework · Node.js · Playwright · parche de fuente (git diff) y reconstrucción verificada byte a byte (SHA-256 de las compilaciones; parches BPS solo en versiones anteriores, con SHA-1 de la ROM de referencia).

No es una aplicación React, Electron, Unity ni Godot, y no usa servidor, base de datos ni cuentas.

## Estado y validación

La versión 5.7 pasó **310 comprobaciones agrupadas** en 24 grupos (servicios y mapas de Tito, Ulex, combate, randomizador y navegador sin conexión, interfaz de la 4.3 y 4.4, rutinas y recorridos de la 5.x, arreglos de los beta testers; los recorridos de historia se ejecutan como chico y como chica). Es un recuento de comprobaciones, **no un porcentaje de cobertura**; algunas agrupan muchos casos (Poder Oculto se contrasta con 768 combinaciones de DVs). Las comprobaciones de informes de versiones anteriores no se suman.

La reconstrucción también está comprobada: aplicar el parche a la base española y compilar con RGBDS 1.0.0 produce exactamente los SHA-256 de la ROM normal y de la compilación sandbox de los informes.

Límites reales: los montajes omiten la introducción; algunos combates aumentan el daño para recorrer los equipos; en Ruta 17 se desactiva la gravedad solo en la prueba. No se ha completado una campaña entera ni queda demostrado el equilibrio global. El fallo móvil original de Viento Hielo no se reprodujo con el mismo emulador y guardado del usuario. La integración continua (flujo de GitHub Actions y script en [`pruebas/ci`](pruebas/ci)) solo comprueba herramientas y el randomizador contra la ROM de la Release; la compilación y las pruebas con emulador se ejecutan en local. Informe: [evidencias/Validacion-v5.7.json](evidencias/Validacion-v5.7.json).
No implementado: habilidades, megaevolución, generaciones tercera/cuarta, recursos de Prism.

## Contenido del repositorio

| Carpeta | Contenido |
|---|---|
| [`docs/`](docs) | Mecánicas, Superliga y rival, arquitectura, compilación y pruebas, compatibilidad, movimientos, niveles, sandbox, randomizador, recursos |
| [`parches/`](parches) | `Cambios-fuente.patch`: modificaciones del código fuente sobre la base española |
| [`recursos/`](recursos) | Sprites y paleta de Tito Xeluis |
| [`herramientas/`](herramientas) | Randomizador portable y sus fuentes, generador del sprite |
| [`pruebas/`](pruebas) | Scripts de validación portables, herramientas de [playtest automatizado](pruebas/simulacion) y scripts de [integración continua](pruebas/ci) |
| [`evidencias/`](evidencias) | Informes JSON de las pruebas (4.3, 4.4 y 5.0) |
| [`capturas/`](capturas) | Capturas reales |
| [`publicacion/`](publicacion) | Textos de la Release, descripción y resumen para portfolio |

Informe de playtest y equilibrio: [docs/INFORME-PLAYTEST-v4.3.md](docs/INFORME-PLAYTEST-v4.3.md). Cambios por versión: [CHANGELOG.md](CHANGELOG.md). Procedencia: [CREDITOS.md](CREDITOS.md). Licencias (MIT para el código propio, CC BY-NC 4.0 para documentación y arte de Tito; sin licencia propia para parche y ROM): [LICENCIA.md](LICENCIA.md).

## Créditos

Basado en la traducción al español de [MicaelAlighieri/pokecristal](https://github.com/MicaelAlighieri/pokecristal), que a su vez adapta el trabajo inicial de [erosunica](https://github.com/erosunica/), y en el desensamblado de [pret/pokecrystal](https://github.com/pret/pokecrystal). Pokémon y sus personajes pertenecen a sus titulares; este proyecto fan no es oficial ni está afiliado a ellos. Las modificaciones, herramientas y recursos propios (Tito Xeluis, Ulex, reglas, randomizador, pruebas) son de Tito Xeluis, apodo del autor; la marca «©2026 Tito Xeluis inc.» identifica el proyecto, no la base. Detalle en [CREDITOS.md](CREDITOS.md).
