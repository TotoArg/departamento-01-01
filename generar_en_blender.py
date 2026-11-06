"""
Script Python para Blender 3.x / 4.x
Construye automáticamente el Departamento con la especificación geométrica exacta:
- Perímetro rectangular cerrado: 7.00 m (X: 0.00 a 7.00) × 6.20 m (Y: 0.00 arriba a 6.20 abajo).
- Pared inferior continua en Y = 6.20 con Puerta de Entrada en X = 5.40 a 6.20.
- Ejes verticales: X = 1.70 (Placards y Baño), X = 3.00 (Muro central 0.00..3.90, paso abierto 3.90..4.60, y muro Cuarto/Cocina 4.60..6.20), X = 4.60 (Muro derecho Cocina).
- Ejes horizontales: Y = 0.00, Y = 2.30, Y = 2.80, Y = 4.00, Y = 4.60 (línea unificada Cuarto y Cocina), Y = 6.20.
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

    col_ext = get_col("01_Perimetro_Exterior_7x62")
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
        # En Blender: X = X (0 a 7.00), Y = -Y_plano (para que Y=0 esté arriba y Y=6.20 abajo), Z = altura
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

    # 1. Piso (7.00 x 6.20)
    add_box("Piso_7x62", 0.00, 0.00, -0.08, 7.00, 6.20, 0.08, mat_piso, col_ext)

    # 2. Perímetro exterior
    add_box("Muro_Sup_Y0", 0.00, -EXT/2, 0.00, 7.00, EXT, H, mat_ext, col_ext)
    add_box("Muro_Izq_X0", -EXT/2, 0.00, 0.00, EXT, 6.20, H, mat_ext, col_ext)
    add_box("Muro_Der_X7", 7.00 - EXT/2, 0.00, 0.00, EXT, 6.20, H, mat_ext, col_ext)
    add_box("Muro_Inf_Izq_Y620", 0.00, 6.20 - EXT/2, 0.00, 5.40, EXT, H, mat_ext, col_ext)
    add_box("Muro_Inf_Der_Y620", 6.20, 6.20 - EXT/2, 0.00, 0.80, EXT, H, mat_ext, col_ext)

    # 3. Ejes verticales internos
    add_box("Muro_V_X170_Sup", 1.70 - INT/2, 2.00, 0.00, INT, 0.80, H, mat_int, col_int)
    add_box("Muro_V_X170_Inf", 1.70 - INT/2, 3.40, 0.00, INT, 0.80, H, mat_int, col_int)
    add_box("Muro_V_X300_Sup", 3.00 - INT/2, 0.00, 0.00, INT, 3.50, H, mat_int, col_int)
    add_box("Muro_V_X300_Inf", 3.00 - INT/2, 4.20, 0.00, INT, 2.00, H, mat_int, col_int)
    add_box("Muro_V_X460_Cocina", 4.60 - INT/2, 4.20, 0.00, INT, 2.00, H, mat_int, col_int)

    # 4. Líneas horizontales internas (Simetría Estudio = Cuarto = 3.00 x 2.00)
    add_box("Muro_H_Y200_Placard1", 0.00, 2.00 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)
    add_box("Muro_H_Y200_Mocheta_Izq", 1.70, 2.00 - INT/2, 0.00, 0.16, INT, H, mat_int, col_int)
    add_box("Muro_H_Y200_Mocheta_Der", 2.82, 2.00 - INT/2, 0.00, 0.18, INT, H, mat_int, col_int)

    add_box("Muro_H_Y250_Placard1_Bano", 0.00, 2.50 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)
    add_box("Muro_H_Y370_Bano_Placard2", 0.00, 3.70 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)

    add_box("Muro_H_Y420_Placard2_Cuarto", 0.00, 4.20 - INT/2, 0.00, 1.70, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cuarto_Mocheta_Izq", 1.70, 4.20 - INT/2, 0.00, 0.16, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cuarto_Mocheta_Der", 2.82, 4.20 - INT/2, 0.00, 0.18, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cocina_Mocheta_Izq", 3.00, 4.20 - INT/2, 0.00, 0.18, INT, H, mat_int, col_int)
    add_box("Muro_H_Y420_Cocina_Mocheta_Der", 4.38, 4.20 - INT/2, 0.00, 0.22, INT, H, mat_int, col_int)

    print("Departamento 7.00m x 6.20m generado con éxito en Blender.")

if __name__ == "__main__":
    build_exact_apartment()
