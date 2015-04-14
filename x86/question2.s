# PURPOSE: Check whether a given number is prime or not

.section .data

number:
.long 73

str1:
.ascii " is a prime number.\n"
str1_end:

str2:
.ascii " is not a prime number.\n"
str2_end:

.section .text

.globl _start

_start:
  movl number, %ebx     # store the number in %ebx
  call check_prime      # function call
  movl $1, %eax         # system call number for exit
  movl $0, %ebx         # value written to terminal
  int $0x80 
         
 check_prime:
# we look for factors from 2 onwards till we get to a number x such that when the original #number(dividend) is divided by this x, the quotient is greater than x. Basically we look for #divisors from 2 to sqyare root(n). If in this range if we find some factor, then the number n #is not prime, else it is prime .
# %ebx contains the original input number
   
    cmpl $1, %ebx  # checking if the input number is 1  
    
    je prnt   # if the number is 1, we we directly go to (prnt:) to print it as not prime       

    movl $0, %ebp  # %ebp is indicator of whether the number is prime or not. If %ebp=0, it is                                         
                  # prime and if %ebp=1, it is not prime. and %ebp is initialized with 0(prime) 
                  # as %ebp is set to 1 only if we find some non-trivial divisor of the number
  
    movl $2, %edi  # %edi is used to store the current value (of divisor) that we are using to  
                   # test if it is a factor of n, starting from 2 onwards
 loop1: 
     cmpl %ebx, %edi  
     
     je prnt     # Ensuring that the number itself is not used to check if it is a factor
                 # of itself. In that case we jump to print
     
     movl %ebx, %eax  # move number to %eax as idivil requires that the, number to be
                      # divided should be kept in %eax  
     
     cdq             # preparing to divide
    
     divl %edi   # %edi contains the current divisor under test 
    
     cmpl $0, %edx   # %edx contains the remainder and we are checking if remainder=0 

     jne test     # if remainder not equal to 0, then we jump to label (test:)
   
     movl $1, %ebp   # if remainder=0 ,we indicate that n is not prime by putting 1 in %ebp 
  
     jmp prnt   # jump to print as we have found that n is not prime
   
     test:
     cmpl %eax, %edi  # comparing the quotient from division and the current divisor to 
                      # ascertain whether the value in %edi (the current divisor) is greater 
                      # than sq. root(n)   
    
     jg prnt          # if the current divisor is greater than sq.root(n), this means we have 
                      # completed checking all possible divisors so we jump off to prnt
                      
     incl %edi  #divisor value for next iteration of loop is obtained by incrementing %edi by 1
     
     jmp loop1  # jump back to test for other factors
   
   prnt:
   movl %ebx, %edi  #store the number in % edi as %ebx would be modified here
  
# code to print the number -> same as in question 1    
 
    movl number, %eax #storing number in %eax to divide it by 10 and extract digits one by one                  
    movl %esp, %esi   #storing the initial position of the stack pointer in %esi register
    labl:
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
    movl %edx, number+50 # storing the corresponding ascii character into some memory adress
                      #say (number +50) which is randomly chosen memory location to store it
                      # we store it in a memory location to print it by using sytem call no.4 
    
    movl $4, %eax  # 4 is sys call number
    movl $1, %ebx  # 1 refers to stdout
    movl $(number+50), %ecx  # number+50 refers to location where the digit is stored in memory 
    movl $1, %edx    # size of buffer =1, as we print one digit at a time 
    int $0x80    
    cmp %esp, %esi   # checking if the current stack pointer has reached the initial postion
                     # of stack pointer which we stored in %esi at the beginning, before 
                     # starting to push any value
    jne print_num   #if stack pointer has not reached the initial position of stack, we jump 
                    #back to print_num label to pop more values and print them.
      
   cmp $1, %edi
   je print_not_prime  # if number is 1 directly print it as not prime   
   
   cmpl $0, %ebp     # checking if the number was prime or not to print it accordingly as %ebp
                     # is indicator of whether the number is prime or not 
   je print_prime    # if %ebp=0, then we jump to print that it is prime
                     # else we print it as not-prime here right below
  
  
  print_not_prime : 
  # printing the string "is not a prime number.\n" here below
  
   movl $4, %eax                    # 4 is the system call number
   movl $1, %ebx                    # 1 stands for stdout
   movl $str2, %ecx                 # Location of the buffer
   movl $(str2_end - str2), %edx    # Size of the buffer
   int $0x80
   
 ret      # if the number is not a prime, then function returns from here
  
  print_prime:
   # printing the string "is a prime number.\n" here below   
   
   movl $4, %eax                    # 4 is the system call number
   movl $1, %ebx                    # 1 stands for stdout
   movl $str1, %ecx                 # Location of the buffer
   movl $(str1_end - str1), %edx    # Size of the buffer
   int $0x80
   
  ret    # if the number is a prime, then function returns from here
   
   
   
    
    
    
    
    
    
    
    
    



