"""
Script Python para Blender 3.x / 4.x
Construye automáticamente la estructura 3D del Departamento 01-01 (1° Piso)
Distribución exacta y verificada según croquis y videos:

- Lateral Derecho: Living Comedor a lo largo con techos altos de madera y vigas
- Acceso: Puerta de entrada principal en el frente derecho hacia el Living
- Centro Inferior: Cocina semi-integrada
- Centro: Pasillo de circulación hacia sector privado
- Lateral Izquierdo (Frente a Fondo):
    1. Cuarto Principal (Dormitorio) con Placard embutido
    2. Baño Completo con Bañera, Bidet, Inodoro y Vanitory (entre ambos placards)
    3. Estudio Gamer / Segundo Cuarto con Placard y amplio escritorio
- Propuestas de Reforma incluidas en Colecciones separadas:
    * Cocina Abierta con Isla Desayunadora moderna
    * Entrepiso / Mezzanine Loft en el Estudio aprovechando la altura libre
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

    col_muros = get_col("01_Muros_Estructurales")
    col_tabiques = get_col("02_Tabiques_Distribucion_Actual")
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
    mat_fabric = create_mat("Gris_Tapizado", (0.35, 0.40, 0.45), rough=0.7)

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

    # --- 1. PISO ---
    add_box("Piso_General", 0.0, 0.0, -0.05, 8.00, 7.20, 0.05, col_muros, mat_floor)

    # --- 2. MUROS PERIMETRALES EXTERIORES (Espesor 0.20m) ---
    # Muro Sur (Frente / Entrada al Living)
    add_box("Muro_Sur_Izquierda", -0.20, 7.20, 0.0, 5.80, 0.20, 2.70, col_muros, mat_wall)
    add_box("Muro_Sur_Dintel_Entrada", 5.60, 7.20, 2.10, 0.90, 0.20, 0.60, col_muros, mat_wall)
    add_box("Muro_Sur_Derecha", 6.50, 7.20, 0.0, 1.70, 0.20, 2.70, col_muros, mat_wall)

    # Muro Norte (Fondo)
    add_box("Muro_Norte_Fondo", -0.20, -0.20, 0.0, 8.40, 0.20, 3.20, col_muros, mat_wall)
    # Muro Oeste (Lateral Izquierdo)
    add_box("Muro_Oeste_Lateral", -0.20, 0.0, 0.0, 0.20, 7.20, 2.80, col_muros, mat_wall)
    # Muro Este (Lateral Derecho Living)
    add_box("Muro_Este_Lateral_Living", 8.00, 0.0, 0.0, 0.20, 7.20, 2.70, col_muros, mat_wall)

    # --- 3. TABIQUES INTERIORES - ESTADO ACTUAL (0.12m) ---
    # Gran Tabique longitudinal divisorio entre Living y Pasillo/Habitaciones
    add_box("Tabique_Living_Norte", 3.60, 0.0, 0.0, 0.12, 3.60, 3.20, col_tabiques, mat_wall)
    add_box("Dintel_Paso_Living_Pasillo", 3.60, 3.60, 2.10, 0.12, 1.10, 1.10, col_tabiques, mat_wall)
    add_box("Tabique_Living_Cocina", 3.60, 4.70, 0.0, 0.12, 2.50, 3.00, col_tabiques, mat_wall)

    # Tabique Cocina hacia Pasillo
    add_box("Tabique_Cocina_Pasillo", 2.20, 5.20, 0.0, 0.12, 2.00, 2.80, col_tabiques, mat_wall)
    add_box("Dintel_Paso_Cocina", 2.20, 5.20, 2.10, 1.40, 0.12, 0.70, col_tabiques, mat_wall)

    # Tabiques Sector Privado Izquierdo
    # 1. Cuarto Principal
    add_box("Tabique_Cuarto_Placard", 0.00, 5.00, 0.0, 2.20, 0.10, 2.80, col_tabiques, mat_wall)
    add_box("Frente_Placard_Cuarto", 0.00, 4.40, 0.0, 2.20, 0.60, 2.50, col_tabiques, mat_wood)
    add_box("Tabique_Acceso_Cuarto", 2.20, 4.40, 0.0, 0.12, 0.80, 2.80, col_tabiques, mat_wall)

    # 2. Baño Completo (en el centro)
    add_box("Tabique_Bano_Norte", 0.00, 2.80, 0.0, 2.20, 0.10, 3.00, col_tabiques, mat_wall)
    add_box("Tabique_Acceso_Bano", 2.20, 2.80, 0.0, 0.12, 1.60, 3.00, col_tabiques, mat_wall)

    # 3. Estudio Gamer (fondo)
    add_box("Frente_Placard_Estudio", 0.00, 2.20, 0.0, 2.20, 0.60, 2.50, col_tabiques, mat_wood)
    add_box("Tabique_Acceso_Estudio", 2.20, 0.00, 0.0, 0.12, 2.20, 3.20, col_tabiques, mat_wall)

    # --- 4. PROPUESTA A: COCINA ABIERTA CON ISLA ---
    # En esta propuesta se elimina el tabique ciego entre Cocina y Living
    add_box("PropA_Isla_Desayunadora", 3.30, 5.30, 0.0, 0.85, 1.80, 0.92, col_isla, mat_granite)
    # Conserva la separación de las habitaciones privadas
    add_box("PropA_Tabique_Privado", 3.60, 0.0, 0.0, 0.12, 3.60, 3.20, col_isla, mat_wall)
    col_isla.hide_viewport = True
    col_isla.hide_render = True

    # --- 5. PROPUESTA B: ENTREPISO / LOFT EN ESTUDIO (3.85m) ---
    add_box("PropB_Entrepiso_Plataforma", 0.10, 0.10, 2.25, 2.10, 1.80, 0.12, col_loft, mat_wood)
    add_box("PropB_Columna_Hierro", 2.10, 1.90, 0.0, 0.08, 0.08, 2.25, col_loft, mat_iron)
    add_box("PropB_Baranda_Hierro", 0.10, 1.90, 2.37, 2.10, 0.05, 0.85, col_loft, mat_iron)
    col_loft.hide_viewport = True
    col_loft.hide_render = True

    # --- 6. EQUIPAMIENTO REAL SEGÚN VIDEOS ---
    # Cocina
    add_box("Mesada_L_Granito", 2.35, 6.55, 0.0, 1.25, 0.60, 0.88, col_muebles, mat_granite)
    add_box("Mesada_L_Bacha", 2.35, 5.30, 0.0, 0.60, 1.25, 0.88, col_muebles, mat_granite)
    add_box("Heladera", 3.05, 5.30, 0.0, 0.55, 0.60, 1.75, col_muebles, mat_white)
    add_box("Termotanque_Sherman", 2.35, 7.00, 1.30, 0.40, 0.20, 0.85, col_muebles, mat_white)

    # Baño
    add_box("Banera", 0.10, 2.95, 0.0, 0.70, 1.40, 0.45, col_muebles, mat_white)
    add_box("Inodoro", 1.05, 2.95, 0.0, 0.40, 0.55, 0.42, col_muebles, mat_white)
    add_box("Bidet", 1.65, 2.95, 0.0, 0.38, 0.55, 0.40, col_muebles, mat_white)
    add_box("Vanitory", 0.10, 3.75, 0.0, 0.55, 0.60, 0.85, col_muebles, mat_wood)

    # Cuarto Principal
    add_box("Cama_Matrimonial", 0.30, 5.35, 0.0, 1.50, 1.75, 0.45, col_muebles, mat_fabric)
    add_box("Mesa_Luz", 1.85, 5.35, 0.0, 0.35, 0.40, 0.55, col_muebles, mat_wood)

    # Estudio Gamer
    add_box("Escritorio_Gamer_L", 0.10, 0.10, 0.0, 1.50, 0.70, 0.75, col_muebles, mat_iron)
    add_box("Retorno_Escritorio", 0.10, 0.80, 0.0, 0.60, 0.90, 0.75, col_muebles, mat_iron)

    # Living
    add_box("Sillon_Living", 4.80, 4.20, 0.0, 2.20, 0.90, 0.75, col_muebles, mat_fabric)
    add_box("Mesa_Comedor", 5.20, 1.80, 0.0, 1.40, 0.85, 0.76, col_muebles, mat_wood)
    add_box("Calefactor_Gas_Tiro", 7.85, 2.60, 0.0, 0.15, 0.60, 0.65, col_muebles, mat_iron)

    # --- 7. TECHO Y VIGAS DE MADERA A LA VISTA ---
    for i in range(12):
        y_beam = 0.30 + i * 0.58
        add_box(f"Viga_Madera_{i+1}", -0.20, y_beam, 2.70 + (i*0.04), 8.40, 0.08, 0.14, col_techo, mat_beam)

    print("Modelo 3D de Departamento 01-01 generado con éxito en Blender!")

if __name__ == "__main__":
    build_real_apartment()
