model_py = """
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title

"""

forms_py = """
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']

"""

views_py = """
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'object': book})

"""

views_search_py = """
from django.shortcuts import render
from .models import Book
from .forms import BookForm

def book_list(request):
    search_query = request.GET.get('search', '')  # Retrieve the search text from the GET request
    if search_query:
        # Filter books where the search query matches the title or author fields
        books = Book.objects.filter(title__icontains=search_query) | Book.objects.filter(author__icontains=search_query)
    else:
        books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books, 'search_query': search_query})

"""

views_search_pagination_py = """
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Book

def book_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        books = Book.objects.filter(title__icontains=search_query) | Book.objects.filter(author__icontains=search_query)
    else:
        books = Book.objects.all()

    # Pagination
    paginator = Paginator(books, 5)  # Show 5 books per page
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    return render(request, 'books/book_list.html', {'books': books, 'search_query': search_query})

"""

app_urls_py = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('new/', views.book_create, name='book_create'),
    path('edit/<int:pk>/', views.book_update, name='book_update'),
    path('delete/<int:pk>/', views.book_delete, name='book_delete'),
]

"""

# template 
base_template_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Book Management{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container mt-5">
    {% block content %}
    {% endblock %}
</div>
</body>
</html>

"""
app_model_list_search_html = """
{% extends 'base.html' %}

{% block title %}Books List{% endblock %}

{% block content %}
    <h2>Books List</h2>
    <form method="get" class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" name="search" value="{{ search_query }}">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
    <a href="{% url 'book_create' %}" class="btn btn-primary my-3">Add New Book</a>
    <table class="table mt-3">
        <thead>
            <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Published Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.published_date }}</td>
                <td>
                    <a href="{% url 'book_update' book.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'book_delete' book.pk %}" class="btn btn-sm btn-danger">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

"""

app_model_list_pagination_html = """
{% extends 'base.html' %}

{% block title %}Books List{% endblock %}

{% block content %}
    <h2>Books List</h2>
    <form method="get" class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" name="search" value="{{ search_query }}">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
    <a href="{% url 'book_create' %}" class="btn btn-primary my-3">Add New Book</a>
    <table class="table mt-3">
        <thead>
            <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Published Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.published_date }}</td>
                <td>
                    <a href="{% url 'book_update' book.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'book_delete' book.pk %}" class="btn btn-sm btn-danger">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="pagination">
        <span class="step-links">
            {% if books.has_previous %}
                <a href="?page=1&search={{ search_query }}">first</a>
                <a href="?page={{ books.previous_page_number }}&search={{ search_query }}">previous</a>
            {% endif %}
            
            <span class="current">
                Page {{ books.number }} of {{ books.paginator.num_pages }}.
            </span>
            
            {% if books.has_next %}
                <a href="?page={{ books.next_page_number }}&search={{ search_query }}">next</a>
                <a href="?page={{ books.paginator.num_pages }}&search={{ search_query }}">last</a>
            {% endif %}
        </span>
    </div>
{% endblock %}

"""


app_model_list_html = """
{% extends 'base.html' %}

{% block title %}Books List{% endblock %}

{% block content %}
    <h2>Books List</h2>
    <a href="{% url 'book_create' %}" class="btn btn-primary">Add New Book</a>
    <table class="table mt-3">
        <thead>
            <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Published Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.published_date }}</td>
                <td>
                    <a href="{% url 'book_update' book.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'book_delete' book.pk %}" class="btn btn-sm btn-danger">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}

"""

app_model_form_html = """
{% extends 'base.html' %}

{% block title %}Add/Edit Book{% endblock %}

{% block content %}
    <h2>{% if form.instance.pk %}Edit Book{% else %}Add New Book{% endif %}</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-success">{% if form.instance.pk %}Update{% else %}Submit{% endif %}</button>
        <a href="{% url 'book_list' %}" class="btn btn-secondary">Cancel</a>
    </form>
{% endblock %}

"""

app_model_confirm_delete_html = """
{% extends 'base.html' %}

{% block title %}Delete Book{% endblock %}

{% block content %}
    <h2>Are you sure you want to delete "{{ object.title }}"?</h2>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Yes, delete</button>
        <a href="{% url 'book_list' %}" class="btn btn-secondary">Cancel</a>
    </form>
{% endblock %}

"""