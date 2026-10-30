# Sandbox de pruebas y diferencias con la ROM normal

El sandbox es una **compilación separada** (`pokecristal_debug` en el Makefile) para probar mecánicas sin jugar toda la aventura. No se distribuye como descarga del juego: se compila desde la fuente. Tiene su propio nombre y guardado, de modo que no mezcla la partida de la ROM normal.

| | ROM normal | Sandbox |
|---|---|---|
| Archivo de compilación | `pokecristal.gbc` (publicada como `Radical Cristal.gbc`) | `pokecristal_debug.gbc` |
| Descarga pública | Sí (único asset de la Release) | No |
| Menú Start → SANDBOX | No | Sí |
| Guardado | El de la aventura | Distinto, para no mezclarlo |
| SHA-256 de 4.3 | `a6a232589e9ff8859bc9307c3593707c753dcaf8b6be65a8ba835faafe949b1e` | `d6a7449506680bdbb215e3aabeb4f6772585516e55eefe07c396f9543cc401f2` |
| SHA-256 de 4.4 | `b4cff3b076988a780d6570653d677b7fecab1cbb4fdfcc6dde8cda5a22c1e3ef` | `f77fb27ec0e2365985be7cc7d6045fde364a9e3e6ad484e2a1df5aab74b3706e` |
| SHA-256 de 5.0 | `5b9fb58edd1742f2de4b6a1bbc9999e05f48c31d3ac28a44200650e2f3133ecd` | `ec9dbc978709369f95218bb1afca61927ca27b225b95f2f4fd832cee416a0130` |
| SHA-256 de 5.1 | `339f38f5d51b9bd1a4adcd28e1767fbbf32ef4e0e343f4965acbdc9cb4fa00e5` | `b060483611e9bb5c1fbc88607e2f5a218ac500bbb268962279725a1cb4702183` |
| SHA-256 de 5.2 | `6861c67987485a36df0e3c4a83906bd68f778a7b649466984dffdeb31ffc590b` | `2d39b0abac24322576aa1deaa00e5ed09279958f37db97e5e01d69e2af9bf747` |
| SHA-256 de 5.3 | `aab4601450c38aa762b643033df21af26dd698cb30d44dce50f92780783e6408` | `880a161a97ae2321565a751ca58c4284d796263f490c4aba67a1fe5b90f020d6` |
| SHA-256 de 5.4 | `91845e52c2afee9f0f6e0425f15fc62e7685aff5c116284cceee768ac00e67c1` | `4afbf8921e51f9086bbb5412f9d43f7ede1b1271c1aff42d9ff5ec106d9d2020` |
| SHA-256 de 5.5 | `b5530aa12dd945ae99ffb2045d4927c32e9077d9d0dbb899d21cfa3deb5738e8` | `ec31d24151faf0a4dc80640d35aa93f426c8ce5277aac907a3b922dca2ddc050` |

El hash del sandbox figura en `evidencias/Validacion-v4.3.json` (4.3), `evidencias/Validacion-v4.4.json` (4.4) y `evidencias/Validacion-v5.0.json` (5.0). El catálogo de destinos incluye desde la 5.0 los seis mapas de la Superliga (394 destinos) y corresponde a la compilación probada; no se adjunta ninguna ROM sandbox.

## Menú SANDBOX

Start → SANDBOX abre las herramientas en cualquier mapa donde se pueda usar el menú.

- **VIAJAR**: 41 accesos rápidos (centros, eventos, Rojo y los 16 disfraces de Ulex) y la opción TODOS LOS MAPAS, un catálogo de 388 mapas en 26 grupos con coordenadas transitables verificadas. El recorrido visual completo se muestreó en destinos representativos; no se ha jugado visualmente cada mapa entero.
- **SUBIR MEDALLAS**: selector de 0 a 16 medallas de una vez, con recálculo del límite de nivel.
- **LIGA/ROJO**: con 8 medallas alterna la victoria de Liga; con 16, la de Rojo.
- **EQUIPO DE PRUEBA**: sustituye el equipo sandbox por Bayleef, Houndoom y Togetic shiny al nivel del límite menos uno, con estadísticas y PP correctos, Viento Hielo, Poder Oculto, Fuerza Lunar y Surf, equipados con Banda Focus.
- **REINICIAR RETOS**: limpia capturas de zona, intercambio de Tito, victorias de Tito/Rojo, santuario y Ulex. Hay que salir de la zona y volver para recargar sus actores.
- **OBJETOS**: entrega diez unidades de Repelente, Superrepelente, Máximo Repelente, Banda Focus, Poción y Restaurar Todo, más siete MT aleatorias y, desde la 5.3, las siete MO (Corte, Vuelo, Surf, Fuerza, Destello, Torbellino y Cascada), si hay capacidad. Se puede repetir. No es un editor arbitrario de objetos.
- **OPCIONES**: ajustes normales del juego.

Los viajes y las medallas son herramientas de prueba: no completan automáticamente las misiones de historia. Los eventos siguen siendo los reales.

## Recetas de prueba

- **Tito**: avanzar a 16 medallas, activar la victoria de Rojo y visitar un centro.
- **Santuario del Encinar**: viajar al santuario, preparar el equipo y usar Master Ball.
- **Ulex**: viajar a su ruta, hablar con él y avanzar una medalla antes del siguiente.
- **Tope de nivel**: el equipo de prueba está un nivel por debajo; un caramelo alcanza el límite y otro comprueba el bloqueo.

## Fallo corregido en 4.2

OBJETOS se bloqueaba al llamar directamente a `ReceiveRandomTM` desde otro banco de ROM. Ver [CHANGELOG](../CHANGELOG.md) y [ARQUITECTURA](ARQUITECTURA.md). Una prueba entra desde el menú real, usa OBJETOS dos veces, comprueba cantidades y MT, y vuelve al mapa.
