import PyInstaller.__main__

PyInstaller.__main__.run([
    'C:/Projects/NicheTools/LinkRunner/lr_main.py',
    '--onefile',
    '--clean',
    '--distpath',
    'C:/Projects/NicheTools/LinkRunner/Executables/linkrunner/dist',
    '--workpath',
    'C:/Projects/NicheTools/LinkRunner/Executables/linkrunner/build',
])
