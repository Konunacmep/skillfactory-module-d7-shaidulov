from django.db import models


class Author(models.Model):
    full_name = models.TextField(verbose_name='Имя')
    birth_year = models.SmallIntegerField(verbose_name='Дата рождения')
    country = models.CharField(max_length=2, verbose_name='Страна')
    def __str__(self):
        return self.full_name

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='book_images', blank=True, null=True)
    year_release = models.SmallIntegerField(verbose_name='Год издания')
    authors = models.ManyToManyField(Author, through='Inspiration', through_fields=('book', 'author'), verbose_name='Авторы')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Издательство')
    copy_count = models.SmallIntegerField(default=1, verbose_name='Число экземпляров')
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0, verbose_name='Цена')
    @property
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/book_images/book_default.png"
    def __str__(self):
        return self.title

class Inspiration(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Friend(models.Model):
    full_name = models.CharField(max_length=128, verbose_name='Имя')
    books = models.ManyToManyField(Book, through='RentedBooks', verbose_name='Книги')
    def __str__(self):
        return self.full_name

class RentedBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)