.section .data
number:
.long 12

.section .text


.globl _start
_start:
pushl   %ebp
movl    %esp,%ebp
movl    $10,number
movl	$10,-4(%ebp) 
movl	-4(%ebp),%ecx
movl	$10,-4(%ebp)
movl	-4(%ebp),%eax
addl	%ecx,%eax
movl	%eax,-4(%ebp)
movl    -4(%ebp),%eax
movl	%eax,%ebx
movl	$1,%eax
int	$0x80

