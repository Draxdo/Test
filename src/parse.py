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
#            | ptr
#            | bool
#            | hex

def checkExpr(tokens):
  #print(tokens)
  if len(tokens) == 1:
    if tokens[0].getTokenType() == "TT_INTEGER" or tokens[0].getTokenType() == "TT_HEX":
      return True, "implicit_int", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_AMPOINT":
      return True, "ampoint", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_INDEXREF":
      return True, "indexref", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_DEC":
      return True, "double", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_ARR":
      return True, "arr", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_BYTES":
      return True, "bytes", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_PTR":
      return True, "PTR", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_STRING":
      return True, "imp_string", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_CHAR":
      return True, "imp_char", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_IDENTIFIER":
      return True, "identifier", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_STRUCTDEF":
      return True, "structdef", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_STRUCTREF":
      return True, "structdef", Node("int_val", right=tokens[0].getTokenValue())
    elif tokens[0].getTokenType() == "TT_FUNCCALL":
      #print("hit")
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
        return False, None, None
    else:
      print(tokens)
      quit("Unknown expr!")

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

def checkKeyword(token):
  if token.getTokenType() == "TT_KEYWORD":
    return token.getTokenType()
  else:
    return False
  
def parse(tokens):
  AST = Node("global")
  tokstream = []
  tmpstream = []
  tmpid = ""
  fname = None
  sname = None
  for token in tokens:
    #print(tmpstream)
    if tmpid == "fdef":
      if token.getTokenType() == "TT_RBRACE":
        b, fn, args = checkFuncCall(fname.getTokenValue())

        appendEndLeft(AST, Node("fdef1", right=Node(type="finfo", right=args, left=fparse(tmpstream, fname))))
        tmpid = ""
        tmpstream = []
        tokstream = []
        fname = None
      else:
        tokstream = []
        tmpstream.append(token)
    elif tmpid == "gdec":
      if token.getTokenType() == "TT_SEMICOLON":
        x, y, z = checkExpr(tmpstream)
        if not x:
          quit("Expected expression, found {}!".format(tmpstream))
        appendEndLeft(AST, Node("gdec", right=Node("sinfo", right=vname, left=z)))
        tmpid = ""
        tmpstream = []
        tokstream = []
        vname = None
      else:
        tokstream = []
        tmpstream.append(token)
    elif tmpid == "cgdec":
      if token.getTokenType() == "TT_SEMICOLON":
        x, y, z = checkExpr(tmpstream)
        if not x:
          quit("Expected expression, found {}!".format(tmpstream))
        appendEndLeft(AST, Node("cgdec", right=Node("sinfo", right=vname, left=z)))
        tmpid = ""
        tmpstream = []
        tokstream = []
        vname = None
      else:
        tokstream = []
        tmpstream.append(token)
    elif tmpid == "sdef":
      if token.getTokenType() == "TT_RBRACE":

        appendEndLeft(AST, Node("sdef", right=Node(type="sinfo", right=sname, left=sparse(tmpstream, fname))))
        tmpid = ""
        tmpstream = []
        tokstream = []
        sname = None
      else:
        tokstream = []
        tmpstream.append(token)
    else:
      tokstream.append(token)
      
    if len(tokstream) == 4 and tokstream[0].getTokenType() == "TT_KEYWORD" and tokstream[0].getTokenValue() == "new":
      if len(tokstream) == 4 and tokstream[1].getTokenType() == "TT_KEYWORD" and tokstream[1].getTokenValue() == "struct":
        if tokstream[2].getTokenType() == "TT_IDENTIFIER":
          sname = tokstream[2].getTokenValue()
          if tokstream[3].getTokenType() == "TT_LBRACE":
            
            tmpid = "sdef"
            tokstream = []
    elif len(tokstream) == 5 and tokstream[0].getTokenType() == "TT_KEYWORD" and tokstream[0].getTokenValue() == "fn":
      if tokstream[1].getTokenType() == "TT_FUNCCALL":
        fname = tokstream[1]
        if tokstream[2].getTokenType() == "TT_EQUALS":
          if tokstream[3].getTokenType() == "TT_GRTHAN":
            if tokstream[4].getTokenType() == "TT_LBRACE":
              tmpid = "fdef"
              tokstream = []
    elif len(tokstream) == 3 and tokstream[0].getTokenType() == "TT_KEYWORD" and tokstream[0].getTokenValue() == "let":
      if tokstream[1].getTokenType() == "TT_IDENTIFIER":
        vname = tokstream[1].getTokenValue()
        if tokstream[2].getTokenType() == "TT_EQUALS":
          tmpid = "gdec"
          tokstream = []
    elif len(tokstream) == 3 and tokstream[0].getTokenType() == "TT_KEYWORD" and tokstream[0].getTokenValue() == "const":
      if tokstream[1].getTokenType() == "TT_IDENTIFIER":
        vname = tokstream[1].getTokenValue()
        if tokstream[2].getTokenType() == "TT_EQUALS":
          tmpid = "cgdec"
          tokstream = []
  return AST

