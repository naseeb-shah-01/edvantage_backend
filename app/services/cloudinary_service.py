import cloudinary.uploader
import cloudinary.api
from fastapi import HTTPException,Depends
import os
from typing import Optional, Dict, Any
from app.repositories.media_repository import MediaRepository
from app.db.session import get_db 
from sqlalchemy.orm import Session



class CloudinaryService:
    @staticmethod
    async def upload_file(file, folder: str = "fastapi_uploads", resource_type: str = "auto"):
        """
        Upload file to Cloudinary
        
        Args:
            file: Uploaded file from FastAPI
            folder: Folder to upload to
            resource_type: 'image', 'video', 'auto', etc.
        
        Returns:
            dict: Upload response
        """
        try:
            # Read file content
            contents = await file.read()
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                contents,
                folder=folder,
                resource_type=resource_type
            )
            res={
                "public_id": upload_result.get("public_id"),
                "secure_url": upload_result.get("secure_url"),
                "url": upload_result.get("url"),
                "resource_type": upload_result.get("resource_type"),
                "format": upload_result.get("format"),
                "bytes": upload_result.get("bytes"),
                "width": upload_result.get("width"),
                "height": upload_result.get("height"),
                "created_at": upload_result.get("created_at")
            }
            print("Uploaded succeffully")
           
            return res
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    @staticmethod
    def delete_file(public_id: str, resource_type: str = "image"):
        """
        Delete file from Cloudinary
        
        Args:
            public_id: Public ID of the file
            resource_type: Type of resource ('image', 'video', etc.)
        
        Returns:
            dict: Delete result
        """
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    
    @staticmethod
    def get_file_info(public_id: str):
        """
        Get file information
        
        Args:
            public_id: Public ID of the file
        
        Returns:
            dict: File information
        """
        try:
            result = cloudinary.api.resource(public_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    
    @staticmethod
    def list_files(folder: str = "fastapi_uploads", max_results: int = 10):
        """
        List files in a folder
        
        Args:
            folder: Folder path
            max_results: Maximum number of results
        
        Returns:
            list: List of files
        """
        try:
            result = cloudinary.api.resources(
                type="upload",
                prefix=folder,
                max_results=max_results
            )
            return result.get("resources", [])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")