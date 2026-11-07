"""
Generador de Modelo 3D (.OBJ + .MTL) para Blender / CAD.
Estructura arquitectónica exacta en "L" de 6.30 m x 7.00 m (sin muebles fijos).
"""


class OBJBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.current_group = "Default"
        self.current_material = "Default"

    def set_group(self, group_name, material_name):
        self.current_group = group_name
        self.current_material = material_name

    def add_box(self, x1, y1, z1, x2, y2, z2):
        # X: ancho (0.00 a 6.30 m)
        # Y: altura (0.00 a 2.60 m)
        # Z: profundidad (0.00 a 7.00 m)
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)
        z_min, z_max = min(z1, z2), max(z1, z2)

        base_idx = len(self.vertices) + 1
        verts = [
            (x_min, y_min, z_min),
            (x_max, y_min, z_min),
            (x_max, y_max, z_min),
            (x_min, y_max, z_min),
            (x_min, y_min, z_max),
            (x_max, y_min, z_max),
            (x_max, y_max, z_max),
            (x_min, y_max, z_max),
        ]
        self.vertices.extend(verts)

        box_faces = [
            (0, 3, 2, 1),  # Norte (-Z)
            (4, 5, 6, 7),  # Sur (+Z)
            (0, 4, 7, 3),  # Oeste (-X)
            (1, 2, 6, 5),  # Este (+X)
            (3, 7, 6, 2),  # Arriba (+Y)
            (0, 1, 5, 4),  # Abajo (-Y)
        ]

        for f in box_faces:
            self.faces.append({
                "group": self.current_group,
                "material": self.current_material,
                "indices": [base_idx + i for i in f],
            })

    def save(self, obj_path, mtl_path, mtl_filename):
        materials = {
            "Floor_Light": (0.96, 0.96, 0.97),
            "Palier_Ext": (0.91, 0.92, 0.94),
            "Wall_Exterior": (0.85, 0.88, 0.92),
            "Wall_Interior": (0.78, 0.82, 0.88),
        }

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Materiales Arquitectónicos Departamento 6.30m x 7.00m (Planta en L)\n\n")
            for name, (r, g, b) in materials.items():
                mf.write(f"newmtl {name}\n")
                mf.write("Ka 0.200 0.200 0.200\n")
                mf.write(f"Kd {r:.3f} {g:.3f} {b:.3f}\n")
                mf.write("Ks 0.080 0.080 0.080\n")
                mf.write("Ns 30.0\n")
                mf.write("d 1.0\n\n")

        with open(obj_path, "w", encoding="utf-8") as of:
            of.write("# Modelo 3D Arquitectónico Exacto 6.30m x 7.00m (Planta en L)\n")
            of.write(f"mtllib {mtl_filename}\n\n")

            for v in self.vertices:
                of.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")

            of.write("\n")
            last_group = None
            last_mat = None
            for face in self.faces:
                if face["group"] != last_group:
                    of.write(f"\no {face['group']}\n")
                    of.write(f"g {face['group']}\n")
                    last_group = face["group"]
                if face["material"] != last_mat:
                    of.write(f"usemtl {face['material']}\n")
                    last_mat = face["material"]
                idx_str = " ".join(str(i) for i in face["indices"])
                of.write(f"f {idx_str}\n")


def build_apartment():
    b = OBJBuilder()
    H = 2.60       # Altura de muros
    EXT = 0.14     # Espesor muro exterior
    INT = 0.10     # Espesor tabique interior

    # 1. PISO POLIGONAL EN "L" (6.30m x 7.00m) + PALIER EXTERIOR
    b.set_group("00_Piso_General", "Floor_Light")
    b.add_box(0.00, -0.10, 0.00, 6.30, 0.00, 5.70)
    b.add_box(0.00, -0.10, 5.70, 5.20, 0.00, 7.00)

    b.set_group("00_Palier_Edificio", "Palier_Ext")
    b.add_box(5.20, -0.10, 5.70, 6.30, 0.00, 7.00)

    # 2. PERÍMETRO EXTERIOR (Polígono en "L": 6.30m x 7.00m)
    b.set_group("01_Muros_Exteriores", "Wall_Exterior")
    # Muro Superior Norte: Y = 0.00 (X = 0.00 a 6.30)
    b.add_box(0.00, 0.00, -EXT / 2, 6.30, H, EXT / 2)
    # Muro Derecho Este: X = 6.30 (Y = 0.00 a 5.70)
    b.add_box(6.30 - EXT / 2, 0.00, 0.00, 6.30 + EXT / 2, H, 5.70)
    # Retranqueo Palier / Puerta Principal: Y = 5.70 (X = 5.20 a 6.30 con vano 5.38 a 6.12)
    b.add_box(5.20, 0.00, 5.70 - EXT / 2, 5.38, H, 5.70 + EXT / 2)
    b.add_box(6.12, 0.00, 5.70 - EXT / 2, 6.30, H, 5.70 + EXT / 2)
    b.add_box(5.38, 2.05, 5.70 - EXT / 2, 6.12, H, 5.70 + EXT / 2)  # Dintel puerta entrada
    # Muro Derecho Cocina (baja al fondo): X = 5.20 (Y = 5.70 a 7.00)
    b.add_box(5.20 - EXT / 2, 0.00, 5.70, 5.20 + EXT / 2, H, 7.00)
    # Muro Inferior Sur: Y = 7.00 (X = 0.00 a 5.20)
    b.add_box(0.00, 0.00, 7.00 - EXT / 2, 5.20, H, 7.00 + EXT / 2)
    # Muro Izquierdo Oeste: X = 0.00 (Y = 0.00 a 7.00)
    b.add_box(-EXT / 2, 0.00, 0.00, EXT / 2, H, 7.00)

    # 3. TABIQUES INTERIORES
    b.set_group("02_Tabiques_Interiores", "Wall_Interior")
    # Eje Vertical X = 2.30 (Cierre Placards y Baño):
    # - Muro sólido de Y = 2.30 a Y = 2.80 (Placard Sup.)
    b.add_box(2.30 - INT / 2, 0.00, 2.30, 2.30 + INT / 2, H, 2.80)
    # - Puerta Baño: Entre Y = 2.80 e Y = 3.70 (dintel superior)
    b.add_box(2.30 - INT / 2, 2.05, 2.80, 2.30 + INT / 2, H, 3.70)
    # - Muro sólido de Y = 3.70 a Y = 4.50 (tramo Baño 3.70-4.00 + Placard Inf. 4.00-4.50)
    b.add_box(2.30 - INT / 2, 0.00, 3.70, 2.30 + INT / 2, H, 4.50)

    # Eje Vertical Central X = 3.00:
    # - Muro sólido de Y = 0.00 a Y = 3.70 (Estudio y Pasillo / Living)
    b.add_box(3.00 - INT / 2, 0.00, 0.00, 3.00 + INT / 2, H, 3.70)
    # - Vano Abierto de Y = 3.70 a Y = 4.50 (sin muro)
    # - Muro sólido de Y = 4.50 a Y = 7.00 (Cuarto / Cocina)
    b.add_box(3.00 - INT / 2, 0.00, 4.50, 3.00 + INT / 2, H, 7.00)

    # Eje Vertical X = 5.20 (Cocina / Entrada): Y = 4.50 a 5.70
    b.add_box(5.20 - INT / 2, 0.00, 4.50, 5.20 + INT / 2, H, 5.70)

    # Eje Horizontal Y = 2.30 (Base Estudio):
    # - Muro sólido X = 0.00 a 2.30
    b.add_box(0.00, 0.00, 2.30 - INT / 2, 2.30, H, 2.30 + INT / 2)
    # - Dintel Puerta Estudio X = 2.30 a 3.00
    b.add_box(2.30, 2.05, 2.30 - INT / 2, 3.00, H, 2.30 + INT / 2)

    # Eje Horizontal Y = 2.80 (Placard Sup. / Baño): X = 0.00 a 2.30
    b.add_box(0.00, 0.00, 2.80 - INT / 2, 2.30, H, 2.80 + INT / 2)

    # Eje Horizontal Y = 4.00 (Baño / Placard Inf.): X = 0.00 a 2.30
    b.add_box(0.00, 0.00, 4.00 - INT / 2, 2.30, H, 4.00 + INT / 2)

    # Eje Horizontal Y = 4.50 (Línea Cuarto y Cocina):
    # - Muro sólido X = 0.00 a 2.30 (Placard Inf. / Cuarto)
    b.add_box(0.00, 0.00, 4.50 - INT / 2, 2.30, H, 4.50 + INT / 2)
    # - Dintel Puerta Cuarto X = 2.30 a 3.00
    b.add_box(2.30, 2.05, 4.50 - INT / 2, 3.00, H, 4.50 + INT / 2)
    # - Vano Abierto Cocina X = 3.00 a 3.85 (sin muro)
    # - Muro sólido frontal de Cocina X = 3.85 a 5.20
    b.add_box(3.85, 0.00, 4.50 - INT / 2, 5.20, H, 4.50 + INT / 2)

    b.save("Departamento_01-01.obj", "Departamento_01-01.mtl", "Departamento_01-01.mtl")
    print("Modelo 3D (.obj y .mtl) 6.30m x 7.00m generado exitosamente.")


if __name__ == "__main__":
    build_apartment()
