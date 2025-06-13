from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, null=True)
    author = models.CharField(max_length=255, default="Unknown Author")
    published_date = models.DateField(null=True)
    isbn = models.CharField(max_length=13, unique=True, null=True)
    page_count = models.PositiveIntegerField(null=True)
    language = models.CharField(max_length=50, null=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.title
