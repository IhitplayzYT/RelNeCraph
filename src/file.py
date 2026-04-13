import errors
import pandas as pd
from pathlib import Path
import sys
import os

supported_fmts = [".csv",".xls",".xlsx",".pdf",".word",".txt",".html",".docx",".doc",".log",".sql"]
def read_file(path: str) -> (str,errors.RelNeException):
    fmt = path.split(".")[-1]
    known = False
    ret = None
    for i in supported_fmts:
        if not path.endswith(i):
            continue
        else:
            fmt = i 
            known = True
            break
    # Assume raw text or non existent file[check for it]
    if not known:
        os_p = Path(path)
        if not os_p.exists():
            return (path,None)
        else:
            return (None,errors.RelNeException(f"Unable to parse {path} as a valid file of type {fmt}",E_OS)) 
    
    
    if fmt == ".csv":
        ret = pd.read_csv(path,delim=",")
        if not ret:
            return (None,errors.RelNeException(f"Unable to parse as {fmt[1:]} file",E_FMT)) 
    elif fmt == ".xls" or fmt == ".xlsx": 
        ret = pd.read_excel(path,delim=",")
        if not ret:
            return (None,errors.RelNeException(f"Unable to parse as {fmt[1:]} file",E_FMT)) 
    elif fmt == ".pdf":
        pass
    elif fmt == ".word":
        pass
    elif fmt == ".txt":
        pass
    elif fmt == ".html":
        pass
    elif fmt == ".docx" or fmt == ".doc":
        pass
    elif fmt == ".log":
        pass
    elif fmt == ".sql":
        pass
    else:
        return (None,errors.RelNeException(f"Unable to parse as {fmt[1:]} file",E_FMT)) 
