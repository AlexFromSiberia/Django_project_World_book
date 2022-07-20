from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime



def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {'num_books': num_books,
               'num_instances': num_instances,
               'num_instances_available': num_instances_available,
               'num_authors': num_authors,
               'num_visits': num_visits,
               }
    return render(request, 'catalog/index.html', context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return redirect('all-borrowed')
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {'form': form, 'bookinst': book_inst}
    return render(request, 'catalog/book_renew_librarian.html', context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 5


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/detail_view.html'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = "__all__"
    template_name = 'catalog/book_form.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy("book_list")


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = "__all__"
    template_name = 'catalog/book_form.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy("book_list")


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("book_list")
    template_name = 'catalog/book_confirm_delete.html'
    permission_required = 'catalog.can_mark_returned'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    paginate_by = 3


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='5').order_by('due_back')


class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/allborrowedbooks.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='5')


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/authors_detail_view.html'


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = "__all__"
    initial = {"date_of_death": "12/10/2020"}
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy("author_list")


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = "__all__"
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy("author_list")


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("author_list")
    template_name = 'catalog/author_confirm_delete.html'
    permission_required = 'catalog.can_mark_returned'


