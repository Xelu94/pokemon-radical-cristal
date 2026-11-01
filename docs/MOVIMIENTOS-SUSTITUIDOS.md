# Movimientos añadidos y sustituidos

La tabla de movimientos mantiene **254 identificadores** (`NUM_ATTACKS`, `constants/move_constants.asm`). Cada identificador cabe en un byte y está referenciado por guardados, MT, tablas de aprendizaje y animaciones. Para no ampliar la tabla ni romper guardados, el proyecto hace dos cosas:

1. Añade tres movimientos en los últimos identificadores (252–254).
2. Sustituye treinta y cuatro movimientos antiguos poco útiles por movimientos modernos **en el mismo ID**, reutilizando las animaciones del motor.

Los datos salen de `data/moves/moves.asm` y `data/moves/names.asm` de la fuente integrada (formato: efecto, potencia, tipo, categoría, precisión, PP, probabilidad del efecto secundario).

## Movimientos añadidos (IDs 252–254)

| ID | Movimiento | Tipo | Categoría | Potencia | Precisión | PP | Efecto |
|---|---|---|---|---|---|---|---|
| 252 | Fuerza Lunar | Hada | Especial | 95 | 100 | 15 | 30 % de bajar Ataque Especial |
| 253 | Brillo Mágico | Hada | Especial | 80 | 100 | 10 | — |
| 254 | Carantoña | Hada | Física | 90 | 90 | 10 | 10 % de bajar Ataque |

Además, los movimientos de tipo Hada que ya existían en la base (Encanto, Luz Lunar) pasan al tipo Hada.

## Sustituciones por ID

| ID | Movimiento original | Movimiento nuevo | Tipo | Categoría | Potencia | Precisión | PP | Efecto |
|---|---|---|---|---|---|---|---|---|
| 4 | Puño Cometa | Tijera X | Bicho | Física | 80 | 100 | 15 | — |
| 13 | Viento Cortante | Garra Dragón | Dragón | Física | 80 | 100 | 15 | — |
| 117 | Venganza | Pulso Umbrío | Siniestro | Especial | 80 | 100 | 15 | 20 % de retroceso |
| 119 | Movimiento Espejo | Tajo Umbrío | Siniestro | Física | 70 | 100 | 15 | — |
| 121 | Bomba Huevo | Cabeza de Hierro | Acero | Física | 80 | 100 | 15 | 30 % de retroceso |
| 132 | Restricción | Zumbido | Bicho | Especial | 90 | 100 | 10 | 10 % de bajar Defensa Especial |
| 140 | Presa | Pulso Dragón | Dragón | Especial | 85 | 100 | 10 | — |
| 159 | Afilar | Foco Resplandor | Acero | Especial | 80 | 100 | 10 | 10 % de bajar Defensa Especial |
| 186 | Beso Dulce | Viento Hada | Hada | Especial | 40 | 100 | 30 | — |
| 11 | Agarre | Puya Nociva | Veneno | Física | 80 | 100 | 20 | 30 % de envenenar |
| 20 | Atadura | Veneno X | Veneno | Física | 70 | 100 | 20 | 10 % de envenenar |
| 160 | Conversión | Lanzamugre | Veneno | Física | 120 | 80 | 5 | 30 % de envenenar |
| 176 | Conversión2 | Onda Tóxica | Veneno | Especial | 95 | 100 | 10 | 10 % de envenenar |
| 142 | Beso Amoroso | Acua Jet | Agua | Física | 40 | 100 | 20 | Ataca primero (+1) |
| 169 | Telaraña | Bomba Germen | Planta | Física | 80 | 100 | 15 | — |
| 54 | Neblina | Tierra Viva | Tierra | Especial | 90 | 100 | 10 | 10 % de bajar Defensa Especial |
| 96 | Meditación | Vozarrón | Normal | Especial | 90 | 100 | 10 | — |
| 218 | Frustración | Sombra Vil | Fantasma | Física | 40 | 100 | 30 | Ataca primero (+1) |
| 108 | Pantallahumo | Joya De Luz | Roca | Especial | 80 | 100 | 20 | — |
| 110 | Refugio | Acua Cola | Agua | Física | 90 | 90 | 10 | — |
| 111 | Rizo Defensa | Puño Bala | Acero | Física | 40 | 100 | 30 | Ataca primero (+1) |
| 134 | Kinético | Energibola | Planta | Especial | 90 | 100 | 10 | 10 % de bajar Defensa Especial |
| 149 | Psico-onda | Escaldar | Agua | Especial | 80 | 100 | 15 | 30 % de quemar |
| 170 | Telépata | Cabezazo Zen | Psíquico | Física | 80 | 90 | 15 | 20 % de retroceso |
| 171 | Pesadilla | Rayo Señal | Bicho | Especial | 75 | 100 | 15 | 10 % de confundir |
| 180 | Rencor | Roca Afilada | Roca | Física | 100 | 80 | 5 | — |
| 193 | Profecía | Garra Umbría | Fantasma | Física | 70 | 100 | 15 | — |
| 199 | Fijar Blanco | Esfera Aural | Lucha | Especial | 80 | 100 | 20 | No falla |
| 217 | Presente | Puño Drenaje | Lucha | Física | 75 | 100 | 10 | Absorbe PS |
| 244 | Más Psique | Chispazo | Eléctrico | Especial | 80 | 100 | 15 | 30 % de paralizar |
| 99 | Furia | Onda Ígnea | Fuego | Especial | 95 | 90 | 10 | 10 % de quemar |
| 49 | Bomba Sónica | Pájaro Osado | Volador | Física | 120 | 100 | 15 | Retroceso |
| 50 | Anulación | Aire Afilado | Volador | Especial | 75 | 95 | 15 | 30 % de retroceso |
| 28 | Ataque Arena | Colm. Hielo | Hielo | Física | 65 | 95 | 15 | 10 % de congelar |

En el código fuente los nombres antiguos siguen siendo las constantes de los IDs y los nuevos son alias (`DEF X_SCISSOR EQU COMET_PUNCH`, etc.).

## Efecto sobre guardados existentes

- Un Pokémon que **ya conocía** el movimiento antiguo pasa a conocer el nuevo en la misma ranura, porque lo único que guarda la partida es el ID. El movimiento cambia de comportamiento (tipo, categoría, potencia). No se ha documentado ni probado el ajuste de los PP guardados de esos movimientos.
- Las **MT y los hitos de aprendizaje** aleatorizados se resuelven con IDs, así que ofrecen el movimiento nuevo.
- El **recordador de Tito** consulta las tablas originales de movimientos y respeta esos mismos IDs: enseña los movimientos sustituidos en su versión nueva.
- Las **animaciones** se reutilizan del motor existente; no se añadieron gráficos nuevos para estos movimientos.
- Poder Oculto (ID 237) calcula tipo y potencia con los DVs y se muestra con esos valores en pantalla.

## Cómo comprobarlo

```text
constants/move_constants.asm   # alias DEF ... EQU ... y NUM_ATTACKS
data/moves/moves.asm           # datos de los 254 movimientos
data/moves/names.asm           # nombres
```

Estos archivos están en la fuente integrada que se obtiene al aplicar [`parches/Cambios-fuente.patch`](../parches/Cambios-fuente.patch) sobre la base ([compilación](COMPILACION-Y-PRUEBAS.md)).
