	.section .data
	.section .text
	.globl _start

_start:
	call main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80

	.type exit_noerr, @function
exit_noerr:
	pushl %ebp
	movl %esp, %ebp
	movl $0, %ecx
	movl %ecx, %ebx
	movl $1, %eax
	int $0x80
	movl %ebp, %esp
	popl %ebp
	ret

	.type exit_err, @function
exit_err:
	pushl %ebp
	movl %esp, %ebp
	movl $1, %ecx
	movl %ecx, %ebx
	movl $1, %eax
	int $0x80
	movl %ebp, %esp
	popl %ebp
	ret

	.type other, @function
other:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $'a', %ecx
	movl %ecx, -4(%ebp)
	xorl %edx, %edx
	movl $5, %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	popl %edx
	addl %edx, %ecx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %ecx
	movl %ecx, %ebx
	movl $1, %eax
	int $0x80
	movl %ebp, %esp
	popl %ebp
	ret

	.type main, @function
main:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl $1, %ecx
	movl %ecx, -4(%ebp)
	movl $0x0a, %ecx
	movl %ecx, -8(%ebp)
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret
