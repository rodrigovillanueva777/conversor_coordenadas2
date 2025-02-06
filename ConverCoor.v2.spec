# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('icon/pin_icon.png', '.'), ('icon/config_icon.png', '.'), ('icon/paste_icon.png', '.'), ('icon/copy_icon.png', '.'), ('icon/cut_icon.png', '.'), ('icon/convert_icon.png', '.'), ('icon/maps_icon.png', '.'), ('icon/earth_icon.png', '.'), ('icon', 'icon')],
    hiddenimports=[],
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
    name='ConverCoor.v2',
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
    icon=['icon\\convercoor.ico'],
)
