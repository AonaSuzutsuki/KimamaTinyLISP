arg=$1
echo $arg
if [ $arg = clean ]; then
	cd interpreter
	cd tinylisp_parser
	cd parser
	make clean
	cd ../
	cd ../
	cd ../
	rm -r -f bin
elif [ $arg = test ]; then
	cd bin
	python3 interpreter/run.py -p parser -py python3 interpreter/source.txt
	cd ../
else
        cd interpreter
        cd tinylisp_parser
        cd parser
        make install
        cd ../
        cd ../
	python install.py
        cd ../
fi
