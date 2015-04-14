.section .data
temp5:
.ascii	"temp"
temp5_len = . - temp5
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
movl	$10,-4(%ebp)
movl	-4(%ebp),%edi
movl	%edi,a_num__ber__
label_2:
movl	a_num__ber__,%edi
movl	%edi,-8(%ebp)
movl	$20,-12(%ebp)
movl	-8(%ebp),%eax
movl	-12(%ebp),%ebx
cmpl	%eax,%ebx
jl	label_13
movl	$4,%eax
movl	$1,%ebx
movl	$temp5,%ecx
movl	$temp5_len,%edx
int	$0x80
movl	a_num__ber__,%edi
movl	%edi,-16(%ebp)
movl	$1,-20(%ebp)
movl	-16(%ebp),%eax
addl	-20(%ebp),%eax
movl	%eax,-24(%ebp)
movl	-24(%ebp),%edi
movl	%edi,a_num__ber__
jmp	label_2
label_13:
movl	$1,%eax
movl	$0,%ebx
int	$0x80
