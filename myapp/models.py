from django.db import models



class Subject(models.Model):

    subject_name = models.CharField(max_length=30)

    def __str__(self):
        return self.subject_name




class Assignment(models.Model):

    priority = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High")
    ]


    status = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    ]

    title = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    due_date = models.DateField()
    priority = models.CharField(max_length=10,choices=priority,default='Medium')
    status = models.CharField(max_length=20,choices=status,default='Pending')
    attachment = models.FileField( upload_to="assignments/",blank=True,null=True)
    create_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class AptitudeCategory(models.Model):
    category_name = models.CharField(max_length=50)
    

    def __str__(self):
        return self.category_name


class Question(models.Model):
    category=models.ForeignKey(AptitudeCategory,on_delete=models.CASCADE)

    question=models.TextField()

    option_a=models.CharField(max_length=100)
    option_b=models.CharField(max_length=100)
    option_c=models.CharField(max_length=100)
    correct_answer=models.CharField(max_length=1)


    def __str__(self):
        return self.question