from enum import Enum
from typing import Optional
from consts import ERR_STR
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
   E_HTTP = 9

class RelNeException(Exception):
    def __init__(self,message: Optional[str],errorcode: ERRNO):
        super().__init__(f"Error Code[{errorcode}] -> {message if message else ERR_STR[errorcode]}\n")
        self.errorcode = errorcode


