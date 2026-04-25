from enum import Enum
class ERRNO(Enum):
   E_HELP = 0
   E_OS = 1
   E_IO = 2
   E_FOP = 3
   E_LIB = 4
   E_FLOAD = 5
   E_FMT = 6
   E_LOGIN = 7
   E_QUERY = 8

ERR_STR = ["Show Help","Error occured in OS","IO error occured","File Operation Error Occured","Library Not Found",
           "Config file not Found","Format is Unsuppported","Login Failed","Query Failed"]

class RelNeException(Exception):
    def __init__(self,message: Optional[str],errorcode: ErrorCode):
        super().__init__(f"Error Code[{errorcode}] -> {message if message else ERR_STR[errorcode]}\n")
        self.errorcode = errorcode


