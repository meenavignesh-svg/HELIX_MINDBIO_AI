# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ["janet_chat.py"],
    pathex=[],
    binaries=[],
    datas=[("assets/janet_icon.png", "assets")],
    hiddenimports=[
        "helixmind_bio_ai",
        "bioinformatics_tools",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "speech_recognition",
        "pyaudio",
        "pyautogui",
        "pyperclip",
        "tkinter",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="JANET",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="assets/janet_icon.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="JANET",
)
