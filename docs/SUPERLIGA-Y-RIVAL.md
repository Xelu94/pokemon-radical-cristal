# Superliga, el otro protagonista y el duelo de Elm (v5.0)

Todo lo de esta página es de la v5.0 «Radical Cristal». Los textos son los del juego (sin corregir lo que el autor pidió literal).

## Duelo con el profesor Elm

- **Cuándo.** Cuando Elm te da la Master Ball (al tener la última medalla de Johto y hablar con él en su laboratorio). Al terminar te pregunta si quieres un combate «para volver a sentir lo que es ser un entrenador». Si dices que no, te lo vuelve a ofrecer cada vez que hables con él hasta que lo hagas.
- **Equipo.** Togetic, Xatu, Slowking (nivel 50) y Ampharos (53): los niveles de DÉBORA, la líder de Johto de más nivel; como cualquier entrenador sube al mínimo del tope vigente si hace falta.
- **Sin muertes.** Es un duelo de exhibición: tus Pokémon pueden debilitarse pero no mueren (bandera `EVENT_EXHIBITION_BATTLE`, también usada en la Superliga).
- **Imagen.** Elm usa su propia clase de entrenador e imagen desde la 5.3 (antes salía la de Oak).
- **Premio.** Si ganas, Elm te entrega un FERALIGATR, un MEGANIUM y un TYPHLOSION **shiny** a nivel 53 (uno detrás de otro; el juego te deja ponerles mote). Se entregan una sola vez.

## El otro protagonista: GOLD y CRISTAL

Si eres chico, la otra es **CRISTAL**; si eres chica, el otro es **GOLD**. Lleva la clase de entrenador «RIVAL» y la imagen del protagonista que no elegiste.

| Cuándo | Qué ocurre | Equipo |
|---|---|---|
| Pueblo Primavera, la primera vez que con un Pokémon caminas hacia el oeste para entrar en la Ruta 29 (también tras el empujón del rival junto al laboratorio, si hablas antes con él) | Aparece corriendo por detrás de ti y te llama | RATTATA 5 |
| Torre Bellsprout (3.ª planta), cuando Plata se marcha con la Cuerda Huida | Aparece tras la marcha de Plata | RATTATA 12, PIDGEY 12 |
| Guarida Dragón (piso B1), tras hablar con Plata | Plata se va y aparece | RATICATE, ALAKAZAM, SNORLAX, TAUROS, ARCANINE (48) |
| Centro Pokémon de la Meseta Añil, la primera vez que entras (hace falta un hueco en el equipo) | El último combate; te da un huevo y se va por la puerta | RATICATE, ALAKAZAM, SNORLAX, TAUROS, ARCANINE (60), DRAGONITE (62) |

Los niveles se elevan al mínimo del tope vigente, como los de cualquier entrenador. Las tres primeras emboscadas se activan una sola vez. En cada una, al terminar el combate (aunque lo pierdas) ella cura a todo tu equipo, te da una MÁX. POCIÓN y se marcha.

Diálogos de la primera emboscada (los de las otras dos son variantes):

> ¿Que te pensabas, wachín? ¿Que te ibas a librar de pelear?
> ¡Prepara bien ese culito!

Final en la Meseta Añil:

> Prepárate para nuestro último y más épico combate.
> *(si ganas)* Bien hecho, me has dado para el pelo.
> Bueno, parece que no tengo lo que hace falta para enfrentarme a la LIGA. Lo dejo aquí. Voy a dedicarme a coleccionar RATTATA que se llamen ZURULLO.
> Toma, un huevo de recuerdo. ¡Cuídalo mucho!

Si pierdes el último combate, ella se va y la escena se repite la próxima vez que entres al centro.

### Su casa y el canje

