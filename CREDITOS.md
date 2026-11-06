# Procedencia y créditos

Proyecto personal de **Tito Xeluis** (apodo de YouTube del autor; cuenta de GitHub [Xelu94](https://github.com/Xelu94)): **Radical Cristal — Tito Xeluis** (antes «Pokémon Cristal Nuzlocke»). Modificación de aficionado, no oficial.

## Base existente

- Código fuente español: [MicaelAlighieri/pokecristal](https://github.com/MicaelAlighieri/pokecristal). Según el README de esa base, es una adaptación del trabajo inicial de [erosunica](https://github.com/erosunica/), a quien agradece el commit inicial con los cambios.
- Desensamblado de Pokémon Cristal: [pret/pokecrystal](https://github.com/pret/pokecrystal) y la comunidad que lo mantiene, de la que parten la estructura del proyecto, las herramientas de construcción y los recursos del motor.
- Los personajes, marcas y contenido original de **Pokémon** pertenecen a sus titulares (Nintendo, Creatures Inc., GAME FREAK inc. y The Pokémon Company). Este proyecto fan no es una edición oficial ni implica afiliación con ellos.
- La ROM de Pokémon Cristal original **no** se distribuye. La ROM publicada es una compilación del código modificado.

## Contribuciones propias

Distinguido de la base, el trabajo propio de este proyecto incluye:

- Reglas Nuzlocke integradas, topes de nivel, reparto de experiencia y experiencia por captura.
- División física/especial por movimiento, tipo Hada, nuevos movimientos y la sustitución de IDs.
- Aleatorización con restricciones y el randomizador portable sin conexión.
- Tito Xeluis (NPC, servicios, intercambios, jefe extra) y Ulex el Ladrón.
- Mochila y PC reorganizados, MO como herramientas, objetos equipados.
- Sandbox de pruebas y el conjunto de pruebas portables.
- Portada personalizada «Radical Cristal» y la marca «©2026 Tito Xeluis inc.», que identifica **este proyecto**, no la base ni los titulares de Pokémon.

## Recursos gráficos de Tito

Referencias personales aportadas por el autor, apoyo de generación de imágenes y adaptación al formato y paleta del motor. Detalle en [docs/RECURSOS-TITO.md](docs/RECURSOS-TITO.md). No se importaron recursos de Prism.

## Sprite de Dark Lugia

El sprite frontal de Dark Lugia es arte de aficionado de **SageDeoxys** (la imagen trasera es, desde la 5.7, la de Lugia con la paleta de Dark Lugia) ([deviantart.com/sagedeoxys](https://www.deviantart.com/sagedeoxys)), publicado en DeviantArt; el autor del proyecto lo aportó como vídeo animado para usarlo en este juego. No se ha comprobado la licencia de uso de esa obra. Si SageDeoxys pide retirarlo, se sustituirá por otro gráfico (basta cambiar `gfx/pokemon/dark_lugia/front.png`). El frontal se redujo a 56×56 píxeles y cuatro colores (tres fotogramas de animación); no se distribuye el vídeo ni la imagen original.

## Herramientas

RGBDS, Make/GCC, Python, Pillow, PyBoy, Node.js, Playwright, mGBA y Floating IPS (parches BPS). Cada herramienta mantiene su procedencia y su licencia. Sus ejecutables no se distribuyen aquí.

## Licencia

Ver [LICENCIA.md](LICENCIA.md): licencias por tipo de contenido propio (MIT, CC BY-NC 4.0); no se ha asignado ninguna licencia al contenido heredado.
