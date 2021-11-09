from tortoise.models import Model
from tortoise import fields
import hashlib

class StudentInfoMixin():
    nis = fields.IntField(unique=True)
    name = fields.CharField(max_length=100)
    classname = fields.CharField(max_length=30)

class Student(StudentInfoMixin, Model):
    id = fields.IntField(pk=True)
    grade = fields.IntField()
    has_chosen = fields.ForeignKeyField('models.Candidate', related_name='chosen_by', null=True, on_delete=fields.SET_NULL)
    password_hash = fields.CharField(max_length=50)

    def set_password(self, new_password):
        new_password_hash = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        self.password_hash = new_password_hash

    def verify_password(self, password_verify):
        if hashlib.md5(password_verify.encode('utf-8')).hexdigest() != self.password_hash:
            return False

        return True

    def __str__(self):
        return self.name

    @staticmethod
    class InvalidPasswordException(Exception):
        pass

class Candidate(StudentInfoMixin, Model):
    candidate_number = fields.IntField(pk=True, generated=False)
    image = fields.CharField(max_length=100)
    vision = fields.TextField()
    mission = fields.TextField()

    def __str__(self):
        return self.name
