"""
Script Python para Blender 3.x / 4.x
Construye automáticamente el Departamento con la especificación geométrica exacta:
- Perímetro rectangular cerrado: 6.30 m (X: 0.00 a 6.30) × 6.20 m (Y: 0.00 arriba a 6.20 abajo).
- Pared inferior continua en Y = 6.20 con Puerta de Entrada en X = 5.20 a 6.10 (vano 0.90m).
- Ejes verticales:
  * X = 1.70: Cerramiento de Placards y Baño (puerta Baño Y = 2.80 a 3.40)
  * X = 3.00: Muro Living/Estudio (0.00 a 3.50), paso abierto (3.50 a 4.20) y muro Cuarto/Cocina (4.20 a 6.20)
  * X = 5.00: Muro divisorio Cocina con Sector Entrada (4.20 a 6.20)
- Ejes horizontales:
  * Y = 0.00: Muro exterior superior continuo
  * Y = 2.00: Muro Placard 1 (0.00 a 1.70) y vano Estudio (1.90 a 2.80)
  * Y = 2.50: Placard 1 / Baño (0.00 a 1.70)
  * Y = 3.70: Baño / Placard 2 (0.00 a 1.70)
  * Y = 4.20: Línea unificada: Placard 2 (0.00 a 1.70), puerta Cuarto (1.90 a 2.80), y vano Cocina (3.25 a 4.65)
  * Y = 6.20: Muro exterior inferior continuo con Puerta de Entrada en X = 5.20 a 6.10
"""

import bpy

def build_exact_apartment():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    def get_col(name):
        if name in bpy.data.collections:
            return bpy.data.collections[name]
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        return c

    col_ext = get_col("01_Perimetro_Exterior_63x62")
    col_int = get_col("02_Tabiques_Interiores")
    col_muebles = get_col("03_Mobiliario_Editable")

    def create_mat(name, color, rough=0.5):
        m = bpy.data.materials.get(name)
        if not m:
            m = bpy.data.materials.new(name=name)
            m.use_nodes = True
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
                bsdf.inputs['Roughness'].default_value = rough
        return m

    mat_piso = create_mat("Piso", (0.95, 0.96, 0.98), 0.6)
    mat_ext = create_mat("Muro_Exterior", (0.88, 0.91, 0.94), 0.5)
    mat_int = create_mat("Muro_Interior", (0.78, 0.83, 0.88), 0.5)
    mat_madera = create_mat("Mueble_Madera", (0.70, 0.42, 0.22), 0.4)

    def add_box(name, x1, y1, z1, sx, sy, sz, mat, col):
        # En Blender: X = X, Y = -Y_plano (para que Y=0 esté arriba y Y=6.20 abajo), Z = altura
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x1 + sx/2, -(y1 + sy/2), z1 + sz/2))
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = (sx, sy, sz)
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        for c in obj.users_collection:
            c.objects.unlink(obj)
        col.objects.link(obj)
        return obj

    H = 2.60
    EXT = 0.14
    INT = 0.10

    # 1. Piso (6.30 x 6.20)
    add_box("Piso_63x62", 0.00, 0.00, -0.08, 6.30, 6.20, 0.08, mat_piso, col_ext)

    # 2. Perímetro exterior
    add_box("Muro_Sup_Y0", 0.00, -EXT/2, 0.00, 6.30, EXT, H, mat_ext, col_ext)
    add_box("Muro_Izq_X0", -EXT/2, 0.00, 0.00, EXT, 6.20, H, mat_ext, col_ext)
    add_box("Muro_Der_X63", 6.30 - EXT/2, 0.00, 0.00, EXT, 6.20, H, mat_ext, col_ext)
    add_box("Muro_Inf_Izq_Y620", 0.00, 6.20 - EXT/2, 0.00, 5.20, EXT, H, mat_ext, col_ext)
    add_box("Muro_Inf_Der_Y620", 6.10, 6.20 - EXT/2, 0.00, 0.20, EXT, H, mat_ext, col_ext)

    # 3. Ejes verticales internos
    add_box("Muro_V_X170_Sup", 1.70 - INT/2, 2.00, 0.00, INT, 0.80, H, mat_int, col_int)
    add_box("Muro_V_X170_Inf", 1.70 - INT/2, 3.40, 0.00, INT, 0.80, H, mat_int, col_int)
    add_box("Muro_V_X300_Sup", 3.00 - INT/2, 0.00, 0.00, INT, 3.50, H, mat_int, col_int)
    add_box("Muro_V_X300_Inf", 3.00 - INT/2, 4.20, 0.00, INT, 2.00, H, mat_int, col_int)
    add_box("Muro_V_X500_Cocina", 5.00 - INT/2, 4.20, 0.00, INT, 2.00, H, mat_int, col_int)

    # 4. Líneas horizontales internas
    add_box("Muro_H_Y200_Placard1", 0.00, 2.00 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)
    add_box("Muro_H_Y200_Mocheta_Izq", 1.70, 2.00 - INT/2, 0.00, 0.20, INT, H, mat_int, col_int)
    add_box("Muro_H_Y200_Mocheta_Der", 2.80, 2.00 - INT/2, 0.00, 0.20, INT, H, mat_int, col_int)

    add_box("Muro_H_Y250_Placard1_Bano", 0.00, 2.50 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)
    add_box("Muro_H_Y370_Bano_Placard2", 0.00, 3.70 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)

    add_box("Muro_H_Y420_Placard2", 0.00, 4.20 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cuarto_Izq", 1.70, 4.20 - INT/2, 0.00, 0.20, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cuarto_Der", 2.80, 4.20 - INT/2, 0.00, 0.20, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cocina_Izq", 3.00, 4.20 - INT/2, 0.00, 0.25, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cocina_Der", 4.65, 4.20 - INT/2, 0.00, 0.35, INT, H, mat_int, col_int)

    print("Departamento 6.30m x 6.20m generado con éxito en Blender.")

if __name__ == "__main__":
    build_exact_apartment()
