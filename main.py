from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from models import Todo as TodoModel
import models
from models import User
from auth import hash_password, verify_password
from jose import jwt
from datetime import datetime, timedelta



models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
     credentials_exception = HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
     )
     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         username: str = payload.get("sub")
         if username is None:
             raise credentials_exception
     except:
         raise credentials_exception
     return username

class Todo(BaseModel):
    title:str
    completed:bool

class UserCreate(BaseModel):
    email : str
    username : str
    password : str

class UserLogin(BaseModel):
    username : str
    password : str


app = FastAPI()

@app.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    if not current_user:
        return {"error": "Not authenticated"}
    return {"username": current_user}



@app.get('/todos')
async def get_all_todos(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Nađi user objekat
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Vrati samo njegove todos
    return db.query(TodoModel).filter(TodoModel.user_id == user.id).all()


@app.post('/todos')
def create_todos(todo: Todo, db: Session = Depends(get_db)):
    db_todo = TodoModel(
        title=todo.title,
        completed=todo.completed
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


  
@app.put('/todos/{todo_id}')
async def update_todo(todo_id: int, todo: Todo, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_todo = db.query(TodoModel).filter(
    TodoModel.id == todo_id,        # Da li postoji taj todo?
    TodoModel.user_id == user.id    # Da li pripada ovom korisniku?
    ).first()

@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id: int, current_user: str = Depends(get_current_user),  # DODATO
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    db_todo = db.query(TodoModel).filter(
    TodoModel.id == todo_id,
    TodoModel.user_id == user.id  # PROVERA VLASNIŠTVA
    ).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found or access denied")
    
    db.delete(db_todo)
    db.commit()

    return {"message": "Todo deleted", "todo": db_todo}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        return {"error": "Username already exists"}

    hashed_pwd = hash_password(user.password)

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "username": new_user.username}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    print(f"Login attempt for: {user.username}")

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        print("User not found in database")
        return {"error": "Invalid credentials"}

    print(f"User found: {db_user.username}")
    print(f"Checking password...")
    password_ok = verify_password(user.password, db_user.hashed_password)
    print(f"Password valid: {password_ok}")

    if not password_ok:
        return {"error": "Invalid credentials"}

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

