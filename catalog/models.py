from ftplib import MAXLINE
from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model):
  name = models.CharField(max_length=200, help_text='Enter a book genre')

  def __str__(self):
    return self.name

class Language(models.Model):
  language = models.CharField(max_length=20, help_text='Enter book language')

  def __str__(self):
    return self.language


class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
  summary = models.TextField(max_length=1000, help_text='Enter a brief description')
  genre = models.ManyToManyField(Genre, help_text='select a genre for this book')
  language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

  class Meta:
    ordering = [ 'title' ]

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])

  def display_genre(self):
    return ', '.join(genre.name for genre in self.genre.all()[:3])
  display_genre.short_description = 'Genre'


class BookInstance(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book')
  book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
  imprint = models.CharField(max_length=200)
  due_back = models.DateField(null=True, blank=True)
  borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
  )

  status = models.CharField(
    max_length=1,
    choices=LOAN_STATUS,
    blank=True,
    default='m',
    help_text='Book availability',
  )

  class Meta:
    ordering = ['due_back']
    permissions = (("can_mark_returned", "Set book as returned"),)

  def __str__(self):
    return f'{self.id} ({self.book.title})'

  @property
  def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
      return True
    return False

class Author(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField(null=True, blank=True)
  date_of_death = models.DateField(null=True, blank=True)

  class Meta:
    ordering = [ 'last_name', 'first_name' ]
  
  def get_absolute_url(self):
    return reverse('author-detail', args=[str(self.id)])
  
  def __str__(self):
    return f'{self.last_name}, {self.first_name}'

