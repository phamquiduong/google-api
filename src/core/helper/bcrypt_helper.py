from passlib.context import CryptContext


class BcryptHelper:
    def __init__(self) -> None:
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain_text: str, hashed_text: str) -> bool:
        return self.__pwd_context.verify(plain_text, hashed_text)

    def hash(self, text: str) -> str:
        return self.__pwd_context.hash(text)
