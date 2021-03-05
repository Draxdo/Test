import src.lex
import src.parse
import src.eval
import src.tools
import src.optimize
import src.pre
def main(file, n=None):

  import os
  debug = False

  l = src.tools.readSembleFile(file)

  l, fname = src.pre.process(l)

  x = src.lex.lex(l)

  with open("lexout.txt", "w") as fw:
    fw.write(str(x).replace("[", "[\n").replace("]", "]\n"))

  v = src.parse.parse(x)

  with open("parseout.txt", "w") as fw:
    fw.write(str(v).replace("[", "[\n").replace("]", "]\n"))

  src.eval.cmpf(v, "semble.asm")
  
  src.optimize.optimize("semble.asm")

  os.system("as --32 semble.asm -o semble.o")
  if n != None:
    fname = n
  os.system("ld -m elf_i386 -dynamic-linker /lib/ld-linux.so.2 -o " + fname + " semble.o -lc")
  if not debug:
    os.system("rm semble.o parseout.txt lexout.txt")

if __name__ == '__main__':
  #print(src.lex.checkFuncCall("hello(helo,hello, h)"))
  main("hello.smb")