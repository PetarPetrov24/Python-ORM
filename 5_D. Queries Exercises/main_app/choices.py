from django.db import models


class LaptopBrandChoice(models.TextChoices):
    ASUS = "Asus", "Asus"
    ACER = "Acer", "Acer"
    APPLE = "Apple", "Apple"
    LENOVO = "Lenovo", "Lenovo"
    DELL = "Dell", "Dell"


class OperationSystemChoice(models.TextChoices):
    WINDOWS = "Windows", "Windows"
    MACOS = "MacOS", "MacOS"
    LINUX = "Linux", "Linux"
    CHROME_OS = "Chrome OS", "Chrome OS"


class MealTypeChoice(models.TextChoices):
    BREAKFAST = 'Breakfast', 'Breakfast',
    LUNCH = 'Lunch', 'Lunch',
    DINNER = 'Dinner', 'Dinner',
    SNACK = 'Snack', 'Snack',


class DifficultyChoice(models.TextChoices):
    EASY = 'Easy', 'Easy',
    MEDIUM = 'Medium', 'Medium',
    HARD = 'Hard', 'Hard',


class WorkoutChoice(models.TextChoices):
    Calisthenics = 'Calisthenics', 'Calisthenics',
    CrossFit = 'CrossFit', 'CrossFit',
    Cardio = 'Cardio', 'Cardio',
    Strength = 'Strength', 'Strength',
    Yoga = 'Yoga', 'Yoga',
