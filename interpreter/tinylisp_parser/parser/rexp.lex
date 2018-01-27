
special		"+"|"-"|"/"|"*"|"?"|"!"|">"|"<"|"="|"^"|"_"
%{
int linecounter = 1;
%}
%option nounput
%%

"-"[0-9]+\.[0-9]+|[0-9]+\.[0-9]+											{ return(FLOAT); }
"-"[0-9]+|[0-9]+															{ return(INTEGER); }
([a-zA-Z]|{special})([a-zA-Z0-9]|{special})*								{ return(IDENTIFIER); }

"'"																			{ return(QUOTE); }

"("																			{ return(LPAREN); }
")"																			{ return(RPAREN); }

"\""([A-Za-z0-9]|":"|"/"|"."|"-"|" "|"("|")")*"\""							{ return(WQUOTED); }
"@n"																		{ linecounter++; }
"\n"																		{ linecounter++; }
"\r\n"																		{ linecounter++; }
"\r"																		{ linecounter++; }
" "|"\t"																	{  }
.																			{ return(UNKNOWN); }
%%
int yywrap(void) {
	return(1);
}
