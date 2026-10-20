# PyInstaller configuration for the Tkinter desktop app.
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("tkinter")

a = Analysis(
    ["meow.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="DoYouLoveMe",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
