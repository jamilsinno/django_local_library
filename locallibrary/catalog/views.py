from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    """ View function for home page of site. """

    # Generate counts of the some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_vists', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # The total number of books with a certain word
    num_book_match = Book.objects.filter(title__icontains='fiction').count()
    num_genre_match = Genre.objects.filter(name__icontains='fiction').count()

    context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_book_match': num_book_match,
            'num_genre_match': num_genre_match,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    # context_object_name = 'book_list' # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # top 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html' # Specify your own template name/location

    # def get_queryset(self):
    #   return Book.objects.filter(title__icontains='war')[:5] 

    # When defining context data, it is important to follow the pattern below for best practices.
    # def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        # context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['some_data'] = 'This is just some data'
        # return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ Generic class-based view listing books on load to current user. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
                BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )

class LoanedBooksListView(LoginRequiredMixin, generic.ListView):
    """ Generic class-based view listing borrowed books to librarians. """
    model = BookInstance
    template_name='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return (
                BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )
