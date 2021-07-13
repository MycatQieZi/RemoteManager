conda activate box-helper
create-version-file version.yml --outfile version.txt
pyinstaller entrypoint.py -F --windowed --uac-admin --icon=./resources/tool-box-64.ico --version-file=version.txt
@rem pyinstaller entrypoint.py -F --uac-admin --icon=./resources/tool-box-64.ico --version-file=version.txt
pause