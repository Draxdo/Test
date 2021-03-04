from src.parse import *
from src.lex import *
import re

functionProlouge = [
  "\tpushl %ebp\n",
  "\tmovl %esp, %ebp\n"
]

functionEpilouge = [
  "\tmovl %ebp, %esp\n",
  "\tpopl %ebp\n",
  "\tret\n"
]

funcnums = {
  
}

funcs = {
  "_start":["call main", "movl %eax, %ebx", "movl $1, %eax", "int $0x80"],
}

currentFunc = None

tmpid = ""
valueStack = []
ints = []
varias = {
  
}

data = {
  
}

strings = {
  
}

n = 0

def asm(s):
  funcs[currentFunc].append(s)

def getPrefix(v):
  v = str(v)
  if v[0] == "-" and v[-1] == ")":
    return ''
  elif re.match(r"[0-9]+$", v):
    return '$'
  else:
    return '%'

def mov(s, v):
  asm("movl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def add(s, v):
  asm("addl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def cmp(s, v):
  asm("cmpl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def sub(s, v):
  asm("subl " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def mul(s, v):
  asm("imull " + getPrefix(s) + str(s) + ", " + getPrefix(v) + str(v))

def push(s):
  asm("pushl " + getPrefix(s) + str(s))

def pop(s):
  asm("popl " + getPrefix(s) + str(s))

def div(s, v):
  asm("xorl %edx, %edx")
  mov(s, "eax")
  mov(v, "edi")
  asm("idiv %edi")

def cmpl(node):
  global n, currentFunc, funcs, varias
  #print("Entered cmpl()")
  #print("node.left: {}".format(node.left))
  #print(node.type)
  
  
  if currentFunc == None:
    if node != None and node.left != None and node.left.type == "fdef1":
      fname = node.left.right.right.getTokenValue()
      if fname in funcs.keys():
        quit("Cannot redefine function <" + str(fname) + ">!")
      else:
        currentFunc = fname
        funcs[fname] =[]
        funcnums[fname] = 0
        varias = {}
        cmpl(node.left.right)
        currentFunc = None
        cmpl(node.left)
    elif node == None or node.left == None:
      pass

  elif node.left != None and node.left.type == "if_statement":
    things = node.left.right.right
    #print(node.left.left)
    ins = Node("nonode", left=node.left.right.left)
    cmpl(things[0])
    push("ecx")
    cmpl(things[1])
    pop("edx")
    cmp("ecx", "edx")
    prefix = None
    if things[2] == "TT_EQUALS":
      prefix = "ne"
    elif things[2] == "TT_DNEQUAL":
      prefix = "e"
    elif things[2] == "TT_GRTHAN":
      prefix = "l"
    elif things[2] == "TT_LTHAN":
      prefix = "g"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    name = prefix + str(n)
    n += 1
    asm("j" + prefix + " ." + name)
    cmpl(ins)
    asm("." + name + ":")
    cmpl(node.left)
    
  elif node.left != None and node.left.type == "int_dec":
    #print("Entered cmpl.int_dec()")
    if node.left.left.right not in varias.keys():
      cmpl(node.left.right)
      ints.append(node.left.left.right)
      funcnums[currentFunc] += 4
      varias[node.left.left.right] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      asm("movl %ecx, " + varias[node.left.left.right])
      cmpl(node.left.left)
      return None
    else:
      quit("Prenamed variable <" + str(node.left.left.right) + ">!")

  elif node.left != None and node.left.type == "asm_line":
    v = node.left.right
    v = v[1:-1]
    for var in varias:
      v = v.replace("~~" + var, varias[var])
    asm(v)
  
  elif node.left != None and node.left.type == "set_mov_equals":
    #print("hello")
    if node.left.left.right in varias.keys():
      cmpl(node.left.right)
      mov("ecx", varias[node.left.left.right])
      cmpl(node.left.left)
      return None
    else:
      quit("Unknown variable <" + node.left.left.right +">!")

  elif node.left != None and node.left.type == "quit_statement":
    cmpl(node.left.right)
    mov("ecx", "ebx")
    mov(1, "eax")
    asm("int $0x80")

  elif node.left != None and node.left.type == "return_statement":
    cmpl(node.left.right)
    mov("ecx", "eax")
    asm("leave")
    asm("ret")

  elif node.left == None and node.type == "int_val":
    val = node.right
    g = None
        
    if re.match(r'^["][^\n]*["]$', val):
      if val not in strings.keys():
        x ="strLOCK" + str(n)
        n += 1
        data[x] = ".asciz " + val
        strings[val] = x
        asm("movl $" + x + ", %ecx")
      else:
        asm("movl $" + strings[val] + ", %ecx")

    elif is_valid_variable_name(val):
      try:
        g = varias[val]
      except:
        quit("Unknown variable <" + val +">!")
      asm("movl " + g + ", %ecx")

    elif len(val) >= 2 and val[0] == "&" and is_valid_variable_name(val[1:]):
      x = val[1:]
      if x in varias:
        asm("leal " + varias[x] + ", %ecx")
      else:
        quit("Unknown variable <" + str(x) + ">!")

    elif is_valid_variable_name(val.replace("(", "").replace(")", "")) and val[-1] + val[-2] == ")(":
      print(
        'hit'
      )
      funcname = val.replace("(", "").replace(")", "")
      if funcname not in funcs.keys():
        quit("Unknown function <" + str(funcname) + ">!")
      else:
        asm("call " + funcname)
        mov("eax", "ecx")
    else:
      asm("movl $" + val + ", %ecx")



  elif node.type == "add":
    asm("xorl %edx, %edx")
    cmpl(node.right)
    push("ecx")
    cmpl(node.left)
    pop("edx")
    add("edx", "ecx")

  elif node.type == "minus":
    asm("xorl %edx, %edx")
    cmpl(node.right)
    push("ecx")
    cmpl(node.left)
    pop("edx")
    sub("edx", "ecx")
  
  elif node.type == "mul":
    asm("xorl %edx, %edx")
    cmpl(node.right)
    push("ecx")
    cmpl(node.left)
    pop("edx")
    mul("edx", "ecx")
  
  elif node.type == "div":
    #push("eax")
    cmpl(node.left)
    push("ecx")
    cmpl(node.right)
    pop("eax")
    asm("xorl %edx, %edx")
    div("eax", "ecx")
    mov("eax", "ecx")
    #pop("eax")

  elif node.type == "mod":
    #push("eax")
    cmpl(node.left)
    push("ecx")
    cmpl(node.right)
    pop("eax")
    asm("xorl %edx, %edx")
    div("eax", "ecx")
    mov("edx", "ecx")
    #pop("eax")

  


def cmpf(ast, f):
  global funcnums, funcs, currentFunc, tmpid, valueStack, ints, varias, data, strings, n
  funcnums = {
    
  }

  funcs = {
    "_start":["call main", "movl %eax, %ebx", "movl $1, %eax", "int $0x80"],
  }

  currentFunc = None

  tmpid = ""
  valueStack = []
  ints = []
  varias = {
    
  }

  data = {
    
  }

  strings = {
    
  }

  n = 0
  cmpl(ast)
  with open(f, "w") as fw:
    fw.write("\t.section .data\n")
    for d in data:
      fw.write("\n" + d + ":\n")
      di = data[d]
      fw.write("\t" + di + "\n")
    fw.write("\t.section .text\n")
    fw.write("\t.globl _start\n")
    for func in funcs:
      if func != "_start":
        fw.write("\n\t.type " + func + ", @function")
      fw.write("\n" + func + ":\n")
      if func != "_start":
        for pl in functionProlouge:
          fw.write(pl)
        if funcnums[func] > 0:
          fw.write("\n\tsubl $" + str(funcnums[func]) + ", %esp\n")

      for fl in funcs[func]:
        fw.write("\t"+ fl + "\n")

      if func != "_start":
        for el in functionEpilouge:
          fw.write(el)