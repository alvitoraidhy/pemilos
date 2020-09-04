from tortoise.models import Model
from tortoise import fields

class StudentInfoMixin():
    nis = fields.IntField(pk=True, generated=False)
    nisn = fields.IntField()
    name = fields.CharField(max_length=100)
    classname = fields.CharField(max_length=30)

class Student(StudentInfoMixin, Model):
    has_chosen = fields.ForeignKeyField('models.Candidate', related_name='chosen_by')

    def __str__(self):
        return self.name

class Candidate(StudentInfoMixin, Model):
    candidate_number = fields.IntField()
    image = fields.CharField(max_length=100)
    vision = fields.TextField()
    mission = fields.TextField()

    def __str__(self):
        return self.name