Tras el combate final la encuentras siempre en la casa de los vecinos de Pueblo Primavera, con un RATTATA («ZURULLO») al lado. Si le llevas un RATTATA de los que da ULEX (el ZURULLO con SALPICADURA) te lo cambia por un Pokémon aleatorio **de tercera etapa evolutiva**, al nivel del tope vigente menos cinco.

## Superliga

### Cómo se abre

Se desbloquea al vencer a TITO XELUIS (el combate normal). Se entra de dos formas:

1. **Hablando con Tito** en cualquier Centro Pokémon: MÁS / SALIR → **SUPERLIGA**.
2. **Hablando con el entrenador de la Meseta Añil** (el que está en el centro, de pie; se puede llegar con Vuelo).

Si la pierdes, queda cerrada hasta que vuelvas a ganar a Tito.

### Reglas

- Todos los rivales están a **nivel 100**, sin medallas ni topes.
- **Sin muertes.** En la Superliga tus Pokémon pueden debilitarse pero no mueren y no cuentan para la regla Nuzlocke.
- Antes de entrar, el oficial del vestíbulo te da **99 RESTAU. TODO**.
- **Si caes**, conservas todos tus Pokémon y se curan, pero pierdes todos los RESTAU. TODO (también los que tuvieras) y vuelves al Centro Pokémon de la Meseta. Para participar de nuevo hay que ganar otra vez a Tito.
- **Si ganas**, Tito te da su CHARIZARD shiny nivel 100 con una carta (una sola vez; un segundo intento no repite el regalo).

### Retadores

El Alto Mando son Azul, Lance, Rojo y Ulex, de menor a mayor, y el campeón es Tito. Usan las salas de la Liga (mapas nuevos con los mismos gráficos).

| Sala | Rival | Equipo |
|---|---|---|
| 1 | AZUL | 6 Pokémon aleatorios |
| 2 | LANCE | 6 Pokémon aleatorios |
| 3 | ROJO | 6 Pokémon aleatorios |
| 4 | ULEX (aquí no roba) | 6 Pokémon aleatorios |
| 5 | TITO XELUIS (campeón) | MEW, CELEBI, LUGIA, HO-OH, DRAGONITE, MEWTWO |

«Aleatorios» = cada vez que empiezas el combate se eligen seis especies al azar, **totalmente evolucionadas**, con un total de estadísticas base de **al menos 450**, sin repetir en el equipo y sin Dark Lugia. Todos a nivel 100. El equipo del campeón es fijo.

### Diálogos

**Oficial del vestíbulo**
> Bienvenido a la SUPERLIGA #MON. Aquí no hay límites: todos los rivales están al nivel 100.
> Si caes, no perderás tus #MON… pero sí los RESTAU. TODO que te dé hoy.
> Y para volver a participar deberás ganar otra vez a TITO XELUIS.
> Toma 99 RESTAU. TODO. ¡Suerte!

**Azul**
> ¡Vaya, vaya! ¿Tú otra vez? Aquí no hay medallas ni topes. Sólo nivel 100.
> Te voy a demostrar quién es el mejor entrenador de KANTO. ¡Adelante!
> *(derrota)* ¿Qué…? ¡No puede ser! Ni a nivel 100 puedo contigo…
> *(victoria)* ¡Ja! Sigues sin ser rival para mí.
> *(después)* Tienes talento. Pero ojo: LANCE no se anda con contemplaciones.

**Lance**
> Soy LANCE, el domador de dragones. Aquí no tengo que contenerme: mis #MON están al máximo. ¡Muéstrame qué has aprendido!
> *(derrota)* Un poder digno de un campeón… Me inclino ante ti.
> *(después)* Sigue adelante. ROJO espera en silencio, y su silencio pesa más que mis dragones.

