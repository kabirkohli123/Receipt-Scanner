import os
from fastapi.responses import RedirectResponse

from fastapi import FastAPI, File, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from backend.models import Base, Receipt
from backend.ocr_utils import extract_text_from_image
from backend.parser_utils import parse

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="backend/templates")

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

engine = create_engine("sqlite:///receipts.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = UPLOAD_DIR + file.filename

    # Save uploaded file
    with open(path, "wb") as f:
        f.write(await file.read())

    size = os.path.getsize(path)
    print("\n============================")
    print("File saved at:", path)
    print("File size:", size, "bytes")
    print("============================\n")

    # OCR
    text = extract_text_from_image(path)

    # Load ML classifier
    from backend.ml_classifier import ReceiptClassifier
    classifier = ReceiptClassifier()
    classifier.load()

    # CORRECT way to predict
    category = classifier.predict(text)

    print("Predicted Category:", category)

    # Parse fields
    data = parse(text)

    # OVERRIDE parser category with ML category
    data["category"] = category
    data["raw_text"] = text  # include full OCR for frontend

    # Save to DB
    db = Session()
    receipt = Receipt(**data, filename=file.filename)
    db.add(receipt)
    db.commit()

    return RedirectResponse("/", status_code=303)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@app.get("/upload-page", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    receipts = db.query(Receipt).all()
    db.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "receipts": receipts})