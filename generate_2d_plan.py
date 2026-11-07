from PIL import Image, ImageDraw, ImageFont
import math

def generate_2d_plan(output_path="plano_arquitectonico_2d.png"):
    # Escala alta definición: 1 metro = 200 píxeles
    scale = 200
    margin_x = 160
    margin_y = 150

    W_m = 6.30
    H_m = 6.20

    img_w = int(round(W_m * scale + margin_x * 2))
    img_h = int(round(H_m * scale + margin_y * 2))

    img = Image.new("RGB", (img_w, img_h), "#ffffff")
    draw = ImageDraw.Draw(img)

    def to_px(x_m, y_m):
        return (int(round(margin_x + x_m * scale)), int(round(margin_y + y_m * scale)))

    def draw_wall(x1, y1, x2, y2, width_px=8, color="#212529"):
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        draw.line([p1, p2], fill=color, width=width_px)

    def draw_dashed(x1, y1, x2, y2, dash_m=0.06, gap_m=0.06, width_px=2, color="#94a3b8"):
        dist = math.hypot(x2 - x1, y2 - y1)
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

    # =========================================================================
    # 1. PERÍMETRO EXTERIOR (6.30 m x 6.20 m)
    # =========================================================================
    # Superior (Y = 0.00): [0.00, 0.00] a [6.30, 0.00]
    draw_wall(0.00, 0.00, 6.30, 0.00, EXT_W)
    # Izquierdo (X = 0.00): [0.00, 0.00] a [0.00, 6.20]
    draw_wall(0.00, 0.00, 0.00, 6.20, EXT_W)
    # Derecho (X = 6.30): [6.30, 0.00] a [6.30, 6.20]
    draw_wall(6.30, 0.00, 6.30, 6.20, EXT_W)
    # Inferior (Y = 6.20): [0.00, 6.20] a [6.30, 6.20] con vano de entrada entre 5.20 y 6.10
    draw_wall(0.00, 6.20, 5.20, 6.20, EXT_W)
    draw_wall(6.10, 6.20, 6.30, 6.20, EXT_W)

    # Detalle vano puerta principal en base Y = 6.20 (X=5.20 a 6.10, vano de 0.90m)
    draw_wall(5.20, 6.08, 5.20, 6.32, 4, "#212529")
    draw_wall(6.10, 6.08, 6.10, 6.32, 4, "#212529")
    draw_wall(5.20, 6.20, 6.10, 6.20, 2, "#cbd5e1")

    # =========================================================================
    # 2. DIVISIONES HORIZONTALES SECTOR IZQUIERDO (X = 0.00 a 1.70)
    # =========================================================================
    # Y = 2.00: Muro cerrado que divide Estudio de Placard 1
    draw_wall(0.00, 2.00, 1.70, 2.00, INT_W)
    # Y = 2.50: Muro cerrado que divide Placard 1 de Baño
    draw_wall(0.00, 2.50, 1.70, 2.50, INT_W)
    # Y = 3.70: Muro cerrado que divide Baño de Placard 2
    draw_wall(0.00, 3.70, 1.70, 3.70, INT_W)
    # Y = 4.20: Muro cerrado que divide Placard 2 de Cuarto
    draw_wall(0.00, 4.20, 1.70, 4.20, INT_W)

    # =========================================================================
    # 3. MURO IZQUIERDO DEL PASILLO (X = 1.70) Y PUERTA DEL BAÑO
    # =========================================================================
    # X = 1.70: de Y = 2.00 a 2.80 (muro)
    draw_wall(1.70, 2.00, 1.70, 2.80, INT_W)
    # Vano puerta del Baño: de Y = 2.80 a 3.40 (abertura hacia el pasillo)
    draw_dashed(1.70, 2.80, 1.70, 3.40)
    # X = 1.70: de Y = 3.40 a 4.20 (muro)
    draw_wall(1.70, 3.40, 1.70, 4.20, INT_W)

    # =========================================================================
    # 4. ENTRADA AL ESTUDIO (Y = 2.00, remate superior del Pasillo)
    # =========================================================================
    # Muros extremos del vano:
    draw_wall(1.70, 2.00, 1.90, 2.00, INT_W)
    # Vano entre X = 1.90 y X = 2.80
    draw_dashed(1.90, 2.00, 2.80, 2.00)
    draw_wall(2.80, 2.00, 3.00, 2.00, INT_W)

    # =========================================================================
    # 5. EJE CENTRAL VERTICAL (X = 3.00)
    # =========================================================================
    # Muro divisorio Living con Estudio y Pasillo: de Y = 0.00 a Y = 3.50
    draw_wall(3.00, 0.00, 3.00, 3.50, INT_W)
    draw_wall(2.91, 3.50, 3.09, 3.50, 4, "#212529") # remate de mocheta
    # Paso totalmente abierto de 0.70 m entre Living y Pasillo: de Y = 3.50 a Y = 4.20
    draw_dashed(3.00, 3.50, 3.00, 4.20)
    # Muro divisorio entre Cuarto y Cocina: de Y = 4.20 a Y = 6.20
    draw_wall(3.00, 4.20, 3.00, 6.20, INT_W)

    # =========================================================================
    # 6. LÍNEA HORIZONTAL UNIFICADA CRÍTICA (Y = 4.20)
    # =========================================================================
    # Entrada Cuarto (entre Pasillo y Cuarto):
    draw_wall(1.70, 4.20, 1.90, 4.20, INT_W)
    draw_dashed(1.90, 4.20, 2.80, 4.20)
    draw_wall(2.80, 4.20, 3.00, 4.20, INT_W)

    # Frente Cocina (de X = 3.00 a X = 5.00 en Y = 4.20):
    # Vano/abertura amplia entre X = 3.25 y X = 4.65
    draw_wall(3.00, 4.20, 3.25, 4.20, INT_W)
    draw_dashed(3.25, 4.20, 4.65, 4.20)
    draw_wall(4.65, 4.20, 5.00, 4.20, INT_W)

    # =========================================================================
    # 7. COCINA SECTOR DERECHO (X = 5.00)
    # =========================================================================
    # Muro divisorio entre Cocina y Sector Entrada: de Y = 4.20 a Y = 6.20
    draw_wall(5.00, 4.20, 5.00, 6.20, INT_W)

    # =========================================================================
    # 8. ETIQUETAS TIPOGRÁFICAS ARQUITECTÓNICAS
    # =========================================================================
    try:
        font_lg = ImageFont.truetype("consolab.ttf", 30)
        font_md = ImageFont.truetype("consolab.ttf", 24)
        font_sm = ImageFont.truetype("consolab.ttf", 18)
        font_dim = ImageFont.truetype("consola.ttf", 22)
    except:
        try:
            font_lg = ImageFont.truetype("arialbd.ttf", 28)
            font_md = ImageFont.truetype("arialbd.ttf", 22)
            font_sm = ImageFont.truetype("arialbd.ttf", 16)
            font_dim = ImageFont.truetype("arial.ttf", 20)
        except:
            font_lg = ImageFont.load_default()
            font_md = font_lg
            font_sm = font_lg
            font_dim = font_lg

    def draw_centered_text(x_m, y_m, text, font, color="#1e293b"):
        px, py = to_px(x_m, y_m)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((px - tw / 2, py - th / 2), text, fill=color, font=font)

    # Ambientes principales centrados en sus cajas
    # Estudio: [0.00, 0.00] a [3.00, 2.00] (centro 1.50, 1.00)
    draw_centered_text(1.50, 1.00, "ESTUDIO", font_md)

    # Placard 1: [0.00, 2.00] a [1.70, 2.50] (centro 0.85, 2.25)
    draw_centered_text(0.85, 2.25, "PLACARD", font_sm)

    # Baño: [0.00, 2.50] a [1.70, 3.70] (centro 0.85, 3.10)
    draw_centered_text(0.85, 3.10, "BAÑO", font_md)

    # Placard 2: [0.00, 3.70] a [1.70, 4.20] (centro 0.85, 3.95)
    draw_centered_text(0.85, 3.95, "PLACARD", font_sm)

    # Cuarto: [0.00, 4.20] a [3.00, 6.20] (centro 1.50, 5.20)
    draw_centered_text(1.50, 5.20, "CUARTO", font_md)

    # Cocina: [3.00, 4.20] a [5.00, 6.20] (centro 4.00, 5.20)
    draw_centered_text(4.00, 5.20, "COCINA", font_md)

    # Living: [3.00, 0.00] a [6.30, 4.20] (centro 4.65, 2.10)
    draw_centered_text(4.65, 2.10, "LIVING", font_lg)

    # Entrada: X = 5.20 a 6.10 en Y = 6.20
    draw_centered_text(5.65, 6.55, "ENTRADA", font_sm)

    # Pasillo vertical: [1.70, 2.00] a [3.00, 4.20] (centro 2.35, 3.10)
    pasillo_img = Image.new("RGBA", (200, 48), (255, 255, 255, 0))
    p_draw = ImageDraw.Draw(pasillo_img)
    bbox = p_draw.textbbox((0, 0), "PASILLO", font=font_sm)
    p_draw.text((100 - (bbox[2]-bbox[0])/2, 24 - (bbox[3]-bbox[1])/2), "PASILLO", fill="#1e293b", font=font_sm)
    pasillo_rot = pasillo_img.rotate(90, expand=True)
    px_pas, py_pas = to_px(2.35, 3.10)
    img.paste(pasillo_rot, (int(px_pas - pasillo_rot.width / 2), int(py_pas - pasillo_rot.height / 2)), pasillo_rot)

    # =========================================================================
    # 9. COTAS GENERALES EXTERIORES
    # =========================================================================
    # Cota Horizontal Superior: 6.30 m
    draw_centered_text(3.15, -0.28, "6.30 m", font_dim, "#475569")
    draw_dashed(0.00, -0.15, 6.30, -0.15, dash_m=0.1, gap_m=0.05, width_px=1, color="#94a3b8")

    # Cota Vertical Izquierda: 6.20 m
    dim_v_img = Image.new("RGBA", (180, 48), (255, 255, 255, 0))
    dv_draw = ImageDraw.Draw(dim_v_img)
    bbox = dv_draw.textbbox((0, 0), "6.20 m", font=font_dim)
    dv_draw.text((90 - (bbox[2]-bbox[0])/2, 24 - (bbox[3]-bbox[1])/2), "6.20 m", fill="#475569", font=font_dim)
    dim_v_rot = dim_v_img.rotate(90, expand=True)
    px_dv, py_dv = to_px(-0.28, 3.10)
    img.paste(dim_v_rot, (int(px_dv - dim_v_rot.width / 2), int(py_dv - dim_v_rot.height / 2)), dim_v_rot)

    img.save(output_path)
    print(f"Plano 2D exacto guardado exitosamente en: {output_path}")

if __name__ == "__main__":
    generate_2d_plan()
