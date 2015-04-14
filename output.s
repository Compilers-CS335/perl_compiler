.section .data
ret_str__ing__:
.ascii	"aavik"
ret_len = . - ret_str__ing__
temp8:
.ascii	"aavik"
temp8_len = . - temp8
temp14:
.ascii	"aavik"
temp14_len = . - temp14
temp15:
.ascii	"aavik"
temp15_len = . - temp15
a_num__ber__:
	.long	0
temp11:
.ascii	"\n"
temp11_len = . - temp11
temp12:
.ascii	"aavik"
temp12_len = . - temp12
temp13:
.ascii	"aavik"
temp13_len = . - temp13
b_str__ing__:
.ascii	"aavik"
b_len = . - b_str__ing__
i_num__ber__:
	.long	0
.section .text
true:
movl	$1,%eax
ret
.globl _start
_start:
pushl	%ebp
movl	%esp,%ebp
movl	$10,-4(%ebp)
movl	-4(%ebp),%edi
movl	%edi,a_num__ber__
movl	$1,-8(%ebp)
movl	-8(%ebp),%edi
movl	%edi,i_num__ber__
call giveTwenty
movl	$4,%eax
movl	$1,%ebx
movl	$temp15,%ecx
movl	$temp15_len,%edx
int	$0x80
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
movl	a_num__ber__,%edi
movl	%edi,-4(%ebp)
movl	-4(%ebp),%ecx
call printIntNumber
movl	i_num__ber__,%edi
movl	%edi,-8(%ebp)
movl	$20,-12(%ebp)
movl	-8(%ebp),%eax
movl	-12(%ebp),%ebx
cmpl	%eax,%ebx
jle	label_13
movl	$5,-16(%ebp)
movl	i_num__ber__,%eax
addl	-16(%ebp),%eax
movl	%eax,i_num__ber__
call giveTwenty
jmp	label_21
label_13:
movl	$1,-20(%ebp)
movl	a_num__ber__,%eax
addl	-20(%ebp),%eax
movl	%eax,a_num__ber__
movl	a_num__ber__,%edi
movl	%edi,-24(%ebp)
movl	-24(%ebp),%ecx
call printIntNumber
movl	$4,%eax
movl	$1,%ebx
movl	$temp11,%ecx
movl	$temp11_len,%edx
int	$0x80
label_21:
movl	%ebp,%esp
popl	%ebp
popl %esi
popl %edi
popl %edx
popl %ecx
popl %eax
ret
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
