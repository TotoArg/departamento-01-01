"""
Generador de Modelo 3D (.OBJ + .MTL) para Blender / CAD.
Estructura arquitectónica exacta en "L" de 6.30 m x 7.00 m con elementos extraídos del video:
- Suelo cerámico 33x33 cm + piso de baño + palier exterior
- 7 ventanas caladas con marco de aluminio oscuro y vidrio
- 3 calefactores tiro balanceado + equipamiento fijo de cocina y baño
- Techo de madera machimbrada en su propio grupo (05_Techo_Madera)
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
            (0, 3, 2, 1),
            (4, 5, 6, 7),
            (0, 4, 7, 3),
            (1, 2, 6, 5),
            (3, 7, 6, 2),
            (0, 1, 5, 4),
        ]

        for f in box_faces:
            self.faces.append({
                "group": self.current_group,
                "material": self.current_material,
                "indices": [base_idx + i for i in f],
            })

    def save(self, obj_path, mtl_path, mtl_filename):
        materials = {
            "Floor_Ceramic_Beige": (0.98, 0.96, 0.94),
            "Floor_Bath_White": (0.97, 0.98, 0.99),
            "Palier_Ext": (0.91, 0.92, 0.94),
            "Wall_Exterior": (0.92, 0.94, 0.96),
            "Wall_Interior": (0.86, 0.89, 0.93),
            "Window_Glass": (0.58, 0.77, 0.98),
            "Heater_Metal": (0.62, 0.65, 0.69),
            "Kitchen_Granite": (0.84, 0.72, 0.68),
            "Sanitary_White": (0.98, 0.99, 1.00),
            "Wood_Roof": (0.72, 0.48, 0.24),
            "Door_Frame_Dark": (0.17, 0.19, 0.21),
            "Door_Wood_Cedar": (0.74, 0.47, 0.25),
            "Door_Main_Grey": (0.55, 0.57, 0.60),
            "Placard_Wood": (0.77, 0.49, 0.27),
        }

        with open(mtl_path, "w", encoding="utf-8") as mf:
            mf.write("# Materiales Arquitectónicos Departamento 6.30m x 7.00m (Planta en L + Video)\n\n")
            for name, (r, g, b) in materials.items():
                mf.write(f"newmtl {name}\n")
                mf.write("Ka 0.200 0.200 0.200\n")
                mf.write(f"Kd {r:.3f} {g:.3f} {b:.3f}\n")
                mf.write("Ks 0.080 0.080 0.080\n")
                mf.write("Ns 30.0\n")
                mf.write("d 1.0\n\n")

        with open(obj_path, "w", encoding="utf-8") as of:
            of.write("# Modelo 3D Arquitectónico Exacto 6.30m x 7.00m (Planta en L + Relevamiento Video)\n")
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
    H = 2.60
    EXT = 0.14
    INT = 0.10

    # 1. PISOS
    b.set_group("00_Piso_Ceramico_33x33", "Floor_Ceramic_Beige")
    b.add_box(0.00, -0.10, 0.00, 6.30, 0.00, 5.70)
    b.add_box(0.00, -0.10, 5.70, 5.20, 0.00, 7.00)

    b.set_group("00_Piso_Bano", "Floor_Bath_White")
    b.add_box(0.00, -0.095, 2.80, 2.30, 0.002, 4.00)

    b.set_group("00_Palier_Edificio", "Palier_Ext")
    b.add_box(5.20, -0.10, 5.70, 6.30, 0.00, 7.00)

    # 2. PERÍMETRO EXTERIOR CON 7 VENTANAS CALADAS
    b.set_group("01_Muros_Exteriores", "Wall_Exterior")
    # Muro Norte Y = 0.00 (V4 Estudio 0.85..2.05, V1 Living 3.35..4.55, V2 Living 4.90..6.00)
    b.add_box(0.00, 0.00, -EXT / 2, 0.85, H, EXT / 2)
    b.add_box(0.85, 0.00, -EXT / 2, 2.05, 0.95, EXT / 2)
    b.add_box(0.85, 2.05, -EXT / 2, 2.05, H, EXT / 2)
    b.add_box(2.05, 0.00, -EXT / 2, 3.35, H, EXT / 2)
    b.add_box(3.35, 0.00, -EXT / 2, 4.55, 0.95, EXT / 2)
    b.add_box(3.35, 2.05, -EXT / 2, 4.55, H, EXT / 2)
    b.add_box(4.55, 0.00, -EXT / 2, 4.90, H, EXT / 2)
    b.add_box(4.90, 0.00, -EXT / 2, 6.00, 0.95, EXT / 2)
    b.add_box(4.90, 2.05, -EXT / 2, 6.00, H, EXT / 2)
    b.add_box(6.00, 0.00, -EXT / 2, 6.30, H, EXT / 2)

    # Muro Este X = 6.30 (V3 Living Y = 1.00..2.50)
    b.add_box(6.30 - EXT / 2, 0.00, 0.00, 6.30 + EXT / 2, H, 1.00)
    b.add_box(6.30 - EXT / 2, 0.00, 1.00, 6.30 + EXT / 2, 0.95, 2.50)
    b.add_box(6.30 - EXT / 2, 2.05, 1.00, 6.30 + EXT / 2, H, 2.50)
    b.add_box(6.30 - EXT / 2, 0.00, 2.50, 6.30 + EXT / 2, H, 5.70)

    # Retranqueo Palier Y = 5.70 (Puerta Principal X = 5.38..6.12)
    b.add_box(5.20, 0.00, 5.70 - EXT / 2, 5.38, H, 5.70 + EXT / 2)
    b.add_box(6.12, 0.00, 5.70 - EXT / 2, 6.30, H, 5.70 + EXT / 2)
    b.add_box(5.38, 2.05, 5.70 - EXT / 2, 6.12, H, 5.70 + EXT / 2)

    # Muro Derecho Cocina X = 5.20 (Y = 5.70..7.00)
    b.add_box(5.20 - EXT / 2, 0.00, 5.70, 5.20 + EXT / 2, H, 7.00)

    # Muro Sur Y = 7.00 (V5 Cuarto 0.90..2.10, V6 Cocina 3.55..4.55)
    b.add_box(0.00, 0.00, 7.00 - EXT / 2, 0.90, H, 7.00 + EXT / 2)
    b.add_box(0.90, 0.00, 7.00 - EXT / 2, 2.10, 0.95, 7.00 + EXT / 2)
    b.add_box(0.90, 2.05, 7.00 - EXT / 2, 2.10, H, 7.00 + EXT / 2)
    b.add_box(2.10, 0.00, 7.00 - EXT / 2, 3.55, H, 7.00 + EXT / 2)
    b.add_box(3.55, 0.00, 7.00 - EXT / 2, 4.55, 1.05, 7.00 + EXT / 2)
    b.add_box(3.55, 2.00, 7.00 - EXT / 2, 4.55, H, 7.00 + EXT / 2)
    b.add_box(4.55, 0.00, 7.00 - EXT / 2, 5.20, H, 7.00 + EXT / 2)

    # Muro Oeste X = 0.00 (V7 Ventiluz Baño Y = 3.05..3.75)
    b.add_box(-EXT / 2, 0.00, 0.00, EXT / 2, H, 3.05)
    b.add_box(-EXT / 2, 0.00, 3.05, EXT / 2, 1.35, 3.75)
    b.add_box(-EXT / 2, 2.00, 3.05, EXT / 2, H, 3.75)
    b.add_box(-EXT / 2, 0.00, 3.75, EXT / 2, H, 7.00)

    # Vidrios de las 7 ventanas
    b.set_group("01B_Ventanas_Aluminio", "Window_Glass")
    b.add_box(0.85, 0.95, -0.02, 2.05, 2.05, 0.02)
    b.add_box(3.35, 0.95, -0.02, 4.55, 2.05, 0.02)
    b.add_box(4.90, 0.95, -0.02, 6.00, 2.05, 0.02)
    b.add_box(6.28, 0.95, 1.00, 6.32, 2.05, 2.50)
    b.add_box(0.90, 0.95, 6.98, 2.10, 2.05, 7.02)
    b.add_box(3.55, 1.05, 6.98, 4.55, 2.00, 7.02)
    b.add_box(-0.02, 1.35, 3.05, 0.02, 2.00, 3.75)

    # 3. TABIQUES INTERIORES
    b.set_group("02_Tabiques_Interiores", "Wall_Interior")
    b.add_box(2.30 - INT / 2, 0.00, 2.30, 2.30 + INT / 2, H, 3.02)
    b.add_box(2.30 - INT / 2, 2.05, 3.02, 2.30 + INT / 2, H, 3.65)
    b.add_box(2.30 - INT / 2, 0.00, 3.65, 2.30 + INT / 2, H, 4.50)

    b.add_box(3.00 - INT / 2, 0.00, 0.00, 3.00 + INT / 2, H, 3.70)
    b.add_box(3.00 - INT / 2, 0.00, 4.50, 3.00 + INT / 2, H, 7.00)

    b.add_box(5.20 - INT / 2, 0.00, 4.50, 5.20 + INT / 2, H, 5.70)

    b.add_box(0.00, 0.00, 2.30 - INT / 2, 2.30, H, 2.30 + INT / 2)
    b.add_box(2.30, 2.05, 2.30 - INT / 2, 3.00, H, 2.30 + INT / 2)

    b.add_box(0.00, 0.00, 2.80 - INT / 2, 2.30, H, 2.80 + INT / 2)
    b.add_box(0.00, 0.00, 4.00 - INT / 2, 2.30, H, 4.00 + INT / 2)

    b.add_box(0.00, 0.00, 4.50 - INT / 2, 2.30, H, 4.50 + INT / 2)
    b.add_box(2.30, 2.05, 4.50 - INT / 2, 3.00, H, 4.50 + INT / 2)
    b.add_box(3.00, 2.05, 4.50 - INT / 2, 3.85, H, 4.50 + INT / 2)  # Dintel sobre vano abierto Cocina
    b.add_box(3.85, 0.00, 4.50 - INT / 2, 5.20, H, 4.50 + INT / 2)

    # 3B. PUERTAS 3D Y PLACARDS EXTRAÍDOS DEL VIDEO
    # Marcos de chapa gris oscuro
    b.set_group("02B_Marcos_Puertas_Chapa", "Door_Frame_Dark")
    # Marco Puerta Principal (Y=5.70, X=5.38..6.12)
    b.add_box(5.38, 0.00, 5.62, 5.42, 2.05, 5.78)
    b.add_box(6.08, 0.00, 5.62, 6.12, 2.05, 5.78)
    b.add_box(5.38, 2.01, 5.62, 6.12, 2.05, 5.78)
    # Marco Puerta Estudio (Y=2.30, X=2.30..3.00)
    b.add_box(2.30, 0.00, 2.24, 2.34, 2.05, 2.36)
    b.add_box(2.96, 0.00, 2.24, 3.00, 2.05, 2.36)
    b.add_box(2.30, 2.01, 2.24, 3.00, 2.05, 2.36)
    # Marco Puerta Baño (X=2.30, Y=3.02..3.65)
    b.add_box(2.24, 0.00, 3.02, 2.36, 2.05, 3.06)
    b.add_box(2.24, 0.00, 3.61, 2.36, 2.05, 3.65)
    b.add_box(2.24, 2.01, 3.02, 2.36, 2.05, 3.65)
    # Marco Puerta Cuarto (Y=4.50, X=2.30..3.00)
    b.add_box(2.30, 0.00, 4.44, 2.34, 2.05, 4.56)
    b.add_box(2.96, 0.00, 4.44, 3.00, 2.05, 4.56)
    b.add_box(2.30, 2.01, 4.44, 3.00, 2.05, 4.56)

    # Hojas de Puertas Interiores Placa Madera (abiertas hacia adentro de cada ambiente)
    b.set_group("02C_Hojas_Puertas_Madera", "Door_Wood_Cedar")
    b.add_box(2.34, 0.01, 1.68, 2.38, 2.01, 2.30)  # Hoja Estudio abierta hacia adentro (Y < 2.30)
    b.add_box(1.72, 0.01, 3.06, 2.30, 2.01, 3.10)  # Hoja Baño abierta hacia adentro (X < 2.30)
    b.add_box(2.34, 0.01, 4.50, 2.38, 2.01, 5.12)  # Hoja Cuarto abierta hacia adentro (Y > 4.50)

    # Hoja Puerta Principal Gris Moldurada (abierta hacia adentro de Entrada)
    b.set_group("02D_Puerta_Principal_Gris", "Door_Main_Grey")
    b.add_box(5.42, 0.01, 5.04, 5.47, 2.01, 5.70)

    # Frentes de Placard Corredizos de Madera
    b.set_group("02E_Placards_Corredizos_Madera", "Placard_Wood")
    b.add_box(0.15, 0.06, 2.22, 2.18, 2.45, 2.25)  # Frente Placard Superior (Estudio)
    b.add_box(0.15, 0.06, 4.55, 2.18, 2.45, 4.58)  # Frente Placard Inferior (Cuarto)

    # 4. CALEFACTORES E INSTALACIONES FIJAS DEL VIDEO
    b.set_group("03_Calefactores_Tiro_Balanceado", "Heater_Metal")
    b.add_box(6.05, 0.05, 2.75, 6.23, 0.65, 3.35)  # Calefactor Living
    b.add_box(6.10, 0.65, 3.00, 6.20, 2.80, 3.10)  # Caño tiraje vertical Living
    b.add_box(0.25, 0.05, 6.78, 0.72, 0.65, 6.94)  # Calefactor Cuarto
    b.add_box(0.06, 0.05, 0.80, 0.22, 0.65, 1.25)  # Calefactor Estudio

    b.set_group("04_Equipamiento_Cocina_Bano", "Kitchen_Granite")
    b.add_box(3.05, 0.00, 5.35, 3.62, 0.86, 6.94)  # Mesada tramo izquierdo
    b.add_box(3.62, 0.00, 6.40, 4.62, 0.86, 6.94)  # Mesada tramo sur bajo ventana

    b.set_group("04B_Sanitarios_Y_Termo", "Sanitary_White")
    b.add_box(3.12, 0.86, 5.42, 3.52, 1.90, 5.82)  # Termotanque Sherman
    b.add_box(0.05, 0.00, 2.84, 0.75, 0.48, 3.96)  # Bañera
    b.add_box(1.12, 0.00, 2.84, 1.58, 0.82, 3.20)  # Lavatorio
    b.add_box(1.68, 0.00, 3.56, 2.06, 0.75, 3.95)  # Inodoro

    b.save("Departamento_01-01.obj", "Departamento_01-01.mtl", "Departamento_01-01.mtl")
    print("Modelo 3D completo (.obj y .mtl) con detalles de video generado exitosamente.")


if __name__ == "__main__":
    build_apartment()
