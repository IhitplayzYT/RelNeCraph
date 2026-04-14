from enum import Enum
class ERRNO(Enum):
   E_HELP = 0
   E_OS = 1
   E_IO = 2
   E_FOP = 3
   E_LIB = 4
   E_FMT = 5

class RelNeException(Exception):
    def __init__(self,message: str,errorcode: ErrorCode):
        super().__init__(f"Error Code[{errorcode}] -> {message}\n")
        self.errorcode = errorcode


