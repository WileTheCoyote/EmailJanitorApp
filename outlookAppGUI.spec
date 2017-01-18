# -*- mode: python -*-

block_cipher = None


a = Analysis(['../PyInstaller-3.2/outlookAppGUI.py'],
             pathex=['/Users/OldMacbook/EmailJanitorApp/PyInstaller-3.2/outlookAppGUI'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('jan.jpg','/Users/OldMacbook/EmailJanitorApp/PyInstaller-3.2/jan.jpg','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Email Janitor',
          debug=False,
          strip=True,
          upx=True,
          console=False , icon='/Users/OldMacbook/EmailJanitorApp/PyInstaller-3.2/trash.icns')
app = BUNDLE(exe,
             name='Email Janitor.app',
             icon='trash.icns',
             bundle_identifier=None)
