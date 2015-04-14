.section .data
c:
	.long	30
.section .text
true:
movl	$1,%eax
ret
.globl _start
_start:
pushl	%ebp
movl	%esp,%ebp
movl	$40,-4(%ebp)
movl	$30,-8(%ebp)
movl	-4(%ebp),%eax
imull	-8(%ebp),%eax
movl	%eax,-12(%ebp)
movl	-12(%ebp),%eax
movl	%eax,c
movl	$1,%eax
movl	c,%ebx
int	$0x80

