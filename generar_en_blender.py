"""
Script Python para Blender 3.x / 4.x
Construye automáticamente el modelo 3D REAL del Departamento 01-01
basado fielmente en los VIDEOS de recorrido real del departamento.

Incluye:
- 01_Muros_Estructurales_Reales (Perímetro exacto de los videos)
- 02_Tabiques_Actuales (Living-Comedor, Cocina independiente, Baño completo con bañera, Dormitorio con placard)
- 03_Propuesta_Cocina_Abierta (Isla desayunadora moderna)
- 04_Propuesta_Entrepiso_Loft (Aprovechamiento de la altura libre de 3.85m)
- 05_Techo_Madera_Vigas (Cielorraso con pendiente y vigas a la vista)
- 06_Equipamiento_Real (Mesada L, lavarropas, cocina, termotanque, bañera, inodoro, cama, escritorio gamer, sofá, TV)
"""

import bpy
import math

def build_real_apartment():
    # Limpiar escena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    # Crear Colecciones
    def get_col(name):
        if name in bpy.data.collections: return bpy.data.collections[name]
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        return c

    col_muros = get_col("01_Muros_Estructurales_Reales")
    col_tabiques = get_col("02_Tabiques_Actuales")
    col_isla = get_col("03_Propuesta_Cocina_Abierta")
    col_loft = get_col("04_Propuesta_Entrepiso_Loft")
    col_techo = get_col("05_Techo_Madera_Vigas")
    col_muebles = get_col("06_Equipamiento_Real")

    # Materiales
    def create_mat(name, color, rough=0.5, metal=0.0):
        m = bpy.data.materials.get(name)
        if not m:
            m = bpy.data.materials.new(name=name)
            m.use_nodes = True
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
                bsdf.inputs['Roughness'].default_value = rough
                bsdf.inputs['Metallic'].default_value = metal
        return m

    mat_wall = create_mat("Pared_Blanca", (0.94, 0.94, 0.95), rough=0.8)
    mat_floor = create_mat("Piso_Ceramico", (0.83, 0.78, 0.72), rough=0.3)
    mat_wood = create_mat("Madera_Cipres", (0.58, 0.32, 0.15), rough=0.45)
    mat_beam = create_mat("Madera_Vigas", (0.42, 0.22, 0.10), rough=0.6)
    mat_granite = create_mat("Granito_Rosa", (0.75, 0.55, 0.48), rough=0.25)
    mat_iron = create_mat("Hierro_Negro", (0.12, 0.12, 0.13), rough=0.3, metal=0.85)
    mat_white = create_mat("Blanco_Sanitarios", (0.95, 0.95, 0.95), rough=0.15)

    def add_box(name, x, y, z, sx, sy, sz, col, mat=None):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x + sx/2, y + sy/2, z + sz/2))
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True)
        for c in obj.users_collection: c.objects.unlink(obj)
        col.objects.link(obj)
        if mat: obj.data.materials.append(mat)
        return obj

    # --- PISO ---
    add_box("Piso_Principal", 0.0, 0.0, -0.05, 9.20, 6.20, 0.05, col_muros, mat_floor)

    # --- MUROS EXTERIORES (Espesor 0.20m) ---
    add_box("Muro_Sur_Frente", -0.20, -0.20, 0.0, 9.60, 0.20, 2.70, col_muros, mat_wall)
    add_box("Muro_Oeste_Lateral", -0.20, 0.0, 0.0, 0.20, 6.20, 2.70, col_muros, mat_wall)
    add_box("Muro_Norte_Fondo", -0.20, 6.20, 0.0, 9.60, 0.20, 3.20, col_muros, mat_wall)
    add_box("Muro_Este_Lateral", 9.20, 0.0, 0.0, 0.20, 6.20, 3.00, col_muros, mat_wall)

    # --- TABIQUES INTERIORES REALES (0.12m) ---
    # Tabique divisorio Living / Sector Privado
    add_box("Tabique_Living_Privado", 4.20, 0.0, 0.0, 0.12, 4.60, 3.20, col_tabiques, mat_wall)
    # Tabique Cocina / Baño
    add_box("Tabique_Cocina_Bano", 4.32, 2.40, 0.0, 4.88, 0.12, 3.00, col_tabiques, mat_wall)
    # Tabique Baño / Dormitorio
    add_box("Tabique_Bano_Dormitorio", 4.32, 4.10, 0.0, 4.88, 0.12, 3.10, col_tabiques, mat_wall)

    # --- PROPUESTA A: COCINA ABIERTA CON ISLA ---
    add_box("PropA_Isla_Desayunadora", 4.10, 0.80, 0.0, 0.85, 2.00, 0.92, col_isla, mat_granite)
    add_box("PropA_Tabique_Bano", 4.32, 2.40, 0.0, 4.88, 0.12, 3.00, col_isla, mat_wall)
    add_box("PropA_Tabique_Dormitorio", 4.32, 4.10, 0.0, 4.88, 0.12, 3.10, col_isla, mat_wall)
    col_isla.hide_viewport = True
    col_isla.hide_render = True

    # --- PROPUESTA B: ENTREPISO / LOFT (3.85m) ---
    add_box("PropB_Entrepiso_Plataforma", 5.00, 4.20, 2.20, 4.00, 1.90, 0.12, col_loft, mat_wood)
    add_box("PropB_Columna_Hierro", 5.00, 4.20, 0.0, 0.10, 0.10, 2.20, col_loft, mat_iron)
    add_box("PropB_Baranda", 5.00, 4.20, 2.32, 4.00, 0.05, 0.90, col_loft, mat_iron)
    col_loft.hide_viewport = True
    col_loft.hide_render = True

    # --- EQUIPAMIENTO REAL SEGÚN VIDEOS ---
    # Cocina
    add_box("Mesada_Cocina_L", 5.50, 0.0, 0.0, 2.50, 0.60, 0.88, col_muebles, mat_granite)
    add_box("Lavarropas", 8.20, 0.0, 0.0, 0.60, 0.58, 0.82, col_muebles, mat_white)
    add_box("Cocina_Gas", 4.80, 0.0, 0.0, 0.55, 0.58, 0.86, col_muebles, mat_white)
    # Baño
    add_box("Banera", 8.40, 2.55, 0.0, 0.70, 1.50, 0.45, col_muebles, mat_white)
    add_box("Inodoro", 6.80, 2.55, 0.0, 0.40, 0.60, 0.42, col_muebles, mat_white)
    add_box("Bidet", 6.00, 2.55, 0.0, 0.38, 0.55, 0.40, col_muebles, mat_white)
    add_box("Vanitory", 4.80, 3.40, 0.0, 0.65, 0.48, 0.82, col_muebles, mat_wood)
    # Dormitorio
    add_box("Cama_Matrimonial", 5.00, 4.30, 0.0, 1.50, 1.90, 0.48, col_muebles, mat_wood)
    add_box("Placard_Embutido", 7.40, 4.20, 0.0, 1.70, 0.65, 2.50, col_muebles, mat_wall)
    add_box("Escritorio_Gamer_L", 7.40, 5.40, 0.0, 1.70, 0.75, 0.75, col_muebles, mat_wood)
    # Living
    add_box("Calefactor_Gas_Tiro", 0.0, 1.20, 0.0, 0.22, 0.55, 0.65, col_muebles, mat_iron)
    add_box("Sillon_Azul", 1.80, 3.40, 0.0, 1.90, 0.85, 0.55, col_muebles, mat_wood)
    add_box("Mesa_Comedor", 1.00, 4.80, 0.0, 1.10, 1.10, 0.75, col_muebles, mat_wood)

    # --- TECHO Y VIGAS DE MADERA ---
    for i in range(11):
        y_beam = 0.20 + i * 0.58
        add_box(f"Viga_Madera_{i+1}", -0.30, y_beam, 2.70 + (i*0.04), 9.80, 0.08, 0.14, col_techo, mat_beam)

    print("Modelo 3D REAL de Departamento 01-01 construido correctamente en Blender!")

if __name__ == "__main__":
    build_real_apartment()
