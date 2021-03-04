import src.linkmain
import os

num = 0

def process(code, n="semble.out"):
  global num
  # include
  # define
  newcode = ""
  code = code.split("\n")
  name = n
  idx = -1
  for line in code:
    idx += 1
    if line.startswith("#include"):
      l = line.replace("#include ", "")
      l = l.split(", ")
      for f in l:
        newcode += importf(f, newcode)
    elif line.startswith("#program"):
      l = line.replace("#program ", "")
      name = l
    elif line.startswith("#file"):
      l = line.replace("#file ", "")
      try:
        lines = '\n'.join(code[idx+1:])
      except:
        pass
      with open("ppfcf.smb", "w") as fw:
        fw.write(lines)
      src.linkmain.compilefile("ppfcf.smb", l)
      try:
        os.system("rm ppfcf.smb")
      except:
        pass
      break
    else:
      newcode += "\n" + line
    
  return newcode, name
  
def importf(f, code):
  try:
    with open("libs/" + f, "r") as file:
      for l in file:
        code += "\n" + l
      return code
  except:
    quit("Unkown file!")

'''
#program main

fn main {
  quit 0;
}

#file other

fn main {
  quit 2;
}

#linkedfile somefile

fn other {
  quit 1;
}
'''