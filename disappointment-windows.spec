# -*- mode: python -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['./'],
             binaries=[(HOMEPATH + '/sdl2/libogg-0.dll', ''),
                       (HOMEPATH + '/sdl2/libvorbis-0.dll', ''),
                       (HOMEPATH + '/sdl2/libvorbisfile-3.dll', ''),
                       (HOMEPATH + '/sdl2/libpng16-16.dll', '')],
             datas=[('disappointment/res', 'res')],
             hiddenimports=['_cffi_backend'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='disappointment',
          debug=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
name='disappointment')
