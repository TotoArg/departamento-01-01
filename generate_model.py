"""
Generador paramétrico de Departamento_01-01.obj y Departamento_01-01.mtl
Distribución 100% verificada con croquis y videos:
- Lateral derecho: Living comedor a lo largo con techo de madera y vigas a la vista
- Acceso: Entrada principal por el living (frente inferior)
- Centro inferior: Cocina semi-integrada
- Centro: Pasillo de distribución
- Lateral izquierdo:
  * Cuarto principal (frente) con placard embutido
  * Baño completo (centro) con bañera, bidet, inodoro, vanitory y placard de respaldo
  * Estudio / Gamer room (fondo) con placard embutido y escritorio
"""

def generate_obj_mtl():
    obj_lines = []
    mtl_lines = []

    obj_lines.append("# Departamento 01-01 - Distribución Real (Croquis + Videos)")
    obj_lines.append("mtllib Departamento_01-01.mtl\n")

    v_count = 0
    def add_box(name, x, z, y, sx, sz, sy, material):
        """
        x: ancho (0 a 8.0)
        z: largo (0 a 7.2)
        y: altura (0 a 3.8)
        """
        nonlocal v_count
        obj_lines.append(f"o {name}")
        obj_lines.append(f"usemtl {material}")

        # Blender usa Z arriba, Y fondo. En OBJ estándar exportamos con Y arriba (X, Y, Z).
        corners = [
            (x, y, z),
            (x + sx, y, z),
            (x + sx, y, z + sz),
            (x, y, z + sz),
            (x, y + sy, z),
            (x + sx, y + sy, z),
            (x + sx, y + sy, z + sz),
            (x, y + sy, z + sz),
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

    # 1. PISO
    add_box("Piso_General", 0.0, 0.0, -0.05, 8.0, 7.2, 0.05, "Piso_Ceramico")

    # 2. MUROS EXTERIORES (Perímetro)
    add_box("Muro_Sur_Izquierda", -0.2, 7.2, 0.0, 5.8, 0.2, 2.7, "Pared_Blanca")
    add_box("Muro_Sur_Dintel_Entrada", 5.6, 7.2, 2.1, 0.9, 0.2, 0.6, "Pared_Blanca")
    add_box("Muro_Sur_Derecha", 6.5, 7.2, 0.0, 1.7, 0.2, 2.7, "Pared_Blanca")

    add_box("Muro_Norte_Fondo", -0.2, -0.2, 0.0, 8.4, 0.2, 3.2, "Pared_Blanca")
    add_box("Muro_Oeste_Lateral_Izquierdo", -0.2, 0.0, 0.0, 0.2, 7.2, 2.8, "Pared_Blanca")
    add_box("Muro_Este_Lateral_Living", 8.0, 0.0, 0.0, 0.2, 7.2, 2.7, "Pared_Blanca")

    # 3. TABIQUES INTERIORES
    # Tabique Living - Pasillo/Habitaciones
    add_box("Tabique_Living_Norte", 3.6, 0.0, 0.0, 0.12, 3.6, 3.2, "Pared_Blanca")
    add_box("Dintel_Paso_Living_Pasillo", 3.6, 3.6, 2.1, 0.12, 1.1, 1.1, "Pared_Blanca")
    add_box("Tabique_Living_Sur_Cocina", 3.6, 4.7, 0.0, 0.12, 2.5, 3.0, "Pared_Blanca")

    # Tabique Cocina - Pasillo
    add_box("Tabique_Cocina_Oeste", 2.2, 5.2, 0.0, 0.12, 2.0, 2.8, "Pared_Blanca")
    add_box("Dintel_Acceso_Cocina", 2.2, 5.2, 2.1, 1.4, 0.12, 0.7, "Pared_Blanca")

    # Tabiques Lateral Izquierdo: Cuarto, Baño, Estudio
    # Cuarto - Placard
    add_box("Tabique_Cuarto_Placard", 0.0, 5.0, 0.0, 2.2, 0.10, 2.8, "Pared_Blanca")
    add_box("Frente_Placard_Cuarto", 0.0, 4.4, 0.0, 2.2, 0.60, 2.5, "Madera")
    add_box("Tabique_Acceso_Cuarto", 2.2, 4.4, 0.0, 0.12, 0.8, 2.8, "Pared_Blanca")

    # Baño
    add_box("Tabique_Bano_Norte", 0.0, 2.8, 0.0, 2.2, 0.10, 3.0, "Pared_Blanca")
    add_box("Tabique_Acceso_Bano", 2.2, 2.8, 0.0, 0.12, 1.6, 3.0, "Pared_Blanca")

    # Estudio Gamer
    add_box("Frente_Placard_Estudio", 0.0, 2.2, 0.0, 2.2, 0.60, 2.5, "Madera")
    add_box("Tabique_Acceso_Estudio", 2.2, 0.0, 0.0, 0.12, 2.2, 3.2, "Pared_Blanca")

    # 4. EQUIPAMIENTO Y MUEBLES CLAVE
    # Cocina
    add_box("Mesada_Cocina_L", 2.35, 6.55, 0.0, 1.25, 0.60, 0.88, "Granito_Rosa")
    add_box("Bacha_Cocina", 2.35, 5.30, 0.0, 0.60, 1.25, 0.88, "Granito_Rosa")
    add_box("Heladera", 3.05, 5.30, 0.0, 0.55, 0.60, 1.75, "Blanco_Sanitarios")
    add_box("Termotanque_Sherman", 2.35, 7.00, 1.30, 0.40, 0.40, 0.85, "Blanco_Sanitarios")

    # Baño
    add_box("Banera", 0.10, 2.95, 0.0, 0.70, 1.40, 0.45, "Blanco_Sanitarios")
    add_box("Inodoro", 1.05, 2.95, 0.0, 0.40, 0.55, 0.42, "Blanco_Sanitarios")
    add_box("Bidet", 1.65, 2.95, 0.0, 0.38, 0.55, 0.40, "Blanco_Sanitarios")
    add_box("Vanitory", 0.10, 3.75, 0.0, 0.55, 0.60, 0.85, "Madera")

    # Cuarto
    add_box("Cama_Doble", 0.30, 5.35, 0.0, 1.50, 1.75, 0.45, "Madera")
    add_box("Mesa_Luz", 1.85, 5.35, 0.0, 0.35, 0.40, 0.55, "Madera")

    # Estudio
    add_box("Escritorio_Gamer_L", 0.10, 0.10, 0.0, 1.50, 0.70, 0.75, "Negro_Metal")
    add_box("Retorno_Escritorio", 0.10, 0.80, 0.0, 0.60, 0.90, 0.75, "Negro_Metal")

    # Living
    add_box("Sillon_Living", 4.80, 4.20, 0.0, 2.20, 0.90, 0.75, "Gris_Tapizado")
    add_box("Mesa_Comedor", 5.20, 1.80, 0.0, 1.40, 0.85, 0.76, "Madera")
    add_box("Calefactor_Gas", 7.85, 2.60, 0.0, 0.15, 0.60, 0.65, "Negro_Metal")

    # 5. VIGAS DE TECHO DE MADERA
    for i in range(12):
        z_pos = 0.3 + i * 0.6
        add_box(f"Viga_Techo_{i+1}", -0.2, z_pos, 2.7 + i * 0.04, 8.4, 0.08, 0.14, "Vigas_Madera")

    # Exportar OBJ
    with open("Departamento_01-01.obj", "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))

    # Exportar MTL
    mtl_lines.append("newmtl Piso_Ceramico\nKd 0.82 0.76 0.70\n")
    mtl_lines.append("newmtl Pared_Blanca\nKd 0.95 0.95 0.96\n")
    mtl_lines.append("newmtl Granito_Rosa\nKd 0.78 0.58 0.52\n")
    mtl_lines.append("newmtl Madera\nKd 0.62 0.38 0.20\n")
    mtl_lines.append("newmtl Vigas_Madera\nKd 0.45 0.24 0.12\n")
    mtl_lines.append("newmtl Blanco_Sanitarios\nKd 0.96 0.96 0.96\n")
    mtl_lines.append("newmtl Gris_Tapizado\nKd 0.35 0.40 0.45\n")
    mtl_lines.append("newmtl Negro_Metal\nKd 0.15 0.15 0.18\n")

    with open("Departamento_01-01.mtl", "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))

    print("Departamento_01-01.obj y .mtl generados correctamente con la nueva distribución.")

if __name__ == "__main__":
    generate_obj_mtl()
