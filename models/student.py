from tortoise.models import Model
from tortoise import fields

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    classname = fields.CharField(max_length=30)
    nis = fields.IntField()
    nisn = fields.IntField()

    has_chosen = fields.ForeignKeyField('models.Candidate', related_name='chosen_by')

    def __str__(self):
        return self.name

class Candidate(Model):
    id = fields.IntField(pk=True)

    image = fields.CharField(max_length=100)
    vision = fields.TextField()
    mission = fields.TextField()

    student_info = fields.ForeignKeyField('models.Student', related_name='candidate_info')
