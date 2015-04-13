.section .data
b:
	.long	13
c:
	.long	19
a:
	.long	12
.section .text
.globl _start
_start:
pushl	%ebp
movl	%esp,%ebp
movl	$10,-4(%ebp)
movl	-4(%ebp),%eax
movl	%eax,a
movl	$19,-8(%ebp)
movl	-8(%ebp),%eax
movl	%eax,b
movl	a,%eax
addl	b,%eax
movl	%eax,-12(%ebp)
movl	-12(%ebp),%eax
movl	%eax,c
movl	$12,-16(%ebp)
movl	c,%eax
addl	-16(%ebp),%eax
movl	%eax,-20(%ebp)
movl	-20(%ebp),%eax
movl	%eax,a
movl	$13,-24(%ebp)
movl	-24(%ebp),%eax
addl	a,%eax
movl	%eax,-28(%ebp)
movl	-28(%ebp),%eax
movl	%eax,b
movl	$14,-32(%ebp)
movl	c,%eax
addl	-32(%ebp),%eax
movl	%eax,c
movl	c,%eax
addl	a,%eax
movl	%eax,c
movl	$1,%eax
movl	$0,%ebx
int	$0x80

