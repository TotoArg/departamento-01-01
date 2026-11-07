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

    # --- COCINA: Mesada en "L" de granito rosa + Bacha doble + Cocina 4H + Termo Sherman ---
    # Tramo vertical mesada (X=3.00 a 3.60, Y=5.35 a 7.00) y tramo horizontal (X=3.00 a 4.65, Y=6.40 a 7.00)
    granite_fill = (228, 208, 200)
    granite_border = (160, 135, 125)
    draw.polygon(
        [
            px(3.03, 5.35),
            px(3.62, 5.35),
            px(3.62, 6.40),
            px(4.62, 6.40),
            px(4.62, 6.96),
            px(3.03, 6.96),
        ],
        fill=granite_fill,
        outline=granite_border,
    )
    # Termotanque Sherman (círculo blanco en X=3.32, Y=5.65)
    tx, ty = px(3.32, 5.65)
    r_termo = int(0.21 * SCALE)
    draw.ellipse([tx - r_termo, ty - r_termo, tx + r_termo, ty + r_termo], fill=(255, 255, 255), outline=(100, 116, 139), width=2)
    draw.text((tx, ty), "TERMO", fill=(71, 85, 105), font=load_font(10, bold=True), anchor="mm")

    # Cocina 4 hornallas (X=3.05 a 3.60, Y=5.92 a 6.38)
    draw.rectangle([*px(3.05, 5.92), *px(3.60, 6.38)], fill=(255, 255, 255), outline=(100, 116, 139), width=2)
    for bx, by in [(3.20, 6.04), (3.44, 6.04), (3.20, 6.26), (3.44, 6.26)]:
        cx_b, cy_b = px(bx, by)
        draw.ellipse([cx_b - 6, cy_b - 6, cx_b + 6, cy_b + 6], outline=(71, 85, 105), width=2)

    # Bacha doble de acero inoxidable bajo ventana cocina (X=3.72 a 4.42, Y=6.48 a 6.88)
    draw.rectangle([*px(3.72, 6.48), *px(4.42, 6.88)], fill=(226, 232, 240), outline=(100, 116, 139), width=2)
    draw.rectangle([*px(3.76, 6.53), *px(4.04, 6.83)], fill=(241, 245, 249), outline=(148, 163, 184), width=1)
    draw.rectangle([*px(4.09, 6.53), *px(4.37, 6.83)], fill=(241, 245, 249), outline=(148, 163, 184), width=1)

    # --- BAÑO: Bañera (X=0.04..0.74, Y=2.84..3.96), Lavatorio (X=1.10..1.55, Y=2.84..3.22), Inodoro (X=1.65..2.05, Y=3.55..3.96) ---
    draw.rectangle([*px(0.05, 2.84), *px(0.75, 3.96)], fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    draw.rounded_rectangle([*px(0.12, 2.92), *px(0.68, 3.88)], radius=12, fill=(241, 245, 249), outline=(148, 163, 184), width=1)
    draw.text(px(0.40, 3.40), "BAÑERA", fill=(100, 116, 139), font=load_font(10, bold=True), anchor="mm")

    # Lavatorio
    draw.rounded_rectangle([*px(1.12, 2.84), *px(1.58, 3.20)], radius=8, fill=(255, 255, 255), outline=(148, 163, 184), width=2)
    # Inodoro
    draw.rounded_rectangle([*px(1.68, 3.56), *px(2.06, 3.95)], radius=8, fill=(255, 255, 255), outline=(148, 163, 184), width=2)

    # --- CALEFACTORES TIRO BALANCEADO (3 relevados en el video) ---
    heater_fill = (254, 215, 170)
    heater_border = (234, 88, 12)
    # 1) Living Este (X=6.08 a 6.26, Y=2.75 a 3.35)
    draw.rectangle([*px(6.06, 2.75), *px(6.26, 3.35)], fill=heater_fill, outline=heater_border, width=2)
    draw.text(px(5.78, 3.05), "CALEFACTOR", fill=heater_border, font=load_font(10, bold=True), anchor="mm")
    # 2) Cuarto Sur (X=0.25 a 0.72, Y=6.78 a 6.96)
    draw.rectangle([*px(0.25, 6.78), *px(0.72, 6.96)], fill=heater_fill, outline=heater_border, width=2)
    draw.text(px(0.48, 6.65), "CALEF.", fill=heater_border, font=load_font(10, bold=True), anchor="mm")
    # 3) Estudio Oeste (X=0.04 a 0.22, Y=0.80 a 1.25)
    draw.rectangle([*px(0.04, 0.80), *px(0.22, 1.25)], fill=heater_fill, outline=heater_border, width=2)
    draw.text(px(0.48, 1.02), "CALEF.", fill=heater_border, font=load_font(10, bold=True), anchor="mm")

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
    draw.line([px(5.20, 5.70), px(5.38, 5.70)], fill=WALL_COLOR, width=EXT_W - 2)
    draw.line([px(6.12, 5.70), px(6.30, 5.70)], fill=WALL_COLOR, width=EXT_W - 2)
    draw.line([px(5.38, 5.70), px(6.12, 5.70)], fill=(195, 202, 210), width=7)
    draw.line([px(5.38, 5.58), px(5.38, 5.82)], fill=WALL_COLOR, width=5)
    draw.line([px(6.12, 5.58), px(6.12, 5.82)], fill=WALL_COLOR, width=5)

    # -------------------------------------------------------------------------
    # 3. VENTANAS EXTERIORES EXTRAÍDAS DEL VIDEO (7 ABERTURAS)
    # -------------------------------------------------------------------------
    # V1 y V2: Dos ventanas gemelas en pared Norte del Living (Y=0.00)
    draw_window_h(draw, px, 3.35, 4.55, 0.00, EXT_W)
    draw_window_h(draw, px, 4.90, 6.00, 0.00, EXT_W)
    # V3: Ventana lateral Este del Living (X=6.30, Y=1.00 a 2.50)
    draw_window_v(draw, px, 6.30, 1.00, 2.50, EXT_W)
    # V4: Ventana Norte del Estudio Ampliado (Y=0.00, X=0.85 a 2.05)
    draw_window_h(draw, px, 0.85, 2.05, 0.00, EXT_W)
    # V5: Ventana Sur del Cuarto Ampliado (Y=7.00, X=0.90 a 2.10)
    draw_window_h(draw, px, 0.90, 2.10, 7.00, EXT_W)
    # V6: Ventana Sur de la Cocina sobre bacha (Y=7.00, X=3.55 a 4.55)
    draw_window_h(draw, px, 3.55, 4.55, 7.00, EXT_W)
    # V7: Ventiluz Oeste del Baño sobre bañera (X=0.00, Y=3.05 a 3.75)
    draw_window_v(draw, px, 0.00, 3.05, 3.75, EXT_W)

    # -------------------------------------------------------------------------
    # 4. MUROS INTERNOS, PUERTAS (CON ARCOS) Y VANOS ABIERTOS
    # -------------------------------------------------------------------------
    # Eje Vertical X = 2.30 (Cierre de Placards y Baño):
    draw.line([px(2.30, 2.30), px(2.30, 2.80)], fill=WALL_COLOR, width=INT_W)
    draw_dashed_line(draw, *px(2.30, 2.80), *px(2.30, 3.70), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.30, 3.55), (2.48, 3.35), (2.52, 3.12), (2.30, 2.95), DOOR_COLOR, width=3)
    draw.line([px(2.30, 3.70), px(2.30, 4.50)], fill=WALL_COLOR, width=INT_W)

    # Eje Vertical Central X = 3.00:
    draw.line([px(3.00, 0.00), px(3.00, 3.70)], fill=WALL_COLOR, width=INT_W)
    draw_dashed_line(draw, *px(3.00, 3.70), *px(3.00, 4.50), fill=DASH_COLOR, width=3)
    draw.line([px(3.00, 4.50), px(3.00, 7.00)], fill=WALL_COLOR, width=INT_W)

    # Eje Vertical X = 5.20 (separa Cocina de Entrada): de Y = 4.50 a Y = 5.70
    draw.line([px(5.20, 4.50), px(5.20, 5.70)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 2.30 (Base Estudio):
    draw.line([px(0.00, 2.30), px(2.30, 2.30)], fill=WALL_COLOR, width=INT_W)
    draw_dashed_line(draw, *px(2.30, 2.30), *px(3.00, 2.30), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.35, 2.30), (2.55, 2.48), (2.75, 2.48), (2.85, 2.30), DOOR_COLOR, width=3)

    # Eje Horizontal Y = 2.80 (Divide Placard Superior y Baño): de X = 0.00 a X = 2.30
    draw.line([px(0.00, 2.80), px(2.30, 2.80)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 4.00 (Divide Baño y Placard Inferior): de X = 0.00 a X = 2.30
    draw.line([px(0.00, 4.00), px(2.30, 4.00)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 4.50 (Línea Cuarto y Cocina):
    draw.line([px(0.00, 4.50), px(2.30, 4.50)], fill=WALL_COLOR, width=INT_W)
    draw_dashed_line(draw, *px(2.30, 4.50), *px(3.00, 4.50), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.35, 4.50), (2.55, 4.32), (2.75, 4.32), (2.85, 4.50), DOOR_COLOR, width=3)
    draw_dashed_line(draw, *px(3.00, 4.50), *px(3.85, 4.50), fill=DASH_COLOR, width=3)
    draw.line([px(3.85, 4.50), px(5.20, 4.50)], fill=WALL_COLOR, width=INT_W)

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

    draw.text(px(1.50, 1.15), "ESTUDIO AMPLIADO", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(1.15, 2.55), "PLACARD", fill=TEXT_COLOR, font=f_sm, anchor="mm")
    draw.text(px(1.38, 3.40), "BAÑO AMPLIO", fill=TEXT_COLOR, font=f_bano, anchor="mm")
    draw.text(px(1.15, 4.25), "PLACARD", fill=TEXT_COLOR, font=f_sm, anchor="mm")
    draw.text(px(1.50, 5.65), "CUARTO AMPLIADO", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(4.55, 1.95), "LIVING", fill=TEXT_COLOR, font=f_living, anchor="mm")
    draw.text(px(4.40, 2.28), "(Techo madera en pendiente + vigas vistas)", fill=SUB_COLOR, font=f_sub, anchor="mm")
    draw.text(px(4.32, 5.42), "COCINA", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(4.32, 5.70), "(Acceso junto al pasillo)", fill=SUB_COLOR, font=f_sub, anchor="mm")
    draw.text(px(5.75, 5.20), "ENTRADA", fill=TEXT_COLOR, font=f_sm, anchor="mm")
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
