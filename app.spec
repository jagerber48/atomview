# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import cmocean


block_cipher = None

cmocean_rbg_path = str(Path(Path(cmocean.__file__).parent, 'rgb'))
datas = [(cmocean_rbg_path, 'cmocean\\rgb'),
         ('src\\atomview\\icon\\favicon.ico', 'icon')]

a = Analysis(
    ['src\\atomview\\app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='AtomView',
    icon='src\\atomview\\icon\\favicon.ico',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AtomView',
)
