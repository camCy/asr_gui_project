# ASR GUI — Audio → Texto en Español (MKV soportado)

Interfaz gráfica local con **Streamlit** que convierte audio/vídeo (incluye **.mkv**) a texto en **español**, generando **TXT** y **JSON**. Todo el procesamiento ocurre **en tu equipo** usando **faster-whisper** (Whisper optimizado).

---

## 🚀 Características
- Subida de archivos desde GUI (WAV/MP3/MP4/FLAC/**MKV**).
- Normalización automática a **FLAC 16 kHz mono** con `ffmpeg`.
- Transcripción local en **español** (o autodetección).
- Salidas: **texto (.txt)** y **JSON** con métricas (latencia, rtf).
- Funciona en CPU o GPU (si hay CUDA/MPS).

---

## 📁 Estructura del proyecto
```
app/
  app_streamlit.py   # Interfaz Streamlit
  asr_core.py        # Lógica: ffmpeg + faster-whisper
tools/
  normalize_audio.py # Normalización por lotes (opcional)
  install_ffmpeg.sh  # Solo Linux (descarga ffmpeg estático)
configs/
  app.example.yaml   # Parámetros por defecto
data/
  audio_raw/         # Entradas originales (no subir a GitHub)
  audio_clean/       # Audios normalizados (no subir a GitHub)
models/              # (opcional) caché/modelos
requirements.txt
Makefile
README.md
```

---

## 🧩 Requisitos
- **Windows 10/11 64-bit** (también funciona en Linux/macOS).
- **Python 3.11 o 3.12** (64-bit) — recomendado.
- **FFmpeg** instalado (ver instrucciones abajo).

---

## 🛠️ Instalación (paso a paso)

### Windows (PowerShell)
```powershell
# 1) Crear y activar entorno
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt

# 3) Verificar que ffmpeg existe
ffmpeg -version   # debe imprimir versión
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
ffmpeg -version
```

> Si `ffmpeg` no existe, ve a la sección **Instalación de FFmpeg**.

---

## 🎛️ Ejecución
Desde la **raíz** del proyecto, con el entorno activado:
```powershell
python -m streamlit run app/app_streamlit.py
```
- Se abrirá la GUI en `http://localhost:8501`.
- Sube tu archivo (incluye **.mkv**), selecciona modelo y transcribe.
- Descarga resultados: **.txt** (solo texto) y **.json** (estructura + métricas).

### Opciones útiles
- Forzar otro puerto:
  ```powershell
  python -m streamlit run app/app_streamlit.py --server.port 8502
  ```
- Si la primera ejecución tarda: es la descarga inicial del modelo (caché).

---

## 🎚️ Instalación de FFmpeg

### Windows
- **winget (recomendado):**
  ```powershell
  winget install -e --id Gyan.FFmpeg
  ```
- **Chocolatey:**
  ```powershell
  choco install ffmpeg -y
  ```
- **Comprobar:** `ffmpeg -version`

> Si `ffmpeg` no queda en PATH, puedes colocar un binario en `tools\bin\ffmpeg.exe`.  
> La app lo detecta automáticamente a través de la variable `FFMPEG_BIN`.

### Linux
```bash
sudo apt-get update && sudo apt-get install -y ffmpeg  # Debian/Ubuntu
# o: sudo dnf install ffmpeg  # Fedora
```

### macOS
```bash
brew install ffmpeg
```

---

## 🧠 Cómo funciona (resumen técnico)
1. **Subida del archivo** desde la GUI.
2. **Normalización** a **FLAC 16 kHz mono** con `ffmpeg` (extrae solo el audio en contenedores como **.mkv**).
3. **Transcripción** con `faster-whisper` (selección de modelo: tiny/base/small/medium/large).
4. **Post-proceso**: se unifican segmentos, se calculan métricas (latencia, RTF).
5. **Exportación**: se guardan **.txt** y **.json** (con timestamps de segmentos y metadatos).

Todo ocurre **localmente**, sin envíos a la nube. Si hay GPU disponible, se usa automáticamente (CUDA/MPS).

---

## 🧪 Solución de problemas
- **ModuleNotFoundError: faster_whisper** → Instalar en el **mismo venv** que ejecuta Streamlit:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  python -m pip install -r requirements.txt
  python -m streamlit run apppp_streamlit.py
  ```
- **ffmpeg no encontrado** → Instala con winget/apt/brew o coloca `tools\bin\ffmpeg.exe`.
- **Puerto ocupado** → `--server.port 8502`.
- **Python 3.13** → usa **3.11/3.12** (mejor compatibilidad de wheels).
- **VC++ runtime** (Windows) →
  ```powershell
  winget install --id=Microsoft.VCRedist.2015+.x64 --source=winget
  ```

---

**Linux/macOS:**
```bash
rm -rf build dist run_app.spec
# opcional: rm run_app.py
pip uninstall -y pyinstaller
```

---


## 📜 Licencias y uso
- **Whisper**: licencia MIT.
- Respeta las licencias de los audios que proceses.

