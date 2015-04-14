# perl_compiler
A cross-compiler from 'perl' to 'x86' using 'python'

Part1: Lexer Usage: python lexer.py abc.pl


I printed the debug into the file 'strerr_output' by the command

python parser1.py test_expr.pl 2> strerr_output

python parser1.py test_expr.pl | dot -Tps > tmp
evince tmp


-- 
> ++ and -- not implemented
> Hash (%hashName) not implemented
> not giving zero integer value to strings. 
> cannot compare booleans 
	i.e. (a>b)==(c<d) will raise ERROR
> repeat does not creat arrays
> Not implementing Hash
> Print function only works with parenthesis
> Multiple assignments in a single statement are now not allowed
> Functions do not take parameters. Since any variable defined WITHOUT "my" can be used by any function.
> The update assignment in FOR loops cannot take any variable in the RHS. ($a = $a+1 might not work correctly if $a has been modified inside the loop)
> An array in our implementation can only contain elements of a single type... either all int, or all float or all string.
> also, array can only be accessed using @array_name[index] ... and not $array_name[index]
> Array assignment :-   @array_name = (...);   -: is mandatory
> Can't use name parent root  type scope returntype scope_depth








-----------------------UPDATE OVER AVIKALP's README-------------------------------
> You cannot use return more than once in a function. What ever you want to return, boil it down to a single variable and then return that variable
> It goes without saying that you can return only one kind of value from a function (else it will give trouble even where it is called)... {This has to be stated because a programmer may switch the return value type based on context inside a Functions}


HOW TO RUN:-
python parser.py <perl_file_destination> 
as -32 output.s -o output.o
ld -m elf_i386 output.o -o output