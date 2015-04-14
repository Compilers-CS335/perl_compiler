.section .data
c_str__ing__:
.ascii	"nikhiltanana"
c_len = . - c_str__ing__
temp4:
.ascii	"tanana"
temp4_len = . - temp4
temp5:
.ascii	"nikhiltanana"
temp5_len = . - temp5
temp6:
.ascii	"nikhil"
temp6_len = . - temp6
temp7:
.ascii	"nikhiltanana"
temp7_len = . - temp7
a_str__ing__:
.ascii	"nikhil"
a_len = . - a_str__ing__
temp1:
.ascii	"nikhil"
temp1_len = . - temp1
temp2:
.ascii	"tanana"
temp2_len = . - temp2
temp3:
.ascii	"nikhil"
temp3_len = . - temp3
b_str__ing__:
.ascii	"tanana"
b_len = . - b_str__ing__
.section .text
true:
movl	$1,%eax
ret
.globl _start
_start:
pushl	%ebp
movl	%esp,%ebp
movl	$4,%eax
movl	$1,%ebx
movl	$temp7,%ecx
movl	$temp7_len,%edx
int	$0x80
movl	$1,%eax
movl	$0,%ebx
int	$0x80
