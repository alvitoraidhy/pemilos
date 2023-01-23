from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields
import hashlib


class Admin(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    username = fields.CharField(max_length=20, unique=True)
    password_hash = fields.CharField(max_length=50)

    def set_password(self, new_password):
        new_password_hash = hashlib.md5(new_password.encode("utf-8")).hexdigest()
        self.password_hash = new_password_hash

    def verify_password(self, password_verify):
        if (
            hashlib.md5(password_verify.encode("utf-8")).hexdigest()
            != self.password_hash
        ):
            raise self.InvalidPasswordException(
                "Supplied password does not match stored hash"
            )

    async def serialize(self):
        pydantic_model = pydantic_model_creator(Admin)
        pydantic_instance = await pydantic_model.from_tortoise_orm(self)
        return pydantic_instance.json()

    def __str__(self):
        return self.name

    class PydanticMeta:
        exclude = ("password_hash",)

    @staticmethod
    class InvalidPasswordException(Exception):
        pass
