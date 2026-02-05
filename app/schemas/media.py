from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
from datetime import datetime

class UploadResponse(BaseModel):
    public_id: str
    secure_url: str
    url: str
    resource_type: str
    format: Optional[str] = None
    bytes: int
    width: Optional[int] = None
    height: Optional[int] = None
    created_at: str

class DeleteResponse(BaseModel):
    result: str
    message: Optional[str] = None

class FileInfo(BaseModel):
    public_id: str
    secure_url: str
    resource_type: str
    format: str
    bytes: int
    width: int
    height: int
    created_at: datetime
    tags: Optional[list] = []
    metadata: Optional[Dict[str, Any]] = {}

class StoreMediaEntry(BaseModel):
    public_id:str
    resource_type:str
    size:int
