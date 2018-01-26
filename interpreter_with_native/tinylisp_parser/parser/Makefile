
CC=gcc
OUT=parser
CCARG=-Wall -o $(OUT)
LEX=flex
YACC=yacc

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
	rm lex.yy.c y.tab.c
	rm $(OUT)