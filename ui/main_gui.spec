# -*- mode: python -*-

block_cipher = None


a = Analysis(['main_gui.py'],
             pathex=['D:\\coding\\SCRS_RS_AI-developer_0311\\ui'],
             binaries=[],
             datas=[],
             hiddenimports=["pywt","pywt._extensions._cwt",'tensorflow.python._pywrap_tensorflow_internal'],
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
          [],
          exclude_binaries=True,
          name='main_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main_gui')
