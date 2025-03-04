import os
import django
from django.core.exceptions import ValidationError

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import RegularRestaurantReview, Restaurant, MenuReview, Menu
# Keep the data from the previous exercise, so you can reuse it







# def delete():
#     Menu.objects.all().delete()
#     Restaurant.objects.all().delete()
#
# delete()