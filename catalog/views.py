from ast import Delete
from lib2to3.pgen2.pgen import ParserGenerator
from pyexpat import model
from webbrowser import BackgroundBrowser
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
  num_authors = Author.objects.count()
  genres = Genre.objects.count()

  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1

  context = {
    'num_books' : num_books,
    'num_instances' : num_instances,
    'num_instances_available' : num_instances_available,
    'num_authors': num_authors,
    'genres': genres,
    'num_visits': num_visits,
  }

  return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(LoginRequiredMixin, generic.ListView):
  model = Book
  paginate_by = 10

class BookDetailView(generic.DetailView):
  model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
  model = Author
  paginate_by = 5

class AuthorDetailView(generic.DetailView):
  model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 5

  def get_queryset(self):
    return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')

  
class LoanedBooksListView(LoginRequiredMixin, generic.ListView):
  # permission_required = 'catalog.can_mark_returned'
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed.html'
  paginate_by = 10

  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')



import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk=pk)

  if request.method == 'POST':
    form = RenewBookForm(request.POST)

    if form.is_valid():
      book_instance.due_back = form.cleaned_data['renewal_date']
      book_instance.save()

      return HttpResponseRedirect(reverse('all-borrowed'))

  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

  context = {
    'form': form,
    'book_instance': book_instance,
  }
  return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author

class AuthorCreate(CreateView):
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
  initial = {'date_of_death': datetime.date.today()}

class AuthorUpdate(UpdateView):
  model = Author
  fields = '__all__'

class AuthorDelete(DeleteView):
  model = Author
  success_url = reverse_lazy('authors')


from catalog.models import Book

class BookCreate(CreateView):
  model = Book
  fields = ['title', 'author', 'summary', 'genre', 'language']

class BookUpdate(UpdateView):
  model = Book
  fields = '__all__'

class BookDelete(DeleteView):
  model = Book
  success_url = reverse_lazy('books')