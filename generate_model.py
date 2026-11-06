"""
Generador paramétrico de Departamento_01-01.obj y Departamento_01-01.mtl
Dimensiones exactas según Escritura Oficial y Plano Catastral:
- Edificio Glaciares II - Calle Günter Plüschow 235, El Calafate
- Unidad Funcional N° 6, Depto "A", Polígono 01-01
- Superficie cubierta oficial: 54,16 m² (Cálculo exacto: (9.30 x 6.20) - (2.30 x 1.40) - (0.40 x 0.70) = 54,16 m²)
"""

def generate_obj_mtl():
    obj_lines = []
    mtl_lines = []

    obj_lines.append("# Edificio Glaciares II - Depto 01-01 (1° Piso)")
    obj_lines.append("# Superficie Escriturada Oficial: 54.16 m2 | Porcentual: 10.03%")
    obj_lines.append("mtllib Departamento_01-01.mtl\n")

    v_count = 0
    def add_box(name, x, z, y, sx, sz, sy, material):
        """
        x: ancho (0 a 9.30)
        z: largo (0 a 6.20)
        y: altura (0 a 3.85)
        Exportación estándar OBJ: X = ancho, Y = altura, Z = profundidad
        """
        nonlocal v_count
        obj_lines.append(f"o {name}")
        obj_lines.append(f"usemtl {material}")

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

    # 1. PISO (Subdividido en secciones para coincidir exactamente con los 54.16 m2)
    # Sector Principal Oeste (Calle Günter Plüschow a Living): 7.00 x 6.20 minus ducto
    add_box("Piso_Sector_Oeste_Principal", 0.00, 0.00, -0.05, 5.10, 6.20, 0.05, "Piso_Ceramico")
    add_box("Piso_Sector_Cocina_Frente_Ducto", 5.10, 0.00, -0.05, 0.40, 5.50, 0.05, "Piso_Ceramico")
    add_box("Piso_Sector_Centro", 5.50, 0.00, -0.05, 1.50, 6.20, 0.05, "Piso_Ceramico")
    # Sector Este (Living frente al palier): 2.30 x 4.80 (de Z=1.40 a 6.20)
    add_box("Piso_Sector_Este_Living", 7.00, 1.40, -0.05, 2.30, 4.80, 0.05, "Piso_Ceramico")

    # 2. MUROS EXTERIORES PERIMETRALES (54.16 m2)
    # Muro Norte (Medianera 01-02: 7.00 m)
    add_box("Muro_Norte_Medianera", -0.20, -0.20, 0.0, 7.20, 0.20, 3.20, "Pared_Blanca")
    # Saliente Cubierta Común (1.40 m)
    add_box("Muro_Saliente_Palier", 7.00, -0.20, 0.0, 0.20, 1.60, 3.00, "Pared_Blanca")
    # Muro Acceso Palier (2.30 m) con Puerta
    add_box("Muro_Acceso_Palier_Izq", 7.00, 1.40, 0.0, 0.60, 0.20, 2.70, "Pared_Blanca")
    add_box("Dintel_Puerta_Palier", 7.60, 1.40, 2.10, 0.90, 0.20, 0.60, "Pared_Blanca")
    add_box("Muro_Acceso_Palier_Der", 8.50, 1.40, 0.0, 0.80, 0.20, 2.70, "Pared_Blanca")
    # Muro Este (Lateral Living: 4.80 m)
    add_box("Muro_Este_Lateral_Living", 9.30, 1.40, 0.0, 0.20, 4.80, 2.70, "Pared_Blanca")
    # Muro Sur Living (3.80 m)
    add_box("Muro_Sur_Living", 5.50, 6.20, 0.0, 4.00, 0.20, 2.80, "Pared_Blanca")
    # Ducto Ventilación / Instalaciones (0.40 x 0.70 m)
    add_box("Ducto_Pared_Este", 5.50, 5.50, 0.0, 0.10, 0.70, 3.20, "Pared_Blanca")
    add_box("Ducto_Pared_Fondo", 5.10, 5.50, 0.0, 0.40, 0.10, 3.20, "Pared_Blanca")
    add_box("Ducto_Pared_Oeste", 5.10, 5.50, 0.0, 0.10, 0.70, 3.20, "Pared_Blanca")
    # Muro Sur Cuarto y Cocina (5.10 m)
    add_box("Muro_Sur_Cuarto_Cocina", -0.20, 6.20, 0.0, 5.30, 0.20, 2.80, "Pared_Blanca")
    # Muro Oeste (Fachada Calle Günter Plüschow: 6.20 m)
    add_box("Muro_Oeste_Calle_Gunter", -0.20, 0.00, 0.0, 0.20, 6.20, 3.00, "Pared_Blanca")

    # 3. TABIQUES INTERIORES (Distribución Real)
    # Divisorio Living / Privado
    add_box("Tabique_Living_Privado_Norte", 3.50, 0.00, 0.0, 0.12, 2.20, 3.20, "Pared_Blanca")
    add_box("Dintel_Paso_Living_Pasillo", 3.50, 2.20, 2.10, 0.12, 1.10, 1.10, "Pared_Blanca")
    add_box("Tabique_Living_Cocina", 3.50, 4.20, 0.0, 0.12, 2.00, 2.90, "Pared_Blanca")

    # Cocina
    add_box("Tabique_Cocina_Pasillo", 2.40, 4.20, 0.0, 1.10, 0.12, 2.80, "Pared_Blanca")
    add_box("Tabique_Cocina_Cuarto", 2.40, 4.20, 0.0, 0.12, 2.00, 2.80, "Pared_Blanca")

    # Sector Privado (Calle Günter Plüschow):
    # Cuarto Principal
    add_box("Tabique_Cuarto_Placard", 0.00, 4.80, 0.0, 2.40, 0.10, 2.80, "Pared_Blanca")
    add_box("Frente_Placard_Cuarto", 0.00, 4.30, 0.0, 2.40, 0.50, 2.50, "Madera")
    add_box("Tabique_Acceso_Cuarto", 2.40, 4.30, 0.0, 0.12, 0.50, 2.80, "Pared_Blanca")

    # Baño Completo (Centro)
    add_box("Tabique_Bano_Norte", 0.00, 2.70, 0.0, 2.40, 0.10, 3.00, "Pared_Blanca")
    add_box("Tabique_Acceso_Bano", 2.40, 2.70, 0.0, 0.12, 1.60, 3.00, "Pared_Blanca")

    # Estudio Gamer (Fondo)
    add_box("Frente_Placard_Estudio", 0.00, 2.20, 0.0, 2.40, 0.50, 2.50, "Madera")
    add_box("Tabique_Acceso_Estudio", 2.40, 0.00, 0.0, 0.12, 2.20, 3.20, "Pared_Blanca")

    # 4. MOBILIARIO Y EQUIPAMIENTO REAL
    # Cocina
    add_box("Mesada_Cocina", 3.70, 5.60, 0.0, 1.40, 0.60, 0.88, "Granito_Rosa")
    add_box("Cocina_Gas", 3.10, 5.60, 0.0, 0.55, 0.60, 0.86, "Blanco_Sanitarios")
    add_box("Termotanque_Sherman", 4.70, 5.60, 1.30, 0.40, 0.40, 0.85, "Blanco_Sanitarios")

    # Baño
    add_box("Banera", 0.10, 2.85, 0.0, 0.70, 1.40, 0.45, "Blanco_Sanitarios")
    add_box("Inodoro", 1.40, 2.85, 0.0, 0.40, 0.55, 0.42, "Blanco_Sanitarios")
    add_box("Bidet", 1.95, 2.85, 0.0, 0.38, 0.55, 0.40, "Blanco_Sanitarios")
    add_box("Vanitory", 1.40, 3.65, 0.0, 0.60, 0.50, 0.85, "Madera")

    # Cuarto
    add_box("Cama_Doble", 0.50, 4.95, 0.0, 1.40, 1.90, 0.45, "Gris_Tapizado")
    add_box("Mesa_Luz", 1.95, 5.60, 0.0, 0.40, 0.45, 0.55, "Madera")

    # Estudio
    add_box("Escritorio_Gamer_L", 0.10, 0.10, 0.0, 1.50, 0.70, 0.75, "Negro_Metal")
    add_box("Retorno_Escritorio", 0.10, 0.80, 0.0, 0.60, 0.90, 0.75, "Negro_Metal")

    # Living
    add_box("Sillon_Living", 5.60, 4.00, 0.0, 2.10, 0.90, 0.75, "Gris_Tapizado")
    add_box("Mesa_Comedor", 6.80, 2.00, 0.0, 1.40, 0.85, 0.76, "Madera")
    add_box("Calefactor_Gas_Tiro", 9.15, 2.60, 0.0, 0.15, 0.60, 0.65, "Negro_Metal")

    # 5. VIGAS DE TECHO DE MADERA
    for i in range(12):
        z_pos = 0.25 + i * 0.52
        add_box(f"Viga_Techo_{i+1}", -0.20, z_pos, 2.70 + i * 0.03, 9.60, 0.08, 0.14, "Vigas_Madera")

    with open("Departamento_01-01.obj", "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))

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

    print("Departamento_01-01.obj y .mtl generados con éxito con 54.16 m2 oficiales.")

if __name__ == "__main__":
    generate_obj_mtl()
