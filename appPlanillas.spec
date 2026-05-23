# -*- mode: python ; coding: utf-8 -*-
import sysconfig
from pathlib import Path

block_cipher = None

# Finds site-packages regardless of Python version or OS
_sp = Path(sysconfig.get_paths()["purelib"])

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("assets/planillaVacia.jpg",          "assets"),
        ("assets/LiberationSans-Regular.ttf", "assets"),
        ("assets/fotoTernero.ico",            "assets"),
        (str(_sp / "flet/controls/material/icons.json"),
         "flet/controls/material"),
        (str(_sp / "flet/controls/cupertino/cupertino_icons.json"),
         "flet/controls/cupertino"),
    ],
    hiddenimports=[
        "flet",
        "flet.controls",
        "PIL",
        "PIL.Image",
        "PIL.ImageDraw",
        "PIL.ImageFont",
        "fpdf",
        "openpyxl",
        "dateutil",
        "dateutil.parser",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="appPlanillas",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/fotoTernero.ico",
)
