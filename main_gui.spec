# -*- mode: python -*-

block_cipher = None


a = Analysis(['main_gui.py'],
             pathex=['D:\\coding\\qiaozh\\SCRS_RS_AI_2'],
             binaries=[],
             datas=[('C:/Program Files/Anaconda3/envs/tfpy35/Lib/site-packages/tensorflow/python/_pywrap_tensorflow_internal.pyd', 'tensorflow/python')],
             hiddenimports=["pywt","pywt._extensions._cwt","win32timezone"],
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
