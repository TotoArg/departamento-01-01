# Especificaciones Técnicas, Cotas Arquitectónicas y Registro de Muebles

**Proyecto:** Departamento 01-01  
**Versión de Esquema BIM:** `2026.11.15.v6`  
**Motor Gráfico:** Three.js r128 WebGL / PWA Service Worker `gemelo-3d-pwa-v3.0`  

---

## 1. Cotas Generales de la Propiedad

* **Superficie Cubierta:** $47,16\text{ m}^2$
* **Superficie Balcón Terraza:** $7,00\text{ m}^2$
* **Superficie Total Escritura:** $54,16\text{ m}^2$
* **Altura Cielorraso General:** $2,60\text{ m}$
* **Altura Bajo Viga:** $2,30\text{ m}$
* **Espesor Muro Perimetral Oeste (Medianera principal):** $0,12\text{ m}$ ($8,00\text{ m}$ de longitud)
* **Espesor Muros Interiores:** $0,10\text{ m}$
* **Cota Zócalos:** $0,08\text{ m}$ blanco mate hidrófugo.

---

## 2. Inventario y Coordenadas del Mobiliario Calibrado

### Estudio (Oficina y Coleccionables)

| Elemento | Ancho (m) | Prof. (m) | Alto (m) | Coord. $X$ | Coord. $Y$ | Coord. $Z$ | Notas de Montaje |
|---|---|---|---|---|---|---|---|
| **Mesa Tijera + Ajedrez LotR** | 0.40 | 0.40 | 0.62 | 0.28 | 0.40 | 0.24 | Tablero temático, holgura de 5 cm con guitarra azul. |
| **Guitarra Eléctrica Azul** | 0.24 | 0.14 | 1.02 | 0.28 | 0.00 | 0.65 | Funda acolchada azul petróleo sobre pie de apoyo. |
| **Biblioteca Alta Principal** | 2.40 | 0.44 | 2.29 | 0.30 | 0.00 | 1.48 | 5 estantes, libros, consolas, desacoplada en selección. |
| **Guitarra Acústica Negra** | 0.24 | 0.14 | 1.05 | 0.28 | 0.00 | 2.23 | Funda acolchada negra entre biblioteca y diorama. |
| **Mesa Plegable + Diorama Jedi** | 0.40 | 0.40 | 0.62 | 0.30 | 0.42 | 2.55 | Sillas del Consejo Jedi circulares en radio 0.38 m. |
| **Estantes Flotantes (3 Niveles)**| 1.80 | 0.20 | 0.85 | 2.86 | 1.72 | 1.22 | Montados en pared divisoria Este, sin contacto con Oeste. |
| **Escritorio Gamer Principal** | 1.50 | 0.70 | 0.75 | 2.30 | 0.00 | 1.60 | Melamina fresno negro, pasacables y regleta oculta. |
| **Monitor Curvo Ultrawide** | 0.82 | 0.25 | 0.48 | 2.30 | 0.75 | 1.60 | Brazo hidráulico fijado a la tapa del escritorio. |
| **Gabinete Gamer Thermaltake** | 0.22 | 0.45 | 0.48 | 2.63 | 0.24 | 1.96 | Vidrio templado, RGB configurable, sobre base auxiliar. |

---

### Living y Comedor

| Elemento | Dimensiones Principales | Coordenadas Clave | Notas de Diseño |
|---|---|---|---|
| **Mesa de Comedor Redonda Nórdica** | Diámetro: $1,05\text{ m}$, Alto: $0,76\text{ m}$ | Centro en $X = 3.85\text{ m}, Z = 2.15\text{ m}$ | Tapa madera paraíso, base cónica / cruzada. |
| **Sillas Nórdicas Tapizadas (x4)** | Asiento: $0,45\times 0,45\text{ m}$, Respaldo $0,82\text{ m}$ | `chairRadius = 0.37 m` | Calibradas para meterse completamente bajo la mesa. |
| **Comederos de las Perras** | $0,44\times 0,22\text{ m}$ (bandeja doble) | $X = 4.44\text{ m}, Y = 0.05\text{ m}, Z = 5.03\text{ m}$ | Estrictamente 2 platos (verde esmeralda y rojo rubí). |
| **Sillón Esquinero en L** | $2,20\times 1,60\times 0,85\text{ m}$ | Esquina $X = 3.60\text{ m}, Z = 0.50\text{ m}$ | Lino gris antimanchas, pata metálica negra. |
| **Mueble de TV Bajo** | $1,80\times 0,40\times 0,55\text{ m}$ | Pared divisoria Living/Dormitorio | 3 cajones con guías telescópicas. |
| **Smart TV 55"** | $1,23\times 0,08\times 0,72\text{ m}$ | Elevación $Y = 1.05\text{ m}$ | Panel con bisel ultra-delgado. |

---

### Baño y Distribución

| Elemento | Dimensiones (W x D x H) | Ubicación / Ajustes |
|---|---|---|
| **Bacha de Lavatorio Cerámica** | $0,44\times 0,35\times 0,14\text{ m}$ | Sobre mesada de vanitory, compacta según video real. |
| **Accesorios de Bacha** | Dispenser jabón ($0,08\text{ m}$) + Base Oral-B | Centrados sobre la margen derecha de la mesada. |
| **Cortina de Ducha Doble** | Barral curvo cromado a $2,05\text{ m}$ | Capa 1: Liner PEVA impermeable interno en bañera.  <br>Capa 2: Cortina textil blanca externa decorativa con argollas dobles. |
| **Inodoro con Mochila Dual Flush**| $0,38\times 0,65\times 0,80\text{ m}$ | Cota lateral con bidet a $0,35\text{ m}$ de separación libre. |
| **Bidet con Grifería Monocomando**| $0,38\times 0,62\times 0,40\text{ m}$ | Grifería cromada con transferencia. |

---

### Hall de Entrada

| Elemento | Dimensiones | Ubicación / Estado |
|---|---|---|
| **Perchero y Zapatero Metálico** | $0,80\times 0,32\times 1,75\text{ m}$ | Junto a puerta de acceso principal. |
| **Caja Organizadora Plástica** | $0,38\times 0,28\times 0,20\text{ m}$ | Entidad desacoplada en el piso para selección individual. |
| **Espejo Vertical de Cuerpo Entero** | $0,50\times 1,60\text{ m}$ | Marco de aluminio anodizado negro sobre muro de entrada. |

---

## 3. Red de Luminarias Inteligentes WiZ (9 Puntos)

1. **Luminaria Hall de Entrada:** Plafón circular WiZ cálido ($2700\text{K}$).
2. **Luminaria Cocina:** Plafón rectangular LED de alto rendimiento ($4000\text{K}$ blanco neutro).
3. **Luminaria Comedor:** Colgante cilíndrico sobre mesa nórdica ($2700\text{K}$).
4. **Luminaria Living:** Plafón central regulable con dimmer virtual.
5. **Aplique Pasillo Baño:** Montado sobre dintel de puerta ($2700\text{K}$).
6. **Luminaria Baño:** Plafón hermético IP44 sobre vanitory ($4000\text{K}$).
7. **Luminaria Estudio (General):** Plafón de alto flujo lumínico ($4000\text{K}-5000\text{K}$).
8. **Lámpara de Escritorio Estudio:** Luz puntual direccionable sobre plano de trabajo ($3000\text{K}$).
9. **Luminaria Dormitorio:** Luz ambiental cálida con dimmer suave ($2700\text{K}$).
