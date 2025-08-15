import json, tempfile
from pathlib import Path
import streamlit as st
from asr_core import transcribe_file, save_json_and_txt


st.set_page_config(page_title="ASR Español — MKV", page_icon="🎙️")

st.title("🎙️ Audio → Texto (Español) — Soporta MKV")
st.caption("Streamlit + faster-whisper | Entrada: WAV/MP3/MP4/FLAC/MKV → Texto (JSON + TXT)")

with st.sidebar:
    st.header("⚙️ Config")
    model_size = st.selectbox("Modelo", ["tiny","base","small","medium","large"], index=2)
    device = st.selectbox("Dispositivo", ["auto","cpu","cuda","mps"], index=0)
    language = st.selectbox("Idioma", ["es","auto"], index=0)
    out_dir = st.text_input("Salida", "data")

up = st.file_uploader("Sube archivo (incluye .mkv)", type=["wav","mp3","mp4","flac","mkv"])

if up is not None:
    st.audio(up)
    if st.button("Transcribir"):
        with st.spinner("Procesando... (requiere ffmpeg instalado)"):
            tmpdir = Path(tempfile.mkdtemp())
            src = tmpdir / up.name
            with open(src, "wb") as f:
                f.write(up.getbuffer())
            payload = transcribe_file(src, language=None if language=='auto' else language, model_size=model_size, device=device)
            base = Path(out_dir) / Path(up.name).stem
            save_json_and_txt(payload, base)
        st.success("¡Listo! Descarga tus resultados:")
        st.download_button("TXT", data=payload.get("transcript",""), file_name=f"{base.stem}.txt")
        st.download_button("JSON", data=json.dumps(payload, ensure_ascii=False, indent=2), file_name=f"{base.stem}.json")
