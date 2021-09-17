from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Author, Photo
from .forms import ReviewForm
import os
import uuid
import boto3

from django.http import HttpResponse




def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def books_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, 'books/index.html', { 'books': books })

@login_required
def books_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    authors_book_doesnt_have = Author.objects.exclude(id__in = book.authors.all().values_list('id'))
    review_form = ReviewForm()
    return render(request, 'books/detail.html', { 'book': book, 'review_form': review_form, 'authors': authors_book_doesnt_have })

class BookCreate(LoginRequiredMixin, CreateView):
  model = Book
  fields = '__all__'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class BookUpdate(LoginRequiredMixin, UpdateView):
  model = Book
  fields = ['description']

class BookDelete(LoginRequiredMixin, DeleteView):
  model = Book
  success_url = '/books/'

@login_required
def add_review(request, book_id):
  form = ReviewForm(request.POST)
  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.book_id = book_id
    new_review.save()
  return redirect('detail', book_id=book_id)

class AuthorList(LoginRequiredMixin, ListView):
    model = Author

class AuthorDetail(LoginRequiredMixin, DetailView):
    model = Author

class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'

class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = '/authors'

@login_required
def assoc_author(request, book_id, author_id):
    Book.objects.get(id=book_id).authors.add(author_id)
    return redirect('detail', book_id=book_id)

@login_required
def add_photo(request, book_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, book_id=book_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', book_id=book_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