def sparse(tokens, sname):
  AST = Node("structdef", right=sname)
  names = listTokenSplitter(tokens, "TT_COMMA")
  #print(names)
  for n in names:
    name = n[0]
    if name.getTokenType() == "TT_IDENTIFIER":
      #print(Node("stiden", right=name.getTokenValue()))
      appendEndLeft(
        AST,
        Node("stiden", right=name.getTokenValue())
      )
    else:
      quit("Expected 'TT_IDENTIFIER', found '{}' or '{}'!".format(name.getTokenType(), name.getTokenValue()))
  return AST

def listCombine(l):
  ''' l = [
    [],
    [],
    [],
    []
  ]
  '''
  vals = []
  for i in l:
    for v in i:
      vals.append(v)
    vals.append(Token(TT_SEMICOLON))
  return vals
      
# def new <structname> <vname> <data>
# def new Person person1 "Jerry" 56
def fparse(tokens, funcname):
  AST = Node("funcdef", right=funcname)

  # split our list
  statements = listTokenSplitter(tokens, "TT_SEMICOLON")


  inif = []
  idx = -1
  skip = 0

  for statement in statements:
    #print('e')
    #print("\n\n\n\n" + str(statement) + "\n\n")
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
      depth = 0
      
      for statement in statements[idx+1:]:
        statesParsed += 1
        if len(statement) == 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "endif":
          if depth == 0:
            #print("hit2")
            break
          else:
            tmpis.append(statement)
            depth -= 1
        elif len(statement) >= 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "if":
          #print("hit")
          tmpis.append(statement)
          depth += 1
        else:
          tmpis.append(statement)

      #print(type(listCombine(tmpis)[0]))

      tmpf = fparse(listCombine(tmpis), "tmpf")

      stuff = tmpf.left
      
      #rint(stuff)

      appendEndLeft(c.right, stuff)

      skip += statesParsed

      appendEndLeft(AST, c)
    elif statement[0].getTokenType() == "TT_IDENTIFIER" or statement[0].getTokenType() == "TT_STRUCTDEF" or statement[0].getTokenType() == "TT_INDEXREF":
      #print("eueu")
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
      elif statement[1].getTokenType() == "TT_KEYWORD" and statement[1].getTokenValue() == "as":
        sname = statement[0].getTokenValue()
        if statement[2].getTokenType() == "TT_KEYWORD" and statement[2].getTokenValue() == "struct":
          if statement[3].getTokenType() == "TT_IDENTIFIER":
            svname = statement[3].getTokenValue()
            appendEndLeft(
              AST,
              Node("asstruct", right=(sname, svname))
            )
      elif statement[1].getTokenType() == "TT_IDENTIFIER":
        sname = statement[0].getTokenValue()
        vname = statement[1].getTokenValue()
        if statement[2].getTokenType() == "TT_EQUALS":
          stuffs = listTokenSplitter(statement[3:], "TT_COMMA")
          #print(stuffs)
          for stuff in stuffs:
            x, y, z = checkExpr(stuff)
            if not x:
              quit("Semble: Error: expected 'expression' found '{}'!".format(y))
          appendEndLeft(
            AST,
            Node("srdef", right=(sname, vname, stuffs))
          )

    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "while":
      name = None
      value = None

      expr = statement[1:]

      x, y, ttype = checkLogicalExpr(expr)

      c = Node("while_loop", right=Node("while_details", right=(x, y, ttype)))

      tmpis = []

      #global statesParsed

      statesParsed = 0
      depth = 0
      
      for statement in statements[idx+1:]:
        statesParsed += 1
        if len(statement) == 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "endwhile":
          if depth == 0:
            #print("hit2")
            break
          else:
            tmpis.append(statement)
            depth -= 1
        elif len(statement) >= 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "while":
          #print("hit")
          tmpis.append(statement)
          depth += 1
        else:
          tmpis.append(statement)

      #print(type(listCombine(tmpis)[0]))

      tmpf = fparse(listCombine(tmpis), "tmpf")

      stuff = tmpf.left
      
      #rint(stuff)

      appendEndLeft(c.right, stuff)

      skip += statesParsed

      appendEndLeft(AST, c)
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "break":
      appendEndLeft(
        AST,
        Node("break")
      )
    
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "for":
      #print("Hel")
      # for i from 0 to 10;
      if statement[1].getTokenType() == "TT_IDENTIFIER":
        name = statement[1].getTokenValue()
        if statement[2].getTokenType() == "TT_KEYWORD" and statement[2].getTokenValue() == "from":
          st = statement[3:]
          sts = []
          j = False
          ix = 3
          for s in st:
            if s.getTokenValue() != "to":
              ix += 1
              sts.append(s)
            else:
              j = True
              break
          if not j:
            quit("Expected 'to' in for block!")
          else:
            #print(sts)
            b, t, s = checkExpr(sts)
            if not b:
              quit("Unknown expr!")
            else:
              n1ex = s
              ix += 1
              stuff = statement[ix:]
              b, t, s = checkExpr(sts)
              if not b:
                quit("Unknown expr!")
              else:
                #print(stuff)
                b, t, s = checkExpr(stuff)
                c = Node("forloop", right=Node("fordetails", left=None, right=(name, n1ex, s)))
                tmpis = []

                #global statesParsed

                statesParsed = 0
                depth = 0
                
                for statement in statements[idx+1:]:
                  statesParsed += 1
                  if len(statement) == 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "endfor":
                    if depth == 0:
                      #print("hit2")
                      break
                    else:
                      tmpis.append(statement)
                      depth -= 1
                  elif len(statement) >= 1 and statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "for":
                    #print("hit")
                    tmpis.append(statement)
                    depth += 1
                  else:
                    tmpis.append(statement)

                #print(type(listCombine(tmpis)[0]))

                tmpf = fparse(listCombine(tmpis), "tmpf")

                stuff = tmpf.left
                
                #rint(stuff)

                appendEndLeft(c.right, stuff)

                skip += statesParsed

                appendEndLeft(AST, c)

              
    elif statement[0].getTokenType() == "TT_FUNCCALL":
      #print(Node("funccall", right=statement[0].getTokenValue()))
      appendEndLeft(
        AST,
        Node("funccall", right=statement[0].getTokenValue())
      )
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
          except TypeError as te:
            #print(statement[3:])
            #print(statement)
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
          quit("Var Dec: Parser Error: Expected 'equals' found {}".format(statement[2].getTokenType()))


      else:
        quit("Parser Error: Expected 'identifier' found '{}'".format(statement[1].getTokenType()))
    elif statement[0].getTokenType() == "TT_KEYWORD" and statement[0].getTokenValue() == "const":
      # found int dec keyword, will now parse...

      if statement[1].getTokenType() == "TT_IDENTIFIER":
        name = statement[1].getTokenValue()


        if statement[2].getTokenType() == "TT_EQUALS":
          try:
            x, y, z = checkExpr(statement[3:])
          except TypeError as te:
            #print(statement[3:])
            #print(statement)
            quit("Parser Error: Expected 'expression' found {}".format(statement[3].getTokenType()))


          if x:
            value = z
            x = None
            if isinstance(value, list):
              x = Node("const_dec", left=Node("identifier", right=name), right=value)
            else:
              x = Node("const_dec", left=Node("identifier", right=name), right=value)
            appendEndLeft(AST, x)


          else:
             quit("Parser Error: Expected 'expression' found {}".format(statement[3].getTokenType()))


        else:
          quit("Const Dec: Parser Error: Expected 'equals' found {}".format(statement[2].getTokenType()))


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
    else:
      quit("Unknown statement '{}'!".format(statement))
  return AST
