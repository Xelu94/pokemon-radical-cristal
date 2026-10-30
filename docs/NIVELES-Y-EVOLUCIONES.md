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

### Ataque de su tipo (5.5)

Con **seis o más medallas** (Johto y Kanto sumadas), todo Pokémon salvaje o de entrenador conoce al menos un ataque de daño de uno de sus tipos. Si no lo tiene al generarse, el cuarto movimiento se sustituye por uno aleatorio que lo cumpla.

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
