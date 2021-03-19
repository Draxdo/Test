from src.parse import *
from src.lex import *
import re

functionProlouge = [
  "\tpushl %ebp\n",
  "\tmovl %esp, %ebp\n"
]

breaker = []

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

structbeenptrs = {
  
}

funcargs = {

}

bss = {

}

fstructs = {

}

def checkStructDef(s):
  return s.split(".")

class Struct:
  def __init__(self, name, variz, starting):
    self.name = name
    self.variz = variz
    self.starting = starting
  def getvalue(self, s):
    if s in self.variz:
      return str(self.variz.index(s) * 4) + "(" + self.starting + ")"
    else:
      return False

n = 0
nextAdd = 0

def asm(s):
  funcs[currentFunc].append(s)
  
def divver(x, y):
  x = int(x)
  y = int(y)
  z = 0
  while True:
    if x >= y:
      x -= y
      z += 1
    else:
      break
  return z
    

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

structs = {}

def rndz(i):
  i = i - 1
  if i < 0:
    return 0
  else:
    return i

def div(s, v):
  asm("xorl %edx, %edx")
  mov(s, "eax")
  mov(v, "edi")
  asm("idiv %edi")

def divl(s, v):
  asm("xorl %edx, %edx")
  mov(s, "eax")
  mov(v, "edi")
  asm("div %edi")

def seval(name, node):
  v = []
  if node.left != None:
    if node.left.right == None:
      x = seval(name, node.left)
      v = v + x
      return v
    v.append(node.left.right)
    x = seval(name, node.left)
    v = v + x
  return v

