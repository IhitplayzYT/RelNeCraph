import errors
import file
import helper
import sys
import dbs
STD_DB = "RelNeCraph"


if __name__ == "main":
    clargs = helper.CLARGS()
    clargs.Parse()
    if not clargs:
        sys.exit(-1)
    if clargs.dbg:
        clargs.show()
    to_update = []
    to_exec = []
    to_update.extend([{filename: "USERINPUT", filetype: file.FMT.RAW,filecontent: preproc(x)} for x in clargs.raw])
    for fname in clargs.files:
        content,err,ftype = file.read_file(fname)
        if err:
            raise err
        if ftype != file.FMT.SQL:
            to_update.append({filename: fname,filetype: ftype, filecontent: preproc(content)})
        else:
            to_exec.extend(x for x in content.split(";"))
    ret = dbs.Exec_Queries(clargs,to_exec) 






    
        

        