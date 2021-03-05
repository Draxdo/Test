	.section .data

strLOCK0:
	.asciz "\n"

strLOCK2:
	.asciz "Hello. Please enter your name >>> "

strLOCK3:
	.asciz "%s"

strLOCK4:
	.asciz "You entered: %s\n"
	.section .bss

.lcomm BSSLOCK1, 65
	.section .text
	.globl _start

_start:
	call main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80

	.type printl, @function
printl:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl 8(%ebp), %ecx
	pushl %ecx
	call printf
	movl %eax, %ecx
	movl %ecx, -4(%ebp)
	movl $strLOCK0, %ecx
	pushl %ecx
	call printf
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	xorl %edx, %edx
	movl -8(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	popl %edx
	addl %edx, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type main, @function
main:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl $BSSLOCK1, %ecx
	movl %ecx, -4(%ebp)
	movl $strLOCK2, %ecx
	pushl %ecx
	call printf
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	movl $strLOCK3, %ecx
	pushl %ecx
	call scanf
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	movl $strLOCK4, %ecx
	pushl %ecx
	call printf
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret
