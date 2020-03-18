# -*- mode: python -*-

block_cipher = None


a = Analysis(['train_yp.py'],
             pathex=['D:\\coding\\SCRS_RS_AI-developer_0311'],
             binaries=[],
             datas=[('C:/Program Files/Anaconda3/envs/tfpy35/Lib/site-packages/tensorflow/python/_pywrap_tensorflow_internal.pyd', 'tensorflow/python')],
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
          name='train_yp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
