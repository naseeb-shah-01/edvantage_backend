import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import settings





# Configure Cloudinary
print(settings.api_key,settings.api_secret,settings.cloud_name)
cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
    secure=True
)