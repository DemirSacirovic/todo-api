from database import engine
from models import Base

print("Kreiram novu bazu...")
Base.metadata.create_all(bind=engine)
print("Baza kreirana!")
