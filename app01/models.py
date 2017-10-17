from django.db import models

# Create your models here.


class Classes(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption


class Students(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, null=True)
    cls = models.ForeignKey('Classes')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    cls = models.ManyToManyField('Classes')

    def __str__(self):
        return self.name


class Administrator(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username



