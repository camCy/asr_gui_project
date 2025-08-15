SHELL := /bin/bash

.PHONY: venv install run normalize

venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

run:
	. .venv/bin/activate && streamlit run app/app_streamlit.py

normalize:
	. .venv/bin/activate && python tools/normalize_audio.py --in "data/audio_raw/*" --out "data/audio_clean"
