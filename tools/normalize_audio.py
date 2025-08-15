#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path

def normalize_audio(src: Path, outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / (src.stem + ".flac")
    cmd = ["ffmpeg","-y","-i",str(src),"-vn","-ac","1","-ar","16000",str(out)]
    subprocess.run(cmd, check=True)
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inglob", required=True)
    p.add_argument("--out", dest="outdir", required=True)
    a = p.parse_args()
    paths = list(Path(".").glob(a.inglob))
    if not paths:
        print("No files")
        return
    outdir = Path(a.outdir)
    for src in paths:
        try:
            out = normalize_audio(src, outdir)
            print(f"OK {src} -> {out}")
        except Exception as e:
            print(f"ERROR {src}: {e}")

if __name__ == "__main__":
    main()
