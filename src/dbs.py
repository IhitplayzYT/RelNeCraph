GRAPH_PATTERNS = [
    r"\bMATCH\s*\(",          # graph match clause
    r"\bcypher\s*\(",         # Apache AGE
    r"\bCREATE\s+GRAPH\b",
    r"\bEDGE\b|\bVERTEX\b",
]

VECTOR_PATTERNS = [
    r"<->|<#>|<=>",           # distance operators
    r"\bcosine_distance\b",
    r"\bl2_distance\b",
    r"\bembedding\b",
    r"\bvector\b",
]

class SQL_VAR(Enum):
    ERR=0
    REL=1
    GRAPH=2
    VEC=3



def classify_sql(query:str) -> SQL_VAR:
    q = query.lower()
    for p in GRAPH_PATTERNS:
        if re.search(p, q):
            return SQL_VAR.GRAPH
    for p in VECTOR_PATTERNS:
        if re.search(p, q):
            return SQL_VAR.VEC
    return SQL_VAR.REL


def Init_DB():
    pass
def Init_Rel_DB():
    pass
def Init_Vec_DB():
    pass
def Init_Graph_DB():
    pass

def Exec_Queries(queries: [str]):
    pass