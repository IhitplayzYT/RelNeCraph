import sys
import os
from file import supported_fmts
import re
from enum import Enum
DBG_STR = f"Usage:\npython3 RelNeCraph [OPTIONS] [FILES...]\nOptions:\n\n-d, --DEBUG\nEnable debug mode\n\n-nr=<name>\nRelational database name / identifier\n\n-ng=<name>\nGraph database name / identifier\n\n-vdim=<int>\nVector dimension size (integer)\n\n-O0 | -O1 | -O2\nOptimization level\nO0 → no optimization\nO1 → basic optimization\nO2 → aggressive optimization\n\n-r=<string>\n--raw=<string>\nAdd raw input string \n\n-h, --help\nShow help message and exit\n\nArguments:\nFILES...\nInput files (must match supported formats)\n\nNotes:\n\n* Unknown flags or unsupported file formats will trigger this help.\n* Multiple -r/--raw entries are appended in order.\nSupported fiLE formats: .csv, .xls, .xlsx, .pdf, .txt, .html, .docx, .doc, .log, .sql(Will be executed), LINKS\n"
DEFAULT_VDIM = 128
class CLARGS:
    def __init__(self):
       self.dbg = False
       self.files = []
       self.MODE = 0
       self.raw = []
       self.RDB = ""
       self.GDB = ""
       self.vdim = DEFAULT_VDIM

    def Parse(self):
        args = sys.argv[1:] 
        for i in args:
            if i == "--DEBUG" or i == "-d":
                self.dbg = True
            elif i.startswith("-nr="):
                self.RDB = i[4:]
            elif i.startswith("-vdim="):
                self.vdim = int(i[7:])
            elif i.startswith("-ng="):
                self.GDB = i[4:]
            elif i == "-O0" or i == "-O1" or i == "-O2":
                self.MODE = i[2] 
            elif i == "-h" or i == "--help":
                print(DBG_STR)
                sys.exit(0)
            elif i.startswith("-r="):
                i = i[3:]
                self.raw.append(i)
            elif i.startswith("--raw="):
                i = i[5:]
                self.raw.append(i)
            else:
                if any(i.endswith(k) for k in supported_fmts):
                    self.files.append(i)
                else:
                    print(DBG_STR)
                    sys.exit(0)
    def show(self):
        print(f"CLARGS: {{\nDEBUG: {clargs.dbg}\nOP_MODE: {clargs.MODE}\nDB: Rel={clargs.RDB} VecDim={clargs.vdim} Gra={clargs.GDB}\nFILES: {clargs.files}\nRAW: {clargs.raw}\n}}")

def help():
    print(DBG_STR)



    

