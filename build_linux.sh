#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --user --upgrade pyinstaller
python3 -m PyInstaller --clean --noconfirm meow.spec
chmod +x dist/DoYouLoveMe

echo
echo "Built Linux executable: dist/DoYouLoveMe"
echo "Run it with: ./dist/DoYouLoveMe"
