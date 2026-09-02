from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

import qrcode


router = APIRouter(
    prefix="/qr",
    tags=["QR Code"]
)


QR_FOLDER = Path("qr_codes")

QR_FOLDER.mkdir(
    exist_ok=True
)


@router.get("/attendance")
def generate_attendance_qr():

    # IMPORTANT:
    # Replace this IP with your laptop's IPv4 address.
    #
    # Example:
    # http://192.168.1.15:8501

    url = "http://YOUR_LAPTOP_IP:8501"

    file_path = QR_FOLDER / "attendance_qr.png"

    qr = qrcode.make(url)

    qr.save(file_path)

    return FileResponse(
        path=file_path,
        media_type="image/png"
    )