from __future__ import annotations
import json, time, tempfile, subprocess
from pathlib import Path
from typing import Dict, Any
from faster_whisper import WhisperModel

def _ffmpeg_to_flac16(src: Path) -> Path:
    tmp = Path(tempfile.mkdtemp())
    out = tmp / (src.stem + ".flac")
    cmd = ["ffmpeg","-y","-i",str(src),"-vn","-ac","1","-ar","16000",str(out)]
    subprocess.run(cmd, check=True)
    return out

def _pick_device(dev: str) -> str:
    if dev != "auto": return dev
    try:
        import torch
        if torch.cuda.is_available(): return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available(): return "mps"
    except Exception:
        pass
    return "cpu"

def transcribe_file(path: str|Path, language: str="es", model_size: str="small", device: str="auto") -> Dict[str, Any]:
    src = Path(path)
    norm = _ffmpeg_to_flac16(src)
    device = _pick_device(device)
    compute_type = "int8" if device == "cpu" else "float16"
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    t0 = time.time()
    segments, info = model.transcribe(str(norm), language=language, beam_size=5, vad_filter=False)
    txt = []
    words = []
    for s in segments:
        txt.append(s.text.strip())
        words.append({"start": float(s.start), "end": float(s.end), "text": s.text.strip()})
    transcript = " ".join([x for x in txt if x])
    t1 = time.time()
    duration = float(getattr(info, "duration", 0.0))

    return {
        "source_file": str(src),
        "route": "whisper",
        "language": language,
        "duration_sec": duration,
        "transcript": transcript,
        "words": words,
        "speakers": [],
        "metrics": {"latency_ms": int((t1-t0)*1000), "rtf": (t1-t0)/max(duration,1e-6)},
        "cost_estimate": {"currency": "USD", "per_min": 0.0, "total": 0.0}
    }

def save_json_and_txt(payload: Dict[str, Any], base: Path) -> None:
    base.parent.mkdir(parents=True, exist_ok=True)
    with open(base.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(base.with_suffix(".txt"), "w", encoding="utf-8") as f:
        f.write(payload.get("transcript",""))
