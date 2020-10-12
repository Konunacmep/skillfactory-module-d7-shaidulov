from django.shortcuts import render, redirect
from .models import Book, Author, Friend, Publisher
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template import loader
from .forms import AuthorForm, BookForm, FriendForm, PublisherForm
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def publishers(request):
    template = loader.get_template('publishers.html')
    books = Book.objects.all().prefetch_related('publisher')
    publishers = []
    for book in books:
        if book.publisher:
            publishers.append(book.publisher.name)
    # publishers = [x.publisher.name for x in books]
    publishers = sorted(set(publishers))
    biblio_data = {
        "publishers": publishers,
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))

class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:authors_list')
    template_name = 'author_edit.html'
    def dispatch(self, request, *args, **kwargs):  
        if self.request.user.is_anonymous:  
            template = loader.get_template('base.html')
            return HttpResponse(template.render())  
        return super(AuthorEdit, self).dispatch(request, *args, **kwargs) 

class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'

@login_required
def AuthorCreateMany(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='author')
        for author_form in author_formset:
            if author_form.is_valid() and author_form.has_changed():
                author_form.save()
        return HttpResponseRedirect(reverse_lazy('p_library:authors_list'))
    else:
        author_formset = AuthorFormSet(prefix='author')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

@login_required
def BooksAuthorsCreateMAny(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        for author_form in author_formset:
            if author_form.is_valid() and author_form.has_changed():
                author_form.save()
        for book_form in book_formset:
            if book_form.is_valid() and book_form.has_changed():
                book_form.save()
        # return HttpResponseRedirect(reverse_lazy('/index/'))
        return redirect('/index/')
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
        request, 'manage_books_authors.html', {
            'author_formset': author_formset,
            'book_formset': book_formset,
        }
    )


def Friends(request):
    template = loader.get_template('friend_list.html')
    friends = Friend.objects.all().prefetch_related('books')
    return HttpResponse(template.render({'friends': friends}, request))

class FriendCreate(LoginRequiredMixin, CreateView):
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('p_library:friend_list')
    template_name = 'friend_edit.html'
    login_url = 'account_login'

class FriendUpdate(LoginRequiredMixin, UpdateView):
    model = Friend
    form_class = FriendForm
    success_url = reverse_lazy('p_library:friend_list')
    template_name = 'friend_edit.html'
    login_url = 'account_login'

def FriendDelete(request):
    if request.method == 'POST':
        friend_id = request.POST['id']
        if not friend_id:
            return redirect('/editing/friend/')
        else:
            friend = Friend.objects.filter(id=friend_id).first()
            if not friend:
                return redirect('/editing/friend/')
            friend.delete()
        return redirect('/editing/friend/')
    else:
        return redirect('/editing/friend/')

def AuthorDelete(request):
    if request.method == 'POST':
        author_id = request.POST['id']
        if not author_id:
            return redirect('/editing/author/')
        else:
            author = Author.objects.filter(id=author_id).first()
            if not author:
                return redirect('/editing/author/')
            author.delete()
        return redirect('/editing/author/')
    else:
        return redirect('/editing/author/')

class PublisherCreate(LoginRequiredMixin, CreateView):
    model = Publisher
    form_class = PublisherForm
    success_url = reverse_lazy('publishers')
    template_name = 'publisher_edit.html'
    login_url = 'account_login'