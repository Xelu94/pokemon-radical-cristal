# Resumen para portfolio

**Radical Cristal — Tito Xeluis (v5.6)**

Modificación personal de Pokémon Cristal para Game Boy Color, construida sobre la fuente española de MicaelAlighieri/pokecristal y el desensamblado de la comunidad pret/pokecrystal. Integra en el motor un Nuzlocke con muerte permanente y primera captura por zona, topes de nivel ligados a los líderes, física/especial por movimiento, tipo Hada, mochila reorganizada, aleatorización por restricciones y dos personajes propios: Tito Xeluis (intercambios, recordador de movimientos y jefe extra) y Ulex el Ladrón (16 encuentros disfrazados).

El trabajo es ingeniería sobre un proyecto existente: ensamblador SM83 con bancos de ROM, WRAM y far calls; reutilización de identificadores de movimiento para no romper guardados; migración de inventario; asignación de VRAM y sprites de 16×16 en 2bpp; y un randomizador en HTML/CSS/JavaScript que genera la ROM en el navegador sin conexión. La validación ejecuta la ROM con PyBoy y el randomizador con Node y Playwright: 137 comprobaciones agrupadas en 4.3 y reconstrucción exacta de las ROM desde el parche, sin pretender una cobertura porcentual ni una campaña completa.

Tecnologías: RGBDS 1.0.0, Make/GCC, Python/Pillow, PyBoy, Node.js, Playwright, parche de fuente y hashes SHA-256.

Se distribuye una única ROM `.gbc` en GitHub Releases. Proyecto fan no oficial; la base y los derechos de Pokémon se reconocen en el repositorio.
