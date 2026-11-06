"""
Script Python para Blender 3.x / 4.x
Construye automáticamente la estructura 3D del Departamento 01-01 (1° Piso)
Edificio Glaciares II - Calle Günter Plüschow 235, El Calafate
Unidad Funcional N° 6, Depto "A", Polígono 01-01 (54,16 m² oficiales)

Distribución interior 100% fiel al plano esquemático 2D:
- Estudio con Placard interior propio y umbral de acceso horizontal al Pasillo
- Cuarto con Placard interior propio y umbral de acceso horizontal al Pasillo
- Baño completo en el centro flanqueado por las espaldas ciegas de ambos placards
- Pasillo con acceso directo al Baño y apertura fluida hacia el Living
- Cocina con acceso desde la circulación y tabique divisorio al Living
- Gran Living longitudinal con entrada principal en la esquina inferior derecha
"""

import bpy
import math

def build_real_apartment():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0

    def get_col(name):
        if name in bpy.data.collections: return bpy.data.collections[name]
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        return c

    col_muros = get_col("01_Muros_Estructurales_Oficiales")
    col_tabiques = get_col("02_Tabiques_Distribucion_Actual")
    col_isla = get_col("03_Propuesta_Cocina_Abierta")
    col_loft = get_col("04_Propuesta_Entrepiso_Loft")
    col_techo = get_col("05_Techo_Madera_Vigas")
    col_muebles = get_col("06_Equipamiento_Real")

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

    # 1. PISO OFICIAL (54.16 m2)
    add_box("Piso_Oeste", 0.00, 0.00, -0.05, 5.10, 6.20, 0.05, col_muros, mat_floor)
    add_box("Piso_Ducto_Frente", 5.10, 0.00, -0.05, 0.40, 5.50, 0.05, col_muros, mat_floor)
    add_box("Piso_Centro", 5.50, 0.00, -0.05, 1.50, 6.20, 0.05, col_muros, mat_floor)
    add_box("Piso_Este_Living", 7.00, 1.40, -0.05, 2.30, 4.80, 0.05, col_muros, mat_floor)

    # 2. MUROS EXTERIORES (54.16 m2)
    add_box("Muro_Norte_Medianera", -0.20, -0.20, 0.0, 7.20, 0.20, 3.20, col_muros, mat_wall)
    add_box("Muro_Saliente_Palier", 7.00, -0.20, 0.0, 0.20, 1.60, 3.00, col_muros, mat_wall)
    add_box("Muro_Acceso_Palier", 7.00, 1.40, 0.0, 2.30, 0.20, 2.70, col_muros, mat_wall)
    add_box("Muro_Este_Living", 9.30, 1.40, 0.0, 0.20, 4.80, 2.70, col_muros, mat_wall)
    add_box("Muro_Sur_Living", 5.50, 6.20, 0.0, 4.00, 0.20, 2.80, col_muros, mat_wall)
    add_box("Ducto_Este", 5.50, 5.50, 0.0, 0.10, 0.70, 3.20, col_muros, mat_wall)
    add_box("Ducto_Fondo", 5.10, 5.50, 0.0, 0.40, 0.10, 3.20, col_muros, mat_wall)
    add_box("Ducto_Oeste", 5.10, 5.50, 0.0, 0.10, 0.70, 3.20, col_muros, mat_wall)
    add_box("Muro_Sur_Cuarto_Cocina", -0.20, 6.20, 0.0, 5.30, 0.20, 2.80, col_muros, mat_wall)
    add_box("Muro_Oeste_Calle_Gunter", -0.20, 0.00, 0.0, 0.20, 6.20, 3.00, col_muros, mat_wall)

    # 3. TABIQUES INTERIORES
    add_box("Tabique_Estudio_Living", 3.50, 0.00, 0.0, 0.12, 2.10, 3.20, col_tabiques, mat_wall)
    add_box("Tabique_Pasillo_Living_Norte", 3.50, 2.10, 0.0, 0.12, 1.40, 3.00, col_tabiques, mat_wall)
    add_box("Dintel_Paso_Pasillo_Living", 3.50, 3.50, 2.10, 0.12, 1.10, 0.90, col_tabiques, mat_wall)
    add_box("Tabique_Pasillo_Living_Sur", 3.50, 4.60, 0.0, 0.12, 0.30, 3.00, col_tabiques, mat_wall)

    # Estudio
    add_box("Tabique_Bano_Estudio_Ciego", 0.00, 2.70, 0.0, 2.40, 0.10, 3.00, col_tabiques, mat_wall)
    add_box("Tabique_Placard_Estudio_Pasillo", 2.40, 2.10, 0.0, 0.12, 0.60, 3.00, col_tabiques, mat_wall)
    add_box("Placard_Interior_Estudio", 0.10, 2.15, 0.0, 2.20, 0.55, 2.45, col_muebles, mat_wood)
    add_box("Dintel_Acceso_Estudio", 2.40, 2.10, 2.10, 1.10, 0.12, 0.90, col_tabiques, mat_wall)

    # Baño
    add_box("Tabique_Bano_Pasillo_Norte", 2.40, 2.70, 0.0, 0.12, 0.40, 3.00, col_tabiques, mat_wall)
    add_box("Dintel_Puerta_Bano", 2.40, 3.10, 2.10, 0.12, 0.80, 0.90, col_tabiques, mat_wall)
    add_box("Tabique_Bano_Pasillo_Sur", 2.40, 3.90, 0.0, 0.12, 0.40, 3.00, col_tabiques, mat_wall)

    # Cuarto
    add_box("Tabique_Bano_Cuarto_Ciego", 0.00, 4.30, 0.0, 2.40, 0.10, 2.80, col_tabiques, mat_wall)
    add_box("Tabique_Placard_Cuarto_Pasillo", 2.40, 4.30, 0.0, 0.12, 0.60, 2.80, col_tabiques, mat_wall)
    add_box("Placard_Interior_Cuarto", 0.10, 4.35, 0.0, 2.20, 0.55, 2.45, col_muebles, mat_wood)
    add_box("Dintel_Acceso_Cuarto", 2.40, 4.90, 2.10, 1.10, 0.12, 0.70, col_tabiques, mat_wall)
    add_box("Tabique_Cuarto_Cocina", 2.40, 4.90, 0.0, 0.12, 1.30, 2.80, col_tabiques, mat_wall)

    # Cocina
    add_box("Dintel_Acceso_Cocina", 3.50, 4.90, 2.10, 1.30, 0.12, 0.70, col_tabiques, mat_wall)
    add_box("Tabique_Cocina_Living", 4.80, 4.90, 0.0, 0.12, 1.30, 2.80, col_tabiques, mat_wall)

    # Propuestas
    add_box("Prop1_Isla_Desayunadora", 4.50, 4.90, 0.0, 0.85, 1.80, 0.92, col_isla, mat_granite)
    col_isla.hide_viewport = True
    col_isla.hide_render = True

    add_box("Prop2_Entrepiso_Plataforma", 0.10, 0.10, 2.25, 2.30, 1.80, 0.12, col_loft, mat_wood)
    add_box("Prop2_Columna_Hierro", 2.30, 1.90, 0.0, 0.08, 0.08, 2.25, col_loft, mat_iron)
    add_box("Prop2_Baranda", 0.10, 1.90, 2.37, 2.30, 0.05, 0.85, col_loft, mat_iron)
    col_loft.hide_viewport = True
    col_loft.hide_render = True

    # Mobiliario
    add_box("Mesada_Cocina", 3.65, 5.60, 0.0, 1.35, 0.60, 0.88, col_muebles, mat_granite)
    add_box("Cocina_Gas", 2.80, 5.60, 0.0, 0.55, 0.60, 0.86, col_muebles, mat_white)
    add_box("Termotanque_Sherman", 4.50, 5.60, 1.30, 0.35, 0.35, 0.85, col_muebles, mat_white)

    add_box("Banera", 0.10, 2.85, 0.0, 0.70, 1.40, 0.45, col_muebles, mat_white)
    add_box("Inodoro", 1.40, 2.85, 0.0, 0.40, 0.55, 0.42, col_muebles, mat_white)
    add_box("Bidet", 1.95, 2.85, 0.0, 0.38, 0.55, 0.40, col_muebles, mat_white)
    add_box("Vanitory", 1.40, 3.65, 0.0, 0.60, 0.50, 0.85, col_muebles, mat_wood)

    add_box("Cama_Doble", 0.50, 5.05, 0.0, 1.40, 1.85, 0.45, col_muebles, mat_fabric)
    add_box("Mesa_Luz", 1.95, 5.60, 0.0, 0.40, 0.45, 0.55, col_muebles, mat_wood)

    add_box("Escritorio_Gamer_L", 0.10, 0.10, 0.0, 1.50, 0.70, 0.75, col_muebles, mat_iron)
    add_box("Retorno_Escritorio", 0.10, 0.80, 0.0, 0.60, 0.90, 0.75, col_muebles, mat_iron)

    add_box("Sillon_Living", 5.60, 4.00, 0.0, 2.10, 0.90, 0.75, col_muebles, mat_fabric)
    add_box("Mesa_Comedor", 6.80, 2.00, 0.0, 1.40, 0.85, 0.76, col_muebles, mat_wood)
    add_box("Calefactor_Gas_Tiro", 9.15, 2.60, 0.0, 0.15, 0.60, 0.65, col_muebles, mat_iron)

    for i in range(12):
        y_beam = 0.25 + i * 0.52
        add_box(f"Viga_Madera_{i+1}", -0.20, y_beam, 2.70 + (i*0.03), 9.60, 0.08, 0.14, col_techo, mat_beam)

    print("Modelo 3D de Departamento 01-01 generado con éxito en Blender!")

if __name__ == "__main__":
    build_real_apartment()
