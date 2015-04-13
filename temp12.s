.section .data
.section .text
.globl _start
exit:
movl $1,%eax
int $0x80
_start:
movl $0,%eax
movl $12,%ebx
movl %rip,%edx
jmp   true
movl %eax,%ebx
jmp exit
true:
movl $1,%eax
jmp *1(%edx)
