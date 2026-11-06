# 📐 Edificio Glaciares II — Depto 01-01 (1° Piso)

Proyecto de modelado 3D interactivo y planos digitales para la **Unidad Funcional N° 6, Departamento "A", Polígono 01-01**, verificado con la **Escritura Oficial de Dominio**, el **Plano Catastral / Subdivisión en PH** y el relevamiento exhaustivo por fotos, croquis y videos reales.

---

## 📋 Datos Legales y Catastrales Oficiales (Escritura)

- **Edificio**: Glaciares II
- **Ubicación**: Calle Günter Plüschow 235 (entre Antoine de Saint Exupéry y Calle 508), El Calafate, Provincia de Santa Cruz.
- **Unidad Funcional**: N° 6 (Seis) — Planta Primer Piso — Departamento "A"
- **Polígono**: 01-01
- **Superficie Cubierta Oficial**: **54,16 m²** *(Cincuenta y cuatro metros con dieciséis decímetros cuadrados)*
- **Porcentual de Dominio**: **10,03 %** *(Diez coma cero tres por ciento)*
- **Nomenclatura Catastral**: Manzana 193, Parcela 14 (Plano de Mensura M-8876)

---

## 📊 Medidas y Dimensiones Verificadas

| Parámetro | Medida Oficial | Observaciones |
| :--- | :--- | :--- |
| **Superficie Cubierta Total** | **54,16 m²** | Coincidencia matemática exacta: `(9.30 × 6.20) - (2.30 × 1.40) - (0.40 × 0.70) = 54,16 m²` |
| **Lado Oeste (Fachada)** | **6.20 m** | Frente directo sobre Calle Günter Plüschow |
| **Lado Norte (Medianera)** | **7.00 m** | Muro divisorio con Unidad 01-02 |
| **Quiebre a Palier Común** | **1.40 m** | Saliente hacia la Cubierta Común |
| **Acceso desde Palier** | **2.30 m** | Muro con Puerta de Acceso Principal al Departamento |
| **Lado Este (Lateral)** | **4.80 m** | Muro exterior Living Comedor |
| **Lado Sur (Sector Living)** | **3.80 m** | Muro exterior hacia patio posterior |
| **Ducto de Ventilación e Instalaciones** | **0.40 m × 0.70 m** | Ventilación y bajada de cañerías cocina/termo |
| **Lado Sur (Sector Cuarto y Cocina)** | **5.10 m** | Muro exterior dormitorio y cocina |
| **Ancho Total (Este-Oeste)** | **9.30 m** | `7.00 m + 2.30 m` = `5.10 m + 0.40 m + 3.80 m` |
| **Altura Libre (Cielorraso)** | **2.65 m a 3.85 m** | Techo de madera en pendiente (machimbre y vigas vistas) |

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
