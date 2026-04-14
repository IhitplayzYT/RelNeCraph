import sys
import os
from file import supported_fmts

DBG_STR = f""

def init_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(description=helper.DBG_STR)
    # TODO: FIXME: ADD the args
    return parser

class CLARGS:
    def __init__(self):
       self.dbg = False
       self.files = []
       self.MODE = 0
       self.DB = ""
    def Parse():
        args = sys.argv[1:] 
        for i in args:
            if i == "--DEBUG" or i == "-d":
                self.dbg = True
            elif i.startswith("-n="):
                self.DB = i[3:]
            elif i.startswith("--NEW-DB="):
                self.DB = i[9:]
            elif i == "-O0" or i == "-O1" or i == "-O2":
                self.MODE = i[2] 
            elif i == "-h" or i == "--help":
                print(DBG_STR)
                sys.exit(0)
            else:
                if any(i.endswith(k) for k in supported_fmts):
                    self.files.append(i)
                else:
                    print(DBG_STR)
                    sys.exit(0)
     

            
                
                

    

