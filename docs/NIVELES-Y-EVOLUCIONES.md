# Límites de nivel y evoluciones modificadas

## Límites de nivel

La rutina `GetCurrentLevelCap` (`engine/pokemon/v2_balance.asm`) devuelve el límite vigente y la comparten la experiencia de combate, los caramelos raros, la guardería y Tito. El límite lo determina el **primer líder pendiente** en el orden de progresión, aunque los gimnasios se visiten en otro orden.

### Johto

| Líder | Medalla (constante) | Límite |
|---|---|---|
| Pegaso | ZEPHYRBADGE | 19 |
| Antón | HIVEBADGE | 24 |
| Blanca | PLAINBADGE | 29 |
| Morti | FOGBADGE | 35 |
| Aníbal | STORMBADGE | 40 |
| Yasmina | MINERALBADGE | 44 |
| Fredo | GLACIERBADGE | 48 |
| Débora | RISINGBADGE | 53 |

Con las ocho medallas de Johto el límite es **65** hasta superar la Liga.

### Kanto

| Líder | Medalla (constante) | Límite |
|---|---|---|
| Lt. Surge | THUNDERBADGE | 67 |
| Sabrina | MARSHBADGE | 70 |
| Erika | RAINBOWBADGE | 73 |
| Sachiko | SOULBADGE | 75 |
| Misty | CASCADEBADGE | 77 |
| Brock | BOULDERBADGE | 80 |
| Blaine | VOLCANOBADGE | 83 |
| Azul | EARTHBADGE | 85 |

### Final

| Situación | Límite |
|---|---|
| Dieciséis medallas | 95 |
| Tras derrotar a Rojo (`EVENT_BEAT_RED_PERMANENT`) | 100 |

Rojo exige las dieciséis medallas y tiene seis Pokémon al nivel 95. El equipo de Tito está al 100.

Los Pokémon que ya superen un nuevo tope no pierden niveles, pero no ganan experiencia por encima de él.

### Excepción: el primer Ulex

El Ulex de la Ruta 31 que se encuentra con cero medallas saca sus tres Pokémon al **nivel 15**. Los demás encuentros con Ulex usan el límite vigente. Ver [MECANICAS.md](MECANICAS.md).

### Escalado de rivales

Salvajes y entrenadores no bajan del **nivel del último líder derrotado** (hasta la 5.4 era ese nivel menos tres). Se exceptúan las rutas iniciales 29, 30 y 31 y los encuentros de nivel especial. El suelo se aplica a la hierba, a la pesca, a los árboles y a todos los equipos de entrenador.

### Evolución según el nivel (5.5)

Cuando se genera un Pokémon salvaje o de entrenador, evoluciona hasta donde su nivel le deja:

- Una evolución por **nivel** se aplica al alcanzar su umbral (Croconaw 30, Kadabra 36, Slowpoke 37 o 40…). Si hay varias, vale la primera cuyo umbral se alcance.
- Una especie con **una o dos evoluciones por piedra** pasa a la primera desde el **nivel 32** (Pikachu → Raichu, Gloom → Vileplume).
- Eevee y las familias con muchas piedras no cambian, igual que las evoluciones por intercambio o amistad que no se convirtieron a nivel.

### Curva de ataques (5.8)

Desde la **cuarta medalla** (Johto y Kanto sumadas), los ataques de los Pokémon salvajes y de entrenador se construyen al empezar el combate, con una potencia mínima que sube con las medallas:

| Medallas | Potencia mínima del 1.er ataque | 4.º ataque |
|---|---|---|
| 4 | 60 | cobertura |
| 5-6 | 65-70 | cobertura |
| 7-9 | 75-85 | apoyo |
| 10 o más | 90 | apoyo |

1. **1.er ataque:** de su primer tipo. 2. **2.º ataque:** de su segundo tipo (o de nuevo del primero), diez de potencia menos. 3. **3.er ataque:** de cobertura (un tipo que no es el suyo). 4. **4.º ataque:** de cobertura hasta la sexta medalla; desde la séptima, un movimiento de apoyo que le valga (Danza Espada o Reflejo para los físicos, Pantalla Luz o Amnesia para los especiales, y Agilidad, Recuperación, Sustituto, Tóxico, Onda Trueno, Protección, Espora, Batido o Amortiguador para cualquiera).

Los ataques son de la categoría (físico o especial) en la que el Pokémon es mejor, tienen al menos 85 % de precisión y se descartan los de recarga, los de dos turnos y los que bloquean al usuario. Si el tipo no tiene ataques tan fuertes, se baja la potencia de diez en diez hasta 40. Con menos de cuatro medallas los ataques siguen siendo aleatorios. Esto sustituye a la regla de la 5.5 «un ataque de su tipo desde la sexta medalla».

### Superliga (5.8)

Azul, Lance y Rojo llevan tres Pokémon totalmente evolucionados con 500 o más de estadísticas base y tres legendarios distintos; Ulex, tres Pokémon fuertes, dos legendarios y Dark Lugia el último. Los legendarios posibles son Articuno, Zapdos, Moltres, Mewtwo, Mew, Raikou, Entei, Suicune, Lugia, Ho-Oh y Celebi. Tito conserva su equipo fijo.
## Evoluciones modificadas

Las evoluciones por intercambio o amistad se sustituyen por nivel o piedra para que todas sean accesibles en un Nuzlocke sin red. Datos de `data/pokemon/evos_attacks.asm`.

| Pokémon | Evoluciona | Condición |
|---|---|---|
| Kadabra | Alakazam | Nivel 36 |
| Machoke | Machamp | Nivel 36 |
| Graveler | Golem | Nivel 36 |
| Haunter | Gengar | Nivel 36 |
| Poliwhirl | Poliwrath | Piedra Agua |
| Poliwhirl | Politoed | Nivel 40 |
| Slowpoke | Slowbro | Nivel 37 |
| Slowpoke | Slowking | Nivel 40 |
| Onix | Steelix | Nivel 40 |
| Seadra | Kingdra | Nivel 40 |
| Scyther | Scizor | Nivel 40 |
| Porygon | Porygon2 | Nivel 40 |
| Pichu | Pikachu | Nivel 15 |
| Cleffa | Clefairy | Nivel 15 |
| Igglybuff | Jigglypuff | Nivel 15 |
| Togepi | Togetic | Nivel 20 |
| Golbat | Crobat | Nivel 36 |
| Chansey | Blissey | Nivel 32 |
| Eevee | Espeon | Piedra Solar |
| Eevee | Umbreon | Piedra Lunar |

Para obtener Slowking, cancela la evolución a Slowbro en los niveles 37, 38 y 39. Las ramas de Eevee hacia Vaporeon, Jolteon y Flareon conservan sus piedras. El resto de especies mantiene su método de evolución original; Tito ofrece una guía en el juego.
