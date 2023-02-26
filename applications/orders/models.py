from django.contrib.auth import get_user_model
from django.db import models

from applications.course.models import Course
User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orders')
    order_confirm = models.BooleanField(default=False)
    confirm_code = models.CharField(max_length=130, default='', null=True, blank=True)

    def create_confirm_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.confirm_code = code



