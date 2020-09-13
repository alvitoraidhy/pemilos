from tortoise.models import Model
from tortoise import fields

class StudentInfoMixin():
    nis = fields.IntField(unique=True)
    nisn = fields.IntField(unique=True)
    name = fields.CharField(max_length=100)
    classname = fields.CharField(max_length=30)

class Student(StudentInfoMixin, Model):
    id = fields.IntField(pk=True)
    grade = fields.IntField()
    has_chosen = fields.ForeignKeyField('models.Candidate', related_name='chosen_by', null=True, on_delete=fields.SET_NULL)

    def __str__(self):
        return self.name

class Candidate(StudentInfoMixin, Model):
    candidate_number = fields.IntField(pk=True, generated=False)
    image = fields.CharField(max_length=100)
    vision = fields.TextField()
    mission = fields.TextField()

    def __str__(self):
        return self.name
