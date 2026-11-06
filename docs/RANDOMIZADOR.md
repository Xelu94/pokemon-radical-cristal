# Randomizador sin conexión

`herramientas/Randomizador.html` es una única página HTML/CSS/JavaScript sin framework ni dependencias externas. Se abre en el navegador, lee la ROM normal elegida por el usuario, genera otra distribución y descarga el resultado. La ROM se procesa en el propio equipo; las pruebas de navegador comprueban que no se realizan solicitudes de red.

## Uso

1. Abre `herramientas/Randomizador.html` en un navegador moderno.
2. Selecciona `Radical Cristal.gbc` (v5.7) o una copia generada antes con esta misma herramienta.
3. Escribe una semilla o pulsa «Otra semilla».
4. Pulsa «Generar y descargar ROM». El archivo se llama `Radical-Cristal-<semilla>.gbc`. *(Desde la 4.4:* debajo aparece una vista previa de la semilla con los iniciales, los equipos de los 22 líderes, Alto Mando y rivales principales y las 50 MT, solo con nombres.)
5. **Empieza una partida nueva**: cambiar de semilla requiere partida nueva y cada guardado pertenece a su aventura.

La misma ROM y la misma semilla producen los mismos bytes.

## Qué cambia y qué no

Cambia (posiciones mutables declaradas en el manifiesto):

- Referencias de especie de iniciales, salvajes, entrenadores, regalos, huevos y eventos (la interfaz informa del recuento: 3774 referencias en la ROM publicada, según la captura de la herramienta).
- Las 50 MT, con contenidos únicos que excluyen Struggle.
- Las tablas de intercambio por especie (ocho candidatas por especie, con fase y potencia comparables).
- Los huevos de la guardería (20 posiciones), con estadísticas recalculadas a partir de los DVs y la experiencia de nivel 5.
- El checksum global de la cabecera (`0x14E–0x14F`), recalculado.

No cambia: código, niveles, MO, restricciones y el equipo fijo de Tito. Los movimientos de los Pokémon siguen aleatorizándose durante la partida con las rutinas del motor.

## Diseño

- **Manifiesto**: el exportador (`herramientas/fuentes/export_portable_randomizer.py`) lee las tablas de la fuente y los símbolos de la compilación y escribe una lista de direcciones mutables y los conjuntos de candidatos por nivel. El manifiesto contiene operandos, no código ejecutable.
- **Núcleo** (`portable_randomizer.js`): generador pseudoaleatorio con semilla (FNV-1a para la semilla y xorshift32), barajado y escritura de bytes. Es una función pura que se prueba en Node.
- **Firma de la parte inmutable**: se ponen a cero todos los rangos mutables y se calcula el SHA-256 del resto. Si no coincide con el del manifiesto, la herramienta rechaza la ROM antes de modificar nada. Así solo acepta esta compilación o copias generadas por ella.
- **Elegibilidad**: los candidatos se calculan con los métodos de evolución actuales (nivel o piedra), no con las tablas históricas.

## Pruebas

- Núcleo (Node): firma, rangos en bounds, determinismo, bytes inmutables intactos, 50 MT únicas, DVs shiny conservados y rechazo de entradas inválidas: 9 comprobaciones.
- Navegador (Playwright): selección, generación y descarga, coincidencia con el núcleo, rechazo de ROM incompatible y ausencia de solicitudes de red: 4 comprobaciones.

Ver [COMPILACION-Y-PRUEBAS.md](COMPILACION-Y-PRUEBAS.md).

## Limitaciones

- No funciona con la ROM original de Pokémon Cristal ni con otras compilaciones.
- El texto de error de la herramienta menciona «la ROM incluida junto a esta herramienta»; en este repositorio la ROM se descarga desde Releases.
- El generador histórico `tools/balanced_randomizer.py` de la fuente no debe ejecutarse sobre la fuente actual (restauraría tablas anteriores). Para otra distribución se usa esta herramienta.
