from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    banner=models.ImageField(upload_to='media/course_banners/', null=True, blank=True)
    price = models.FloatField()
    duration = models.FloatField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='media/lesson_videos/', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Material(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='media/materials/', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    is_active = models.BooleanField(default=True)
    price = models.FloatField()
    progress = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    total_marks = models.FloatField(default=0.0)
    is_certificate_ready= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

class QuestionAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_answers')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='question_answers')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Q&A for {self.user.username} in {self.lesson.title}"