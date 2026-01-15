# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/background_service.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/common', 'src/common'),
        ('src/features', 'src/features'),
        ('src/services', 'src/services'),
        ('users.db', '.')
    ],
    hiddenimports=[
        'pystray', 
        'PIL', 
        'uvicorn', 
        'fastapi', 
        'nicegui',
        'engineio.async_drivers.aiohttp', # Common pyinstaller miss for socketio
        'sklearn.utils._typedefs', # Common for scikit-learn
        'scipy.spatial.transform._rotation_groups'
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
    [],
    exclude_binaries=True,
    name='FaceAuthService',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # THIS IS KEY: No Console Window
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
    name='FaceAuthService',
)
