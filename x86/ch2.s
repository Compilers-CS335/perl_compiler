# imultest.s - An example of the IMUL instruction formats
.section .data
number:
	.long -8888
number:
    .ascii "Hello"
value1:
	.long 1
value2:
	.long 3530000

.section .text
.globl _start
_start:
movl value1, %ebx
movl value2, %ecx
imul %ebx, %ecx
#movl value3, %edx
#imull $2, %edx, %eax
#movl number, %ecx
movl %ecx, %ecx
call printIntNumber

movl $0, %ebx
#movl %ecx, %ebx
movl $1, %eax
int $0x80



jmp EndPrintNum
printIntNumber:
   #movl %ecx, %edi  #store the number in % edi as %ebx would be modified here
  
# code to print the number -> same as in question 1    
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
    ret  
EndPrintNum:
