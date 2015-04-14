# PURPOSE: Reverse the input string in place and then print

.section .data

input_str_begin:
 .ascii "Hello World"
input_str_end:

.section .text

.globl _start

_start:
  
  call reverse   # calling function reverse which is responsible for reversing and printing
                 # the string  
  
  movl $1, %eax  # 1 is system call number for exit
 
  movl $0, %ebx  # value written to the terminal
 
  int $0x80 
  
  
reverse:
  movl $input_str_begin, %ecx  # storing the start location of input string in %ecx--
                               #-- in order to use it for further manipulation 

  movl $input_str_end , %edx   # storing the end location of input string in %edx--
                               #-- in order to use it for further manipulation 

 loop:
# methodology: we have pointers to start and end location of input string. we exchange the #contents of both these pointers and then increment start pointer and decrement the end pointer #till they cross eachother.   

  cmpl %ecx, %edx    #compare both the pointers to find whether they have crossed eachother                   
                    # loop runs till the start and end location of pointers cross eachother
 
  jle prnt   # go to prnt if end location is less than or equal to start location

#Note: movb and xchgb are used for byte level transfers
  
  movb (%ecx), %bl  # store the current start charcter in a temporary 8-bit register %bl
                # (%ecx) is the value at the location given by %ecx->indirect addressing mode

  movb (%edx), %al  # store the current last charcter in a temporary 8-bit register %al
                # (%edx) is the value at the location given by %edx->indirect addressing mode

  xchgb %bl, %al  # exchanging the contents at the current extremes
 
  movb %bl, (%ecx) # copy back the exchanged values into their memory location

  movb %al, (%edx) # copy back the exchanged values into their memory location

#NOTE: we are having to copy the charcters to temporary registers before we exchange them as #xchg does not work with indirect addressing mode or else could have done:xchgb (%ecx),(%edx)
#directly. so only we copy them to temporary registers %bl and %al before we exchange them  

  incl %ecx    # incrementing the start location pointer 

  decl %edx    # decrementing the end location pointer 

  jmp loop     # loop back
  
 prnt:
 # prints the string

  movl $4, %eax                   # 4 is the system call number

  movl $1, %ebx                   # 1 stands for stdout

  movl $input_str_begin, %ecx                     # Location of the buffer

  movl $(input_str_end - input_str_begin+1), %edx    # Size of the buffer

  int $0x80

  ret                             # after printing, we return
  
