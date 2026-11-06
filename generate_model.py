"""
Generador de archivos Departamento_01-01.obj y Departamento_01-01.mtl
actualizados según el relevamiento de los videos.
"""

def generate_real_obj():
    obj_lines = []
    mtl_lines = []

    obj_lines.append("# Departamento 01-01 - Relevamiento Real 3D (Videos)")
    obj_lines.append("mtllib Departamento_01-01.mtl\n")

    v_count = 0
    def add_box(name, x, y, z, sx, sy, sz, material):
        nonlocal v_count
        obj_lines.append(f"o {name}")
        obj_lines.append(f"usemtl {material}")

        corners = [
            (x, z, y),
            (x + sx, z, y),
            (x + sx, z, y + sy),
            (x, z, y + sy),
            (x, z + sz, y),
            (x + sx, z + sz, y),
            (x + sx, z + sz, y + sy),
            (x, z + sz, y + sy),
        ]
        for vx, vy, vz in corners:
            obj_lines.append(f"v {vx:.3f} {vy:.3f} {vz:.3f}")

        b = v_count
        obj_lines.append(f"f {b+1} {b+2} {b+3} {b+4}")
        obj_lines.append(f"f {b+5} {b+8} {b+7} {b+6}")
        obj_lines.append(f"f {b+1} {b+5} {b+6} {b+2}")
        obj_lines.append(f"f {b+2} {b+6} {b+7} {b+3}")
        obj_lines.append(f"f {b+3} {b+7} {b+8} {b+4}")
        obj_lines.append(f"f {b+4} {b+8} {b+5} {b+1}")
        v_count += 8
        obj_lines.append("")

    # Piso
    add_box("Piso_General", 0.0, 0.0, -0.05, 9.2, 6.2, 0.05, "Piso_Ceramico")

    # Muros exteriores
    add_box("Muro_Sur", -0.2, -0.2, 0.0, 9.6, 0.2, 2.7, "Pared_Blanca")
    add_box("Muro_Oeste", -0.2, 0.0, 0.0, 0.2, 6.2, 2.7, "Pared_Blanca")
    add_box("Muro_Norte", -0.2, 6.2, 0.0, 9.6, 0.2, 3.2, "Pared_Blanca")
    add_box("Muro_Este", 9.2, 0.0, 0.0, 0.2, 6.2, 3.0, "Pared_Blanca")

    # Tabiques interiores
    add_box("Tabique_Living_Privado", 4.2, 0.0, 0.0, 0.12, 4.6, 3.2, "Pared_Blanca")
    add_box("Tabique_Cocina_Bano", 4.32, 2.4, 0.0, 4.88, 0.12, 3.0, "Pared_Blanca")
    add_box("Tabique_Bano_Dormitorio", 4.32, 4.1, 0.0, 4.88, 0.12, 3.1, "Pared_Blanca")

    # Muebles clave
    add_box("Bañera", 8.4, 2.55, 0.0, 0.7, 1.5, 0.45, "Blanco_Sanitarios")
    add_box("Mesada_Cocina", 5.5, 0.0, 0.0, 2.5, 0.6, 0.88, "Granito_Rosa")
    add_box("Cama_Dormitorio", 5.0, 4.3, 0.0, 1.5, 1.9, 0.48, "Madera")
    add_box("Placard", 7.4, 4.2, 0.0, 1.7, 0.65, 2.5, "Pared_Blanca")

    # Techo vigas
    for i in range(10):
        y_b = 0.3 + i * 0.6
        add_box(f"Viga_{i+1}", -0.3, y_b, 2.7 + i*0.04, 9.8, 0.08, 0.14, "Vigas_Madera")

    with open("Departamento_01-01.obj", "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
    
    mtl_lines.append("newmtl Piso_Ceramico\nKd 0.83 0.78 0.72\n")
    mtl_lines.append("newmtl Pared_Blanca\nKd 0.94 0.94 0.95\n")
    mtl_lines.append("newmtl Granito_Rosa\nKd 0.75 0.55 0.48\n")
    mtl_lines.append("newmtl Madera\nKd 0.58 0.32 0.15\n")
    mtl_lines.append("newmtl Blanco_Sanitarios\nKd 0.95 0.95 0.95\n")
    mtl_lines.append("newmtl Vigas_Madera\nKd 0.42 0.22 0.10\n")

    with open("Departamento_01-01.mtl", "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))
    
    print("Modelo 3D OBJ/MTL generado con éxito.")

if __name__ == "__main__":
    generate_real_obj()
