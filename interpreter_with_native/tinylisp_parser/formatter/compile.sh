flex rexp.lex
yacc syns.yac
cc -W -o y.tab.o -c y.tab.c
cc -W -o main.o -c main.c
cc -W -o tiny main.o y.tab.o
./tiny.exe < src.txt
