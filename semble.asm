	.section .data

globalLOCK1:
	.long 0

strLOCK6:
	.asciz "%s\n"

strLOCK17:
	.asciz "Hello "

strLOCK18:
	.asciz "World!"

strLOCK19:
	.asciz " Jimmy!"


L45SDEF:

	.section .bss
	.section .text
	.globl _start

_start:
	movl $0x80, %ecx
	movl %ecx, globalLOCK1
	call main
	movl %eax, %ebx
	movl $1, %eax
	int $0x80

	.type Size, @function
Size:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	pushl $4
	call malloc
	movl %eax, -4(%ebp)
	movl 8(%ebp), %ecx
	movl -4(%ebp), %ebx
	movl %ecx, (%ebx)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver2
	.leaver2:
	movl %ebp, %esp
	popl %ebp
	ret

	.type Space, @function
Space:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl 8(%ebp), %ecx
	pushl %ecx
	call malloc
	movl %eax, %ecx
	movl %ecx, -4(%ebp)
	pushl $8
	call malloc
	movl %eax, -8(%ebp)
	movl -4(%ebp), %ecx
	movl -8(%ebp), %ebx
	movl %ecx, (%ebx)
	movl 8(%ebp), %ecx
	movl -8(%ebp), %ebx
	movl %ecx, 4(%ebx)
	movl -8(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver3
	.leaver3:
	movl %ebp, %esp
	popl %ebp
	ret

	.type resizeSpace, @function
resizeSpace:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call realloc
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	movl 8(%ebp), %ebx
	movl 4(%ebx), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	movl -8(%ebp), %ecx
	pushl %ecx
	call memcpy
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver4
	movl 12(%ebp), %ecx
	movl 8(%ebp), %ebx
	movl %ecx, 4(%ebx)
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver4
	movl -8(%ebp), %ecx
	movl 8(%ebp), %ebx
	movl %ecx, (%ebx)
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver4
	movl 12(%ebp), %ecx
	movl 8(%ebp), %ebx
	movl %ecx, 4(%ebx)
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver4
	.leaver4:
	movl %ebp, %esp
	popl %ebp
	ret

	.type write, @function
write:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl 12(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -4(%ebp)
	movl globalLOCK1, %edi
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl 16(%ebp), %ebx
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl $4, %eax
	movl globalLOCK1, %edi
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl 12(%ebp), %edx
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl $4, %eax
	movl globalLOCK1, %edi
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl 8(%ebp), %ecx
	movl globalLOCK1, %edi
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl 16(%ebp), %ebx
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	movl $4, %eax
	movl globalLOCK1, %edi
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver5
	.leaver5:
	movl %ebp, %esp
	popl %ebp
	ret

	.type print, @function
print:
	pushl %ebp
	movl %esp, %ebp
	movl 8(%ebp), %ecx
	pushl %ecx
	movl $strLOCK6, %ecx
	pushl %ecx
	call printf
	popl %ebx
	.leaver6:
	movl %ebp, %esp
	popl %ebp
	ret

	.type String, @function
String:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	pushl $4
	call malloc
	movl %eax, -4(%ebp)
	movl 8(%ebp), %ecx
	movl -4(%ebp), %ebx
	movl %ecx, (%ebx)
	movl $0, %ecx
	movl -4(%ebp), %ebx
	movl %ecx, 4(%ebx)
	movl $0, %ecx
	movl -4(%ebp), %ebx
	movl %ecx, 8(%ebx)
	movl 8(%ebp), %ecx
	pushl %ecx
	call strlen
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver8
	leal -4(%ebp), %ecx
	movl -4(%ebp), %ebx
	movl %ecx, 8(%ebx)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver8
	movl -8(%ebp), %ecx
	movl -4(%ebp), %ebx
	movl %ecx, 4(%ebx)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver8
	leal -4(%ebp), %ecx
	movl -4(%ebp), %ebx
	movl %ecx, 8(%ebx)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver8
	.leaver8:
	movl %ebp, %esp
	popl %ebp
	ret

	.type stringLength, @function
stringLength:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	pushl $4
	call malloc
	movl %eax, -4(%ebp)
	movl $0, %ecx
	movl -4(%ebp), %ebx
	movl %ecx, (%ebx)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver9
	movl 8(%ebp), %ecx
	pushl %ecx
	call strlen
	movl %eax, %ecx
	movl -4(%ebp), %ebx
	movl %ecx, (%ebx)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver9
	.leaver9:
	movl %ebp, %esp
	popl %ebp
	ret

	.type nullLength, @function
nullLength:
	pushl %ebp
	movl %esp, %ebp
	movl 8(%ebp), %ecx
	pushl %ecx
	call strlen
	movl %eax, %ecx
	movl %ecx, %eax
	jmp .leaver10
	.leaver10:
	movl %ebp, %esp
	popl %ebp
	ret

	.type areStringsEqual, @function
areStringsEqual:
	pushl %ebp
	movl %esp, %ebp
	movl 12(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	movl 8(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	call strcmp
	movl %eax, %ecx
	pushl %ecx
	movl $0, %ecx
	popl %edx
	cmpl %ecx, %edx
	jne .ne11
	movl $1, %ecx
	movl %ecx, %eax
	jmp .leaver11
	.ne11:
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver11
	.leaver11:
	movl %ebp, %esp
	popl %ebp
	ret

	.type copyString, @function
copyString:
	pushl %ebp
	movl %esp, %ebp
	movl 12(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	movl 8(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	call strcpy
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	jmp .leaver13
	.leaver13:
	movl %ebp, %esp
	popl %ebp
	ret

	.type stringCat, @function
stringCat:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $1000, %ecx
	pushl %ecx
	call Space
	movl %eax, %ecx
	movl %ecx, -4(%ebp)
	movl 8(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	movl -4(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	call strcpy
	popl %ebx
	movl 12(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	movl -4(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	call strcat
	popl %ebx
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver14
	.leaver14:
	movl %ebp, %esp
	popl %ebp
	ret

	.type String__add__, @function
String__add__:
	pushl %ebp
	movl %esp, %ebp

	subl $12, %esp
	movl $1000, %ecx
	pushl %ecx
	call Space
	movl %eax, %ecx
	movl %ecx, -4(%ebp)
	movl 8(%ebp), %ebx
	movl (%ebx), %ecx
	movl %ecx, -8(%ebp)
	movl -8(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	call strcpy
	popl %ebx
	movl 12(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	movl -4(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	call strcat
	popl %ebx
	pushl $4
	call malloc
	movl %eax, -12(%ebp)
	movl -4(%ebp), %ebx
	movl (%ebx), %ecx
	movl -12(%ebp), %ebx
	movl %ecx, (%ebx)
	movl $0, %ecx
	movl -12(%ebp), %ebx
	movl %ecx, 4(%ebx)
	movl $0, %ecx
	movl -12(%ebp), %ebx
	movl %ecx, 8(%ebx)
	movl -12(%ebp), %ecx
	movl %ecx, %eax
	jmp .leaver15
	.leaver15:
	movl %ebp, %esp
	popl %ebp
	ret

	.type String__sub__, @function
String__sub__:
	pushl %ebp
	movl %esp, %ebp
	.leaver16:
	movl %ebp, %esp
	popl %ebp
	ret

	.type main, @function
main:
	pushl %ebp
	movl %esp, %ebp

	subl $16, %esp
	movl $strLOCK17, %ecx
	pushl %ecx
	call String
	movl %eax, %ecx
	movl %ecx, -4(%ebp)
	movl $strLOCK18, %ecx
	pushl %ecx
	call String
	movl %eax, %ecx
	movl %ecx, -8(%ebp)
	movl $strLOCK19, %ecx
	pushl %ecx
	call String
	movl %eax, %ecx
	movl %ecx, -12(%ebp)
	movl -12(%ebp), %ecx
	pushl %ecx
	movl -8(%ebp), %ecx
	pushl %ecx
	call String__add__
	movl %eax, %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call String__add__
	movl %eax, %ecx
	movl %ecx, -16(%ebp)
	movl -16(%ebp), %ebx
	movl (%ebx), %ecx
	pushl %ecx
	movl $strLOCK6, %ecx
	pushl %ecx
	call printf
	popl %ebx
	.leaver17:
	movl %ebp, %esp
	popl %ebp
	ret
