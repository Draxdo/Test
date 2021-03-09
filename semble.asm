	.section .data
	.section .bss
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

	subl $32, %esp
	movl $'H', %ecx
	movl %ecx, -4(%ebp)
	movl $'e', %ecx
	movl %ecx, -8(%ebp)
	movl $'l', %ecx
	movl %ecx, -12(%ebp)
	movl $'l', %ecx
	movl %ecx, -16(%ebp)
	movl $'o', %ecx
	movl %ecx, -20(%ebp)
	movl $0x0a, %ecx
	movl %ecx, -24(%ebp)
	movl $0x00, %ecx
	movl %ecx, -28(%ebp)
	movl -4(%ebp), %ecx
	movl %ecx, -32(%ebp)
	movl -32(%ebp), %ecx
	movl %ecx, %ebx
	movl $1, %eax
	int $0x80
	movl %ebp, %esp
	popl %ebp
	ret
