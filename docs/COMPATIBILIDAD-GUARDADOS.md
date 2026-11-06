# Compatibilidad de guardados

## Actualizar dentro de esta familia

Las actualizaciones de las versiones de este proyecto (v3 → v4 → v4.1 → v4.2 → v4.3 → v4.4 → v5.0 → v5.1 → v5.2 → v5.3 → v5.4 → v5.5 → v5.6 → v5.7) permiten **continuar el guardado interno del juego** (el `.sav` o la memoria de batería del emulador): no hace falta partida nueva.

Procedimiento:

1. En la versión anterior, guarda dentro del juego (menú GUARDAR) y cierra el emulador.
2. Abre la ROM nueva con el mismo guardado.
3. **No uses estados rápidos** (savestates) de otra compilación: guardan también gráficos y estado de ejecución de la compilación anterior y no deben emplearse para actualizar.

## Qué se migra

- **Mochila y PC**: la mochila pasa de 20 a 50 montones y el PC de 50 a 20, conservando los 70 espacios combinados. La migración es automática; se comprobó con guardados v3, tanto el principal como el de respaldo.
- **Movimientos sustituidos**: los Pokémon que conocían uno de los treinta y cuatro movimientos antiguos (desde la 5.5: Agarre, Atadura, Conversión y Conversión2; desde la 5.6: otros 21, p. ej. Fijar Blanco o Kinético) pasan a conocer el nuevo en el mismo ID ([tabla](MOVIMIENTOS-SUSTITUIDOS.md)).
- **Niveles por encima de un nuevo tope**: no se pierden, pero el Pokémon no gana experiencia hasta que el tope lo supere.
- **Recursos de partida nueva** (99 Master Balls, 99 caramelos raros infinitos, objetos equipados): solo se entregan en partidas nuevas. Los guardados existentes conservan las cantidades y montones que tuvieran y lo gastado no se regenera. Desde la 4.3 usar un caramelo raro no lo consume, así que los montones de un guardado anterior también pasan a ser infinitos.
- **Tiendas y curas**: los objetos curativos que ya tenías se conservan. Las tiendas dejan de venderlos.
- **El anciano de CIUDAD CEREZO**: si ya tienes la TARJ. MAPA no ocurre nada; si aún no la tenías, se acerca al volver a entrar en la ciudad.
- **Flags de evento nuevos**: tres flags en un rango de la tabla de eventos que estaba libre; no alteran los existentes.

## Qué no puede recuperarse

- Los **DVs shiny que un guardado anterior ya perdió** no pueden reconstruirse. Desde la corrección correspondiente se conservan al capturar, enviar directamente al PC, depositar o retirar.

## Semillas del randomizador

**Cambiar de semilla requiere una partida nueva.** Las ROM generadas llevan la semilla en el nombre y cada guardado pertenece a una aventura concreta. Ver [RANDOMIZADOR.md](RANDOMIZADOR.md).

## Sandbox

El sandbox usa otro guardado. No sustituyas el guardado de tu aventura por el del sandbox.

## Alcance de lo comprobado

La compatibilidad se verificó con guardados de las versiones de este proyecto y con pruebas de migración. No se afirma compatibilidad con otras ROM, otros hacks ni estados rápidos de emuladores.
