from django.contrib import admin
from applications.course.models import Course, Category, CourseItem, CourseItemFile, Theme

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(CourseItem)
admin.site.register(CourseItemFile)
admin.site.register(Theme)

