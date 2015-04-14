.section .data
i_num__ber__:
	.long	0
temp7:
.ascii	"\n"
temp7_len = . - temp7
a_num__ber__:
	.long	0
.section .text
true:
movl	$1,%eax
ret
.globl _start
_start:
pushl	%ebp
movl	%esp,%ebp
subl	$2000,%esp
movl	$10,-4(%ebp)
movl	-4(%ebp),%eax
movl	%eax,a_num__ber__
movl	$1,-8(%ebp)
movl	-8(%ebp),%eax
movl	%eax,i_num__ber__
call giveTwenty
movl	%ebx,-12(%ebp)
movl	-12(%ebp),%eax
movl	%eax,a_num__ber__
movl	a_num__ber__,%ecx
call printIntNumber
movl	$1,%eax
movl	$0,%ebx
int	$0x80
giveTwenty:
pushl %eax
pushl %ecx
pushl %edx
pushl %edi
pushl %esi
pushl	%ebp
movl	%esp,%ebp
subl	$2000,%esp
movl	a_num__ber__,%ecx
call printIntNumber
movl	$20,-4(%ebp)
movl	i_num__ber__,%eax
movl	-4(%ebp),%ebx
cmpl	%eax,%ebx
jl	label_14
movl	$5,-8(%ebp)
movl	i_num__ber__,%eax
addl	-8(%ebp),%eax
movl	%eax,i_num__ber__
movl	$1,-12(%ebp)
movl	a_num__ber__,%eax
addl	-12(%ebp),%eax
movl	%eax,a_num__ber__
movl	a_num__ber__,%ecx
call printIntNumber
movl	$4,%eax
movl	$1,%ebx
movl	$temp7,%ecx
movl	$temp7_len,%edx
int	$0x80
movl	%ebp,%esp
popl	%ebp
popl %esi
popl %edi
popl %edx
popl %ecx
popl %eax
ret
jmp	label_17
label_14:
call giveTwenty
movl	%ebx,-16(%ebp)
movl	-16(%ebp),%ebx
movl	%ebp,%esp
popl	%ebp
popl %esi
popl %edi
popl %edx
popl %ecx
popl %eax
ret
label_17:
movl	%ebp,%esp
popl	%ebp
popl %esi
popl %edi
popl %edx
popl %ecx
popl %eax
ret



jmp EndPrintNum
printIntNumber:
	pushl %eax #save the  registers
	pushl %ebx
	pushl %ecx
	pushl %edx
	pushl %edi
	pushl %esi
	pushl %ebp
	
    movl %ecx, %eax #storing number in %eax to divide it by 10 and extract digits one by one
    movl %esp, %esi   #storing the initial position of the stack pointer in %esi register
    labl:
    #%eax has quotient after div and %edx has the remainder after division. div R1 does %eax / R1
    cdq    # preparing to divide
    movl $10, %ebx    # store 10 in %ebx register which is the divisor             
    idivl %ebx   #divide number by 10.remainder and quotient are stored in %edx and %eax resp. 
                 #Remainder is the least significant digit of the current number 
    pushl %edx   # pushing the least significant digit (remainder) into stack
    cmpl $0, %eax #comparing quotient with 0 to ascertain whether have we extracted all digits
    jne labl #If q not equal to zero,then we still need to continue extracting more digits,so
             # jump back to labl  
    jmp print_num   # if q=0, then jump to print_num
    
 print_num:
    popl %edx  # poping the topmost element from stack which would be the highest significant 
               # digit of our number as it was pushed last into the stack
    addl $48, %edx  # converting the digit to ascii character by adding 48 to that digit 
                   # as, 48 is the ascii code for digit 0, 49 for 1, 50 for 2 and so on...
    pushl %edx # s is randomly chosen memory location to store it
                      # we store it in a memory location to print it by using sytem call no.4 
    
    movl $4, %eax  # 4 is sys call number
    movl $1, %ebx  # 1 refers to stdout
    movl %esp, %ecx  # number+50 refers to location where the digit is stored in memory 
    movl $1, %edx    # size of buffer =1, as we print one digit at a time 
    int $0x80
    popl %edx       # Pop the digit on the top  
    cmp %esp, %esi   # checking if the current stack pointer has reached the initial postion
                     # of stack pointer which we stored in %esi at the beginning, before 
                     # starting to push any value
    jne print_num   #if stack pointer has not reached the initial position of stack, we jump 
                    #back to print_num label to pop more values and print them.
    popl %ebp #restore the registers
    popl %esi
    popl %edi
    popl %edx
    popl %ecx
    popl %ebx
    popl %eax
    ret  
    EndPrintNum:
