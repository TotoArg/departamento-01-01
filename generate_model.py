"""
Generador paramétrico de Departamento_01-01.obj y Departamento_01-01.mtl
Respeta estrictamente las reglas geométricas y de circulación especificadas:
1. Perímetro exterior: Rectángulo cerrado de 7.00 m (X: 0.00 a 7.00) × 6.20 m (Y/Z: 0.00 a 6.20).
   Pared inferior (Y = 6.20) continua de punta a punta con Puerta de Entrada en X = 5.40 a 6.20.
2. Ejes verticales:
   - X = 1.70: Cerramiento de Placard 1, Baño y Placard 2 (Y = 2.30 a 4.60) con puerta de Baño entre Y = 3.10 y 3.70.
   - X = 3.00: Muro central de Y = 0.00 a 3.90, paso abierto de 0.70 m (Y = 3.90 a 4.60) y muro Cuarto/Cocina (Y = 4.60 a 6.20).
   - X = 4.60: Muro derecho de la Cocina (Y = 4.60 a 6.20).
3. Ejes horizontales:
   - Y = 0.00: Muro exterior superior continuo (X = 0.00 a 7.00).
   - Y = 2.30: Muro Estudio/Placard 1 (X = 0.00 a 1.70) y vano de entrada al Estudio (X = 1.70 a 3.00).
   - Y = 2.80: Muro Placard 1 / Baño (X = 0.00 a 1.70).
   - Y = 4.00: Muro Baño / Placard 2 (X = 0.00 a 1.70).
   - Y = 4.60: Línea unificada de Placard 2 (0.00 a 1.70), entrada Cuarto (1.70 a 3.00) y frente Cocina (3.00 a 4.60).
   - Y = 6.20: Muro exterior inferior continuo (0.00 a 7.00) con Entrada en X = 5.40 a 6.20.
"""

import math

