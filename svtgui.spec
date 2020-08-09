# -*- mode: python ; coding: utf-8 -*-
import shutil

matches = ["LICENSE.txt","METADATA","PKG-INFO","LICENSE"]
lics = []
print("Find 3rd party dependency license files")
for root, dir, files in os.walk("venv/lib"):
    for file in files:
            if file in matches:
               src = f"{root}/{file}"
               dest = f"licenses/{os.path.basename(root)}"
               lics.append((src,dest))
               print(f"\tLicense file: {root}/{file}")
print(f"{len(lics)} dependency licenses found. Copying to /license folder in distribution")

block_cipher = None


a = Analysis(['svtgui.py'],
             pathex=['/home/august/git/svtgui'],
             binaries=[(shutil.which('svtplay-dl'), '.')],
             datas=lics,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='svtgui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
