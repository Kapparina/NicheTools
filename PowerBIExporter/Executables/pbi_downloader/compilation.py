import PyInstaller.__main__

PyInstaller.__main__.run([
    'C:/Projects/NicheTools/PowerBIExporter/PowerBIExporter.spec',
    '--clean',
    '--distpath',
    'C:/Projects/NicheTools/PowerBIExporter/Executables/pbi_downloader/dist',
    '--workpath',
    'C:/Projects/NicheTools/PowerBIExporter/Executables/pbi_downloader/build',
    '--upx-dir',
    'C:/upx-4.0.2-win64',
])
