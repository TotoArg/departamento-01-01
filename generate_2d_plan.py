"""
Generador del Plano 2D Arquitectónico Completo (6.30 m x 7.00 m, Planta en "L")
con los elementos reales relevados del video:
- Suelo: Piso cerámico esmaltado beige 33x33 cm en damero regular con zócalo perimetral.
- Techo (indicado en leyenda/cota): Machimbre de madera en pendiente con vigas vistas.
- Ventanas (7 aberturas reales de aluminio oscuro corredizas):
  * V1 y V2 (Living Norte, Y=0.00): X=3.35..4.55 y X=4.90..6.00
  * V3 (Living Este, X=6.30): Y=1.00..2.50
  * V4 (Estudio Norte, Y=0.00): X=0.85..2.05
  * V5 (Cuarto Sur, Y=7.00): X=0.90..2.10
  * V6 (Cocina Sur, Y=7.00): X=3.55..4.55
  * V7 (Ventiluz Baño Oeste, X=0.00): Y=3.05..3.75
- Calefactores a gas (Tiro Balanceado):
  * Calefactor 1 (Living Este, X=6.30, Y=2.75..3.35) con tiraje vertical al techo
  * Calefactor 2 (Cuarto Sur, Y=7.00, X=0.25..0.68)
  * Calefactor 3 (Estudio Oeste, X=0.00, Y=0.80..1.25)
- Equipamiento fijo de Cocina y Baño relevado del video:
  * Cocina: Mesada en "L" de granito rosa, bacha doble, cocina 4 hornallas y termotanque Sherman.
  * Baño: Bañera en fondo oeste (X=0.00..0.75), lavatorio pedestal e inodoro con mochila.
"""

from PIL import Image, ImageDraw, ImageFont
import math


def load_font(size, bold=False):
    candidates = (
        ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"]
        if bold
        else ["arial.ttf", "segoeui.ttf", "calibri.ttf", "DejaVuSans.ttf"]
    )
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_dashed_line(draw, x1, y1, x2, y2, fill, width=3, dash_len=10, gap_len=9):
    total_len = math.hypot(x2 - x1, y2 - y1)
    if total_len == 0:
        return
    dx = (x2 - x1) / total_len
    dy = (y2 - y1) / total_len
    curr = 0
    while curr < total_len:
        end = min(curr + dash_len, total_len)
        sx = x1 + dx * curr
        sy = y1 + dy * curr
        ex = x1 + dx * end
        ey = y1 + dy * end
        draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)
        curr += dash_len + gap_len


def draw_door_symbol(draw, px_fn, hinge, leaf, ctrl, end, color, width=3):
    hx, hy = px_fn(*hinge)
    lx, ly = px_fn(*leaf)
    cx, cy = px_fn(*ctrl)
    ex, ey = px_fn(*end)
    draw.line([(hx, hy), (lx, ly)], fill=color, width=width)
    steps = 24
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        qx = mt * mt * lx + 2 * mt * t * cx + t * t * ex
        qy = mt * mt * ly + 2 * mt * t * cy + t * t * ey
        pts.append((qx, qy))
    draw.line(pts, fill=color, width=max(2, width - 1))


def draw_window_h(draw, px_fn, x1, x2, y, ext_w):
    """Dibuja símbolo arquitectónico de ventana horizontal en muro exterior."""
    p1x, py = px_fn(x1, y)
    p2x, _ = px_fn(x2, y)
    half = ext_w // 2 + 1
    # Fondo vidrio celeste claro
    draw.rectangle([p1x, py - half, p2x, py + half], fill=(219, 234, 254), outline=(38, 45, 52), width=2)
    # Doble línea central de hojas corredizas
    draw.line([(p1x, py - 2), (p2x, py - 2)], fill=(2, 132, 199), width=2)
    draw.line([(p1x, py + 2), (p2x, py + 2)], fill=(2, 132, 199), width=2)
    # Divisor central de hoja corrediza
    mid_x = (p1x + p2x) // 2
    draw.line([(mid_x, py - half), (mid_x, py + half)], fill=(38, 45, 52), width=2)


