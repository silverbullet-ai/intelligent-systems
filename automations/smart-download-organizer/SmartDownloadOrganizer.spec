
from pathlib import Path

from PyInstaller.utils.hooks import collect_all


# Project directories
PROJECT_ROOT = Path.cwd()
ENTRY_POINT = PROJECT_ROOT / "src" / "main.py"
ICON_PATH = PROJECT_ROOT / "assets" / "icons" / "app_icon.ico"

# Collect CustomTkinter resources and hidden imports
customtkinter_datas, customtkinter_binaries, customtkinter_hiddenimports = (
    collect_all("customtkinter")
)

# Include application resources
datas = customtkinter_datas + [
    (str(PROJECT_ROOT / "config"), "config"),
    (str(PROJECT_ROOT / "assets"), "assets"),
]

hiddenimports = customtkinter_hiddenimports

# Analyze application
a = Analysis(
    [str(ENTRY_POINT)],
    pathex=[str(PROJECT_ROOT)],
    binaries=customtkinter_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Create Python archive
pyz = PYZ(a.pure)

# Build executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SmartDownloadOrganizer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_PATH),
)

# Collect everything into a portable application folder
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="SmartDownloadOrganizer",
)
