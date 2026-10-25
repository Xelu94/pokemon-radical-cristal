# Radical Cristal — Tito Xeluis v5.4

Modificación personal de Pokémon Cristal para Game Boy Color, basada en el código fuente español de MicaelAlighieri/pokecristal y el trabajo de la comunidad pret/pokecrystal. No es un producto oficial de Pokémon.

## Descarga

Un único archivo jugable: **`Radical Cristal.gbc`** (ROM normal v5.4).

- SHA-256: `91845e52c2afee9f0f6e0425f15fc62e7685aff5c116284cceee768ac00e67c1`
- No necesita ROM base ni aplicar parches. Ábrela con un emulador compatible con Game Boy Color (se obtiene por separado).
- No necesita partida nueva respecto a la 5.3, 5.2, 5.1, 5.0 ni 4.4: guarda dentro del juego y carga el `.sav` con la nueva ROM. No uses estados rápidos de otra compilación. Otra semilla del randomizador requiere partida nueva.

## Novedades de 5.4

Revisión de dos beta testers automáticos (uno como GOLD, otro como CRISTAL):

1. **Ya no se reinicia la consola** al elegir otro ataque con Banda, Gafas o Pañuelo Elegidos (probable causa de «Inversión cierra el juego»).
2. **Los PNJ ya no cambian de sprite** al cruzar un mapa a pie (PLATA y el guía en Ciudad Cerezo, la profesora de la Ruta 29, PNJ de Ciudad Trigal).
3. **El PNJ de la Ruta 29 que avisa de Ulex ya no se distorsiona** al andar.
4. Los movimientos **MO que salen al azar se pueden olvidar**.
5. Las comillas del campeón de la Superliga se ven bien.

Detalle y causas: `CHANGELOG.md` y `docs/ERRORES-Y-SOLUCIONES.md`.

## Validación

222 comprobaciones agrupadas, no un porcentaje de cobertura. No se ha completado una campaña entera; el combate del campeón de la Superliga se prueba perdiendo y con atajos. El cruce de mapas apaga la pantalla unos fotogramas: probado en emulador, no en consola real.
