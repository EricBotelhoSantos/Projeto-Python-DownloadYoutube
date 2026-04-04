# -*- mode: python ; coding: utf-8 -*-
# NexusTube Downloader (Desktop) — PyInstaller Configuration

import os
import importlib

# Detectar caminho do customtkinter automaticamente (portável)
ctk_path = os.path.dirname(importlib.import_module('customtkinter').__file__)

a = Analysis(
    ['../desktop/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (ctk_path, 'customtkinter/'),
        ('../desktop/assets/app_icon.ico', '.'),
        ('../desktop/assets/bg.png', '.'),
    ],
    hiddenimports=['yt_dlp'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NexusTubeDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['../desktop/assets/app_icon.ico'],
)
