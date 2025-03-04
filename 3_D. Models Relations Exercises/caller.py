import os
import django

from datetime import timedelta, date


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Song, Artist, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car


# Create queries within functions
def show_all_authors_with_their_books():
    authors_with_books = []
    authors = Author.objects.all().order_by('id')
    for author in authors:
        books = Book.objects.filter(author=author)
        if not books:
            continue
        titles = ', '.join(b.title for b in books)
        authors_with_books.append(f'{author.name} has written - {titles}!')

    return '\n'.join(authors_with_books)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    products = Product.objects.get(name=product_name)
    reviews = products.reviews.all()
    total_rating = sum(r.rating for r in reviews)
    average_rating = total_rating / len(reviews)
    return average_rating


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    result = []
    driving_licenses = DrivingLicense.objects.all().order_by('-license_number')

    for d_license in driving_licenses:
        expiration_date = timedelta(days=365) + d_license.issue_date
        result.append(f"License with number: {d_license.license_number} expires on {expiration_date}!")

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    expired_licenses = due_date - timedelta(days=365)

    drivers_with_expired_licenses = Driver.objects.filter(
        license__issue_date__gt=expired_licenses
    )

    return drivers_with_expired_licenses

def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()
    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

