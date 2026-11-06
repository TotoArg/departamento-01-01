# 📐 Departamento 01-01 — Planos y Modelo 3D Arquitectónico

Proyecto de modelado 3D interactivo y planos digitales para la **Unidad 01-01** (Primer Piso), basado en el **Plano Municipal / Subdivisión en Propiedad Horizontal** y la documentación fotográfica / panorámica 360° del departamento real.

---

## 📊 Medidas y Dimensiones Verificadas

| Parámetro | Medida Oficial | Observaciones |
| :--- | :--- | :--- |
| **Superficie Cubierta Interior** | **~54.16 m²** | Excluyendo muros perimetrales |
| **Lado Oeste (Frente/Lateral)** | **6.20 m** | Muro exterior de 0.20 m de espesor con ventanal |
| **Lado Norte (Medianera)** | **7.00 m** | Muro divisorio ciego con depto 01-02 (0.20 m) |
| **Quiebre de Acceso Pasillo** | **1.40 m** | Conexión con Cubierta Común / Palier |
| **Lado Norte Sector Este** | **2.30 m** | Muro con Puerta Principal de Acceso (0.20 m) |
| **Lado Este** | **4.80 m** | Muro exterior dormitorio con ventana (0.20 m) |
| **Lado Sur Sector Este** | **3.80 m** | Muro exterior |
| **Ducto / Nicho de Ventilación** | **0.40 m × 0.70 m** | Chimenea / ventilación de artefactos a gas |
| **Lado Sur Sector Oeste** | **5.10 m** | Muro exterior living con ventanal |
| **Ancho Total (Este-Oeste)** | **9.30 m** | `7.00m + 2.30m` = `5.10m + 0.40m + 3.80m` (cierre perfecto) |
| **Altura Libre (Cielorraso)** | **2.60 m a 3.90 m** | Techo de madera en pendiente (machimbre y tirantes vistos) |

---

## 🏠 Distribución y Espacios Relevados

1. **Living - Comedor (Estar Principal)**:
   - Gran espacio integrado con cielorraso de madera en pendiente y vigas a la vista.
   - Ventanales en esquina con vista exterior abierta.
   - Calefactor tiro balanceado con tiraje vertical galvanizado que atraviesa el techo.
   - Área de estar con sillón, mesa ratona, mueble rack con Smart TV y sistema de audio.
   - Área de comedor con mesa redonda y sillas junto a los ventanales.

2. **Cocina Semi-Integrada**:
   - Mesada en "L" con tapa de granito rosa del salto y zócalo perimetral.
   - Bacha doble de acero inoxidable con grifería monocomando.
   - Cocina a gas de 4 hornallas con horno (blanca).
   - Termotanque a gas Sherman con conducto de ventilación al exterior.
   - Muebles bajo mesada de madera con cajonera.
   - Ventana propia sobre la bacha con vista al exterior.

3. **Dormitorio Principal / Estudio**:
   - Amplio placard embutido con frente integral de puertas corredizas de madera y baulera superior.
   - Gran escritorio en "L" a medida con doble pantalla, soporte de micrófonos y silla ergonómica gamer.
   - Estantes flotantes de madera con fijaciones metálicas (colección de consolas Nintendo / Game Boy y biblioteca).
   - Panel calefactor eléctrico de pared.
   - Ventana con cortinas y vistas panorámicas.

4. **Baño Completo**:
   - Ubicado sobre el pasillo de distribución central entre la cocina y el dormitorio, contiguo al ducto de instalaciones.

---

## 🚀 Cómo Usar el Visor 3D Interactivo

1. **Abrir directamente**:
   - Hacé doble click en el archivo `abrir_plano_3d.bat` o abrí `index.html` con cualquier navegador moderno (Chrome, Edge, Firefox, Brave, Safari).
2. **Controles de Navegación**:
   - **Click Izquierdo + Arrastrar**: Rotar y orbitar la cámara en 3D.
   - **Click Derecho + Arrastrar**: Paneo y desplazamiento lateral.
   - **Rueda del Ratón**: Zoom in / Zoom out.
3. **Modos de Visualización**:
   - **🔄 Órbita 3D**: Perspectiva general libre del departamento.
   - **📐 Planta 2D (Cotas)**: Vista cenital técnica estilo plano con todas las medidas arquitectónicas oficiales.
   - **🚶 Recorrido Interior (FPS)**: Entrá y caminá por el departamento usando las teclas `W`, `A`, `S`, `D` y el ratón para mirar alrededor (presioná `ESC` para volver a la órbita).
   - **Chips de Acceso Rápido**: Vistas directas del Living, Cocina, Dormitorio/Escritorio y Puerta de Acceso.
4. **Capas y Opciones**:
   - Encender/apagar el techo de madera para ver el interior en corte axonofónico.
   - Ocultar o mostrar el mobiliario real relevado.
   - Activar/desactivar cotas de medidas en metros.
   - Activar modo Rayos X (muros transparentes).
5. **Exportación 3D**:
   - Hacé click en **"💾 Descargar .OBJ"** para exportar el modelo a Blender, SketchUp, AutoCAD, Revit o 3ds Max.

---

## 📦 Archivos Incluidos en este Repositorio

- `index.html`: Visor 3D web interactivo completo con Three.js, materiales procedurales, cotas y modo primera persona.
- `abrir_plano_3d.bat`: Acceso directo para abrir el visor en tu navegador con 1 click.
- `Departamento_01-01.obj`: Modelo 3D Wavefront OBJ listo para importar en software CAD/BIM o motores gráficos.
- `Departamento_01-01.mtl`: Definición de materiales para el archivo OBJ (cerámicos, granito, maderas, muros).
- `generate_model.py`: Script generador del modelo 3D paramétrico.
- `fotos/`: Colección descargada de las 38 fotografías y panorámicas 360° del departamento real.
