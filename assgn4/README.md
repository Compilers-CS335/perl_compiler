# perl_compiler
A cross-compiler from 'perl' to 'x86' using 'python'

++------------------------------------------------------------------------------++
||								FINAL SUBMISSION								||
++------------------------------------------------------------------------------++
+-------------------------------------------------------------------------------+
|	INSTRUCTIONS TO RUN THE COMPILER 											|
+-------------------------------------------------------------------------------+

STEP 1:	Run the following command on the terminal:

		user@computer$ python parser.py <destination of perl file>
		user@computer$ ./output

		- This will create :-
			1. The Symbol Table in 'symbolTable.gen'
			2. The 3-address code in 'Three_Address_Code.gen'
			3. The x86 assembly code in 'output.s'
			4. Object file 'output.o' and
			5. The executable binary in 'output'

STEP 2: Cleaning the working directory:

		user@computer$ rm output output.o output.s lexer.pyc lex.pyc parser.out parsetab.py parsetab.pyc symbolTable.gen symbolTable.pyc tac.pyc Three_Address_Code.gen yacc.pyc

+-------------------------------------------------------------------------------+
|	FEATURES IMPLEMENTED														|
+-------------------------------------------------------------------------------+
1. DATA TYPES: Strings and numbers (Arrays only till 3-AC implementation)
2. OPERATIONS: 	- Addition, Subtraction, Multiplication, Division, Unary Minus,
				- Less than, greater than, Less equal, Greater equal, equal to, not equal to
				- All operations follow the correct precedence and associativity
3. ASSIGNMENTS:	*	Normal assignment
				*	Advance Assignment (+=, -=, *=, /=)
				*	increment and decrement not implemented
4. CONDITIONAL OPERATIONS: If-then, If-then-else, Unless, ternary operation and Switch
5. LOOP OPERATIONS: While, Do-while, Until, For
				* Loops support "next" and "last" statements
6. FUNCTIONS:   -	Do not take parameters because all variables in perl are GLOBAL (unless specified otherwise).
					Hence, any parameter that has to be passed in a function will already be in the global scope.
				-	Recursion in functions in supported.
				-	Functions do NOT work if constant numbers are returned (eg. return 5;)


+---------------------------------------------------+
|	LIMITATIONS AND VARIATIONS IN IMPLEMENTATION 	|
+---------------------------------------------------+
	>	strings cannot be redefined as new strings
	> 	Can't use 'name', 'parent', 'root', 'type', 'scope', 'returntype', 'scope_depth' as variable or function names
	>	You cannot use return more than once in a function. What ever you want to return, boil it down to a single variable and then return that variable
	> 	It goes without saying that you can return only one kind of value from a function (else it will give trouble even where it is called)... {This has to be stated because a programmer may switch the return value type based on context inside a Functions}
	> 	Additionally you cannot change the type of a variable to which you are returning from a function.
	>	Concatenate can only occur on strings (although there is no restriction on the number of strings that can be concatenated at a time)

+-----------------------------------------------------+
|	ERROR REPORTING									  |
+-----------------------------------------------------+

	~ 	Till the parsing phase, any error will only be reported to exist.
	~	In the semantic phase, the line number is also printed along with the error committed.

+----------------------------------------------------+
|	COMMENTS										 |
+----------------------------------------------------+

> not giving zero integer value to strings. (Like perl does)
> cannot compare booleans 
	i.e. (a>b)==(c<d) will raise ERROR
> Hash (%hashName) not implemented
> Multiple assignments in a single statement are now not allowed


##################### Not necessary now.. only for reference #################
	as -32 output.s -o output.o
	ld -m elf_i386 output.o -o output
