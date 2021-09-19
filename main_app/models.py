from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

RATING = (
    ('1', 'NOT MY CUP OF TEA!'),
    ('3', 'IT WAS GOOD!'),
    ('5', 'IT WAS AMAZING! I COULD NOT PUT IT DOWN!')
)

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('authors_detail', kwargs={'pk': self.id})

class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    genre = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'book_id': self.id})

class Review(models.Model):
    date = models.DateField('review date')
    review = models.CharField(
        max_length=1,
        choices=RATING,
        default=RATING[0][0]
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_rating_display()} on {self.date}"

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for book_id: {self.book_id} @{self.url}"
