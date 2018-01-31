@echo off
set arg=%1
If %arg%==clean (
	goto CLEAN
) Else If %arg%==test (
	goto TEST
) Else (
	goto ALL
)

:CLEAN
cd interpreter
cd tinylisp_parser
cd parser
make -f Makefile.win clean
cd ../
cd ../
cd ../
rd /s /q bin
goto END

:ALL
cd interpreter
cd tinylisp_parser
cd parser
make -f Makefile.win install
cd ../
cd ../
python install.py
cd ../
goto END

:TEST
cd bin
python interpreter\run.py -p parser.exe -py python interpreter\source.txt
cd ../

:END
