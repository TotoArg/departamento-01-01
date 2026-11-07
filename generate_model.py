"""
Generador paramétrico de Departamento_01-01.obj y Departamento_01-01.mtl
Respeta estrictamente las reglas geométricas y de circulación especificadas:
1. Perímetro exterior: Rectángulo cerrado de 6.30 m (X: 0.00 a 6.30) × 6.20 m (Y/Z: 0.00 a 6.20).
   Pared inferior (Y = 6.20) continua de punta a punta con Puerta de Entrada en X = 5.20 a 6.10 (vano de 0.90 m).
2. Distribución de ambientes:
   - ESTUDIO: [0.00, 0.00] a [3.00, 2.00] (3.00 x 2.00)
   - CUARTO: [0.00, 4.20] a [3.00, 6.20] (3.00 x 2.00, simétrico al Estudio)
   - BLOQUE IZQUIERDO:
     * PLACARD 1: [0.00, 2.00] a [1.70, 2.50] (1.70 x 0.50)
     * BAÑO: [0.00, 2.50] a [1.70, 3.70] (1.70 x 1.20) con puerta en X = 1.70 (Y = 2.80 a 3.40)
     * PLACARD 2: [0.00, 3.70] a [1.70, 4.20] (1.70 x 0.50)
   - PASILLO: [1.70, 2.00] a [3.00, 4.20] (1.30 x 2.20)
     * Puerta Estudio (Y = 2.00, X = 1.90 a 2.80)
     * Puerta Cuarto (Y = 4.20, X = 1.90 a 2.80)
     * Paso abierto con Living en X = 3.00 (Y = 3.50 a 4.20, 0.70 m)
   - COCINA: [3.00, 4.20] a [5.00, 6.20] (2.00 x 2.00)
     * Vano frente superior en Y = 4.20 (X = 3.25 a 4.65)
     * Muro derecho en X = 5.00 (Y = 4.20 a 6.20)
   - LIVING Y ENTRADA: [3.00, 0.00] a [6.30, 4.20] y continuación [5.00, 4.20] a [6.30, 6.20]
"""

import math

def generate_obj_mtl():
    obj_lines = []
    mtl_lines = []

    obj_lines.append("# Plano 3D Exacto (6.30m x 6.20m)")
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

    # 1. Piso continuo (6.30 x 6.20)
    add_box("Piso_General_63x62", 0.00, 0.00, -0.08, 6.30, 6.20, 0.08, "Piso")

    # 2. Perímetro exterior
    add_box("Muro_Ext_Superior_Y0", 0.00, -EXT/2, 0.00, 6.30, EXT, H, "Muro_Exterior")
    add_box("Muro_Ext_Izquierdo_X0", -EXT/2, 0.00, 0.00, EXT, 6.20, H, "Muro_Exterior")
    add_box("Muro_Ext_Derecho_X63", 6.30 - EXT/2, 0.00, 0.00, EXT, 6.20, H, "Muro_Exterior")
    add_box("Muro_Ext_Inferior_Izq_Y620", 0.00, 6.20 - EXT/2, 0.00, 5.20, EXT, H, "Muro_Exterior")
    add_box("Muro_Ext_Inferior_Der_Y620", 6.10, 6.20 - EXT/2, 0.00, 0.20, EXT, H, "Muro_Exterior")

    # 3. Ejes verticales internos
    # X = 1.70 (Y = 2.00 a 4.20, con vano Baño entre 2.80 y 3.40)
    add_box("Muro_V_X170_Sup", 1.70 - INT/2, 2.00, 0.00, INT, 0.80, H, "Muro_Interior")
    add_box("Muro_V_X170_Inf", 1.70 - INT/2, 3.40, 0.00, INT, 0.80, H, "Muro_Interior")

    # X = 3.00 (Y = 0.00 a 3.50, paso abierto 3.50 a 4.20, y muro Y = 4.20 a 6.20)
    add_box("Muro_V_X300_Living_Estudio_Pasillo", 3.00 - INT/2, 0.00, 0.00, INT, 3.50, H, "Muro_Interior")
    add_box("Muro_V_X300_Cuarto_Cocina", 3.00 - INT/2, 4.20, 0.00, INT, 2.00, H, "Muro_Interior")

    # X = 5.00 (Y = 4.20 a 6.20: pared derecha de la Cocina)
    add_box("Muro_V_X500_Cocina_Entrada", 5.00 - INT/2, 4.20, 0.00, INT, 2.00, H, "Muro_Interior")

    # 4. Líneas horizontales internas
    # Y = 2.00 (X = 0.00 a 1.70 cerrado + mochetas vano Estudio 1.70..1.90 y 2.80..3.00)
    add_box("Muro_H_Y200_Estudio_Placard1", 0.00, 2.00 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")
    add_box("Muro_H_Y200_Mocheta_Izq", 1.70, 2.00 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    add_box("Muro_H_Y200_Mocheta_Der", 2.80, 2.00 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")

    # Y = 2.50 (X = 0.00 a 1.70: Placard 1 / Baño)
    add_box("Muro_H_Y250_Placard1_Bano", 0.00, 2.50 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")

    # Y = 3.70 (X = 0.00 a 1.70: Baño / Placard 2)
    add_box("Muro_H_Y370_Bano_Placard2", 0.00, 3.70 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")

    # Y = 4.20 (Línea unificada):
    # Placard 2 / Cuarto (0.00 a 1.70)
    add_box("Muro_H_Y420_Placard2_Cuarto", 0.00, 4.20 - INT/2, 0.00, 1.70, INT, H, "Muro_Interior")
    # Entrada Cuarto mochetas (1.70..1.90 y 2.80..3.00)
    add_box("Muro_H_Y420_Cuarto_Mocheta_Izq", 1.70, 4.20 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    add_box("Muro_H_Y420_Cuarto_Mocheta_Der", 2.80, 4.20 - INT/2, 0.00, 0.20, INT, H, "Muro_Interior")
    # Frente Cocina mochetas (3.00..3.25 y 4.65..5.00)
    add_box("Muro_H_Y420_Cocina_Frente_Izq", 3.00, 4.20 - INT/2, 0.00, 0.25, INT, H, "Muro_Interior")
    add_box("Muro_H_Y420_Cocina_Frente_Der", 4.65, 4.20 - INT/2, 0.00, 0.35, INT, H, "Muro_Interior")

    with open("Departamento_01-01.obj", "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
    with open("Departamento_01-01.mtl", "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))

    print("Modelo 3D OBJ/MTL (6.30m x 6.20m) generado exitosamente.")

if __name__ == "__main__":
    generate_obj_mtl()
