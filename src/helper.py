import sys
import os
from file import supported_fmts
import re
from enum import Enum
from errors import ERRNO
from consts import DBG_STR,DEFAULT_VDIM,STD_DB 
from file import FMT
class CLARGS:
    def __init__(self):
       self.dbg = False
       self.files = []
       self.MODE = 0
       self.raw = []
       self.RDB = STD_DB
       self.GDB = STD_DB
       self.vdim = DEFAULT_VDIM
       self.specfs = []

    def Parse(self):
        args = sys.argv[1:] 
        if len(args) < 2:
            help()
            sys.exit(ERRNO.E_HELP)
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
                help()
                sys.exit(ERRNO.E_HELP)
            elif i.startswith("-r="):
                i = i[3:]
                self.raw.append(i)
            elif i.startswith("--raw="):
                i = i[5:]
                self.raw.append(i)
            elif "http" in i:
                self.files.append(i)
            elif i.startswith("--csv="):
                self.specfs.append([FMT.CSV,i[6:]])
            elif i.startswith("--xls="):
                self.specfs.append([FMT.XLS,i[6:]])
            elif i.startswith("--xlxs="):
                self.specfs.append([FMT.XLS,i[7:]])
            elif i.startswith("--pdf="):
                self.specfs.append([FMT.PDF,i[6:]])
            elif i.startswith("--txt="):
                self.specfs.append([FMT.TXT,i[6:]])
            elif i.startswith("--html="):
                self.specfs.append([FMT.HTML,i[7:]])
            elif i.startswith("--doc="):
                self.specfs.append([FMT.DOCS,i[6:]])
            elif i.startswith("--docx="):
                self.specfs.append([FMT.DOCS,i[7:]])
            elif i.startswith("--log="):
                self.specfs.append([FMT.LOG,i[6:]])
            elif i.startswith("--sql="):
                self.specfs.append([FMT.SQL,i[6:]])
            elif i.startswith("--link="):
                self.specfs.append([FMT.COM,i[7:]])
            else:
                if any(i.endswith(k) for k in supported_fmts):
                    self.files.append(i)
                else:
                    print([i.endswith(k) for k in supported_fmts])
                    help()
                    sys.exit(ERRNO.E_HELP)

    def show(self):
        print(f"CLARGS: {{\nDEBUG: {self.dbg}\nOP_MODE: {self.MODE}\nDB: Rel={self.RDB} VecDim={self.vdim} Gra={self.GDB}\nFILES: {self.files}\nRAW: {self.raw}\n}}")

def help():
    print(DBG_STR)



    

