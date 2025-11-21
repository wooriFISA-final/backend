from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.user_id"), nullable=False)
    title = Column(String(255))
    content = Column(String(255))

    member = relationship("Member", backref="chat_histories")
