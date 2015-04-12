.section .data
temp1:
.ascii	"hello"
temp1_len = . - temp1
temp2:
.ascii	"world"
temp2_len = . - temp2
a:
.ascii	"world"
a_len = . - a
.section .text
.globl _start
_start:
pushl	%ebp
movl	%esp,%ebp
movl	$4,%eax
movl	$1,%ebx
movl	$temp1,%ecx
movl	$temp1_len,%edx
int	$0x80
movl	$4,%eax
movl	$1,%ebx
movl	$a,%ecx
movl	$a_len,%edx
int	$0x80
movl	$1,%eax
movl	$0,%ebx
int	$0x80
