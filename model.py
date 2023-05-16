from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageGallery(Base):
    __tablename__ = 'image_gallery'

    gallery_id = Column(Integer, primary_key=True, autoincrement=True, comment='主键自增')
    gallery_title = Column(String(200), nullable=False, default='', unique=True, comment='标题')
    img_list = Column(Text, nullable=False, default='[]', comment='图片列表，json')
    create_time = Column(TIMESTAMP, nullable=False, default=func.now(), comment='创建日期')
    op_status = Column(Boolean, nullable=False, default=True, comment='软删标记')

    def __repr__(self):
        return f"<ImageGallery(gallery_id={self.gallery_id}, gallery_title='{self.gallery_title}', img_list='{self.img_list}', create_time='{self.create_time}', op_status={self.op_status})>"