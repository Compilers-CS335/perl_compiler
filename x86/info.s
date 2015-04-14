.section .data
output:
     .ascii "The processor vendor ID is 'xxxxxxxxxxxx'\\n"

.section .text
.globl _start
_start:
	movl $0, %eax		#0 for the Vendor ID and Max CPUID option value supported
	cpuid
	movl $output, %edi   # %edi has the pointer to output string
	movl %ebx, 28(%edi)
	movl %edx, 32(%edi)
	movl %ecx, 36(%edi)
	movl $4, %eax        # 4 for printing it to %ebx file
	movl $1, %ebx        # 1 for STDOUT
	movl $output, %ecx   # ecx has pointer to the output string
	movl $43, %edx
	int $0x80           # system call
	movl $1, %eax	    # 1 is for exit
	movl $0, %ebx       #The value returned by program to terminal
	int $0x80
