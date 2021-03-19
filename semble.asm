	.section .data

strLOCK0:
	.asciz "\n"

strLOCK1:
	.asciz " %[^\n]"

strLOCK2:
	.asciz "%d"

strLOCK3:
	.asciz " %c"

strLOCK6:
	.asciz "w"

strLOCK7:
	.asciz "a"

strLOCK8:
	.asciz "r"

strLOCK13:
	.asciz ""

strLOCK14:
	.asciz "%d\n"

strLOCK15:
	.asciz "Jerry"

strLOCK16:
	.asciz "Pasta"
	.section .bss

.lcomm BSSLOCK11, 100

.lcomm BSSLOCK12, 100
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
	call print
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl $strLOCK0, %ecx
	pushl %ecx
	call print
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -8(%ebp)
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

	.type print, @function
print:
	pushl %ebp
	movl %esp, %ebp
	movl 8(%ebp), %ecx
	pushl %ecx
	call printf
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type strInput, @function
strInput:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	leal 8(%ebp), %ecx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %esi
	movl (%esi), %ecx
	pushl %ecx
	movl $strLOCK1, %ecx
	pushl %ecx
	call scanf
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type intInput, @function
intInput:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $0, %ecx
	movl %ecx, -4(%ebp)
	leal -4(%ebp), %ecx
	pushl %ecx
	movl $strLOCK2, %ecx
	pushl %ecx
	call scanf
	popl %ebx
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type charInput, @function
charInput:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $' ', %ecx
	movl %ecx, -4(%ebp)
	leal -4(%ebp), %ecx
	pushl %ecx
	movl $strLOCK3, %ecx
	pushl %ecx
	call scanf
	popl %ebx
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type pow, @function
pow:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl 12(%ebp), %ecx
	pushl %ecx
	movl $0, %ecx
	popl %edx
	cmpl %ecx, %edx
	jne .ne4
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	.ne4:
	movl 8(%ebp), %ecx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	pushl %ecx
	movl $1, %ecx
	popl %edx
	cmpl %ecx, %edx
	jle .le5
	.LFB6:
	movl 12(%ebp), %ecx
	pushl %ecx
	movl $1, %ecx
	popl %edx
	cmpl %ecx, %edx
	jg .LFB6
	.le5:
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type input, @function
input:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl 12(%ebp), %ecx
	movl %ecx, -4(%ebp)
	movl 8(%ebp), %ecx
	pushl %ecx
	call printl
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call strInput
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type int_to_string, @function
int_to_string:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl 8(%ebp), %ecx
	pushl %ecx
	movl $strLOCK2, %ecx
	pushl %ecx
	movl 12(%ebp), %ecx
	pushl %ecx
	call sprintf
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type string_to_int, @function
string_to_int:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl $0, %ecx
	movl %ecx, -4(%ebp)
	leal -4(%ebp), %ecx
	pushl %ecx
	movl $strLOCK2, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call sscanf
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -8(%ebp)
	movl -4(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type fprintl, @function
fprintl:
	pushl %ebp
	movl %esp, %ebp
	movl 12(%ebp), %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fprintf
	popl %ebx
	movl $strLOCK0, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fprintf
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type writef, @function
writef:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $strLOCK6, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fprintf
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type writefl, @function
writefl:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $strLOCK6, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fprintl
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type appendf, @function
appendf:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $strLOCK7, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fprintf
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type appendfl, @function
appendfl:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $strLOCK7, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl 12(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fprintl
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type readf, @function
readf:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $strLOCK8, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	movl 16(%ebp), %ecx
	pushl %ecx
	movl 12(%ebp), %ecx
	pushl %ecx
	call fgets
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type fgetchar, @function
fgetchar:
	pushl %ebp
	movl %esp, %ebp

	subl $8, %esp
	movl $strLOCK8, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	call fgetc
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -8(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl -8(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type freadline, @function
freadline:
	pushl %ebp
	movl %esp, %ebp

	subl $12, %esp
	movl $strLOCK8, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl $' ', %ecx
	movl %ecx, -8(%ebp)
	movl $0, %ecx
	movl %ecx, -12(%ebp)
	movl $1000, %ecx
	movl %ecx, %esi
	movl -12(%ebp), %ebx
	cmpl %esi, %ebx
	jg .LF10
	.LD10:
	movl -8(%ebp), %ecx
	pushl %ecx
	movl $0x0a, %ecx
	popl %edx
	cmpl %ecx, %edx
	jne .ne10
	jmp .LF10
	.ne10:
	movl $1, %ecx
	pushl %ecx
	leal -8(%ebp), %ecx
	pushl %ecx
	movl 12(%ebp), %ecx
	pushl %ecx
	call strncat
	popl %ebx
	incl -12(%ebp)
	movl -12(%ebp), %ebx
	cmpl %esi, %ebx
	jle .LD10
	.LF10:
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl -12(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type fdelete, @function
fdelete:
	pushl %ebp
	movl %esp, %ebp

	subl $12, %esp
	movl $BSSLOCK11, %ecx
	movl %ecx, -4(%ebp)
	movl $BSSLOCK12, %ecx
	movl %ecx, -8(%ebp)
	movl -8(%ebp), %ecx
	pushl %ecx
	movl -4(%ebp), %ecx
	pushl %ecx
	call strcat
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call system
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -12(%ebp)
	movl -12(%ebp), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type fcreate, @function
fcreate:
	pushl %ebp
	movl %esp, %ebp

	subl $4, %esp
	movl $strLOCK6, %ecx
	pushl %ecx
	movl 8(%ebp), %ecx
	pushl %ecx
	call fopen
	movl %eax, %ecx
	popl %ebx
	movl %ecx, -4(%ebp)
	movl $strLOCK13, %ecx
	pushl %ecx
	call fprintf
	popl %ebx
	movl -4(%ebp), %ecx
	pushl %ecx
	call fclose
	popl %ebx
	movl $0, %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret

	.type printPersonAge, @function
printPersonAge:
	pushl %ebp
	movl %esp, %ebp
	leal 8(%ebp), %ebx
	movl 4(%ebx), %ecx
	pushl %ecx
	movl $strLOCK14, %ecx
	pushl %ecx
	call printf
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type printPersonName, @function
printPersonName:
	pushl %ebp
	movl %esp, %ebp
	leal 8(%ebp), %ebx
	movl 0(%ebx), %ecx
	pushl %ecx
	call printl
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type printPersonFavoriteFood, @function
printPersonFavoriteFood:
	pushl %ebp
	movl %esp, %ebp
	leal 8(%ebp), %ebx
	movl 8(%ebx), %ecx
	pushl %ecx
	call printl
	popl %ebx
	movl %ebp, %esp
	popl %ebp
	ret

	.type main, @function
main:
	pushl %ebp
	movl %esp, %ebp

	subl $12, %esp
	movl $strLOCK15, %ecx
	movl %ecx, -4(%ebp)
	movl $67, %ecx
	movl %ecx, -8(%ebp)
	movl $strLOCK16, %ecx
	movl %ecx, -12(%ebp)
	movl -4(%ebp), %ecx
	pushl %ecx
	call printPersonName
	popl %ebx
	movl $634638, %ecx
	pushl %ecx
	call printPersonName
	popl %ebx
	leal -4(%ebp), %ebx
	movl 4(%ebx), %ecx
	movl %ecx, %eax
	leave
	ret
	movl %ebp, %esp
	popl %ebp
	ret
