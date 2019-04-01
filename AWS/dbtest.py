from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, Float, Date, Sequence, MetaData, Table, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

BD = create_engine('postgres://postgres:@172.20.0.11:5432')
DBlst = BD.execute("select datname from pg_database")
DBlst = [d[0] for d in DBlst]

if 'arrays' not in DBlst:
    BDcon = BD.connect()
    BDcon.execute("commit")
    BDcon.execute("create database arrays")
    BDcon.close()
    DBlst = BD.execute("select datname from pg_database")
    DBlst = [d[0] for d in DBlst]
    print("New container, database need to be created, therefore it's done")

BD.dispose()
BD = create_engine('postgres://postgres:@172.20.0.11:5432/arrays')

Bass = declarative_base()

def _get_date():
    return datetime.now()

class Arrayo(Bass):
    __tablename__ = "Fume table"

    id = Column(Integer, Sequence('arrayo_id_seq'), primary_key=True)
    date = Column(Date, default=_get_date)
    original = Column(ARRAY(Float))
    mastered = Column(ARRAY(Float))

metadata = Bass.metadata
metadata.create_all(BD)
Session = sessionmaker(bind=BD)
session = Session()
meta = MetaData()
metatable = Table('Fume table', meta, autoload = True, autoload_with=BD)

print('Engine roars!')

def addline(arr):
    mastar = sorted(arr)
    inst = Arrayo(original=arr, mastered=mastar)
    session.add(inst)
    session.commit()
    session.refresh(inst)
    return inst.id

def readlinesyield():
    BDcon = BD.connect()
    query = select([metatable])
    ResultProxy = BDcon.execute(query)
    for i in ResultProxy.fetchall():
        yield i
    BDcon.close()