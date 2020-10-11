from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = None

# initialize DB stuff
def initialize(connection_string):
    engine = create_engine(connection_string)
    global Session
    Session = sessionmaker(bind=engine)

def get_session():
    if Session is None: raise Exception("Must call init before get_session")
    return Session()