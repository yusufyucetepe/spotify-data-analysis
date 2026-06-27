from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db import Base


class User(Base):
    __tablename__ = "users"

    spotify_id = Column(String, primary_key=True)
    display_name = Column(String)
    email = Column(String)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    token_expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
