import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_2d_plan(output_path="plano_arquitectonico_2d.png"):
    # Escala alta resolución: 1 metro = 160 píxeles
    scale = 160
    margin_x = 150
    margin_y = 140

    W_m = 7.00
    H_m = 6.20

    img_w = int(W_m * scale + margin_x * 2)
    img_h = int(H_m * scale + margin_y * 2)

    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)

    def to_px(x_m, y_m):
        return (int(round(margin_x + x_m * scale)), int(round(margin_y + y_m * scale)))

    def draw_wall(x1, y1, x2, y2, width_px=7, color="#1a1a1a"):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        draw.line([p1, p2], fill=color, width=width_px)

    def draw_dashed(x1, y1, x2, y2, dash_m=0.055, gap_m=0.055, width_px=2, color="#888888"):
        dist = np.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        dx = (x2 - x1) / dist
        dy = (y2 - y1) / dist
        curr = 0.0
        while curr < dist:
            end_d = min(curr + dash_m, dist)
            p1 = to_px(x1 + dx * curr, y1 + dy * curr)
            p2 = to_px(x1 + dx * end_d, y1 + dy * end_d)
            draw.line([p1, p2], fill=color, width=width_px)
            curr += dash_m + gap_m

    EXT_W = 10
    INT_W = 6

    # ---------------------------------------------------------
    # 1. PERÍMETRO EXTERIOR (Rectángulo simple 7.00 m x 6.20 m)
    # ---------------------------------------------------------
    # Y = 0.00: Muro exterior superior continuo (0.00 a 7.00)
    draw_wall(0.00, 0.00, 7.00, 0.00, EXT_W)
    # X = 0.00: Muro exterior izquierdo continuo (0.00 a 6.20)
    draw_wall(0.00, 0.00, 0.00, 6.20, EXT_W)
    # X = 7.00: Muro exterior derecho continuo (0.00 a 6.20)
    draw_wall(7.00, 0.00, 7.00, 6.20, EXT_W)
    # Y = 6.20: Muro exterior inferior continuo (0.00 a 7.00) con vano de Entrada (5.40 a 6.20)
    draw_wall(0.00, 6.20, 5.40, 6.20, EXT_W)
    draw_wall(6.20, 6.20, 7.00, 6.20, EXT_W)

    # Vano de Puerta de Entrada en Y = 6.20 (entre X = 5.40 y X = 6.20)
    draw_wall(5.40, 6.06, 5.40, 6.32, 4)
    draw_wall(6.20, 6.06, 6.20, 6.32, 4)
    draw_wall(5.40, 6.20, 6.20, 6.20, 2, color="#b0b0b0")

    # ---------------------------------------------------------
    # 2. EJES VERTICALES PRINCIPALES
    # ---------------------------------------------------------
    # X = 1.70: Cerramiento de Baño y Placards (Y = 2.30 a Y = 4.60)
    # Puerta de acceso al Baño en el centro (entre Y = 3.10 y Y = 3.70)
    draw_wall(1.70, 2.30, 1.70, 3.10, INT_W)
    draw_wall(1.70, 3.70, 1.70, 4.60, INT_W)

    # X = 3.00: Eje central divisorio
    # Separa Estudio y Pasillo del Living (desde Y = 0.00 hasta Y = 3.90)
    draw_wall(3.00, 0.00, 3.00, 3.90, INT_W)
    draw_wall(2.91, 3.90, 3.09, 3.90, 5)
    # Paso totalmente abierto de 0.70 m en X = 3.00 (entre Y = 3.90 y Y = 4.60)
    draw_dashed(3.00, 3.90, 3.00, 4.60)
    # Separa el Cuarto de la Cocina (desde Y = 4.60 hasta Y = 6.20)
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
    draw_wall(1.70, 2.30, 1.86, 2.30, INT_W)
    draw_dashed(1.86, 2.30, 2.82, 2.30)
    draw_wall(2.82, 2.30, 3.00, 2.30, INT_W)

    # Y = 2.80: Muro horizontal que divide el Placard 1 del Baño (de X = 0.00 a X = 1.70)
    draw_wall(0.00, 2.80, 1.70, 2.80, INT_W)

    # Y = 4.00: Muro horizontal que divide el Baño del Placard 2 (de X = 0.00 a X = 1.70)
    draw_wall(0.00, 4.00, 1.70, 4.00, INT_W)

    # Y = 4.60: Línea horizontal unificada de Cuarto y Cocina (Regla crítica)
    # 1) Muro inferior del Placard 2 (de X = 0.00 a X = 1.70)
    draw_wall(0.00, 4.60, 1.70, 4.60, INT_W)
    # 2) Vano/puerta de entrada al Cuarto (de X = 1.70 a X = 3.00)
    draw_wall(1.70, 4.60, 1.86, 4.60, INT_W)
    draw_dashed(1.86, 4.60, 2.82, 4.60)
    draw_wall(2.82, 4.60, 3.00, 4.60, INT_W)
    # 3) Frente superior de la Cocina con su abertura de acceso (de X = 3.00 a X = 4.60)
    draw_wall(3.00, 4.60, 3.18, 4.60, INT_W)
    draw_dashed(3.18, 4.60, 4.38, 4.60)
    draw_wall(4.38, 4.60, 4.60, 4.60, INT_W)

    # ---------------------------------------------------------
    # 4. ETIQUETAS Y COTAS
    # ---------------------------------------------------------
    try:
        font_lg = ImageFont.truetype("consolab.ttf", 26)
        font_md = ImageFont.truetype("consolab.ttf", 22)
        font_sm = ImageFont.truetype("consolab.ttf", 17)
        font_dim = ImageFont.truetype("consola.ttf", 20)
    except:
        try:
            font_lg = ImageFont.truetype("arialbd.ttf", 24)
            font_md = ImageFont.truetype("arialbd.ttf", 20)
            font_sm = ImageFont.truetype("arialbd.ttf", 15)
            font_dim = ImageFont.truetype("arial.ttf", 18)
        except:
            font_lg = ImageFont.load_default()
            font_md = font_lg
            font_sm = font_lg
            font_dim = font_lg

    def draw_centered_text(x_m, y_m, text, font, color="#222222"):
        px, py = to_px(x_m, y_m)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((px - tw / 2, py - th / 2), text, fill=color, font=font)

    draw_centered_text(1.50, 1.15, "ESTUDIO", font_md)
    draw_centered_text(0.85, 2.55, "PLACARD", font_sm)
    draw_centered_text(0.85, 3.40, "BAÑO", font_md)
    draw_centered_text(0.85, 4.30, "PLACARD", font_sm)
    draw_centered_text(1.50, 5.40, "CUARTO", font_md)
    draw_centered_text(3.80, 5.45, "COCINA", font_md)
    draw_centered_text(5.00, 2.35, "LIVING", font_lg)
    draw_centered_text(5.80, 6.52, "ENTRADA", font_sm)

    # PASILLO vertical
    pasillo_img = Image.new("RGBA", (180, 44), (255, 255, 255, 0))
    p_draw = ImageDraw.Draw(pasillo_img)
    bbox = p_draw.textbbox((0, 0), "PASILLO", font=font_sm)
    p_draw.text((90 - (bbox[2]-bbox[0])/2, 22 - (bbox[3]-bbox[1])/2), "PASILLO", fill="#222222", font=font_sm)
    pasillo_rot = pasillo_img.rotate(90, expand=True)
    px_pas, py_pas = to_px(2.35, 3.45)
    img.paste(pasillo_rot, (int(px_pas - pasillo_rot.width / 2), int(py_pas - pasillo_rot.height / 2)), pasillo_rot)

    # Cotas exteriores
    draw_centered_text(3.50, -0.25, "7.00 m", font_dim, "#444444")

    dim_v_img = Image.new("RGBA", (160, 44), (255, 255, 255, 0))
    dv_draw = ImageDraw.Draw(dim_v_img)
    bbox = dv_draw.textbbox((0, 0), "6.20 m", font=font_dim)
    dv_draw.text((80 - (bbox[2]-bbox[0])/2, 22 - (bbox[3]-bbox[1])/2), "6.20 m", fill="#444444", font=font_dim)
    dim_v_rot = dim_v_img.rotate(90, expand=True)
    px_dv, py_dv = to_px(-0.25, 3.10)
    img.paste(dim_v_rot, (int(px_dv - dim_v_rot.width / 2), int(py_dv - dim_v_rot.height / 2)), dim_v_rot)

    img.save(output_path)
    print(f"Plano 2D guardado en {output_path}")

if __name__ == "__main__":
    generate_2d_plan()
