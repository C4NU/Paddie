# -*- mode: python ; coding: utf-8 -*-


import platform
import os

# OS별 바이너리 설정
bins = []
if platform.system() == 'Darwin' and os.path.exists('/opt/homebrew/lib/libzstd.1.dylib'):
    bins.append(('/opt/homebrew/lib/libzstd.1.dylib', '.'))

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=bins,
    datas=[
        ('resources/ui', 'resources/ui'),
        ('resources/fonts', 'resources/fonts'),
        ('resources/data', 'resources/data'),
        ('resources/i18n', 'resources/i18n'),
        ('resources/icons', 'resources/icons'),
        ('.env', '.'),
    ],
    hiddenimports=['PyQt6'],
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
    [],
    exclude_binaries=True,
    name='Paddie',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Paddie',
)
app = BUNDLE(
    coll,
    name='Paddie.app',
    icon='resources/icon.icns',
    bundle_identifier='com.canu.paddie_legacy',
)
