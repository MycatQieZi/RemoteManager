conda activate box-helper
create-version-file version.yml --outfile version.txt
pyinstaller entrypoint.py -F --windowed --uac-admin --icon=./gui/resources/tool-box-64.ico --version-file=version.txt
pause