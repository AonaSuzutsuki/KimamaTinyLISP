arg=$1
echo $arg
if [ $arg = clean ]; then
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
	rm -r -f bin
else
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
fi
