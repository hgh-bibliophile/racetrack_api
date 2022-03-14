from sqlalchemy.orm import Session

import models, schemas

# ------
#  User
# ------

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ------
#  Race
# ------

def get_races(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Race).offset(skip).limit(limit).all()


def create_user_race(db: Session, race: schemas.RaceCreate, user_id: int):
    db_race = models.Race(**race.dict(), owner_id=user_id)
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    return db_race