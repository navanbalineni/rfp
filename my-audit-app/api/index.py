import io
import requests
import urllib3
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

# Disable warnings for external registry calls
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Vercel's entrypoint
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "Registry Link Active", "framework": "FastAPI"}

@app.post("/scan")
async def start_audit(
    manual_barcode: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    detected_code = manual_barcode

    # 1. Handle Optical Extraction (Image Upload)
    if file:
        try:
            # We use Pillow to verify the image is valid
            img_content = await file.read()
            img = Image.open(io.BytesIO(img_content))
            img.verify() # Ensure it's a real image
            # Note: For actual barcode reading from images on Vercel, 
            # you would typically call an external OCR API here.
        except Exception as e:
            return {"success": False, "error": f"Invalid Image: {str(e)}"}

    # 2. Logic for Empty Input
    if not detected_code:
        return {"success": False, "error": "No ID or Image provided"}

    # 3. Mock Data Response (Replace this with your actual Database/API logic)
    # This structure matches your index.html requirements
    return {
        "success": True,
        "data": [{
            "details": {
                "found": True,
                "barcode": detected_code,
                "name": "Authenticated Product Sample",
                "brand": "Audit Core Labs",
                "origin": "Verified Registry",
                "ingredients": "Sample ingredient data for verification purposes.",
                "health": {
                    "safety_status": "GOOD",
                    "processing_lvl": "Level 1 (Natural)",
                    "chemical_count": 0,
                    "chemical_list": []
                }
            }
        }]
    }
