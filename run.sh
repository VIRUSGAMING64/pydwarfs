#!/bin/bash
tsc gui/src/main.ts --outDir src/
pip install -r requirements.txt --break-system-packages
python main.py