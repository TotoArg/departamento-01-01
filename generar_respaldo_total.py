import os
import sys
import json
import gzip
import shutil
from datetime import datetime

CONV_ID = "1e627548-1da8-4dd8-a641-13dac54942ad"
BRAIN_DIR = rf"C:\Users\tomas\.gemini\antigravity\brain\{CONV_ID}"
TRANSCRIPT_PATH = os.path.join(BRAIN_DIR, ".system_generated", "logs", "transcript.jsonl")
USER_UPLOADED_DIR = os.path.join(BRAIN_DIR, ".user_uploaded")
SCRATCH_DIR = os.path.join(BRAIN_DIR, "scratch")

REPO_DIR = r"c:\Users\tomas\Documents\Proyectos\Departamento"
BACKUP_DIR = os.path.join(REPO_DIR, "backup_conversacion")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.join(BACKUP_DIR, "transcripcion"), exist_ok=True)
os.makedirs(os.path.join(BACKUP_DIR, "medios_usuario"), exist_ok=True)
os.makedirs(os.path.join(BACKUP_DIR, "planos_pdf"), exist_ok=True)

print(f"Iniciando respaldo integral para conversación {CONV_ID}...")

# 1. Copiar y comprimir transcript.jsonl
gz_target = os.path.join(BACKUP_DIR, "transcripcion", f"transcript_{CONV_ID}.jsonl.gz")
print("Comprimiendo transcript.jsonl...")
if os.path.exists(TRANSCRIPT_PATH):
    with open(TRANSCRIPT_PATH, "rb") as f_in:
        with gzip.open(gz_target, "wb", compresslevel=9) as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"Transcript comprimido con éxito: {os.path.getsize(gz_target):,} bytes")
else:
    print("AVISO: No se encontró transcript.jsonl en la ruta esperada.")

# 2. Copiar medios subidos por el usuario
print("Copiando medios de usuario (.user_uploaded)...")
copied_media = 0
if os.path.exists(USER_UPLOADED_DIR):
    for fname in os.listdir(USER_UPLOADED_DIR):
        src = os.path.join(USER_UPLOADED_DIR, fname)
        if os.path.isfile(src):
            dst = os.path.join(BACKUP_DIR, "medios_usuario", fname)
            shutil.copy2(src, dst)
            copied_media += 1
print(f"Copiados {copied_media} archivos multimedia de usuario.")

# 3. Copiar PDFs de planos arquitectónicos originales
print("Copiando planos arquitectónicos originales en PDF...")
copied_pdfs = 0
for pdf_name in ["Plano_Planta_baja.pdf", "Plano_Primer_piso.pdf", "Plano_Segundo_piso.pdf"]:
    src = os.path.join(SCRATCH_DIR, pdf_name)
    if os.path.exists(src):
        dst = os.path.join(BACKUP_DIR, "planos_pdf", pdf_name)
        shutil.copy2(src, dst)
        copied_pdfs += 1
print(f"Copiados {copied_pdfs} planos PDF.")

# 4. Parsear transcript para extraer todos los diálogos y solicitudes de usuario
print("Extrayendo historial completo de diálogo y requerimientos...")
user_dialogue = []
all_steps_summary = []

if os.path.exists(TRANSCRIPT_PATH):
    step_num = 0
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            step_num += 1
            try:
                obj = json.loads(line)
            except Exception:
                continue
            
            step_type = obj.get("type", "")
            source = obj.get("source", "")
            created_at = obj.get("created_at", "")
            content = obj.get("content", "")
            
            # Detectar solicitudes explícitas de usuario
            if source == "USER_EXPLICIT" or step_type == "USER_INPUT":
                media_list = []
                for m in obj.get("media", []):
                    uri = m.get("uri", "")
                    media_list.append(os.path.basename(uri))
                
                user_dialogue.append({
                    "step": step_num,
                    "timestamp": created_at,
                    "content": content,
                    "media": media_list
                })

print(f"Total de intervenciones del usuario identificadas: {len(user_dialogue)}")

# Escribir HISTORIAL_COMPLETO_DIALOGO.md
dialogue_file = os.path.join(BACKUP_DIR, "HISTORIAL_COMPLETO_DIALOGO.md")
with open(dialogue_file, "w", encoding="utf-8") as f:
    f.write("# Historial Completo de Diálogos y Requerimientos del Usuario\n\n")
    f.write(f"**Proyecto:** Gemelo Digital 3D Departamento 01-01  \n")
    f.write(f"**ID de Conversación Antigravity:** `{CONV_ID}`  \n")
    f.write(f"**Fecha de Respaldo:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
    f.write(f"**Total de Intervenciones Registradas:** {len(user_dialogue)}  \n\n")
    f.write("---\n\n")
    
    for idx, item in enumerate(user_dialogue, 1):
        f.write(f"### Intervención #{idx} — [{item['timestamp']}]\n\n")
        f.write(f"**Mensaje del Usuario:**\n\n")
        f.write(f"> {item['content'].replace(chr(10), chr(10) + '> ')}\n\n")
        if item["media"]:
            f.write(f"**Archivos Adjuntos:** `{', '.join(item['media'])}`  \n")
            for m in item["media"]:
                f.write(f"- [Ver medio adjunto](medios_usuario/{m})\n")
            f.write("\n")
        f.write("---\n\n")

print(f"Guardado {dialogue_file}")
