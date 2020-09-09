from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    # db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db_user = models.User(name=user.name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_weight_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeightRecord).offset(skip).limit(limit).all()


def create_user_weight_record(db: Session, weight_record: schemas.WeightRecord, user_id: int):
    db_weight_record = models.WeightRecord(**weight_record.dict(), user_id=user_id)
    db.add(db_weight_record)
    db.commit()
    db.refresh(db_weight_record)
    return db_weight_record