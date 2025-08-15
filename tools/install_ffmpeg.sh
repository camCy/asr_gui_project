#!/usr/bin/env bash
set -euo pipefail
mkdir -p bin
cd bin
if [[ ! -f ffmpeg ]]; then
  echo "[INFO] Descargando ffmpeg estático (Linux x86_64)..."
  curl -L -o ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
  tar -xf ffmpeg.tar.xz
  rm ffmpeg.tar.xz
  D=$(find . -maxdepth 1 -type d -name "ffmpeg-*-amd64-static" | head -n 1)
  mv "$D/ffmpeg" ./ffmpeg
  rm -rf "$D"
  chmod +x ffmpeg
  echo "[OK] ffmpeg listo en ./bin/ffmpeg"
else
  echo "[OK] ffmpeg ya existe en ./bin/ffmpeg"
fi
echo "export PATH=\"$PWD:$PATH\"" 
