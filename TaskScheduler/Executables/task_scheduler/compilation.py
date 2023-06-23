import PyInstaller.__main__

PyInstaller.__main__.run([
    'C:/Projects/NicheTools/TaskScheduler/ts_main.py',
    '--onefile',
    '--clean',
    '--distpath',
    'C:/Projects/NicheTools/TaskScheduler/Executables/task_scheduler/dist',
    '--workpath',
    'C:/Projects/NicheTools/TaskScheduler/Executables/task_scheduler/build',
    '--upx-dir',
    'C:/upx-4.0.2-win64',
])
