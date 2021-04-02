	.section .data

strLOCK2:
	.asciz "Hello World"

strLOCK3:
	.asciz "%s\n"


L45SDEF:

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

	subl $4, %esp
	pushl $100
	call malloc
	movl %eax, %ecx
	movl %ecx, -4(%ebp)
	movl $strLOCK2, %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call strcpy
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	movl $strLOCK3, %ecx
	pushl %ecx
	call printf
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver1
	.leaver1:
	movl %ebp, %esp
	popl %ebp
	ret
