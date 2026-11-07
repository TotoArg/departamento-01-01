"""
Script de Blender 3.x / 4.x / 5.x para generar la estructura arquitectónica exacta 6.30m x 7.00m (Planta en "L").
Incluye:
- Colecciones organizadas con toggle de visibilidad individual (Ojo):
  * 00_Piso
  * 01_Muros_Exteriores
  * 02_Tabiques_Interiores
  * 03_Mobiliario_Editable
  * 04_Camaras_Y_Luces
- Piso en "L" + bloque de Palier Edificio ([5.20, 5.70] a [6.30, 7.00])
- Puertas y vanos abiertos exactos sin tabiques ni pasillos falsos
- Dintel en puertas (2.05m altura paso, dintel de 2.05m a 2.60m)
- Cámara cenital (Plano 2D) y cámara isométrica 3D preconfiguradas
"""

import bpy
import math


def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = 'METERS'

    cols = {
        "piso": bpy.data.collections.new("00_Piso"),
        "ext": bpy.data.collections.new("01_Muros_Exteriores"),
        "int": bpy.data.collections.new("02_Tabiques_Interiores"),
        "puertas": bpy.data.collections.new("02B_Puertas_Y_Placards_Video"),
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
                if 'Base Color' in bsdf.inputs:
                    bsdf.inputs['Base Color'].default_value = color_rgba
                if 'Roughness' in bsdf.inputs:
                    bsdf.inputs['Roughness'].default_value = rough
        return m

    return {
        "piso": get_or_create("Mat_Piso", (0.96, 0.97, 0.98, 1.0), 0.7),
        "palier": get_or_create("Mat_Palier_Edificio", (0.91, 0.92, 0.94, 1.0), 0.8),
        "ext": get_or_create("Mat_Muro_Exterior", (0.86, 0.89, 0.93, 1.0), 0.45),
        "int": get_or_create("Mat_Muro_Interior", (0.92, 0.94, 0.96, 1.0), 0.45),
        "dintel": get_or_create("Mat_Dintel", (0.82, 0.85, 0.89, 1.0), 0.45),
        "marco_chapa": get_or_create("Mat_Marco_Chapa_Oscuro", (0.17, 0.19, 0.21, 1.0), 0.4),
        "puerta_madera": get_or_create("Mat_Puerta_Placa_Madera", (0.74, 0.47, 0.25, 1.0), 0.45),
        "puerta_principal": get_or_create("Mat_Puerta_Principal_Gris", (0.55, 0.57, 0.60, 1.0), 0.4),
        "placard_madera": get_or_create("Mat_Placard_Corredizo_Madera", (0.77, 0.49, 0.27, 1.0), 0.5),
    }


def add_box(name, x1, y1, z1, sx, sy, sz, mat, col):
    """
    Crea un prisma rectangular.
    En Blender:
    X = X del plano (0.00 a 6.30)
    Y = -Y del plano (para que Y=0 quede al norte y Y=7.00 al sur)
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

    H = 2.60            # Altura total de muros
    H_PASO = 2.05       # Altura de dinteles de puertas
    H_DINT = H - H_PASO # 0.55m de dintel
    EXT = 0.15          # Espesor muros perimetrales
    INT = 0.10          # Espesor muros interiores

    # -------------------------------------------------------------
    # 1. PISO POLIGONAL EN "L" (6.30 m x 7.00 m) + PALIER EXTERIOR
    # -------------------------------------------------------------
    add_box("Piso_Norte_630x570", 0.00, 0.00, -0.10, 6.30, 5.70, 0.10, mats["piso"], cols["piso"])
    add_box("Piso_Sur_520x130", 0.00, 5.70, -0.10, 5.20, 1.30, 0.10, mats["piso"], cols["piso"])
    add_box("Palier_Edificio_Exterior", 5.20, 5.70, -0.10, 1.10, 1.30, 0.10, mats["palier"], cols["piso"])

    # -------------------------------------------------------------
    # 2. PERÍMETRO EXTERIOR (Polígono en "L": 6.30 x 7.00)
    # -------------------------------------------------------------
    # Muro Superior (Norte, Y = 0.00): X = 0.00 a 6.30
    add_box("Muro_Ext_Norte_Y0", 0.00, -EXT / 2, 0.00, 6.30, EXT, H, mats["ext"], cols["ext"])

    # Muro Derecho (Este, X = 6.30): Y = 0.00 a 5.70
    add_box("Muro_Ext_Este_X630", 6.30 - EXT / 2, 0.00, 0.00, EXT, 5.70, H, mats["ext"], cols["ext"])

    # Retranqueo Palier / Puerta Principal (Y = 5.70, X = 5.20 a 6.30)
    add_box("Muro_Ext_Palier_Izq", 5.20, 5.70 - EXT / 2, 0.00, 0.18, EXT, H, mats["ext"], cols["ext"])
    add_box("Muro_Ext_Palier_Der", 6.12, 5.70 - EXT / 2, 0.00, 0.18, EXT, H, mats["ext"], cols["ext"])
    add_box("Dintel_Puerta_Principal", 5.38, 5.70 - EXT / 2, H_PASO, 0.74, EXT, H_DINT, mats["dintel"], cols["ext"])

    # Muro Derecho Cocina (X = 5.20): Y = 5.70 a 7.00
    add_box("Muro_Ext_Cocina_Der_X520", 5.20 - EXT / 2, 5.70, 0.00, EXT, 1.30, H, mats["ext"], cols["ext"])

    # Muro Inferior (Sur, Y = 7.00): X = 0.00 a 5.20
    add_box("Muro_Ext_Sur_Y700", 0.00, 7.00 - EXT / 2, 0.00, 5.20, EXT, H, mats["ext"], cols["ext"])

    # Muro Izquierdo (Oeste, X = 0.00): Y = 0.00 a 7.00
    add_box("Muro_Ext_Oeste_X0", -EXT / 2, 0.00, 0.00, EXT, 7.00, H, mats["ext"], cols["ext"])

    # -------------------------------------------------------------
    # 3. MUROS INTERNOS, PUERTAS Y VANOS ABIERTOS
    # -------------------------------------------------------------
    # Eje Vertical X = 2.30 (Cierre de Placards y Baño):
    # - Muro sólido de Y = 2.30 a Y = 3.02 (Placard Sup. + mocheta superior Baño)
    add_box("Muro_V_X230_Placard_Sup_Bano", 2.30 - INT / 2, 2.30, 0.00, INT, 0.72, H, mats["int"], cols["int"])
    # - Puerta Baño: Entre Y = 3.02 e Y = 3.65 (abre hacia adentro del Baño)
    add_box("Dintel_Puerta_Bano", 2.30 - INT / 2, 3.02, H_PASO, INT, 0.63, H_DINT, mats["dintel"], cols["int"])
    # - Muro sólido de Y = 3.65 a Y = 4.50 (Baño 3.65-4.00 + Placard Inf. 4.00-4.50)
    add_box("Muro_V_X230_Bano_Placard_Inf", 2.30 - INT / 2, 3.65, 0.00, INT, 0.85, H, mats["int"], cols["int"])

    # Eje Vertical Central X = 3.00:
    # - Muro sólido de Y = 0.00 a Y = 3.70 (separa Estudio y parte del Pasillo del Living)
    add_box("Muro_V_X300_Estudio_Pasillo_Living", 3.00 - INT / 2, 0.00, 0.00, INT, 3.70, H, mats["int"], cols["int"])
    # - VANO ABIERTO (Paso Living-Pasillo): Sin muro entre Y = 3.70 e Y = 4.50
    # - Muro sólido de Y = 4.50 a Y = 7.00 (separa Cuarto de Cocina)
    add_box("Muro_V_X300_Cuarto_Cocina", 3.00 - INT / 2, 4.50, 0.00, INT, 2.50, H, mats["int"], cols["int"])

    # Eje Vertical X = 5.20 (separa Cocina de Entrada): de Y = 4.50 a Y = 5.70
    add_box("Muro_V_X520_Cocina_Entrada", 5.20 - INT / 2, 4.50, 0.00, INT, 1.20, H, mats["int"], cols["int"])

    # Eje Horizontal Y = 2.30 (Base Estudio):
    # - Muro sólido de X = 0.00 a X = 2.30
    add_box("Muro_H_Y230_Estudio_Placard_Sup", 0.00, 2.30 - INT / 2, 0.00, 2.30, INT, H, mats["int"], cols["int"])
    # - Puerta Estudio: De X = 2.30 a X = 3.00 (abre hacia adentro del Estudio)
    add_box("Dintel_Puerta_Estudio", 2.30, 2.30 - INT / 2, H_PASO, 0.70, INT, H_DINT, mats["dintel"], cols["int"])

    # Eje Horizontal Y = 2.80 (Placard Sup. / Baño): de X = 0.00 a X = 2.30
    add_box("Muro_H_Y280_Placard_Sup_Bano", 0.00, 2.80 - INT / 2, 0.00, 2.30, INT, H, mats["int"], cols["int"])

    # Eje Horizontal Y = 4.00 (Baño / Placard Inf.): de X = 0.00 a X = 2.30
    add_box("Muro_H_Y400_Bano_Placard_Inf", 0.00, 4.00 - INT / 2, 0.00, 2.30, INT, H, mats["int"], cols["int"])

    # Eje Horizontal Y = 4.50 (Línea Cuarto y Cocina):
    # - Muro sólido de X = 0.00 a X = 2.30
    add_box("Muro_H_Y450_Placard_Inf_Cuarto", 0.00, 4.50 - INT / 2, 0.00, 2.30, INT, H, mats["int"], cols["int"])
    # - Puerta Cuarto: De X = 2.30 a X = 3.00 (abre hacia adentro del Cuarto)
    add_box("Dintel_Puerta_Cuarto", 2.30, 4.50 - INT / 2, H_PASO, 0.70, INT, H_DINT, mats["dintel"], cols["int"])
    # - VANO ABIERTO COCINA (SIN PUERTA): Dintel superior de X = 3.00 a X = 3.85
    add_box("Dintel_Vano_Cocina_Sin_Puerta", 3.00, 4.50 - INT / 2, H_PASO, 0.85, INT, H_DINT, mats["dintel"], cols["int"])
    # - Muro sólido frontal de Cocina: De X = 3.85 a X = 5.20
    add_box("Muro_H_Y450_Frente_Cocina", 3.85, 4.50 - INT / 2, 0.00, 1.35, INT, H, mats["int"], cols["int"])

    # -------------------------------------------------------------
    # 3B. PUERTAS 3D Y PLACARDS RELEVADOS DEL VIDEO
    # -------------------------------------------------------------
    # Hojas de puertas placa de madera (abiertas hacia adentro de Estudio, Baño y Cuarto)
    add_box("Puerta_Madera_Estudio", 2.34, 1.68, 0.01, 0.04, 0.62, 2.00, mats["puerta_madera"], cols["puertas"])
    add_box("Puerta_Madera_Bano", 1.72, 3.05, 0.01, 0.58, 0.04, 2.00, mats["puerta_madera"], cols["puertas"])
    add_box("Puerta_Madera_Cuarto", 2.34, 4.50, 0.01, 0.04, 0.62, 2.00, mats["puerta_madera"], cols["puertas"])
    # Puerta Principal Gris Moldurada (abierta hacia adentro de Entrada)
    add_box("Puerta_Principal_Gris_Moldurada", 5.42, 5.04, 0.01, 0.05, 0.66, 2.00, mats["puerta_principal"], cols["puertas"])
    # Frentes de Placard Corredizos de Madera
    add_box("Frente_Placard_Corredizo_Estudio", 0.15, 2.22, 0.06, 2.03, 0.03, 2.38, mats["placard_madera"], cols["puertas"])
    add_box("Frente_Placard_Corredizo_Cuarto", 0.15, 4.55, 0.06, 2.03, 0.03, 2.38, mats["placard_madera"], cols["puertas"])

    # -------------------------------------------------------------
    # 4. CÁMARAS Y LUCES PRECONFIGURADAS
    # -------------------------------------------------------------
    bpy.ops.object.light_add(type='SUN', location=(10.0, -12.0, 15.0))
    sun = bpy.context.active_object
    sun.name = "Sol_Arquitectonico"
    sun.data.energy = 2.5
    sun.rotation_euler = (math.radians(50), math.radians(20), math.radians(-35))
    for c in list(sun.users_collection):
        c.objects.unlink(sun)
    cols["setup"].objects.link(sun)

    bpy.ops.object.light_add(type='SUN', location=(-10.0, 8.0, 10.0))
    fill = bpy.context.active_object
    fill.name = "Luz_Relleno"
    fill.data.energy = 1.0
    fill.rotation_euler = (math.radians(-40), math.radians(-15), math.radians(140))
    for c in list(fill.users_collection):
        c.objects.unlink(fill)
    cols["setup"].objects.link(fill)

    bpy.ops.object.camera_add(location=(3.15, -13.0, 12.0))
    cam3d = bpy.context.active_object
    cam3d.name = "Camara_3D_Isometrica"
    cam3d.rotation_euler = (math.radians(52), 0, 0)
    for c in list(cam3d.users_collection):
        c.objects.unlink(cam3d)
    cols["setup"].objects.link(cam3d)

    bpy.ops.object.camera_add(location=(3.15, -3.50, 14.5))
    cam2d = bpy.context.active_object
    cam2d.name = "Camara_2D_Plano_Cenital"
    cam2d.data.type = 'ORTHO'
    cam2d.data.ortho_scale = 9.6
    cam2d.rotation_euler = (0, 0, 0)
    for c in list(cam2d.users_collection):
        c.objects.unlink(cam2d)
    cols["setup"].objects.link(cam2d)

    scene.camera = cam3d
    print("✅ DEPARTAMENTO EN 'L' 6.30m x 7.00m CONSTRUIDO CON ÉXITO EN BLENDER")


if __name__ == "__main__":
    build_apartment()
