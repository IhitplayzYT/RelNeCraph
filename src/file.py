import errors
import pandas as pd
from pathlib import Path
import sys
import os
from docx import Document
from PyPDF2 import PdfReader
from enum import Enum
class FMT(Enum):
    NULL=0
    CSV=1
    XLS=2
    PDF=3
    TXT=4
    HTML=5
    DOCS=6
    LOG=7
    SQL=7


supported_fmts = [".csv",".xls",".xlsx",".pdf",".txt",".html",".docx",".doc",".log",".sql"]
seperator = "<| . |>"
def read_file(path: str):
    fmt = path.split(".")[-1]
    known = False
    ret = ""
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
            return (path,None,FMT.NULL)
        else:
            return (None,errors.RelNeException(f"Unable to parse {path} as a valid file of type {fmt}",errors.ERRNO.E_OS),FMT.NULL) 
    
    
    if fmt == ".csv":
        ret = pd.read_csv(path,delim=",")
        if not ret:
            return (None,errors.RelNeException(f"Unable to parse as {fmt[1:]} file",errors.ERRNO.E_FMT),FMT.NULL) 
        return (ret,None,FMT.CSV)
    elif fmt == ".xls" or fmt == ".xlsx": 
        ret = pd.read_excel(path,delim=",")
        if not ret:
            return (None,errors.RelNeException(f"Unable to parse as {fmt[1:]} file",errors.ERRNO.E_FMT),FMT.NULL) 
        return (ret,None,FMT.XLS)
    elif fmt == ".pdf":
        pass
    elif fmt == ".txt":
        pass
    elif fmt == ".html":

        pass
    elif fmt == ".docx" or fmt == ".doc":
        doc = Document(path)
        for x in doc.paragraphs:
            if x.text.strip():
                ret += f"Para:{x}{seperator}"
        if ret.endswith(seperator):
            ret = ret[:-len(seperator)]
        for table in doc.tables:
            ret += "{"
            for row in table.rows:       
                ret += "{" + f"{row}:"
                for cell in row.cells:
                    ret += f"{cell.text}{seperator}"
                if ret.endswith(seperator):
                    ret = ret[:-len(seperator)]
                ret += "},"
            if ret.endswith(","): ret[:-1]
            ret += "}" 
        return (ret,None,FMT.DOCS)
       
    elif fmt == ".log":
        pass
    elif fmt == ".sql":

        pass
    else:
        return (None,errors.RelNeException(f"Unable to parse as {fmt[1:]} file",errors.ERRNO.E_FMT)) 
