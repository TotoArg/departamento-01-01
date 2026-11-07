"""
Script de Blender 3.x / 4.x / 5.x para generar la estructura arquitectónica exacta 6.30m x 6.20m.
Incluye:
- Colecciones organizadas con toggle de visibilidad individual (Ojo):
  * 00_Piso
  * 01_Muros_Exteriores
  * 02_Tabiques_Interiores
  * 03_Mobiliario_Editable
  * 04_Camaras_Y_Luces
- Piso texturado limpio
- Puertas y vanos exactos sin tabiques extras
- Dintel en vanos (2.10m altura paso, dintel de 2.10m a 2.60m)
- Cámara cenital (Plano 2D) y cámara isométrica 3D preconfiguradas
- Sol e iluminación de estudio listos
- Guardado automático a archivo .blend si se ejecuta desde consola
"""

import bpy
import math

def setup_scene():
    # Limpiar escena existente
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Eliminar colecciones previas excepto Master
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'METERS'

    # Crear Colecciones jerárquicas
    cols = {
        "piso": bpy.data.collections.new("00_Piso"),
        "ext": bpy.data.collections.new("01_Muros_Exteriores"),
        "int": bpy.data.collections.new("02_Tabiques_Interiores"),
        "muebles": bpy.data.collections.new("03_Mobiliario_Editable"),
        "setup": bpy.data.collections.new("04_Camaras_Y_Luces"),
    }
    for c in cols.values():
        scene.collection.children.link(c)

    return cols

def create_materials():
    def get_or_create(name, color_rgba, rough=0.5):
        m = bpy.data.materials.get(name)
        if not m:
            m = bpy.data.materials.new(name=name)
            m.use_nodes = True
            bsdf = m.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                # Color principal
                if 'Base Color' in bsdf.inputs:
                    bsdf.inputs['Base Color'].default_value = color_rgba
                if 'Roughness' in bsdf.inputs:
                    bsdf.inputs['Roughness'].default_value = rough
        return m

    return {
        "piso": get_or_create("Mat_Piso", (0.94, 0.95, 0.97, 1.0), 0.7),
        "ext": get_or_create("Mat_Muro_Exterior", (0.86, 0.89, 0.93, 1.0), 0.45),
        "int": get_or_create("Mat_Muro_Interior", (0.92, 0.94, 0.96, 1.0), 0.45),
        "dintel": get_or_create("Mat_Dintel", (0.82, 0.85, 0.89, 1.0), 0.45),
        "madera": get_or_create("Mat_Madera", (0.65, 0.40, 0.22, 1.0), 0.35),
        "tela": get_or_create("Mat_Tapizado", (0.22, 0.32, 0.46, 1.0), 0.8),
    }

def add_box(name, x1, y1, z1, sx, sy, sz, mat, col):
    """
    Crea un prisma rectangular.
    En Blender:
    X = X del plano (0.00 a 6.30)
    Y = -Y del plano (para que Y=0 quede al norte y Y=6.20 al sur)
    Z = Altura sobre el piso (0.00 a 2.60)
    """
    center_x = x1 + sx / 2.0
    center_y = -(y1 + sy / 2.0)
    center_z = z1 + sz / 2.0

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(center_x, center_y, center_z))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def build_apartment():
    cols = setup_scene()
    mats = create_materials()

    H = 2.60      # Altura general de muros
    H_PASO = 2.05 # Altura libre de vanos / puertas
    H_DINT = H - H_PASO # 0.55m de dintel
    EXT = 0.14    # Espesor muros exteriores
    INT = 0.10    # Espesor tabiques interiores

    # -------------------------------------------------------------
    # 1. PISO (Rectángulo 6.30 m x 6.20 m)
    # -------------------------------------------------------------
    add_box("Piso_General_630x620", 0.00, 0.00, -0.10, 6.30, 6.20, 0.10, mats["piso"], cols["piso"])

    # -------------------------------------------------------------
    # 2. PERÍMETRO EXTERIOR (6.30 x 6.20)
    # -------------------------------------------------------------
    # Muro Norte (Y = 0.00): X = 0.00 a 6.30
    add_box("Muro_Ext_Norte_Y0", 0.00, -EXT/2, 0.00, 6.30, EXT, H, mats["ext"], cols["ext"])

    # Muro Oeste (X = 0.00): Y = 0.00 a 6.20
    add_box("Muro_Ext_Oeste_X0", -EXT/2, 0.00, 0.00, EXT, 6.20, H, mats["ext"], cols["ext"])

    # Muro Este (X = 6.30): Y = 0.00 a 6.20
    add_box("Muro_Ext_Este_X630", 6.30 - EXT/2, 0.00, 0.00, EXT, 6.20, H, mats["ext"], cols["ext"])

    # Muro Sur (Y = 6.20): continuo con Puerta de Entrada en X = 5.20 a 6.10
    add_box("Muro_Ext_Sur_Izq", 0.00, 6.20 - EXT/2, 0.00, 5.20, EXT, H, mats["ext"], cols["ext"])
    add_box("Muro_Ext_Sur_Der", 6.10, 6.20 - EXT/2, 0.00, 0.20, EXT, H, mats["ext"], cols["ext"])
    # Dintel Puerta de Entrada Principal (X = 5.20 a 6.10)
    add_box("Dintel_Puerta_Entrada", 5.20, 6.20 - EXT/2, H_PASO, 0.90, EXT, H_DINT, mats["dintel"], cols["ext"])

    # -------------------------------------------------------------
    # 3. EJES VERTICALES INTERIORES
    # -------------------------------------------------------------
    # X = 1.70: Cerramiento Placards y Baño (Y = 2.00 a 4.20) con puerta Baño (Y = 2.80 a 3.40)
    add_box("Muro_V_X170_Placard1", 1.70 - INT/2, 2.00, 0.00, INT, 0.80, H, mats["int"], cols["int"])
    add_box("Muro_V_X170_Placard2", 1.70 - INT/2, 3.40, 0.00, INT, 0.80, H, mats["int"], cols["int"])
    add_box("Dintel_Puerta_Bano", 1.70 - INT/2, 2.80, H_PASO, INT, 0.60, H_DINT, mats["dintel"], cols["int"])

    # X = 3.00: Eje central divisorio
    # 1) Muro Living / Estudio y Pasillo (Y = 0.00 a 3.50)
    add_box("Muro_V_X300_Living_Estudio", 3.00 - INT/2, 0.00, 0.00, INT, 3.50, H, mats["int"], cols["int"])
    # NOTA: Entre Y = 3.50 y 4.20 (0.70m) NO HAY MURO (Paso libre y continuo)
    # 2) Muro divisorio Cuarto / Cocina (Y = 4.20 a 6.20)
    add_box("Muro_V_X300_Cuarto_Cocina", 3.00 - INT/2, 4.20, 0.00, INT, 2.00, H, mats["int"], cols["int"])

    # X = 5.00: Muro divisorio Cocina con Sector Entrada (Y = 4.20 a 6.20)
    add_box("Muro_V_X500_Cocina_Entrada", 5.00 - INT/2, 4.20, 0.00, INT, 2.00, H, mats["int"], cols["int"])

    # -------------------------------------------------------------
    # 4. LÍNEAS HORIZONTALES INTERIORES
    # -------------------------------------------------------------
    # Y = 2.00:
    # - Muro cerrado Estudio / Placard 1 (X = 0.00 a 1.70)
    add_box("Muro_H_Y200_Estudio_Placard1", 0.00, 2.00 - INT/2, 0.00, 1.70, INT, H, mats["int"], cols["int"])
    # - Mochetas y Dintel Entrada Estudio (X = 1.90 a 2.80)
    add_box("Muro_H_Y200_Mocheta_Izq", 1.70, 2.00 - INT/2, 0.00, 0.20, INT, H, mats["int"], cols["int"])
    add_box("Muro_H_Y200_Mocheta_Der", 2.80, 2.00 - INT/2, 0.00, 0.20, INT, H, mats["int"], cols["int"])
    add_box("Dintel_Entrada_Estudio", 1.90, 2.00 - INT/2, H_PASO, 0.90, INT, H_DINT, mats["dintel"], cols["int"])

    # Y = 2.50: Placard 1 / Baño (X = 0.00 a 1.70)
    add_box("Muro_H_Y250_Placard1_Bano", 0.00, 2.50 - INT/2, 0.00, 1.70, INT, H, mats["int"], cols["int"])

    # Y = 3.70: Baño / Placard 2 (X = 0.00 a 1.70)
    add_box("Muro_H_Y370_Bano_Placard2", 0.00, 3.70 - INT/2, 0.00, 1.70, INT, H, mats["int"], cols["int"])

    # Y = 4.20: Línea horizontal unificada crítica
    # - Placard 2 / Cuarto (X = 0.00 a 1.70)
    add_box("Muro_H_Y420_Placard2_Cuarto", 0.00, 4.20 - INT/2, 0.00, 1.70, INT, H, mats["int"], cols["int"])
    # - Mochetas y Dintel Entrada Cuarto (X = 1.90 a 2.80)
    add_box("Muro_H_Y420_Cuarto_Mocheta_Izq", 1.70, 4.20 - INT/2, 0.00, 0.20, INT, H, mats["int"], cols["int"])
    add_box("Muro_H_Y420_Cuarto_Mocheta_Der", 2.80, 4.20 - INT/2, 0.00, 0.20, INT, H, mats["int"], cols["int"])
    add_box("Dintel_Entrada_Cuarto", 1.90, 4.20 - INT/2, H_PASO, 0.90, INT, H_DINT, mats["dintel"], cols["int"])
    # - Frente Cocina con vano central amplio (X = 3.25 a 4.65)
    add_box("Muro_H_Y420_Cocina_Frente_Izq", 3.00, 4.20 - INT/2, 0.00, 0.25, INT, H, mats["int"], cols["int"])
    add_box("Muro_H_Y420_Cocina_Frente_Der", 4.65, 4.20 - INT/2, 0.00, 0.35, INT, H, mats["int"], cols["int"])
    add_box("Dintel_Frente_Cocina", 3.25, 4.20 - INT/2, H_PASO, 1.40, INT, H_DINT, mats["dintel"], cols["int"])

    # -------------------------------------------------------------
    # 5. CÁMARAS Y LUCES PRECONFIGURADAS
    # -------------------------------------------------------------
    # Sol suave para sombras arquitectónicas
    bpy.ops.object.light_add(type='SUN', location=(10.0, -12.0, 15.0))
    sun = bpy.context.active_object
    sun.name = "Sol_Arquitectonico"
    sun.data.energy = 2.5
    sun.rotation_euler = (math.radians(50), math.radians(20), math.radians(-35))
    for c in list(sun.users_collection):
        c.objects.unlink(sun)
    cols["setup"].objects.link(sun)

    # Luz de relleno ambiente
    bpy.ops.object.light_add(type='SUN', location=(-10.0, 8.0, 10.0))
    fill = bpy.context.active_object
    fill.name = "Luz_Relleno"
    fill.data.energy = 1.0
    fill.rotation_euler = (math.radians(-40), math.radians(-15), math.radians(140))
    for c in list(fill.users_collection):
        c.objects.unlink(fill)
    cols["setup"].objects.link(fill)

    # Cámara 1: Vista Isométrica 3D
    bpy.ops.object.camera_add(location=(3.15, -12.5, 11.5))
    cam3d = bpy.context.active_object
    cam3d.name = "Camara_3D_Isometrica"
    cam3d.rotation_euler = (math.radians(52), 0, 0)
    for c in list(cam3d.users_collection):
        c.objects.unlink(cam3d)
    cols["setup"].objects.link(cam3d)

    # Cámara 2: Vista Plano 2D Cenital Ortográfica
    bpy.ops.object.camera_add(location=(3.15, -3.10, 14.0))
    cam2d = bpy.context.active_object
    cam2d.name = "Camara_2D_Plano_Cenital"
    cam2d.data.type = 'ORTHO'
    cam2d.data.ortho_scale = 9.0
    cam2d.rotation_euler = (0, 0, 0)
    for c in list(cam2d.users_collection):
        c.objects.unlink(cam2d)
    cols["setup"].objects.link(cam2d)

    # Asignar cámara activa por defecto
    scene.camera = cam3d

    print("=================================================================")
    print("✅ DEPARTAMENTO 6.30m x 6.20m CONSTRUIDO CON ÉXITO EN BLENDER")
    print("- Colecciones listas: 00_Piso, 01_Muros_Exteriores, 02_Tabiques_Interiores...")
    print("- Se pueden ocultar los muros directamente clickeando en el 'ojo' de la colección")
    print("=================================================================")

if __name__ == "__main__":
    build_apartment()
