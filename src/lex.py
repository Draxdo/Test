import re

class Token:
  def __init__(self, T_TYPE, value=None):
    self.T_TYPE = T_TYPE
    self.value = value
  def getTokenType(self):
    return self.T_TYPE
  def getTokenValue(self):
    return self.value
  def __str__(self):
    return '[Token: TokenType: {} TokenValue: {}]'.format(self.T_TYPE, self.value)
  def __repr__(self):
    return '[Token: TokenType: {} TokenValue: {}]'.format(self.T_TYPE, self.value)

def checkFuncCall(s):
  fn = ""
  args = ""
  idx = 0
  for i in s:
    idx += 1
    if i == "(":
      break
    else:
      fn += i
  if is_valid_variable_name(fn):
    args = s[idx:-1]
    args = args.replace(", ", ",").replace(" , ", ",").replace(" ,", ",").replace("  ,  ", ",").replace(",  ", ",").replace("  ,", ",")
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
    return True, fn, new
  else:
    return False, None, None
     

TT_PLUS = "TT_PLUS"
TT_EQUALS = "TT_EQUALS"
TT_DNEQUAL = "TT_DNEQUAL"
TT_GRTHAN = "TT_GRTHAN"
TT_LTHAN = "TT_LTHAN"
TT_MINUS = "TT_MINUS"
TT_KEYWORD = "TT_KEYWORD"
TT_SEMICOLON = "TT_SEMICOLON"
TT_INTEGER = "TT_INTEGER"
TT_HEX = "TT_HEX"
TT_IDENTIFIER = "TT_IDENTIFIER"
TT_LBRACE = "TT_LBRACE"
TT_RBRACE = "TT_RBRACE"
TT_STRING = "TT_STRING"
TT_AMPOINT = "TT_AMPOINT"
TT_PTR = "TT_PTR"
TT_FUNCCALL = "TT_FUNCCALL"
TT_DEQUAL = "TT_DEQUAL"
TT_MUL = "TT_MUL"
TT_BYTES = "TT_BYTES"
TT_DIV = "TT_DIV"
TT_MOD = "TT_MOD"
TT_CHAR = "TT_CHAR"
TT_ASM = "TT_ASM"
TT_AMP = "TT_AMP"

def findKeyFromValue(dictionary, v):
  for key, val in dictionary.items():
    if val == v:
        return key
  return None
  
KEYWORDS = {
  "INT_DEC": "let",
  "FN_DEC": "fn",
  "QUIT": "quit",
  "RETURN": "return",
  "IF": "if",
  "ASM": "asm",
  "ENDIF": "endif",
  "TRUE": "true",
  "FALSE": "false",
  "CONST": "const",
}

def is_valid_variable_name(name):
    return name.isidentifier() and not name in KEYWORDS.keys()


def lex(s):
  tmp = ""
  tmp2 = ""
  tmpid = ""
  tokens = []
  for i in s:
    #print(list(tmp))
    #print(tmpid)

    #print(tmpid)

    if i == "\"" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tmpid = "quote"
      tmp2 += i
    
    elif i == "\"" and tmpid == "quote" and tmpid != "chr" and tmpid != "paren":
      tmpid = ""
      tmp2 += i

    elif i == "(" and tmpid != "quote" and tmpid != "chr":
      #print("HEEHEJHE")
      tmpid = "paren"
      tmp2 += i
    
    elif i == ")" and tmpid == "paren" and tmpid != "chr" and tmpid != "quote":
      #print("hit2")
      tmpid = ""
      tmp2 += i

    elif i == "'" and tmpid != "chr" and tmpid != "quote" and tmpid != "paren":
      tmpid = "chr"
      tmp2 += i
    
    elif i == "'" and tmpid == "chr" and tmpid != "quote" and tmpid != "paren":
      tmpid = ""
      tmp2 += i
    
    elif i == " " and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      #print(tmpid)
      tmp = tmp2
      tmp2 = ""
    
    elif i == "\n" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
     # print("hey")
      tmp = tmp2
      tmp2 = ""
      
    elif i == "+" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_PLUS))
      tmpid = ""
      tmp2 = ""

    elif i == "&" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_AMP))
      tmpid = ""
      tmp2 = ""

    elif i == "%" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_MOD))
      tmpid = ""
      tmp2 = ""
      
    elif i == "-" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_MINUS))
      tmpid = ""
      tmp2 = ""

    elif i == "*" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_MUL))
      tmpid = ""
      tmp2 = ""

    elif i == "/" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_DIV))
      tmpid = ""
      tmp2 = ""
      
    elif i == "{" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_LBRACE))
      tmpid = ""
      tmp2 = ""
      
    elif i == "}" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_RBRACE))
      tmpid = ""
      tmp2 = ""
      
    elif i == "=" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_EQUALS))
      tmpid = ""
      tmp2 = ""
    
    elif i == "!" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_DNEQUAL))
      tmpid = ""
      tmp2 = ""

    elif i == ">" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_GRTHAN))
      tmpid = ""
      tmp2 = ""
    
    elif i == "<" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      tokens.append(Token(TT_LTHAN))
      tmpid = ""
      tmp2 = ""
      
    elif i == ";" and tmpid != "quote" and tmpid != "chr" and tmpid != "paren":
      #print("hi")
      tmp = tmp2
      tmpid = "semi"
      
    else:
      tmp2 += i

    if len(tmp) >= 4 and re.match(r"^(i8:)\d+$", tmp):
          
      tokens.append(Token(TT_BYTES, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""
      

    elif re.match(r"^[0-9]+$", tmp):
      tokens.append(Token(TT_INTEGER, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^(0[xX])[A-Fa-f0-9]+$", tmp):
      tokens.append(Token(TT_HEX, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r"^['][^\n][']$", tmp):
      tokens.append(Token(TT_CHAR, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif re.match(r'^["][^\n]*["]$', tmp):
      tokens.append(Token(TT_STRING, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif tmp in KEYWORDS.values():
      tokens.append(Token(TT_KEYWORD, KEYWORDS[findKeyFromValue(KEYWORDS, tmp)]))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif len(tmp) >= 2 and tmp[0] == "@" and is_valid_variable_name(tmp[1:]):
      tokens.append(Token(TT_AMPOINT, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""
      
    elif len(tmp) >= 2 and tmp[0] == "$" and is_valid_variable_name(tmp[1:]):
      tokens.append(Token(TT_PTR, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif is_valid_variable_name(tmp):
      tokens.append(Token(TT_IDENTIFIER, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""

    elif len(tmp) >= 3 and checkFuncCall(tmp)[0]:
      tokens.append(Token(TT_FUNCCALL, tmp))
      if tmpid == "semi":
        tokens.append(Token(TT_SEMICOLON))
        tmpid = ""
        tmp2 = ""
      tmpid = ""
      tmp = ""
      
      
  return tokens
  