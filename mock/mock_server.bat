@ECHO OFF
rem start the python mock-server thingy to mock APIs
SET COMMAND=where pip
FOR /F "delims=" %%A IN ('%COMMAND%') DO (
    SET PIP_PATH=%%A
    rem set the path to the mock-server, by slicing the string
    rem from string pos 0 to everything but the last 8 chars
    SET SCRIPT_PATH=%PIP_PATH:~0,-8%
    echo %SCRIPT_PATH%
    GOTO :Exec 
)

:Exec
python %SCRIPT_PATH%\mock-server --dir=. --address=192.168.63.47 --debug