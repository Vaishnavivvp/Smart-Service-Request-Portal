from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from database import SessionLocal, engine, Base
import models
from auth import (
    verify_password,
    create_access_token,
    verify_token,
    hash_password
)

app = FastAPI()

security = HTTPBearer()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# -------------------- DATABASE DEPENDENCY --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- GET CURRENT USER --------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)

    user = db.query(models.User).filter(
        models.User.email == payload["sub"]
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------------------- USER SIGNUP (ALWAYS NORMAL USER) --------------------
@app.post("/signup")
def signup(
    email: str,
    password: str,
    name: str,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)

    new_user = models.User(
        email=email,
        password=hashed_password,
        name=name,
        role="user"   # 🔒 Always user
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# -------------------- LOGIN --------------------
@app.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "role": user.role
    }


# -------------------- CREATE REQUEST --------------------
@app.post("/requests")
def create_request(
    title: str,
    category: str,
    description: str,
    priority: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_request = models.Request(
        title=title,
        category=category,
        description=description,
        priority=priority,
        status="Open",
        requester_id=current_user.id
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return {
        "message": "Request created successfully",
        "request_id": new_request.id
    }


# -------------------- VIEW REQUESTS WITH FILTERS --------------------
@app.get("/requests")
def view_requests(
    category: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Request)

    if category:
        query = query.filter(models.Request.category == category)

    if status:
        query = query.filter(models.Request.status == status)

    if priority:
        query = query.filter(models.Request.priority == priority)

    return query.all()


# -------------------- UPDATE STATUS (STRICT ADMIN ONLY) --------------------
@app.put("/requests/{request_id}/status")
def update_status(
    request_id: int,
    new_status: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 🔒 Only real admin from DB
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can update status"
        )

    request = db.query(models.Request).filter(
        models.Request.id == request_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    allowed_status = ["Open", "In Progress", "Resolved"]

    if new_status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Use: Open, In Progress, Resolved"
        )

    request.status = new_status
    db.commit()

    return {"message": f"Status updated to {new_status}"}
