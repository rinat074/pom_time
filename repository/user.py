from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from dataclasses import dataclass
from models import UserProfile

@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, username: str, password: str, access_token: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username, 
            password=password, 
            access_token=access_token
            ).returning(UserProfile.id)
        with self.db_session() as session:
            user_id:int = session.execute(query).scalar_one()
            session.commit()
            session.flush()
            return self.get_user_by_id(user_id)

    def get_user_by_id(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            user: UserProfile = session.execute(query).scalar_one_or_none()
        return user
    
    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            user: UserProfile = session.execute(query).scalar_one_or_none()
        return user