def generate_obj_mtl():
    obj_lines = []
    mtl_lines = []

    obj_lines.append("# Plano 3D Exacto (7.00m x 6.20m)")
    obj_lines.append("mtllib Departamento_01-01.mtl\n")

    materials = {
        "Piso": (0.95, 0.96, 0.98),
        "Muro_Exterior": (0.88, 0.91, 0.94),
        "Muro_Interior": (0.78, 0.83, 0.88),
        "Mueble_Madera": (0.70, 0.42, 0.22),
        "Mueble_Tapizado": (0.20, 0.30, 0.45),
        "Sanitario": (0.98, 0.98, 1.00),
    }

    for name, (r, g, b) in materials.items():
        mtl_lines.append(f"newmtl {name}")
        mtl_lines.append(f"Kd {r:.3f} {g:.3f} {b:.3f}")
        mtl_lines.append("Ka 0.200 0.200 0.200")
        mtl_lines.append("Ks 0.100 0.100 0.100")
        mtl_lines.append("Ns 30.0\n")

    v_count = 0

    def add_box(name, x1, z1, y1, sx, sz, sy, mat):
        nonlocal v_count
        obj_lines.append(f"o {name}")
        obj_lines.append(f"usemtl {mat}")
        corners = [
            (x1, y1, z1),
            (x1 + sx, y1, z1),
            (x1 + sx, y1, z1 + sz),
            (x1, y1, z1 + sz),
            (x1, y1 + sy, z1),
            (x1 + sx, y1 + sy, z1),
            (x1 + sx, y1 + sy, z1 + sz),
            (x1, y1 + sy, z1 + sz),
        ]
        for vx, vy, vz in corners:
            obj_lines.append(f"v {vx:.3f} {vy:.3f} {vz:.3f}")
        b = v_count
        obj_lines.append(f"f {b+1} {b+2} {b+3} {b+4}")
        obj_lines.append(f"f {b+5} {b+8} {b+7} {b+6}")
        obj_lines.append(f"f {b+1} {b+5} {b+6} {b+2}")
        obj_lines.append(f"f {b+2} {b+6} {b+7} {b+3}")
        obj_lines.append(f"f {b+3} {b+7} {b+8} {b+4}")
        obj_lines.append(f"f {b+4} {b+8} {b+5} {b+1}\n")
        v_count += 8

    H = 2.60
    EXT = 0.14
    INT = 0.10

    # 1. Piso continuo (7.00 x 6.20)
    add_box("Piso_General_7x62", 0.00, 0.00, -0.08, 7.00, 6.20, 0.08, "Piso")

    # 2. Perímetro exterior
    add_box("Muro_Ext_Superior_Y0", 0.00, -EXT/2, 0.00, 7.00, EXT, H, "Muro_Exterior")
    add_box("Muro_Ext_Izquierdo_X0", -EXT/2, 0.00, 0.00, EXT, 6.20, H, "Muro_Exterior")
    add_box("Muro_Ext_Derecho_X7", 7.00 - EXT/2, 0.00, 0.00, EXT, 6.20, H, "Muro_Exterior")
    add_box("Muro_Ext_Inferior_Izq_Y620", 0.00, 6.20 - EXT/2, 0.00, 5.40, EXT, H, "Muro_Exterior")
    add_box("Muro_Ext_Inferior_Der_Y620", 6.20, 6.20 - EXT/2, 0.00, 0.80, EXT, H, "Muro_Exterior")

    # 3. Ejes verticales internos
    # X = 1.70 (Y = 2.30 a 4.60, con vano Baño entre 3.10 y 3.70)
    add_box("Muro_V_X170_Sup", 1.70 - INT/2, 2.30, 0.00, INT, 0.80, H, "Muro_Interior")
    add_box("Muro_V_X170_Inf", 1.70 - INT/2, 3.70, 0.00, INT, 0.90, H, "Muro_Interior")

    # X = 3.00 (Y = 0.00 a 3.90, paso abierto 3.90 a 4.60, y muro Y = 4.60 a 6.20)
    add_box("Muro_V_X300_Living_Estudio_Pasillo", 3.00 - INT/2, 0.00, 0.00, INT, 3.90, H, "Muro_Interior")
    add_box("Muro_V_X300_Cuarto_Cocina", 3.00 - INT/2, 4.60, 0.00, INT, 1.60, H, "Muro_Interior")

    # X = 4.60 (Y = 4.60 a 6.20: pared derecha de la Cocina)
    add_box("Muro_V_X460_Cocina_Living", 4.60 - INT/2, 4.60, 0.00, INT, 1.60, H, "Muro_Interior")

    # 4. Líneas horizontales internas
    # Y = 2.30 (X = 0.00 a 1.70 cerrado + mochetas de entrada a Estudio en 1.70..1.90 y 2.80..3.00)
    add_box("Muro_H_Y230_Estudio_Placard1", 0.00, 2.30 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")
    add_box("Muro_H_Y230_Mocheta_Izq", 1.70, 2.30 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    add_box("Muro_H_Y230_Mocheta_Der", 2.80, 2.30 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")

    # Y = 2.80 (X = 0.00 a 1.70: Placard 1 / Baño)
    add_box("Muro_H_Y280_Placard1_Bano", 0.00, 2.80 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")

    # Y = 4.00 (X = 0.00 a 1.70: Baño / Placard 2)
    add_box("Muro_H_Y400_Bano_Placard2", 0.00, 4.00 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")

    # Y = 4.60 (Línea unificada: Placard 2 [0..1.70], vano Cuarto [1.70..3.00], frente Cocina [3.00..4.60])
    add_box("Muro_H_Y460_Placard2_Cuarto", 0.00, 4.60 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")
    add_box("Muro_H_Y460_Cuarto_Mocheta_Izq", 1.70, 4.60 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    add_box("Muro_H_Y460_Cuarto_Mocheta_Der", 2.80, 4.60 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    add_box("Muro_H_Y460_Cocina_Mocheta_Izq", 3.00, 4.60 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    add_box("Muro_H_Y460_Cocina_Mocheta_Der", 4.35, 4.60 - INT/2, 0.00, 0.25, INT, H, "Muro_Interior")

    with open("Departamento_01-01.obj", "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))

    with open("Departamento_01-01.mtl", "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))

    print("Departamento_01-01.obj y .mtl generados con geometría exacta 7.00m x 6.20m.")

if __name__ == "__main__":
    generate_obj_mtl()
