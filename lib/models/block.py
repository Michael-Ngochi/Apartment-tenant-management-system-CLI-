from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from db import Base,SessionLocal

Session=SessionLocal

class Block(Base):
    __tablename__ = 'blocks'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    units = relationship("Unit", back_populates="block")

    # === CRUD METHODS ===

    @classmethod
    def create(cls, session: Session, name: str):
        if session.query(cls).filter_by(name=name).first():
            print(f"Block '{name}' already exists.")
            return
        block = cls(name=name)
        session.add(block)
        session.commit()
        print(f"Block '{name}' created.")
        return block

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session: Session, block_id: int):
        return session.query(cls).filter_by(id=block_id).first()

    @classmethod
    def update_name(cls, session: Session, block_id: int, new_name: str):
        block = cls.get_by_id(session, block_id)
        if not block:
            print("Block not found.")
            return
        block.name = new_name
        session.commit()
        print(f"Block ID {block_id} renamed to '{new_name}'.")
        return block

    @classmethod
    def delete(cls, session: Session, block_id: int):
        block = cls.get_by_id(session, block_id)
        if not block:
            print("Block not found.")
            return
        session.delete(block)
        session.commit()
        print(f"Block '{block.name}' deleted.")