from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import field_validator
from app.database import Base
from app.database import Scan, SessionLocal
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


from app.virustotal import check_domain, check_ip
from app.dns_lookup import lookup_domain
from app.whois_lookup import lookup_whois
from app.ssl_python import check_ssl
from app.abuseipdb import check_ip_up

from app.target_validation import validate_target_type
from app.risk_engine import calculate_risk
from app.ai_analysis import analyze_threat
from app.pdf_report import create_pdf

from fastapi.responses import FileResponse


from fastapi.middleware.cors import CORSMiddleware # CORS: Cross-Origin Resource Sharing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)


class ScanRequest(BaseModel):
    target : str
    target_type : str

    @field_validator("target") # Pydantic decorator
    @classmethod
    def validate_target(cls, value):
        if not value.strip():
            raise ValueError("target can't be empty")
        
        return value

class ScanResponse(BaseModel):
    id: int
    target: str
    target_type: str
    results: dict
    ai_analysis: str


@app.get("/")
def home():
    return {"Message": "Threat Intelligence Dashboard API is running"}


@app.post("/scan", response_model = ScanResponse)
def scan(request: ScanRequest, db: Session = Depends(get_db)):

    request.target_type = (request.target_type).lower()

    if not validate_target_type(request.target, request.target_type):
        raise HTTPException(
            status_code = 400,
            detail = f"Target doesn't match the target type: {request.target_type}"
        )

    results = {}

    if request.target_type == "domain":

        dns_result = lookup_domain(request.target)
        results["DNS"] = dns_result

        if "Error" in dns_result:
            results["Status"] = "Unresolvable Domain"

        else:
            results["VirusTotal"] = check_domain(request.target)
            results["WHOIS"] = lookup_whois(request.target)
            results["SSL"] = check_ssl(request.target)

    elif request.target_type == "ip":
        results["VirusTotal"] = check_ip(request.target)
        results["AbuseIPDB"] = check_ip_up(request.target)

    else:
        raise HTTPException(
            status_code = 400,
            detail = "Invalid target Type"
        )
    

    results = jsonable_encoder(results)

    if "Status" in results.keys():
        AI_Analysis = "Analysis not performed because the target is unresolvable."

    else:
        risk = calculate_risk(results, request.target_type)
        results["Risk Score"] = risk

        AI_Analysis = analyze_threat(results)

    new_scan = Scan(
        target = request.target,
        target_type = request.target_type,
        results = results,
        ai_analysis = AI_Analysis
    )

    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return {
        "id": new_scan.id,
        "target": new_scan.target,
        "target_type": new_scan.target_type,
        "results": new_scan.results,
        "ai_analysis": new_scan.ai_analysis
    }

@app.get("/scan", response_model = list[ScanResponse])
def get_scans(db: Session = Depends(get_db)):
    scan_records = db.query(Scan).all()
    return scan_records


@app.get("/scan/{scan_id}", response_model = ScanResponse)
def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan_record = db.query(Scan).filter(Scan.id == scan_id).first()
    
    if scan_record is None:
        
        raise HTTPException(status_code = 404, detail = "Scan Not Found")

    filename = create_pdf(scan_record)
    
    return FileResponse(
        filename,
        media_type = "application/pdf",
        filename = filename
    )

@app.put("/scan/{scan_id}", response_model = ScanResponse)
def put_scan(scan_id: int, request: ScanRequest, db: Session = Depends(get_db)):

    scan_record = db.query(Scan).filter(Scan.id == scan_id).first()
    
    if scan_record is None:
        
        raise HTTPException(status_code = 404, detail = "Scan Not Found")
    
    scan_record.target = request.target
    scan_record.target_type = request.target_type

    db.commit()

    return scan_record

@app.delete("/scan/{scan_id}")
def delete_scan(scan_id: int, request: ScanRequest, db: Session = Depends(get_db)):

    scan_record = db.query(Scan).filter(Scan.id == scan_id).first()

    if scan_record is None:
        raise HTTPException(status_code = 404, detail = "Scan Not Found")

    db.delete(scan_record)
    db.commit()

    return {"Message": "Scan deleted successfully"}