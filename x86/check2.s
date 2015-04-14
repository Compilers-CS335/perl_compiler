.section .data
c:
    .long   -14
.section .text
true:
movl    $1,%eax
ret
.globl _start
_start:
pushl   %ebp
#call    printIntNumber
movl    %esp,%ebp
movl    c, %ecx
movl    %ecx,-4(%ebp)
movl    $1,-8(%ebp)
movl    -4(%ebp),%eax
imull   -8(%ebp),%eax
movl    %eax,-12(%ebp)
movl    -12(%ebp),%eax
movl    %eax,c
movl    c, %ecx
call printIntNumber
movl    $1,%eax
movl    $0,%ebx
int $0x80







jmp EndPrintNum
printIntNumber:
    pushl %eax #save the  registers
    pushl %ebx
    pushl %ecx
    pushl %edx
    pushl %edi
    pushl %esi
    pushl %ebp
    
    cmpl $0, %ecx
    jge positive_print
    notl     %ecx   #Take BIT wise NOT
    inc %ecx
    movl %ecx, %edi

    movl    $45, %eax
    pushl   %eax

    movl $4, %eax
    movl $1, %ebx
    movl %esp, %ecx
    movl $1, %edx
    int $0x80
    popl %eax
    movl %edi, %ecx


    positive_print:
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
