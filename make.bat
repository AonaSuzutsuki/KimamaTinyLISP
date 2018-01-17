@echo off
set arg=%1
If %arg%==clean (
	goto CLEAN
) Else (
	goto ALL
)

:CLEAN
cd interpreter
cd tinylisp_parser
cd formatter
make clean
cd ../
cd parser
make clean
cd ../
cd ../
cd ../
rd /s /q bin
goto END

:ALL
cd interpreter
cd tinylisp_parser
cd formatter
make install
cd ../
cd parser
make install
cd ../
cd ../
python install.py
cd ../
goto END

:END
