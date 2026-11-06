import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_2d_plan(output_path="plano_arquitectonico_2d.png"):
    # Escala: 1 metro = 140 píxeles
    scale = 140
    margin_x = 140
    margin_y = 140

    W_m = 7.00
    H_m = 6.20

    img_w = int(W_m * scale + margin_x * 2)
    img_h = int(H_m * scale + margin_y * 2)

    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    def to_px(x_m, y_m):
        return (int(round(margin_x + x_m * scale)), int(round(margin_y + y_m * scale)))

    def draw_wall(x1, y1, x2, y2, width_px=6, color="black"):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        draw.line([p1, p2], fill=color, width=width_px)

    def draw_dashed_opening(x1, y1, x2, y2, dash_len_m=0.06, gap_len_m=0.05, width_px=2, color="#777777"):
        dist = np.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        dx = (x2 - x1) / dist
        dy = (y2 - y1) / dist
        curr = 0.0
        while curr < dist:
            end_d = min(curr + dash_len_m, dist)
            p1 = to_px(x1 + dx * curr, y1 + dy * curr)
            p2 = to_px(x1 + dx * end_d, y1 + dy * end_d)
            draw.line([p1, p2], fill=color, width=width_px)
            curr += dash_len_m + gap_len_m

    # Espesores visuales en px
    EXT_W = 8
    INT_W = 5

    # ---------------------------------------------------------
    # 1. PERÍMETRO EXTERIOR (Rectángulo simple 7.00 m x 6.20 m)
    # ---------------------------------------------------------
    # Muro superior continuo (Y = 0.00, X = 0.00 a 7.00)
    draw_wall(0.00, 0.00, 7.00, 0.00, EXT_W)
    # Muro izquierdo continuo (X = 0.00, Y = 0.00 a 6.20)
    draw_wall(0.00, 0.00, 0.00, 6.20, EXT_W)
    # Muro derecho continuo (X = 7.00, Y = 0.00 a 6.20)
    draw_wall(7.00, 0.00, 7.00, 6.20, EXT_W)
    # Muro inferior continuo (Y = 6.20, X = 0.00 a 7.00) con vano de Entrada entre X = 5.40 y X = 6.20
    draw_wall(0.00, 6.20, 5.40, 6.20, EXT_W)
    draw_wall(6.20, 6.20, 7.00, 6.20, EXT_W)

    # Vano de Puerta de Entrada en Y = 6.20 (X = 5.40 a 6.20)
    # Líneas de jamba / umbral
    draw_wall(5.40, 6.10, 5.40, 6.30, 3)
    draw_wall(6.20, 6.10, 6.20, 6.30, 3)
    draw_wall(5.40, 6.20, 6.20, 6.20, 2, color="#aaaaaa")

    # ---------------------------------------------------------
    # 2. EJES VERTICALES INTERNOS
    # ---------------------------------------------------------
    # X = 1.70: Cerramiento de Placard 1, Baño y Placard 2 (Y = 2.30 a Y = 4.60)
    # Puerta del Baño en el centro: entre Y = 3.10 y Y = 3.70
    draw_wall(1.70, 2.30, 1.70, 3.10, INT_W)
    draw_wall(1.70, 3.70, 1.70, 4.60, INT_W)

    # X = 3.00: Eje central divisorio
    # Separa Estudio y Pasillo del Living: desde Y = 0.00 hasta Y = 3.90
    draw_wall(3.00, 0.00, 3.00, 3.90, INT_W)
    # Pequeña mocheta de remate en Y = 3.90
    draw_wall(2.92, 3.90, 3.08, 3.90, 4)
    # Paso abierto entre Living y Pasillo: de Y = 3.90 a Y = 4.60 (0.70 m)
    draw_dashed_opening(3.00, 3.90, 3.00, 4.60)
    # Separa Cuarto de Cocina: desde Y = 4.60 hasta Y = 6.20
    draw_wall(3.00, 4.60, 3.00, 6.20, INT_W)

    # X = 4.60: Pared derecha de la Cocina (desde Y = 4.60 hasta Y = 6.20)
    draw_wall(4.60, 4.60, 4.60, 6.20, INT_W)

    # ---------------------------------------------------------
    # 3. LÍNEAS HORIZONTALES Y ALINEACIONES CRÍTICAS
    # ---------------------------------------------------------
    # Y = 2.30: Línea de cierre del Estudio
    # De X = 0.00 a X = 1.70: Muro cerrado que divide el Estudio del Placard 1
    draw_wall(0.00, 2.30, 1.70, 2.30, INT_W)
    # De X = 1.70 a X = 3.00: Vano/puerta de entrada al Estudio (remate superior del Pasillo)
    draw_wall(1.70, 2.30, 1.90, 2.30, INT_W)
    draw_dashed_opening(1.90, 2.30, 2.80, 2.30)
    draw_wall(2.80, 2.30, 3.00, 2.30, INT_W)

    # Y = 2.80: Muro horizontal que divide el Placard 1 del Baño (de X = 0.00 a X = 1.70)
    draw_wall(0.00, 2.80, 1.70, 2.80, INT_W)

    # Y = 4.00: Muro horizontal que divide el Baño del Placard 2 (de X = 0.00 a X = 1.70)
    draw_wall(0.00, 4.00, 1.70, 4.00, INT_W)

    # Y = 4.60: Línea horizontal unificada de Cuarto y Cocina (Regla crítica)
    # 1) Muro inferior del Placard 2 (de X = 0.00 a X = 1.70)
    draw_wall(0.00, 4.60, 1.70, 4.60, INT_W)
    # 2) Vano/puerta de entrada al Cuarto (de X = 1.70 a X = 3.00)
    draw_wall(1.70, 4.60, 1.90, 4.60, INT_W)
    draw_dashed_opening(1.90, 4.60, 2.80, 4.60)
    draw_wall(2.80, 4.60, 3.00, 4.60, INT_W)
    # 3) Frente superior de la Cocina con su abertura de acceso (de X = 3.00 a X = 4.60)
    draw_wall(3.00, 4.60, 3.20, 4.60, INT_W)
    draw_dashed_opening(3.20, 4.60, 4.35, 4.60)
    draw_wall(4.35, 4.60, 4.60, 4.60, INT_W)

    # ---------------------------------------------------------
    # 4. ETIQUETAS Y COTAS
    # ---------------------------------------------------------
    try:
        font_main = ImageFont.truetype("arialbd.ttf", 22)
        font_med = ImageFont.truetype("arialbd.ttf", 18)
        font_sm = ImageFont.truetype("arialbd.ttf", 14)
        font_dim = ImageFont.truetype("arial.ttf", 18)
    except:
        font_main = ImageFont.load_default()
        font_med = font_main
        font_sm = font_main
        font_dim = font_main

    def draw_centered_text(x_m, y_m, text, font, color="#222222"):
        px, py = to_px(x_m, y_m)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((px - tw / 2, py - th / 2), text, fill=color, font=font)

    # Textos de ambientes
    draw_centered_text(1.50, 1.15, "ESTUDIO", font_main)
    draw_centered_text(0.85, 2.55, "PLACARD", font_sm)
    draw_centered_text(0.85, 3.40, "BAÑO", font_med)
    draw_centered_text(0.85, 4.30, "PLACARD", font_sm)
    draw_centered_text(1.50, 5.40, "CUARTO", font_main)
    draw_centered_text(3.80, 5.45, "COCINA", font_med)
    draw_centered_text(5.00, 2.35, "LIVING", font_main)
    draw_centered_text(5.80, 6.50, "ENTRADA", font_sm)

    # Texto vertical PASILLO
    pasillo_img = Image.new("RGBA", (160, 40), (255, 255, 255, 0))
    p_draw = ImageDraw.Draw(pasillo_img)
    bbox = p_draw.textbbox((0, 0), "PASILLO", font=font_sm)
    p_draw.text((80 - (bbox[2]-bbox[0])/2, 20 - (bbox[3]-bbox[1])/2), "PASILLO", fill="#222222", font=font_sm)
    pasillo_rot = pasillo_img.rotate(90, expand=True)
    px_pas, py_pas = to_px(2.35, 3.45)
    img.paste(pasillo_rot, (int(px_pas - pasillo_rot.width / 2), int(py_pas - pasillo_rot.height / 2)), pasillo_rot)

    # Cotas exteriores
    draw_centered_text(3.50, -0.30, "7.00 m", font_dim, "#444444")

    dim_v_img = Image.new("RGBA", (140, 40), (255, 255, 255, 0))
    dv_draw = ImageDraw.Draw(dim_v_img)
    bbox = dv_draw.textbbox((0, 0), "6.20 m", font=font_dim)
    dv_draw.text((70 - (bbox[2]-bbox[0])/2, 20 - (bbox[3]-bbox[1])/2), "6.20 m", fill="#444444", font=font_dim)
    dim_v_rot = dim_v_img.rotate(90, expand=True)
    px_dv, py_dv = to_px(-0.30, 3.10)
    img.paste(dim_v_rot, (int(px_dv - dim_v_rot.width / 2), int(py_dv - dim_v_rot.height / 2)), dim_v_rot)

    img.save(output_path)
    print(f"Plano 2D guardado en {output_path}")

if __name__ == "__main__":
    generate_2d_plan()