**Rojo**
> …… …………  *(ROJO te mira fijamente y lanza una # BALL.)*
> *(derrota)* …… …………
> *(después)* …… …… *(asiente con la cabeza y señala la puerta.)*

**Ulex**
> Jejeje. ¿Creías que sólo robaba #MON por las rutas? Aquí no me hace falta robar nada. Hoy sólo hay combate, y es del bueno.
> *(derrota)* ¡Vaya! Esta vez no me llevo nada. ¡Qué lástima!
> *(después)* Pasa, pasa. El campeón te espera. Dicen que su equipo es de leyenda…

**Tito Xeluis**
> Eyyyy siiiii, has llegado hasta aquí, wachin. Soy el campeón de la SUPERLIGA y estos son mis #MON de leyenda. ¡Vamoh a darle!
> *(derrota)* Ostias… me has dado para el pelo otra vez. El campeón eres tú.
> *(después)* Mi favorito es este CHARIZARD SHINY, y hoy es tuyo.
> *(la carta que lleva)* «Eres el puto amo, has conseguido completar el juego y sobre todo este desafío, que es el más jodido de todos. ¡Eres la cabra!»

La carta que aparece en el objeto equipado dice solo «¡ERES EL AMO! / ¡ERES LA CABRA!» porque el correo del juego admite 32 caracteres; el mensaje completo se muestra en el diálogo.

## Dark Lugia

- Especie nueva nº 252 (id `$fc`), tipo **Siniestro/Volador**, estadísticas invertidas respecto a Lugia: PS 106, Ataque 130, Defensa 90, Velocidad 110, Ataque Especial 154, Defensa Especial 90.
- **No es capturable**: no está en ninguna tabla de encuentros, y el randomizador y el generador de huevos la excluyen. Se obtiene una sola vez al **ganar por primera vez a TITO XELUIS**, a nivel 100.
- El sprite frontal es el arte de aficionado de Dark Lugia que aportó el autor del proyecto (obra de [SageDeoxys](https://www.deviantart.com/sagedeoxys) en DeviantArt; ver [CREDITOS.md](../CREDITOS.md)). Se convirtió desde un vídeo animado (280×280, 56×56 píxeles ampliados ×5) a 4 colores y tres fotogramas de animación (`herramientas/fuentes/build_dark_lugia_sprite.py`; el resultado va dentro del parche, en `gfx/pokemon/dark_lugia/`). Desde la 5.1 la imagen trasera es otro arte de SageDeoxys aportado por el autor (56×56 reducido a 48×48, con la marca roja de la barriga eliminada). Su grito es el de Lugia con otro tono. El aprendizaje por nivel es el de Lugia con CRUNCH y SHADOW_BALL (la generación aleatoria de movimientos del juego sigue aplicándose a los Pokémon que se generan).

## Notas técnicas

- Mapas nuevos en el grupo de la Meseta Añil: `SUPER_LEAGUE_LOBBY`, `SUPER_LEAGUE_AZUL`, `SUPER_LEAGUE_LANCE`, `SUPER_LEAGUE_ROJO`, `SUPER_LEAGUE_ULEX` y `SUPER_LEAGUE_TITO` (copias de las salas de Mento y del campeón; sin escenas para no gastar WRAM). Aparecen también en el sandbox.
- Banderas de evento nuevas (todas en el rango que estaba libre): copia shiny forzada, duelo de Elm, tres emboscadas, combate final, ocultación de los objetos GOLD/CRISTAL/RATTATA, escena activa, Superliga perdida/ganada, restauraciones entregadas, cuatro salas superadas, Dark Lugia, exhibición.
- La elección aleatoria se hace en `SuperLeagueRandomizeSpecies` (`engine/events/super_league.asm`), llamada desde `TrainerType1` solo para las cuatro entradas nuevas (`LANCE_SUPER`, `RED_SUPER`, `BLUE_SUPER`, `ULEX_SUPER`).
- La regla «si caes pierdes los RESTAU. TODO» es el script estándar `SuperLeagueLostScript`. `NuzlockeMarkPartyMonDead` no marca muertes mientras está activa `EVENT_EXHIBITION_BATTLE`.
