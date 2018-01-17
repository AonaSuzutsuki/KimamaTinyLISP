
CC=cl
OUT=formatter.exe
CCARG=/Fe:$(OUT)
LEX=flex
YACC=bison

LSRC=rexp.lex
YSRC=syns.yac
TSRC=src.txt

all:
	$(LEX) $(LSRC)
	$(YACC) -o y.tab.c $(YSRC)
	$(CC) $(CCARG) y.tab.c main.c
test:all
	$(OUT) < $(TSRC)
install:all
	python install.py $(OUT)
clean:
	del lex.yy.c y.tab.c
	del *.obj
	del *.exe