def cmpl(node):
  global n, currentFunc, funcs, varias, funcnums, funcargs, nextAdd, breaker, fstructs
  #print(fstructs)
  #print(varias)
  #print("Entered cmpl()")
  #print("node.left: {}".format(node.left))
  #print(node.type)
  
  if node == None:
    return None
  
  if currentFunc == None:
    if node != None and node.left != None and node.left.type == "fdef1":
      #print(node.left.right.left.right)
      fname = node.left.right.left.right.getTokenValue()
      args = node.left.right.right
      if fname in funcs.keys():
        quit("Cannot redefine function <" + str(fname) + ">!")
      else:
        fname = checkFuncCall(fname)[1]
        currentFunc = fname
        funcs[fname] =[]
        funcargs[fname] = []
        funcnums[fname] = 0
        fstructs = {}
        varias = {}
        idx = 4
        for arg in args:
          idx += 4
          if arg == "":
            break
          elif is_valid_variable_name(arg):
            varias[arg] = str(idx) + "(%ebp)"
            
            funcargs[currentFunc].append(args)

          else:
            quit("Invalid argument <" + arg + ">!")
        cmpl(node.left.right.left)
        currentFunc = None
        cmpl(node.left)
    elif node != None and node.left != None and node.left.type == "sdef":
      # struct
      sname = node.left.right.right
      v = seval(sname, node.left.right)
      if v == []:
        print("Semble: Warning: Empty struct '{}', due to this being a waste of memory, it will not be generated.".format(sname))
        cmpl(node.left)
        return None
      else:
        structs[sname] = v

        cmpl(node.left)
        return None

    elif node == None or node.left == None:
      pass

  elif node.left != None and node.left.type == "srdef":
    #print("he")
    sname = node.left.right[0]
    vname = node.left.right[1]
    stuffs = node.left.right[2]
    # you're to have a place in memory
    idx = -1
    first = "-" + str(funcnums[currentFunc] + 4) + "(%ebp)"
    for i in structs[sname]:
      idx += 1
      funcnums[currentFunc] += 4
      if stuffs[idx] == None:
        asm("movl $0 %ecx")
      else:
        cmpl(checkExpr(stuffs[idx])[2])
        if nextAdd > 0 and currentFunc != None:
          funcnums[currentFunc] += nextAdd
          nextAdd = 0
          v = True
      if sname + "__" + i in varias:
        quit("Predefined {}!")
      varias[vname + "__" + i] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
        
      asm("movl %ecx, " + varias[vname + "__" + i])
    varias[vname] = first
    sva = Struct(sname, structs[sname], first)
    fstructs[vname] = sva
    cmpl(node.left)

  elif node.left != None and node.left.type == "asstruct":
    if node.left.right[0] in varias:
      x = Struct(node.left.right[0], structs[node.left.right[1]], varias[node.left.right[0]])
      fstructs[node.left.right[0]] = x
      cmpl(node.left)
      return None
    else:
      quit("Value <{}> not a variable!".format(node.left.right[1]))

  elif node.left != None and node.left.type == "break":
    br = breaker[-1]
    #print(br)
    asm("jmp " + br)
    cmpl(node.left)
    return None

  elif node.left != None and node.left.type == "funccall":
    val = node.left.right
    b, fn, args = checkFuncCall(val)
    for arg in reversed(args):
      if arg == "":
        break
      else:
        bo, ty, no = checkExpr(lex(arg + "\n"))
        if bo:
          cmpl(no)
          push("ecx")
        else:
          quit("Invalid expression <" + arg + ">!")
    asm("call " + fn)
    pop("ebx")
    cmpl(node.left)
    return None
  
  elif node.left != None and node.left.type == "forloop":
    fordetails = node.left.right
    vname = fordetails.right[0]
    fromv = fordetails.right[1]
    tov = fordetails.right[2]
    nexts = Node("nonode", left=fordetails.left)
    if vname not in varias:
      cmpl(fromv)
      funcnums[currentFunc] += 4
      varias[vname] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      asm("movl %ecx, " + varias[vname])
      cmpl(tov)
      mov("ecx", "esi")
      n += 1
      mov(varias[vname], "ebx")
      cmp("esi", "ebx")
      nname = "LF" + str(n)
      nname2 = "LD" + str(n)
      asm("jg ." + nname)
      asm("." + nname2 + ":")
      breaker.append("." + nname)
      cmpl(nexts)
      breaker.pop(-1)
      asm("incl " + varias[vname])
      mov(varias[vname], "ebx")
      cmp("esi", "ebx")
      asm("jle ." + nname2)
      asm("." + nname + ":")
      #breaker = "." + nname
      cmpl(node.left)
      return None;
    else:
      quit("Prenamed variable <{}>!".format(vname))
  elif node.left != None and node.left.type == "if_statement":
    things = node.left.right.right
    #print("\n\n#################\n\n" + str(node.left) + "\n\n")
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
      prefix = "le"
    elif things[2] == "TT_LTHAN":
      prefix = "ge"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    name = prefix + str(n)
    n += 1
    asm("j" + prefix + " ." + name)
    cmpl(ins)
    #print(ins)
    asm("." + name + ":")
    cmpl(node.left)

  elif node.left != None and node.left.type == "while_loop":
    things = node.left.right.right
    #print("\n\n#################\n\n" + str(node.left) + "\n\n")
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
      prefix = "le"
    elif things[2] == "TT_LTHAN":
      prefix = "ge"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    name = prefix + str(n)
    n += 1
    asm("j" + prefix + " ." + name)
    abc = "LFB" + str(n)
    asm("." + abc + ":")
    breaker.append("." + name)
    cmpl(ins)
    breaker.pop(-1)
    
    cmpl(things[0])
    push("ecx")
    cmpl(things[1])
    pop("edx")
    cmp("ecx", "edx")
    prefix = None
    if things[2] == "TT_EQUALS":
      prefix = "e"
    elif things[2] == "TT_DNEQUAL":
      prefix = "ne"
    elif things[2] == "TT_GRTHAN":
      prefix = "g"
    elif things[2] == "TT_LTHAN":
      prefix = "l"
    else:
      quit("Unknown operator type <" + str(things[2]) + ">!")
    asm("j" + prefix + " ." + abc)

    #print(ins)
    asm("." + name + ":")
    #breaker = "." + name
    cmpl(node.left)
    return None
    
  elif node.left != None and node.left.type == "int_dec":
    #print("Entered cmpl.int_dec()")
    if node.left.left.right not in varias.keys():
      cmpl(node.left.right)
      ints.append(node.left.left.right)
      funcnums[currentFunc] += 4
      varias[node.left.left.right] = "-" + str(funcnums[currentFunc]) + "(%ebp)"
      v = False
      if nextAdd > 0 and currentFunc != None:
        funcnums[currentFunc] += nextAdd
        nextAdd = 0
        v = True
      if not v:
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
    cmpl(node.left)
    return None
  
  elif node.left != None and node.left.type == "set_mov_equals":
    #print(node.left.left.right)
    if node.left.left.right in varias.keys():
      cmpl(node.left.right)
      asm("movl %ecx, " + varias[node.left.left.right])
      cmpl(node.left.left)
      return None
    elif checkIndexRef(node.left.left.right)[0]:
      val = node.left.left.right
      b, fn, index = checkIndexRef(val)
      print(varias[fn])
      val = re.match(r"^\-(\d+)\(\%ebp\)$", varias[fn]).group(1)
      ab = int(val)
      cmpl(checkExpr(lex(index + "\n"))[2])
      mul(4, "ecx")
      asm("cmpl $0, %ecx")
      asm("jz .sksb" + str(n))
      asm("subl $1, %ecx")
      asm(".sksb" + str(n) + ":")
      n += 1
      add(str(ab), "ecx")
      print(val)
      print(ab)
      asm("movl %ebp, %edi")
      sub("ecx", "edi")
      cmpl(node.left.right)
      asm("movl %ecx, (%ebp)")
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
    #print(val)
    
    if val in ["true", "false"]:
      if val == "true":
        asm("movl $1, %ecx")
      else:
        asm("movl $0, %ecx")

    elif is_valid_struct_def(val):
      x = checkStructDef(val)
      if x[0] in fstructs:
        fstructs[x[0]].getvalue(x[1])
        asm("leal " + fstructs[x[0]].starting + ", %ebx")
        if x[1] in fstructs[x[0]].variz:
          asm("movl " + str(fstructs[x[0]].variz.index(x[1]) * 4) + "(%ebx), %ecx")
        else:
          quit("Semble: Error: Data structure '{}' has no type '{}'!".format(x[0], x[1]))
      else:
        quit("Unknown type '{}'!".format(x[0]))

    elif checkIndexRef(val)[0]:
      b, fn, index = checkIndexRef(val)
      print(varias[fn])
      val = re.match(r"^\-(\d+)\(\%ebp\)$", varias[fn]).group(1)
      ab = int(val)
      cmpl(checkExpr(lex(index + "\n"))[2])
      mul(4, "ecx")
      asm("cmpl $0, %ecx")
      asm("je .sksb" + str(n))
      asm("subl $1, %ecx")
      asm(".sksb" + str(n) + ":")
      n += 1
      add(str(ab), "ecx")
      print(val)
      print(ab)
      asm("movl %ebp, %edi")
      sub("ecx", "edi")
      asm("movl (%ebp), %ecx")

    elif re.match(r"^\[(\d+)\]\[(.*\,)*(.*)\]$", val):
      x = re.match(r"^\[(\d+)\]\[(.*\,)*(.*)\]$", val)
      length = x.group(1)
      values = x.group(2) + x.group(3)
      args = parseFuncCall(values)
      tmpid = 0
      tmpi = ""
      tmp = ""
      new = []
      for i in args:
        if i == "(" and tmpi == "":
          tmp += i
          tmpid += 1
        elif i == ")" and tmpi == "":
          tmp += i
          tmpid -= 1
        elif i == "\"" and tmpi == "":
          tmp += i
          tmpi = "quote"
        elif i == "\"" and tmpi == "quote":
          tmp += i
          tmpi = ""
        elif i == "'" and tmpi == "":
          tmp += i
          tmpi = "char"
        elif i == "'" and tmpi == "char":
          tmp += i
          tmpi = ""
        elif tmpid == 0 and i == "," and tmpi == "":
          new.append(tmp)
          tmp = ""
        else:
          tmp += i
      new.append(tmp)
      #print(new)
      fnc = funcnums[currentFunc] + 4
      idx = 0
      #print(new)
      for arg in new:
        #print(lex(arg + " "))
        #print(list(arg + " "))
        if arg != "":
          b, ty, no = checkExpr(lex(arg + " "))
          if not b:
            quit("Invalid expression '" + arg + "'!")
          else:
            cmpl(no)
            print(no)
            asm("movl %ecx, -" + str(fnc + (4 * idx)) + "(%ebp)")
            idx += 1
        else:
          break
      #asm("movl $0, %ecx")
      nextAdd += (4 * int(length)) - 4



    elif re.match(r"^(i8:)\d+$", val):
      v = val[3:]
      bss["BSSLOCK" + str(n)] = str(v)
      asm("movl $" + "BSSLOCK" + str(n) + ", %ecx")
      n += 1
        
    elif re.match(r'^["][^\n]*["]$', val):
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

    elif len(val) >= 2 and val[0] == "@" and is_valid_variable_name(val[1:]):
      x = val[1:]
      if x in varias:
        asm("leal " + varias[x] + ", %ecx")
      else:
        quit("Unknown variable <" + str(x) + ">!")
    
    elif len(val) >= 2 and val[0] == "$" and is_valid_variable_name(val[1:]):
      x = val[1:]
      if x in varias:
        asm("movl " + varias[x] + ", %esi")
        asm("movl (%esi), %ecx")
      else:
        quit("Unknown variable <" + str(x) + ">!")

    elif checkFuncCall(val)[0]:
      b, fn, args = checkFuncCall(val)
      #print(args)
      #print(args)
      for arg in reversed(args):
        if arg == "":
          break
        else:
          #print(arg)
          bo, ty, node = checkExpr(lex(arg + "\n"))
          if bo:
            cmpl(node)
            push("ecx")
          else:
            quit("Invalid expression <" + arg + ">!")
      asm("call " + fn)
      mov("eax", "ecx")
      pop("ebx")
    else:
      asm("movl $" + val + ", %ecx")
      return val



  elif node.type == "add":
    #asm("xorl %edx, %edx")
    x = cmpl(node.right)
    push("ecx")
    y = cmpl(node.left)
    pop("edx")
    add("edx", "ecx")

  elif node.type == "minus":
    #asm("xorl %edx, %edx")
    x = cmpl(node.right)
    push("ecx")
    y = cmpl(node.left)
    pop("edx")
    sub("edx", "ecx")

    
  
  elif node.type == "mul":
    #asm("xorl %edx, %edx")
    x = cmpl(node.right)
    push("ecx")
    y = cmpl(node.left)
    pop("edx")
    mul("edx", "ecx")

  
  elif node.type == "div":
    #push("eax")
    x = cmpl(node.left)
    push("ecx")
    y = cmpl(node.right)
    pop("eax")
    asm("xorl %edx, %edx")
    div("eax", "ecx")
    mov("eax", "ecx")
    #pop("eax")

  elif node.type == "mod":
    #push("eax")
    y = cmpl(node.left)
    push("ecx")
    x = cmpl(node.right)
    pop("eax")
    asm("xorl %edx, %edx")
    divl("eax", "ecx")
    mov("edx", "ecx")
    #pop("eax")

  


def cmpf(ast, f):
  global funcnums, funcs, currentFunc, tmpid, valueStack, ints, varias, data, strings, n, bss
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
    fw.write("\t.section .bss\n")
    for b in bss:
      fw.write("\n.lcomm " + b + ", " + str(bss[b]) + "\n")
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