	.section .data
	.section .text
	.globl _start

_start:
	call main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80

	.type main, @function
main:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl $15, %ecx
	pushl %ecx
	movl $3, %ecx
	movl $5, %ecx
	movl %ecx, -4(%ebp)
	movl $6, -4(%ebp)
	leal -4(%ebp), %ecx
	movl %ecx, -8(%ebp)
	movl -8(%ebp), %esi
	movl (%esi), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret
