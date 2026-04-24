from sqlalchemy import create_engine
from neo4j import GraphDatabase
import faiss
from dotenv import load_dotenv
import errors
import os
import helper
RELATIONALDB,VECTORDB,GRAPHDB = None,None,None



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


def Init_DB(rdb,dim):
    load_dotenv()

    ru,rp,rh,rpo =  os.getenv("RDB_USER"),os.getenv("RDB_PASS"), os.getenv("RDB_HOST"),os.getenv("RDB_PORT")
    if not ru or not rp:
        raise errors.RelNeException(errors.ERRNO.E_LOGIN,"Username and Password not provided for RelationalDB!")
    r_conn = Init_Rel_DB(ru,rp,rh,rpo,rdb)

    v_conn = Init_Vec_DB(dim)

    gu,gp,gh,gpo =  os.getenv("GDB_USER"),os.getenv("GDB_PASS"), os.getenv("GDB_HOST"),os.getenv("GDB_PORT")  
    if not gu or not gp:
        raise errors.RelNeException(errors.ERRNO.E_LOGIN,"Username and Password not provided for GraphDB!")
    g_conn = Init_Graph_DB(gu,gp,gh,gpo)
    RELATIONALDB,VECTORDB,GRAPHDB = r_conn,v_conn,g_conn 
    return r_conn,g_conn,v_conn

def Init_Rel_DB(u,p,h,po,db):
    h = "localhost" if not h else h
    po = "3306" if not po else po
    engine = create_engine(f"mysql+pymysql://{u}:{p}@{h}:{po}/{db}")
    return engine

def Init_Vec_DB(dim):
    dim = 128 if not dim else dim
    return faiss.IndexFlatL2(dim)

def Init_Graph_DB(u,p,h,po):
    h = "localhost" if not h else h
    po = "7687" if not po else po
    driver = GraphDatabase.driver(f"bolt://{h}:{po}",auth=(u,p))
    return driver


def Exec_Queries(clargs:helper.CLARGS,queries: [str]):
    if not RELATIONALDB and not VECTORDB and not GRAPHDB:
        Init_DB(clargs.RDB,clargs.vdim)
    # TODO: FIXME:
    pass
    