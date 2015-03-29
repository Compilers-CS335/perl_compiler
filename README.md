# perl_compiler
A cross-compiler from 'perl' to 'x86' using 'python'

Part1: Lexer Usage: python lexer.py abc.pl


I printed the debug into the file 'strerr_output' by the command

python parser1.py test_expr.pl 2> strerr_output

python parser1.py test_expr.pl | dot -Tps > tmp
evince tmp


-- 
> not giving zero integer value to strings. 
> cannot compare booleans 
	i.e. (a>b)==(c<d) will raise ERROR
> repeat does not creat arrays
> Not implementing Hash
> Print function only works with parenthesis
> Multiple assignments in a single statement are now not allowed