from sqlmodel import SQLModel, Field

# Generic message
class Message(SQLModel):
    message: str