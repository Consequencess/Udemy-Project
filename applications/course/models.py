from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Theme(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    LANGUAGE = (
        ('Russia', 'Russia'),
        ('English', 'English'),
        ('Kyrgyz', 'Kyrgyz'),
        ('Mandarin Chinese', 'Mandarin Chinese'),
        ('Hindi', 'Hindi'),
        ('Spanish', 'Spanish'),
        ('French', 'French'),
        ('Arab', 'Arab'),
        ('Bengali', 'Bengali'),
        ('Portuguese', 'Portuguese'),
        ('German', 'German')
    )

    LVL = (
        ('elementary', 'elementary'),
        ('average', 'average'),
        ('professional', 'professional'),
        ('all levels', 'all levels')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses', default='mentor sphere')
    title = models.CharField(max_length=60)
    sub_title = models.CharField(max_length=60)
    description = models.TextField()
    language = models.CharField(max_length=100, choices=LANGUAGE)
    level = models.CharField(max_length=100, choices=LVL)
    sub_category = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='video/', blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='themes')

    def __str__(self):
        return self.title


class CourseItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_items')
    title = models.CharField(max_length=128)
    description = models.TextField()


class CourseItemFile(models.Model):
    course_item = models.ForeignKey(CourseItem, on_delete=models.CASCADE, related_name='files')
    FILE_TYPES = (
        ('video', 'Video'),
        ('slides', 'Slides'),
        ('article', 'Article'),
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    content = models.TextField(blank=True)


class Files(models.Model):
    course = models.ForeignKey(CourseItemFile, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/')






