from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from pydantic import BaseModel
import uuid

# -----------------------
# Database Setup
# -----------------------
DATABASE_URL = "sqlite:///./notes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------
# Models
# -----------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    share_uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="notes")

Base.metadata.create_all(bind=engine)

# -----------------------
# Schemas
# -----------------------
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class NoteCreate(BaseModel):
    title: str
    content: str
    user_id: int

class NoteUpdate(BaseModel):
    title: str
    content: str

# -----------------------
# FastAPI App
# -----------------------
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Routes
# -----------------------

# Register
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# Login
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": db_user.id}

# Create Note
@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content, owner_id=note.user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content,
        "share_uuid": new_note.share_uuid,
        "share_url": f"/share/{new_note.share_uuid}",
        "owner_id": new_note.owner_id
    }

# Get Notes for a User
@app.get("/notes/{user_id}")
def get_notes(user_id: int, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.owner_id == user_id).all()
    return [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "share_uuid": note.share_uuid,
            "share_url": f"/share/{note.share_uuid}"
        }
        for note in notes
    ]

# Update Note
@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_update.title
    note.content = note_update.content
    db.commit()
    db.refresh(note)
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "share_uuid": note.share_uuid,
        "share_url": f"/share/{note.share_uuid}"
    }

# Delete Note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}

# Share Note
@app.get("/share/{share_uuid}")
def share_note(share_uuid: str, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.share_uuid == share_uuid).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"title": note.title, "content": note.content}
