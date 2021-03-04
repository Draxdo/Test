from src.lex import *
import itertools

class Node:
  def __init__(self, type, left=None, right=None):
    self.left = left
    self.right = right
    self.type = type
    
  def __repr__(self):
    return '[ Node: Type: [{}] Left: [{}] Right: [{}] ]'.format(self.type, self.left, self.right)
  def __str__(self):
    return '[ Node: Type: {} Left: {} Right: {} ]'.format(self.type, self.left, self.right)
    
class Expression:
  def __init__(self, left=None, right=None):
    pass

# expression | expression + expression
#            | expression - expression
#            | expression * expression
#            | expression / expression
#            | expression % expression
#            | int
#            | name
#            | char
#            | string
#            | funccall
#            | ampoint  

def checkExpr(tokens):
  if len(tokens) == 1:
    if tokens[0].getTokenType() == "TT_INTEGER" or tokens[0].getTokenType() == "TT_HEX":
      return True, "implicit_int", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_AMPOINT":
      return True, "ampoint", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_STRING":
      return True, "imp_string", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_CHAR":
      return True, "imp_char", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_IDENTIFIER":
      return True, "identifier", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_FUNCCALL":
      return True, "funccall", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_KEYWORD" and tokens[0].getTokenValue() in ["true", "false"]:
      return True, "boolean", Node("int_val", right=tokens[0].getTokenValue())
    else:
      return False
      #quit("Parser Error: Unknown expression '{}' for implicit_int!".format(tokens[0]))
  elif len(tokens) == 3:
    if tokens[1].getTokenType() == "TT_PLUS":
      x, y, z = checkExpr([tokens[2]])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "add", Node("add", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_MINUS":
      x, y, z = checkExpr([tokens[2]])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "minus", Node("minus", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_MUL":
      x, y, z = checkExpr([tokens[2]])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "mul", Node("mul", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_DIV":
      x, y, z = checkExpr([tokens[2]])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "div", Node("div", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_MOD":
      x, y, z = checkExpr([tokens[2]])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "mod", Node("mod", left=z1, right=z)
      else:
        return False
  else:
    if tokens[1].getTokenType() == "TT_PLUS":
      x, y, z = checkExpr(tokens[2:])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "add", Node("add", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_MINUS":
      x, y, z = checkExpr(tokens[2:])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "minus", Node("minus", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_MUL":
      x, y, z = checkExpr(tokens[2:])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "mul", Node("mul", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_DIV":
      x, y, z = checkExpr(tokens[2:])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "div", Node("div", left=z1, right=z)
      else:
        return False
    elif tokens[1].getTokenType() == "TT_MOD":
      x, y, z = checkExpr(tokens[2:])
      x1, y1, z1 = checkExpr([tokens[0]])
      if x and x1:
        return True, "mod", Node("mod", left=z1, right=z)
      else:
        return False

def checkLogicalExpr(exprs):
  #print(exprs)
  exprs, ttype = listTokenSplitters(exprs, ["TT_EQUALS", "TT_DNEQUAL", "TT_GRTHAN", "TT_LTHAN"])
  #print(exprs)
  if len(exprs) == 2:
    try:
      x, y, z = checkExpr(exprs[0])
    except TypeError:
      quit("Parser Error: Expected 'expression'!")
    try:
      x1, y1, z1 = checkExpr(exprs[1])
    except TypeError:
      quit("Parser Error: Expected 'expression'!")
    if x and x1:
      return z, z1, ttype
    else:
      quit("Parser Error: Expected 'expression'!")
  else:
    quit("Unknown logical operator!")
# int_dec | int <name> = <expression>;

def fprint(s):
  with open("outtest.txt", 'w') as fe:
    fe.write("\nst:\n\n" + s)

def appendEndLeft(st, v):
  if st.left == None:
    st.left = v
    #fprint(str(st))
  else:
    appendEndLeft(st.left, v)

def listTokenSplitter(l, ttype):
  nl = []
  tmp = []
  for iv in l:
    if iv.getTokenType() == ttype:
      nl.append(tmp)
      tmp = []
    else:
      tmp.append(iv)
  if tmp != []:
    nl.append(tmp)
  return nl

def listTokenSplitters(l, ttypes):
  nl = []
  tmp = []
  fi = None
  for i in l:
    if i.getTokenType() in ttypes:
      nl.append(tmp)
      fi = i.getTokenType()
      tmp = []
    else:
      tmp.append(i)
  if tmp != []:
    nl.append(tmp)
  return nl, fi
  
def parse(tokens):
  AST = Node("global")
  tokstream = []
  tmpstream = []
  tmpid = ""
  fname = None
  for token in tokens:
    #print(tmpstream)
    if tmpid == "fdef":
      if token.getTokenType() == "TT_RBRACE":
        appendEndLeft(AST, Node("fdef1", right=fparse(tmpstream, fname)))
        tmpid = ""
        tmpstream = []
        tokstream = []
        fname = None
      else:
        tokstream = []
        tmpstream.append(token)
    else:
      tokstream.append(token)
    if len(tokstream) == 5 and tokstream[0].getTokenType() == "TT_KEYWORD" and tokstream[0].getTokenValue() == "fn":
      if tokstream[1].getTokenType() == "TT_IDENTIFIER":
        fname = tokstream[1]
        if tokstream[2].getTokenType() == "TT_EQUALS":
          if tokstream[3].getTokenType() == "TT_GRTHAN":
            if tokstream[4].getTokenType() == "TT_LBRACE":
              tmpid = "fdef"
              tokstream = []
  return AST
      
      
def fparse(tokens, funcname):
  AST = Node("funcdef", right=funcname)

  # split our list
  statements = listTokenSplitter(tokens, "TT_SEMICOLON")

  inif = []
  idx = -1
  skip = 0

  for statement in statements:
    #print(statement)
    # int x = 5;
    idx += 1
    depth = 0
    if skip > 0:
      skip -= 1
      continue 

    if statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "if":
      name = None
      value = None

      expr = statement[1:]

      x, y, ttype = checkLogicalExpr(expr)

      c = Node("if_statement", right=Node("if_details", right=(x, y, ttype)))

      tmpis = []

      #global statesParsed

      statesParsed = 0
      
      for statement in statements[idx+1:]:
        statesParsed += 1
        if len(statement) == 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "endif":
          if depth == 0:
            break
          else:
            depth -= 1
        elif len(statement) >= 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "if":
          depth += 1
        else:
          tmpis.append(statement)
      
      tmpf = fparse(tmpis[0], "tmpf")

      stuff = tmpf.left

      c.right.left = stuff

      skip += statesParsed

      appendEndLeft(AST, c)
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "asm":
      if statement[1].getTokenType() == "TT_STRING":
        v = Node("asm_line", right=statement[1].getTokenValue())
        appendEndLeft(AST, v)
      else:
        quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "let":
      # found int dec keyword, will now parse...

      if statement[1].getTokenType() == "TT_IDENTIFIER":
        name = statement[1].getTokenValue()


        if statement[2].getTokenType() == "TT_EQUALS":
          try:
            x, y, z = checkExpr(statement[3:])
          except TypeError:
            quit("Parser Error: Expected 'expression' found {}".format(statement[3].getTokenType()))


          if x:
            value = z
            x = None
            if isinstance(value, list):
              x = Node("int_dec", left=Node("identifier", right=name), right=value)
            else:
              x = Node("int_dec", left=Node("identifier", right=name), right=value)
            appendEndLeft(AST, x)


          else:
             quit("Parser Error: Expected 'expression' found {}".format(statement[3].getTokenType()))


        else:
          quit("Parser Error: Expected 'equals' found {}".format(statement[2].getTokenType()))


      else:
        quit("Parser Error: Expected 'identifier' found '{}'".format(statement[1].getTokenType()))
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "quit":
      try:
        x, y, z = checkExpr(statement[1:])
      except TypeError:
        quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))

      if x:
        value = z
        x = Node("quit_statement", right=value)
        appendEndLeft(AST, x)
      else:
        quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))
    elif statement[0].getTokenType() == "TT_IDENTIFIER":
      name = statement[0].getTokenValue()
      if statement[1].getTokenType() == "TT_EQUALS":
        try:
          x, y, z = checkExpr(statement[2:])
        except TypeError:
          quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))
        
        if x:
          value = z
          x = Node("set_mov_equals", left=Node("identifier", right=name), right=value)
          appendEndLeft(AST, x)
        else:
          quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))
      else:
        quit("Expected 'equals'! Found <" + statement[1].getTokenType() + ">")
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "return":
      try:
        x, y, z = checkExpr(statement[1:])
      except TypeError:
        quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))

      if x:
        value = z
        x = Node("return_statement", right=value)
        appendEndLeft(AST, x)
      else:
        quit("Parser Error: Expected 'expression' found {}".format(statement[1].getTokenType()))
  return AST
