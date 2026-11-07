"""
Generador del Plano 2D Esquemático Exacto (6.30 m x 7.00 m, Planta en "L").
Coordenadas exactas desde [0.00, 0.00] (Esquina Superior Izquierda / Noroeste):
1. PERÍMETRO EXTERIOR (Polígono en "L"):
   - Muro Superior (Norte): [0.00, 0.00] a [6.30, 0.00] (6.30 m)
   - Muro Derecho (Este): [6.30, 0.00] a [6.30, 5.70]
   - Retranqueo Palier (Puerta Principal en Y=5.70): [6.30, 5.70] a [5.20, 5.70]
   - Muro Derecho Cocina: [5.20, 5.70] a [5.20, 7.00]
   - Muro Inferior (Sur): [5.20, 7.00] a [0.00, 7.00]
   - Muro Izquierdo (Oeste): [0.00, 7.00] a [0.00, 0.00] (7.00 m)
   - Palier Edificio (Exterior): [5.20, 5.70] a [6.30, 7.00]
2. AMBIENTES Y COORDENADAS EXACTAS:
   - ESTUDIO AMPLIADO: [0.00, 0.00] a [3.00, 2.30]
   - PLACARD SUPERIOR: [0.00, 2.30] a [2.30, 2.80]
   - BAÑO AMPLIO: [0.00, 2.80] a [2.30, 4.00]
   - PLACARD INFERIOR: [0.00, 4.00] a [2.30, 4.50]
   - CUARTO AMPLIADO: [0.00, 4.50] a [3.00, 7.00]
   - PASILLO DISTRIBUIDOR: [2.30, 2.30] a [3.00, 4.50]
   - LIVING: [3.00, 0.00] a [6.30, 4.50] (Abierto, sin columnas)
   - ENTRADA: [5.20, 4.50] a [6.30, 5.70]
   - COCINA: [3.00, 4.50] a [5.20, 7.00]
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
    # Hoja de la puerta
    draw.line([(hx, hy), (lx, ly)], fill=color, width=width)
    # Arco cuadrático suave
    steps = 24
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        qx = mt * mt * lx + 2 * mt * t * cx + t * t * ex
        qy = mt * mt * ly + 2 * mt * t * cy + t * t * ey
        pts.append((qx, qy))
    draw.line(pts, fill=color, width=max(2, width - 1))


def main():
    SCALE = 150  # 1 metro = 150 px
    PAD_X = 135
    PAD_Y = 120

    PLAN_W = 6.30
    PLAN_H = 7.00

    W = int(PLAN_W * SCALE + PAD_X * 2)
    H = int(PLAN_H * SCALE + PAD_Y * 2)

    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    def px(xm, ym):
        return int(round(PAD_X + xm * SCALE)), int(round(PAD_Y + ym * SCALE))

    WALL_COLOR = (38, 45, 52)       # Gris carbón oscuro para muros
    DASH_COLOR = (130, 142, 155)    # Gris medio para líneas punteadas
    DOOR_COLOR = (60, 70, 82)       # Trazo de puertas y arcos
    TEXT_COLOR = (35, 42, 50)
    SUB_COLOR = (82, 92, 105)
    PALIER_BG = (233, 236, 239)     # #e9ecef
    PALIER_TEXT = (108, 117, 125)
    EXT_W = 11                      # Espesor de muro perimetral exterior
    INT_W = 6                       # Espesor de tabiques interiores

    # -------------------------------------------------------------------------
    # 0. SOMBRA / BLOQUE EXTERIOR DEL PALIER ([5.20, 5.70] a [6.30, 7.00])
    # -------------------------------------------------------------------------
    p1x, p1y = px(5.20, 5.70)
    p2x, p2y = px(6.30, 7.00)
    draw.rectangle([p1x, p1y, p2x, p2y], fill=PALIER_BG)

    # -------------------------------------------------------------------------
    # 1. PERÍMETRO EXTERIOR (Polígono en "L": 6.30 m x 7.00 m)
    # -------------------------------------------------------------------------
    # Muro Superior: [0.00, 0.00] a [6.30, 0.00]
    draw.line([px(0.00, 0.00), px(6.30, 0.00)], fill=WALL_COLOR, width=EXT_W)
    # Muro Derecho: [6.30, 0.00] a [6.30, 5.70]
    draw.line([px(6.30, 0.00), px(6.30, 5.70)], fill=WALL_COLOR, width=EXT_W)
    # Muro Derecho Cocina (baja al fondo): [5.20, 5.70] a [5.20, 7.00]
    draw.line([px(5.20, 5.70), px(5.20, 7.00)], fill=WALL_COLOR, width=EXT_W)
    # Muro Inferior: [0.00, 7.00] a [5.20, 7.00]
    draw.line([px(0.00, 7.00), px(5.20, 7.00)], fill=WALL_COLOR, width=EXT_W)
    # Muro Izquierdo: [0.00, 0.00] a [0.00, 7.00]
    draw.line([px(0.00, 0.00), px(0.00, 7.00)], fill=WALL_COLOR, width=EXT_W)

    # Tapar esquinas exteriores para unión perfecta
    r_ext = EXT_W // 2
    for cx, cy in [(0.00, 0.00), (6.30, 0.00), (6.30, 5.70), (5.20, 7.00), (0.00, 7.00)]:
        x, y = px(cx, cy)
        draw.rectangle([x - r_ext, y - r_ext, x + r_ext, y + r_ext], fill=WALL_COLOR)

    # Retranqueo Palier / Puerta Principal en Y = 5.70 (X = 5.20 a 6.30)
    # Mochetas laterales (5.20 a 5.38 y 6.12 a 6.30) + barra de umbral + jambas verticales
    draw.line([px(5.20, 5.70), px(5.38, 5.70)], fill=WALL_COLOR, width=EXT_W - 2)
    draw.line([px(6.12, 5.70), px(6.30, 5.70)], fill=WALL_COLOR, width=EXT_W - 2)
    draw.line([px(5.38, 5.70), px(6.12, 5.70)], fill=(195, 202, 210), width=7)
    draw.line([px(5.38, 5.58), px(5.38, 5.82)], fill=WALL_COLOR, width=5)
    draw.line([px(6.12, 5.58), px(6.12, 5.82)], fill=WALL_COLOR, width=5)

    # -------------------------------------------------------------------------
    # 2. MUROS INTERNOS, PUERTAS (CON ARCOS) Y VANOS ABIERTOS
    # -------------------------------------------------------------------------
    # Eje Vertical X = 2.30 (Cierre de Placards y Baño):
    # - Muro sólido de Y = 2.30 a Y = 2.80 (Placard Sup.)
    draw.line([px(2.30, 2.30), px(2.30, 2.80)], fill=WALL_COLOR, width=INT_W)
    # - PUERTA BAÑO: Entre Y = 2.80 e Y = 3.70 (abre hacia el pasillo)
    draw_dashed_line(draw, *px(2.30, 2.80), *px(2.30, 3.70), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.30, 3.55), (2.48, 3.35), (2.52, 3.12), (2.30, 2.95), DOOR_COLOR, width=3)
    # - Muro sólido de Y = 3.70 a Y = 4.50 (tramo Baño 3.70-4.00 + Placard Inf. 4.00-4.50)
    draw.line([px(2.30, 3.70), px(2.30, 4.50)], fill=WALL_COLOR, width=INT_W)

    # Eje Vertical Central X = 3.00:
    # - Muro sólido de Y = 0.00 a Y = 3.70 (separa Estudio y parte del Pasillo del Living)
    draw.line([px(3.00, 0.00), px(3.00, 3.70)], fill=WALL_COLOR, width=INT_W)
    # - VANO ABIERTO (Paso Living-Pasillo): Sin muro entre Y = 3.70 e Y = 4.50
    draw_dashed_line(draw, *px(3.00, 3.70), *px(3.00, 4.50), fill=DASH_COLOR, width=3)
    # - Muro sólido de Y = 4.50 a Y = 7.00 (separa Cuarto de Cocina)
    draw.line([px(3.00, 4.50), px(3.00, 7.00)], fill=WALL_COLOR, width=INT_W)

    # Eje Vertical X = 5.20 (separa Cocina de Entrada): de Y = 4.50 a Y = 5.70
    draw.line([px(5.20, 4.50), px(5.20, 5.70)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 2.30 (Base Estudio):
    # - Muro sólido de X = 0.00 a X = 2.30
    draw.line([px(0.00, 2.30), px(2.30, 2.30)], fill=WALL_COLOR, width=INT_W)
    # - PUERTA ESTUDIO: De X = 2.30 a X = 3.00 (abre hacia abajo, al pasillo)
    draw_dashed_line(draw, *px(2.30, 2.30), *px(3.00, 2.30), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.35, 2.30), (2.55, 2.48), (2.75, 2.48), (2.85, 2.30), DOOR_COLOR, width=3)

    # Eje Horizontal Y = 2.80 (Divide Placard Superior y Baño): de X = 0.00 a X = 2.30
    draw.line([px(0.00, 2.80), px(2.30, 2.80)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 4.00 (Divide Baño y Placard Inferior): de X = 0.00 a X = 2.30
    draw.line([px(0.00, 4.00), px(2.30, 4.00)], fill=WALL_COLOR, width=INT_W)

    # Eje Horizontal Y = 4.50 (Línea Cuarto y Cocina):
    # - Muro sólido de X = 0.00 a X = 2.30
    draw.line([px(0.00, 4.50), px(2.30, 4.50)], fill=WALL_COLOR, width=INT_W)
    # - PUERTA CUARTO: De X = 2.30 a X = 3.00 (abre hacia arriba, al pasillo)
    draw_dashed_line(draw, *px(2.30, 4.50), *px(3.00, 4.50), fill=DASH_COLOR, width=3)
    draw_door_symbol(draw, px, (2.35, 4.50), (2.55, 4.32), (2.75, 4.32), (2.85, 4.50), DOOR_COLOR, width=3)
    # - VANO ABIERTO COCINA: Sin muro de X = 3.00 a X = 3.85 (acceso libre pegado al pasillo)
    draw_dashed_line(draw, *px(3.00, 4.50), *px(3.85, 4.50), fill=DASH_COLOR, width=3)
    # - Muro sólido frontal de Cocina: De X = 3.85 a X = 5.20
    draw.line([px(3.85, 4.50), px(5.20, 4.50)], fill=WALL_COLOR, width=INT_W)

    # -------------------------------------------------------------------------
    # 3. TIPOGRAFÍA Y ETIQUETAS DE AMBIENTES
    # -------------------------------------------------------------------------
    f_living = load_font(30, bold=True)
    f_room = load_font(23, bold=True)
    f_bano = load_font(20, bold=True)
    f_sm = load_font(16, bold=True)
    f_sub = load_font(15, bold=False)
    f_palier = load_font(14, bold=True)
    f_dim = load_font(19, bold=False)

    # Estudio Ampliado: [0.00, 0.00] a [3.00, 2.30]
    draw.text(px(1.22, 1.05), "ESTUDIO AMPLIADO", fill=TEXT_COLOR, font=f_room, anchor="mm")

    # Placard Superior: [0.00, 2.30] a [2.30, 2.80]
    draw.text(px(1.15, 2.55), "PLACARD", fill=TEXT_COLOR, font=f_sm, anchor="mm")

    # Baño Amplio: [0.00, 2.80] a [2.30, 4.00]
    draw.text(px(1.15, 3.40), "BAÑO AMPLIO", fill=TEXT_COLOR, font=f_bano, anchor="mm")

    # Placard Inferior: [0.00, 4.00] a [2.30, 4.50]
    draw.text(px(1.15, 4.25), "PLACARD", fill=TEXT_COLOR, font=f_sm, anchor="mm")

    # Cuarto Ampliado: [0.00, 4.50] a [3.00, 7.00]
    draw.text(px(1.22, 5.65), "CUARTO AMPLIADO", fill=TEXT_COLOR, font=f_room, anchor="mm")

    # Living: [3.00, 0.00] a [6.30, 4.50]
    draw.text(px(4.65, 2.00), "LIVING", fill=TEXT_COLOR, font=f_living, anchor="mm")

    # Cocina: [3.00, 4.50] a [5.20, 7.00]
    draw.text(px(4.10, 5.65), "COCINA", fill=TEXT_COLOR, font=f_room, anchor="mm")
    draw.text(px(4.10, 5.95), "(Acceso junto al pasillo)", fill=SUB_COLOR, font=f_sub, anchor="mm")

    # Entrada: [5.20, 4.50] a [6.30, 5.70]
    draw.text(px(5.75, 5.20), "ENTRADA", fill=TEXT_COLOR, font=f_sm, anchor="mm")

    # Palier Edificio: [5.20, 5.70] a [6.30, 7.00]
    draw.text(px(5.75, 6.23), "PALIER", fill=PALIER_TEXT, font=f_palier, anchor="mm")
    draw.text(px(5.75, 6.42), "EDIFICIO", fill=PALIER_TEXT, font=f_palier, anchor="mm")

    # Texto vertical: PASILLO en (2.68, 3.25)
    pasillo_img = Image.new("RGBA", (200, 50), (255, 255, 255, 0))
    p_draw = ImageDraw.Draw(pasillo_img)
    p_draw.text((100, 25), "PASILLO", fill=(108, 117, 125), font=load_font(15, bold=True), anchor="mm")
    pasillo_rot = pasillo_img.rotate(90, expand=True)
    px_pas, py_pas = px(2.68, 3.25)
    img.paste(pasillo_rot, (px_pas - pasillo_rot.width // 2, py_pas - pasillo_rot.height // 2), pasillo_rot)

    # Cota superior: 6.30 m
    draw.text(px(3.15, -0.22), "6.30 m", fill=SUB_COLOR, font=f_dim, anchor="mm")

    # Cota izquierda vertical: 7.00 m
    dim_v_img = Image.new("RGBA", (200, 50), (255, 255, 255, 0))
    dv_draw = ImageDraw.Draw(dim_v_img)
    dv_draw.text((100, 25), "7.00 m", fill=SUB_COLOR, font=f_dim, anchor="mm")
    dim_v_rot = dim_v_img.rotate(90, expand=True)
    px_dv, py_dv = px(-0.24, 3.50)
    img.paste(dim_v_rot, (px_dv - dim_v_rot.width // 2, py_dv - dim_v_rot.height // 2), dim_v_rot)

    output_path = "plano_arquitectonico_2d.png"
    img.save(output_path, "PNG", optimize=True)
    print(f"Plano 2D exacto generado exitosamente en: {output_path} ({W}x{H} px)")


if __name__ == "__main__":
    main()
