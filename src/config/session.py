from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try: 
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()