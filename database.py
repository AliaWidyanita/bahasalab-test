from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "postgresql://postgres.khpeusonnmimmqxybwos:bahasalab-test@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

def get_engine():
    return create_engine(DATABASE_URI)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()