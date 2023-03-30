from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

# Create your views here.


@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2

    # alternatively redirect them where to login from
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    # context_object_name = 'book_list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # template_name = 'books/my_arbitrary_template_name_list.html'

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]

    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['some_data'] = 'This is just some data'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


# def book_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10

    # pagination is accessed by
    # /catalog/books/?page=2.


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
