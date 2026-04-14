import errors
import file
import helper
import sys

STD_DB = "RelNeCraph"


if __name__ == "main":
    clargs = helper.CLARGS()
    clargs.Parse
    if not clargs:
        sys.exit(-1)
    if clargs.dbg:
        print(f"CLARGS: {{\nDEBUG: {clargs.dbg}\nOP_MODE: {clargs.MODE}\nDB: {clargs.DB if clargs.DB else STD_DB}\nFILES: {clargs.files}\n}}")
    
        