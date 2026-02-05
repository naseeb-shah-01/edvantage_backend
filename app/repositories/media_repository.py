
from app.models.media import Media
from app.schemas.media import UploadResponse,StoreMediaEntry


class MediaRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def createMedia(self, data: StoreMediaEntry):
        mediaEntry = Media(**data.dict())
        self.db_session.add(mediaEntry)
        self.db_session.commit()
        self.db_session.refresh(mediaEntry)
        return mediaEntry
    def delete_file(self, public_id: str) -> bool:
        deleted = (
            self.db_session
            .query(Media)
            .filter(Media.public_id == public_id)
            .delete(synchronize_session=False)
        )

        self.db_session.commit()
        return deleted > 0
    def findById(self,id:int):
        m=self.db_session.query(Media).filter(id=id).first()
        return m

   