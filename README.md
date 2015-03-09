# perl_compiler
A cross-compiler from 'perl' to 'x86' using 'python'

Part1: Lexer Usage: python lexer.py abc.pl


I printed the debug into the file 'strerr_output' by the command

python parser1.py test_expr.pl 2> strerr_output

python parser1.py test_expr.pl | dot -Tps > tmp
evince tmp