from sqlalchemy import create_engine,text
from sqlalchemy.exc import SQLAlchemyError
from neo4j import GraphDatabase
import faiss
from dotenv import load_dotenv
import errors
import os
import helper
import errors
import re
import ast
from enum import Enum
from typing import Optional
RELATIONALDB,VECTORDB,GRAPHDB = None,None,None
from consts import GRAPH_PATTERNS,VECTOR_PATTERNS



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


def exec_rquery(query:str) -> Optional[str]:
    qtype = query.strip().split()[0].lower()
    try:
        with RELATIONALDB.connect() as conn:
            ret = conn.execute(text(query))
            # ---- SELECT ----
            if qtype == "select":
                rows = ret.mappings().all() 
                return "Ok" + "\n".join(rows)

            # ---- INSERT ----
            elif qtype == "insert":
                if ret.inserted_primary_key:
                    return f"Ok: {ret.inserted_primary_key[0]}"
                return "Ok" if ret.rowcount > 0 else "Err"

            # ---- UPDATE / DELETE ----
            elif qtype in ("update", "delete"):
                return "Ok" if ret.rowcount > 0 else "Err"
            else:
                return "Ok"

    except SQLAlchemyError as e:
        return f"Err:{e}"


def exec_gquery(query: str):
    qtype = query.strip().split()[0].lower()
    try:
        with GRAPHDB.session() as session:
            ret = session.run(query)

            # ---- READ (MATCH / RETURN) ----
            if qtype in ("match", "return"):
                data = [record.data() for record in ret]
                return "Ok" + "\n".join(data)

            # ---- WRITE (CREATE / MERGE / SET / DELETE) ----
            else:
                summary = ret.consume()
                counters = summary.counters

                changed = (
                    counters.nodes_created
                    + counters.nodes_deleted
                    + counters.relationships_created
                    + counters.relationships_deleted
                    + counters.properties_set
                )

                return "Ok" if changed > 0 else "Err"

    except Neo4jError as e:
        return f"Err:{e}"


def eval_shortform(expr):
    m = re.match(r"\[(.+)\]\*(\d+)", expr)
    if not m:
        return None

    val = float(m.group(1))
    count = int(m.group(2))
    return [val] * count

def safe_eval(expr):
    try:
        return ast.literal_eval(expr)
    except:
        try:
            repeat = eval_shortform(expr)
            if repeat is not None:
                return repeat
            return None
        except:
            return None


def get_vec_param(query: str) -> []:
    parts = query.split("|")
    if len(parts) < 6:
        return [None]*6
    op = parts[0].lower()
    vectors = safe_eval(parts[1])
    ids = safe_eval(parts[2])
    query_vec = safe_eval(parts[3])
    k = safe_eval(parts[4])
    meta = safe_eval(parts[5])
    return [op,vectors,ids,query_vec,k,meta]


def exec_vquery(query:str):
    """  Please change the params to work with the entire detail encoded as a string"""
    query = "".join(filter(lambda x: x != ' ' and x != '\n',query.strip()))
# Sample: insert|[[0.1]*128,[0.2]*128]|[1,2]|[0.1]*128|3|[{"name":"a"},{"name":"b"}]
    results = []
    try:
        op,vectors_s,ids_s,query_vec_s,k,meta = get_vec_param(query)
        if op == None:
            return "Err" 

        # ---- SEARCH (SELECT equivalent) ----
        if op == "search":
            if query_vec is None:
                return "Err"

            D, I = VECTORDB.search(np.array([query_vec]).astype("float32"), k)

            for dist, idx in zip(D[0], I[0]):
                if idx == -1:
                    continue
                results.append(f"idx={int(idx)} dist={float(dist)} meta={metadata_store.get(int(idx))}")
            return results

        # ---- INSERT ----
        elif op == "insert":
            if vectors is None or ids is None:
                return "Err"

            vecs = np.array(vectors).astype("float32")
            ids_np = np.array(ids).astype("int64")
            index.add_with_ids(vecs, ids_np)
            # store metadata if provided
            if meta:
                for i, m in zip(ids, meta):
                    metadata_store[i] = m
            return "Ok"

        # ---- DELETE ----
        elif op == "delete":
            if ids is None:
                return "Err"
            ids_np = np.array(ids).astype("int64")
            removed = index.remove_ids(ids_np)
            for i in ids:
                metadata_store.pop(i, None)
            return "Ok" if removed > 0 else "Err"

        # ---- UPDATE (remove + add) ----
        elif op == "update":
            if vectors is None or ids is None:
                return "Err"
            ids_np = np.array(ids).astype("int64")
            index.remove_ids(ids_np)
            vecs = np.array(vectors).astype("float32")
            index.add_with_ids(vecs, ids_np)
            if meta:
                for i, m in zip(ids, meta):
                    metadata_store[i] = m

            return "Ok"

        else:
            return "Err"

    except Exception as e:
        return f"Err:{e}"




def Exec_Queries(clargs:helper.CLARGS,queries: [str]) -> [[int,str]]:
    ret = []
    if not RELATIONALDB and not VECTORDB and not GRAPHDB:
        Init_DB(clargs.RDB,clargs.vdim)
    for i,query in enumerate(queries):
        qtype = classify_sql(query)

        res = exec_rquery(query=query) if qtype == SQL_VAR.REL else exec_gquery(query=query) if qtype == SQL_VAR.GRAPH else exec_vquery(query=query) 
        if res.startswith("Err"):
            errors.RelNeException(res if res != "Err" else None,E_QUERY)
        else:
            if len(res) == 2 and res == "Ok":
                continue
            else:
                ret.append([i+1,res[2:]])

    
    return ret


def execute_query(query:str,type_query:SQL_VAR) -> str:
    if type_query == SQL_VAR.REL:
       return exec_rquery(query=query)
    elif type_query == SQL_VAR.GRAPH:
        return exec_gquery(query=query)
    elif type_query == SQL_VAR.VEC:
        return exec_vquery(query=query)
    else:
        return "Err"


# // A: exact match
# MATCH (root:Node {text: $term})
# 
# // B: local expansion
# OPTIONAL MATCH p = (root)-[*1..2]-(local)
# WITH root, collect(DISTINCT local) AS local_nodes
# 
# // C: vector search
# CALL db.index.vector.queryNodes("node_vec", $topN, $embedding)
# YIELD node AS candidate, score
# 
# // D: filter out connected
# WHERE NOT (root)-[*1..2]-(candidate)
#   AND candidate <> root
# 
# WITH root, local_nodes,
#      collect(candidate)[0..$k_vec] AS global_nodes
# 
# RETURN root, local_nodes, global_nodes; 