def draw_window_v(draw, px_fn, x, y1, y2, ext_w):
    """Dibuja símbolo arquitectónico de ventana vertical en muro exterior."""
    px_val, p1y = px_fn(x, y1)
    _, p2y = px_fn(x, y2)
    half = ext_w // 2 + 1
    draw.rectangle([px_val - half, p1y, px_val + half, p2y], fill=(219, 234, 254), outline=(38, 45, 52), width=2)
    draw.line([(px_val - 2, p1y), (px_val - 2, p2y)], fill=(2, 132, 199), width=2)
    draw.line([(px_val + 2, p1y), (px_val + 2, p2y)], fill=(2, 132, 199), width=2)
    mid_y = (p1y + p2y) // 2
    draw.line([(px_val - half, mid_y), (px_val + half, mid_y)], fill=(38, 45, 52), width=2)


def main():
    SCALE = 150  # 1 metro = 150 px
    PAD_X = 145
    PAD_Y = 130

    PLAN_W = 6.30
    PLAN_H = 7.00

    W = int(PLAN_W * SCALE + PAD_X * 2)
    H = int(PLAN_H * SCALE + PAD_Y * 2 + 45)

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    def px(xm, ym):
        return int(round(PAD_X + xm * SCALE)), int(round(PAD_Y + ym * SCALE))

    WALL_COLOR = (38, 45, 52)
    DASH_COLOR = (120, 132, 145)
    DOOR_COLOR = (55, 65, 78)
    TEXT_COLOR = (30, 37, 45)
    SUB_COLOR = (82, 92, 105)
    PALIER_BG = (233, 236, 239)
    PALIER_TEXT = (108, 117, 125)
    TILE_BG = (252, 249, 244)       # Tono cerámico beige suave
    TILE_GRID = (236, 230, 220)     # Junta de baldosas 33x33 cm
    EXT_W = 11
    INT_W = 6

    # -------------------------------------------------------------------------
    # 0. PISO CERÁMICO BEIGE 33x33 cm (EXTRAÍDO DEL VIDEO) + PALIER EXTERIOR
    # -------------------------------------------------------------------------
    draw.rectangle([*px(0.00, 0.00), *px(6.30, 5.70)], fill=TILE_BG)
    draw.rectangle([*px(0.00, 5.70), *px(5.20, 7.00)], fill=TILE_BG)
    # Baño con cerámico claro
    draw.rectangle([*px(0.00, 2.80), *px(2.30, 4.00)], fill=(247, 250, 252))

    # Grilla de cerámicos 0.33 m x 0.33 m
    tile_step = 0.3333
    x_t = tile_step
    while x_t < 6.30:
        max_y = 5.70 if x_t > 5.20 else 7.00
        draw.line([px(x_t, 0.00), px(x_t, max_y)], fill=TILE_GRID, width=1)
        x_t += tile_step
    y_t = tile_step
    while y_t < 7.00:
        max_x = 5.20 if y_t > 5.70 else 6.30
        draw.line([px(0.00, y_t), px(max_x, y_t)], fill=TILE_GRID, width=1)
        y_t += tile_step

    # Palier Exterior
    draw.rectangle([*px(5.20, 5.70), *px(6.30, 7.00)], fill=PALIER_BG)

    # -------------------------------------------------------------------------
    # 1. EQUIPAMIENTO FIJO EXTRAÍDO DEL VIDEO (COCINA, BAÑO, CALEFACTORES)
    # -------------------------------------------------------------------------
    f_tiny = load_font(12, bold=True)

    # --- COCINA (según las fotos reales): Heladera -> 1° tramo mesada + Calefón mural -> Cocina 4H -> 2° tramo mesada en "L" con Bacha sobre Muro Este (X=5.20); Lavarropas + Estación Café bajo ventana Sur (lado Oeste); Muro Oeste libre con portero y cestos ---
    granite_fill = (228, 208, 200)
    granite_border = (160, 135, 125)
    # 1° tramo de mesada entre Heladera y Cocina 4H (X=4.58 a 5.16, Y=5.22 a 5.62)
    draw.rectangle([*px(4.58, 5.22), *px(5.16, 5.62)], fill=granite_fill, outline=granite_border, width=2)
    # Calefón mural a gas blanco (Orbis/Bosch) colgado sobre el 1° tramo de mesada (muro Este X=5.20)
    draw.rounded_rectangle([*px(4.84, 5.25), *px(5.15, 5.59)], radius=4, fill=(255, 255, 255), outline=(100, 116, 139), width=2)

    # Cocina a gas blanca de 4 hornallas sobre muro Este (X=4.58 a 5.16, Y=5.62 a 6.16)
    draw.rectangle([*px(4.58, 5.62), *px(5.16, 6.16)], fill=(255, 255, 255), outline=(100, 116, 139), width=2)
    for bx, by in [(4.75, 5.76), (5.00, 5.76), (4.75, 6.02), (5.00, 6.02)]:
        cx_b, cy_b = px(bx, by)
        draw.ellipse([cx_b - 6, cy_b - 6, cx_b + 6, cy_b + 6], outline=(71, 85, 105), width=2)

    # 2° tramo de mesada en "L" (X=4.58 a 5.16, Y=6.16 a 6.96 + retorno Sur X=3.88 a 5.16, Y=6.40 a 6.96)
    draw.polygon(
        [
            px(4.58, 6.16),
            px(5.16, 6.16),
            px(5.16, 6.96),
            px(3.88, 6.96),
            px(3.88, 6.40),
            px(4.58, 6.40),
        ],
        fill=granite_fill,
        outline=granite_border,
    )
    # Bacha doble esquinera de acero inoxidable + filtro PSA en esquina Sureste (X=4.44 a 5.08, Y=6.32 a 6.82)
    draw.rectangle([*px(4.62, 6.30), *px(5.08, 6.76)], fill=(226, 232, 240), outline=(100, 116, 139), width=2)
    draw.rectangle([*px(4.67, 6.35), *px(5.03, 6.53)], fill=(241, 245, 249), outline=(148, 163, 184), width=1)
    draw.rectangle([*px(4.67, 6.56), *px(5.03, 6.72)], fill=(241, 245, 249), outline=(148, 163, 184), width=1)

    # --- BAÑO (según fotos #23 a #29): Bañera (X=0.05..0.75), Lavatorio + Botiquín (X=1.18..1.64, Y=2.84..3.20), Bidet (X=1.02..1.38, Y=3.56..3.95) e Inodoro (X=1.56..1.94, Y=3.56..3.95) ---
    draw.rectangle([*px(0.05, 2.84), *px(0.75, 3.96)], fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    draw.rounded_rectangle([*px(0.12, 2.92), *px(0.68, 3.88)], radius=12, fill=(241, 245, 249), outline=(148, 163, 184), width=1)

    # Lavatorio (Norte)
    draw.rounded_rectangle([*px(1.18, 2.84), *px(1.64, 3.20)], radius=8, fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    # Bidet (Sur-Oeste) e Inodoro (Sur-Este)
    draw.rounded_rectangle([*px(1.02, 3.56), *px(1.38, 3.95)], radius=8, fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    draw.rounded_rectangle([*px(1.56, 3.56), *px(1.94, 3.95)], radius=8, fill=(255, 255, 255), outline=(148, 163, 184), width=2)

    # --- CALEFACTORES (Living tiro balanceado + Cuarto y Estudio paneles eléctricos negros, fotos #13, #17 y #33) ---
    heater_fill = (254, 215, 170)
    heater_border = (234, 88, 12)
    # 1) Living Este (X=6.06 a 6.26, Y=1.64 a 2.16, entre ventana V3 y el Rack de TV)
    draw.rectangle([*px(6.06, 1.64), *px(6.26, 2.16)], fill=heater_fill, outline=heater_border, width=2)
    # 2) Cuarto Sur-Este (X=2.25 a 2.72, Y=6.78 a 6.96)
    draw.rectangle([*px(2.25, 6.78), *px(2.72, 6.96)], fill=heater_fill, outline=heater_border, width=2)
    # 3) Estudio Norte (X=0.68 a 1.16, Y=0.05 a 0.20, a la izquierda de la ventana V4, foto #33)
    draw.rectangle([*px(0.20, 0.05), *px(0.70, 0.20)], fill=heater_fill, outline=heater_border, width=2)

    # --- MUEBLES, ELECTRODOMÉSTICOS Y DECORACIÓN (SIN TEXTOS SOBRE MUEBLES) ---
    # A) LIVING Y ENTRADA (Futón, Mesa Ratona y Rack + TV 50" alineados sobre el mismo eje Y = 2.80):
    # - Perchero + Zapatero Entrada (X=5.92..6.22, Y=4.06..4.70) y Maceta Sansevieria (X=6.05, Y=3.75)
    draw.rounded_rectangle([*px(5.92, 4.06), *px(6.22, 4.70)], radius=5, fill=(226, 232, 240), outline=(71, 85, 105), width=2)
    cx_p, cy_p = px(6.05, 3.75)
    draw.ellipse([cx_p - 12, cy_p - 12, cx_p + 12, cy_p + 12], fill=(187, 247, 208), outline=(22, 101, 52), width=2)

    # - Rack TV de madera + Smart TV 50" + 2 Torres Home Theater LG (X=5.78..6.22, Y=2.14..3.46, centrado en Y=2.80)
    draw.rounded_rectangle([*px(5.78, 2.14), *px(6.22, 3.46)], radius=6, fill=(254, 226, 226), outline=(153, 27, 27), width=2)

    # - Futón 3 Cuerpos Azul Petróleo (X=3.06..3.92, Y=1.84..3.76, centrado en Y=2.80)
    draw.rounded_rectangle([*px(3.06, 1.84), *px(3.92, 3.76)], radius=8, fill=(219, 234, 254), outline=(30, 64, 175), width=2)
    # - Mesa Ratona Elevable frente al futón y alineada con la TV (X=4.10..4.64, Y=2.29..3.31, centrada en Y=2.80)
    draw.rounded_rectangle([*px(4.10, 2.29), *px(4.64, 3.31)], radius=6, fill=(241, 245, 249), outline=(71, 85, 105), width=2)

    # - Mesa de Comedor Redonda (X=4.55, Y=1.22, Ø 1.08m) + 4 Sillas con almohadón verde lima + Cuchas perros
    cx_m, cy_m = px(4.55, 1.22)
    r_m = int(0.54 * SCALE)
    for sx, sy in [(4.55, 0.58), (4.55, 1.85), (3.92, 1.22), (5.18, 1.22)]:
        draw.rounded_rectangle([*px(sx - 0.18, sy - 0.18), *px(sx + 0.18, sy + 0.18)], radius=5, fill=(217, 249, 157), outline=(101, 163, 13), width=2)
    draw.ellipse([cx_m - r_m, cy_m - r_m, cx_m + r_m, cy_m + r_m], fill=(254, 226, 226), outline=(153, 27, 27), width=2)
    # - Cuchas grises de los perros bajo ventanas Norte (X=5.10..6.00, Y=0.10..0.66)
    draw.rounded_rectangle([*px(5.10, 0.10), *px(6.00, 0.66)], radius=8, fill=(226, 232, 240), outline=(100, 116, 139), width=2)

    # B) COCINA: Heladera con Freezer + Bodega al Noreste (X=4.55..5.15, Y=4.56..5.20), Lavarropas + Estación Café bajo ventana Sur (lado Oeste: X=3.24..3.86, Y=6.38..6.94) y Cestos + Portero sobre pared Oeste (X=3.06..3.42, Y=5.30..6.26)
    draw.rounded_rectangle([*px(4.55, 4.56), *px(5.15, 5.20)], radius=6, fill=(248, 250, 252), outline=(71, 85, 105), width=2)
    draw.rounded_rectangle([*px(3.25, 6.38), *px(3.85, 6.94)], radius=6, fill=(248, 250, 252), outline=(71, 85, 105), width=2)
    cx_w, cy_w = px(3.55, 6.66)
    draw.ellipse([cx_w - 14, cy_w - 14, cx_w + 14, cy_w + 14], fill=(226, 232, 240), outline=(100, 116, 139), width=2)
    draw.rounded_rectangle([*px(3.25, 5.30), *px(3.55, 6.26)], radius=5, fill=(226, 232, 240), outline=(100, 116, 139), width=2)

    # C) CUARTO AMPLIADO: Cama 2 Plazas (X=0.10..2.00, Y=5.12..6.52) + Respaldo Ancho Nogal y 2 Mesas de Luz sobre pared Oeste (X=0.00) + Cesto Ropa al Este
    draw.rounded_rectangle([*px(0.10, 5.12), *px(2.00, 6.52)], radius=8, fill=(226, 232, 240), outline=(71, 85, 105), width=2)
    draw.rectangle([*px(0.05, 4.68), *px(0.14, 6.92)], fill=(120, 53, 15), outline=(69, 26, 3), width=2)
    draw.rounded_rectangle([*px(0.08, 4.68), *px(0.50, 5.08)], radius=4, fill=(254, 243, 199), outline=(120, 53, 15), width=2)
    draw.rounded_rectangle([*px(0.08, 6.54), *px(0.50, 6.92)], radius=4, fill=(254, 243, 199), outline=(120, 53, 15), width=2)
    draw.rounded_rectangle([*px(2.48, 6.12), *px(2.88, 6.58)], radius=5, fill=(226, 232, 240), outline=(71, 85, 105), width=2)

    # D) ESTUDIO AMPLIADO (según fotos #31 a #40): Escritorio en "L" + PC Gamer + 3 Estantes + Silla Gamer + Mesa Ajedrez NO + Biblioteca 6 Estantes + Mesa redonda Ajedrez LOTR SO
    draw.polygon([px(1.35, 0.09), px(2.95, 0.09), px(2.95, 1.78), px(2.32, 1.78), px(2.32, 0.67), px(1.35, 0.67)], fill=(254, 226, 226), outline=(153, 27, 27), width=2)
    cx_sg, cy_sg = px(1.95, 1.12)
    draw.ellipse([cx_sg - 22, cy_sg - 22, cx_sg + 22, cy_sg + 22], fill=(254, 202, 202), outline=(185, 28, 28), width=2)
    # Mesa plegable cuadrada con ajedrez clásico en esquina Noroeste (foto #33)
    draw.rounded_rectangle([*px(0.08, 0.08), *px(0.50, 0.50)], radius=4, fill=(254, 243, 199), outline=(120, 53, 15), width=2)
    # Biblioteca alta de 6 estantes en pared Oeste (foto #35)
    draw.rounded_rectangle([*px(0.06, 0.74), *px(0.38, 1.60)], radius=4, fill=(254, 243, 199), outline=(120, 53, 15), width=2)
    # Mesita redonda con Ajedrez LOTR en esquina Suroeste junto al placard (foto #37)
    cx_aj, cy_aj = px(0.30, 2.02)
    draw.ellipse([cx_aj - 30, cy_aj - 30, cx_aj + 30, cy_aj + 30], fill=(254, 243, 199), outline=(120, 53, 15), width=2)

    # -------------------------------------------------------------------------
    # 2. PERÍMETRO EXTERIOR (Polígono en "L": 6.30 m x 7.00 m)
    # -------------------------------------------------------------------------
    draw.line([px(0.00, 0.00), px(6.30, 0.00)], fill=WALL_COLOR, width=EXT_W)
    draw.line([px(6.30, 0.00), px(6.30, 5.70)], fill=WALL_COLOR, width=EXT_W)
    draw.line([px(5.20, 5.70), px(5.20, 7.00)], fill=WALL_COLOR, width=EXT_W)
    draw.line([px(0.00, 7.00), px(5.20, 7.00)], fill=WALL_COLOR, width=EXT_W)
    draw.line([px(0.00, 0.00), px(0.00, 7.00)], fill=WALL_COLOR, width=EXT_W)

    r_ext = EXT_W // 2
    for cx, cy in [(0.00, 0.00), (6.30, 0.00), (6.30, 5.70), (5.20, 7.00), (0.00, 7.00)]:
        x, y = px(cx, cy)
        draw.rectangle([x - r_ext, y - r_ext, x + r_ext, y + r_ext], fill=WALL_COLOR)

    # Retranqueo Palier / Puerta Principal en Y = 5.70 (X = 5.20 a 6.30)
    draw.line([px(5.20, 5.70), px(5.34, 5.70)], fill=WALL_COLOR, width=EXT_W - 2)
    draw.line([px(6.18, 5.70), px(6.30, 5.70)], fill=WALL_COLOR, width=EXT_W - 2)
    draw.line([px(5.34, 5.70), px(6.18, 5.70)], fill=(195, 202, 210), width=7)
    draw.line([px(5.34, 5.58), px(5.34, 5.82)], fill=WALL_COLOR, width=5)
    draw.line([px(6.18, 5.58), px(6.18, 5.82)], fill=WALL_COLOR, width=5)
    # Símbolo arquitectónico de puerta de entrada batiendo 90° hacia el Norte sobre pared Este (fotos reales #1 y #3)
    draw_door_symbol(draw, px, (6.14, 5.70), (6.14, 4.96), (5.40, 4.96), (5.40, 5.70), DOOR_COLOR, width=3)
    # Comederos de mascota junto al zócalo de la pared divisoria Cocina-Entrada (fotos #0 y #3)
    cx_g, cy_g = px(5.12, 4.80)
    draw.ellipse([cx_g - 6, cy_g - 6, cx_g + 6, cy_g + 6], fill=(34, 197, 94), outline=(21, 128, 61), width=1)
    cx_r, cy_r = px(5.12, 4.52)
    draw.ellipse([cx_r - 6, cy_r - 6, cx_r + 6, cy_r + 6], fill=(239, 68, 68), outline=(185, 28, 28), width=1)

    # -------------------------------------------------------------------------
    # 3. VENTANAS EXTERIORES EXTRAÍDAS DEL VIDEO (7 ABERTURAS)
    # -------------------------------------------------------------------------
    # V1 y V2: Dos ventanas gemelas en pared Norte del Living (Y=0.00)
    draw_window_h(draw, px, 3.25, 4.35, 0.00, EXT_W)
    draw_window_h(draw, px, 4.95, 6.05, 0.00, EXT_W)
    # V3: Ventana lateral corrida Este del Living (X=6.30, Y=0.50 a 4.60)
    draw_window_v(draw, px, 6.30, 0.25, 1.45, EXT_W)
    # V4: Ventana Norte del Estudio Ampliado (Y=0.00, X=1.35 a 2.55, encuadrada sobre el ala Norte del escritorio en L)
    draw_window_h(draw, px, 0.90, 2.10, 0.00, EXT_W)
    # V5: Ventana Sur del Cuarto Ampliado (Y=7.00, X=0.90 a 2.10)
    draw_window_h(draw, px, 0.90, 2.10, 7.00, EXT_W)
    # V6: Ventana Sur de la Cocina sobre escurridor y lavarropas (Y=7.00, X=3.25 a 4.55)
    draw_window_h(draw, px, 3.25, 4.55, 7.00, EXT_W)
    # V7: Ventiluz Oeste del Baño sobre bañera (X=0.00, Y=3.05 a 3.75)
    draw_window_v(draw, px, 0.00, 3.05, 3.75, EXT_W)

    # -------------------------------------------------------------------------
    # 4. MUROS INTERNOS, PUERTAS (HACIA ADENTRO DE HABITACIONES Y BAÑO) Y VANOS
    # -------------------------------------------------------------------------
    # Eje Vertical X = 2.30 (Cierre de Placards y Baño):
    # - Muro sólido superior más largo (de Y = 2.30 a Y = 3.02: Placard Sup. + mocheta superior del Baño)
    draw.line([px(2.30, 2.30), px(2.30, 3.02)], fill=WALL_COLOR, width=INT_W)
    # - Puerta Baño (de Y = 3.02 a Y = 3.65): bisagra al Sur (Y=3.65), abre HACIA ADENTRO del Baño (foto #23)
    draw_dashed_line(draw, *px(2.30, 3.02), *px(2.30, 3.65), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.30, 3.62), (2.08, 3.42), (2.04, 3.20), (2.30, 3.05), DOOR_COLOR, width=3)
    # - Muro sólido inferior (de Y = 3.65 a Y = 4.50: mocheta inferior del Baño + Placard Inf.)
    draw.line([px(2.30, 3.65), px(2.30, 4.50)], fill=WALL_COLOR, width=INT_W)

    # Eje Vertical Central X = 3.00:
    draw.line([px(3.00, 0.00), px(3.00, 3.70)], fill=WALL_COLOR, width=INT_W)
    draw_dashed_line(draw, *px(3.00, 3.70), *px(3.00, 4.50), fill=DASH_COLOR, width=3)
    draw.line([px(3.00, 4.50), px(3.20, 4.50)], fill=WALL_COLOR, width=INT_W)
    draw.line([px(3.20, 4.50), px(3.20, 7.00)], fill=WALL_COLOR, width=INT_W)

    # Eje Vertical X = 5.20 (separa Cocina de Entrada): de Y = 4.50 a Y = 5.70
    draw.line([px(5.20, 4.50), px(5.20, 5.70)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 2.30 (Frente Placard y Puerta Estudio):
    # - Mochetas laterales del placard (0.00..0.22 y 2.12..2.30)
    draw.line([px(0.00, 2.30), px(0.22, 2.30)], fill=WALL_COLOR, width=INT_W)
    draw.line([px(2.12, 2.30), px(2.30, 2.30)], fill=WALL_COLOR, width=INT_W)
    # - Frente de hojas corredizas del placard (líneas técnicas dobles)
    draw.line([px(0.22, 2.285), px(1.19, 2.285)], fill=(100, 116, 139), width=3)
    draw.line([px(1.15, 2.315), px(2.12, 2.315)], fill=(100, 116, 139), width=3)
    # - Puerta Estudio (de X = 2.30 a X = 3.00): bisagra al Este (X=3.00), abre HACIA ADENTRO del Estudio sobre muro Este (fotos #39 y #40)
    draw_dashed_line(draw, *px(2.30, 2.30), *px(3.00, 2.30), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.95, 2.30), (2.75, 2.08), (2.55, 2.08), (2.42, 2.30), DOOR_COLOR, width=3)

    # Eje Horizontal Y = 2.80 (Divide Placard Superior y Baño): de X = 0.00 a X = 2.30
    draw.line([px(0.00, 2.80), px(2.30, 2.80)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 4.00 (Divide Baño y Placard Inferior): de X = 0.00 a X = 2.30
    draw.line([px(0.00, 4.00), px(2.30, 4.00)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 4.50 (Línea Cuarto y Cocina / Frente Placard):
    # - Mochetas laterales del placard (0.00..0.22 y 2.12..2.30)
    draw.line([px(0.00, 4.50), px(0.22, 4.50)], fill=WALL_COLOR, width=INT_W)
    draw.line([px(2.12, 4.50), px(2.30, 4.50)], fill=WALL_COLOR, width=INT_W)
    # - Frente de hojas corredizas del placard (hoja izquierda exterior en 4.515, hoja derecha interior en 4.485)
    draw.line([px(0.22, 4.515), px(1.19, 4.515)], fill=(100, 116, 139), width=3)
    draw.line([px(1.15, 4.485), px(2.12, 4.485)], fill=(100, 116, 139), width=3)
    # - Puerta Cuarto (de X = 2.30 a X = 3.00): bisagra al Este (X=3.00), abre HACIA ADENTRO del Cuarto sobre muro Este (fotos #17 y #22)
    draw_dashed_line(draw, *px(2.30, 4.50), *px(3.00, 4.50), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.95, 4.50), (2.75, 4.72), (2.55, 4.72), (2.42, 4.50), DOOR_COLOR, width=3)
    # - Cocina SIN PUERTA (vano abierto libre de X = 3.00 a X = 4.45; mocheta de X = 4.45 a X = 5.20 delante de la heladera)
    draw_dashed_line(draw, *px(3.20, 4.50), *px(4.45, 4.50), fill=DASH_COLOR, width=3)
    draw.line([px(4.45, 4.50), px(5.20, 4.50)], fill=WALL_COLOR, width=INT_W)

    # -------------------------------------------------------------------------
    # 5. TIPOGRAFÍA Y ETIQUETAS DE AMBIENTES
    # -------------------------------------------------------------------------
    f_living = load_font(30, bold=True)
    f_room = load_font(22, bold=True)
    f_bano = load_font(18, bold=True)
    f_sm = load_font(15, bold=True)
    f_sub = load_font(14, bold=False)
    f_palier = load_font(14, bold=True)
    f_dim = load_font(19, bold=False)

    draw.text(px(1.25, 1.55), "ESTUDIO", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(1.15, 2.55), "PLACARD", fill=TEXT_COLOR, font=f_sm, anchor="mm")
    draw.text(px(1.38, 3.40), "BAÑO", fill=TEXT_COLOR, font=f_bano, anchor="mm")
    draw.text(px(1.15, 4.25), "PLACARD", fill=TEXT_COLOR, font=f_sm, anchor="mm")
    draw.text(px(1.72, 4.88), "CUARTO", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(4.92, 3.68), "LIVING", fill=TEXT_COLOR, font=f_living, anchor="mm")
    draw.text(px(4.92, 3.94), "(Techo madera + vigas vistas)", fill=SUB_COLOR, font=f_sub, anchor="mm")
    draw.text(px(4.15, 5.50), "COCINA", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(5.58, 5.38), "ENTRADA", fill=TEXT_COLOR, font=f_sm, anchor="mm")
    draw.text(px(5.75, 6.23), "PALIER", fill=PALIER_TEXT, font=f_palier, anchor="mm")
    draw.text(px(5.75, 6.42), "EDIFICIO", fill=PALIER_TEXT, font=f_palier, anchor="mm")

    # Texto vertical: PASILLO
    pasillo_img = Image.new("RGBA", (200, 50), (255, 255, 255, 0))
    p_draw = ImageDraw.Draw(pasillo_img)
    p_draw.text((100, 25), "PASILLO", fill=(108, 117, 125), font=load_font(15, bold=True), anchor="mm")
    pasillo_rot = pasillo_img.rotate(90, expand=True)
    px_pas, py_pas = px(2.68, 3.25)
    img.paste(pasillo_rot, (px_pas - pasillo_rot.width // 2, py_pas - pasillo_rot.height // 2), pasillo_rot)

    # Cota superior: 6.30 m
    draw.text(px(3.15, -0.24), "6.30 m", fill=SUB_COLOR, font=f_dim, anchor="mm")

    # Cota izquierda vertical: 7.00 m
    dim_v_img = Image.new("RGBA", (200, 50), (255, 255, 255, 0))
    dv_draw = ImageDraw.Draw(dim_v_img)
    dv_draw.text((100, 25), "7.00 m", fill=SUB_COLOR, font=f_dim, anchor="mm")
    dim_v_rot = dim_v_img.rotate(90, expand=True)
    px_dv, py_dv = px(-0.26, 3.50)
    img.paste(dim_v_rot, (px_dv - dim_v_rot.width // 2, py_dv - dim_v_rot.height // 2), dim_v_rot)

    # Leyenda inferior de materiales relevados en video
    legend_y = H - 38
    draw.text(
        (W // 2, legend_y),
        "Relevamiento de Video: Suelo Cerámico 33×33cm Beige  |  Techo Machimbre y Vigas en Pendiente  |  7 Ventanas Aluminio Negro  |  3 Calefactores Tiro Balanceado",
        fill=(71, 85, 105),
        font=load_font(14, bold=True),
        anchor="mm",
    )

    output_path = "plano_arquitectonico_2d.png"
    img.save(output_path, "PNG", optimize=True)
    print(f"Plano 2D completo con detalles de video generado en: {output_path} ({W}x{H} px)")


if __name__ == "__main__":
    main()
