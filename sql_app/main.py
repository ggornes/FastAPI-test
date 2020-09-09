from datetime import datetime
import hashlib
import os
import pathlib
import shutil
from typing import List

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

# from . import crud, models, schemas
from . import schemas
from . import models
from . import crud


from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/weight_records/", response_model=schemas.WeightRecord)
def create_weight_record_for_user(
    user_id: int, weight_record: schemas.WeightRecordCreate, db: Session = Depends(get_db)
):
    return crud.create_user_weight_record(db=db, weight_record=weight_record, user_id=user_id)


@app.get("/weight_records/", response_model=List[schemas.WeightRecord])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    weight_records = crud.get_weight_records(db, skip=skip, limit=limit)
    return weight_records

@app.post("/uploadfile/")
async def save_upload_file(file: UploadFile = File(...)):
    """ file: uploaded file
        :returns new_filename
    """
    file_name = os.path.splitext(file.filename)[0]
    file_extension = os.path.splitext(file.filename)[1]
    # new_filename = str(user_id) + ' - ' + file.filename + ' - ' + str(datetime.now())
    temp_filename = file_name + ' - ' + str(datetime.now())
    hashed_filename = hashlib.md5(temp_filename.encode())
    new_name = hashed_filename.hexdigest() + str(file_extension)
    print(temp_filename)
    print(new_name)

    # global upload_folder
    file_object = file.file
    # Create empty file to copy the file_object to
    if not os.path.exists(os.path.join(pathlib.Path().absolute() / 'uploads')):
        os.makedirs(os.path.join(pathlib.Path().absolute() / 'uploads'))
    upload_folder = open(os.path.join(pathlib.Path().absolute() / 'uploads', new_name), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
    # await file.write(file.filename)
    # print(content)
    # extension = os.path.splitext(file.filename[1] _, path)
    return {"filename": new_name}