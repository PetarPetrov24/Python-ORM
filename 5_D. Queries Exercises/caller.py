import os
from typing import List

import django
from django.db.models import Case, When, Value, QuerySet
from django.forms import models

from main_app.choices import OperationSystemChoice, DifficultyChoice, WorkoutChoice

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


# Create and check models


def show_the_most_expensive_laptop() -> str:
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    """
    UPDATE laptop
    SET storage = 512
    WHERE brand in (Asus, Lenovo)
    """

    Laptop.objects.filter(brand__in=("Asus", "Lenovo")).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=("Apple", "Dell", "Acer")).update(memory=16)


def update_operation_systems() -> None:
    # Solution 1
    Laptop.objects.update(
        operation_system=Case(
            When(brand="Asus", then=Value(OperationSystemChoice.WINDOWS)),
            When(brand="Apple", then=Value(OperationSystemChoice.MACOS)),
            When(brand__in=("Dell", "Acer"), then=Value(OperationSystemChoice.LINUX)),
            When(brand="Lenovo", then=Value(OperationSystemChoice.CHROME_OS))
        )
    )

    # Solution 2
    # Laptop.objects.filter(brand="Asus").update(operation_system=OperationSystemChoice.WINDOWS)
    # Laptop.objects.filter(brand="Apple").update(operation_system=OperationSystemChoice.MACOS)
    # Laptop.objects.filter(brand__in=("Dell", "Acer")).update(operation_system=OperationSystemChoice.LINUX)
    # Laptop.objects.filter(brand="Lenovo").update(operation_system=OperationSystemChoice.CHROME_OS)


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title='IM')

def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title='FM')

def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')


def set_new_chefs():
    Meal.objects.filter(meal_type='Breakfast').update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type='Lunch').update(chef='Julia Child')
    Meal.objects.filter(meal_type='Dinner').update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type='Snack').update(chef='Thomas Keller')


def set_new_preparation_times():
    Meal.objects.filter(meal_type='Breakfast').update(preparation_time='10 minutes')
    Meal.objects.filter(meal_type='Lunch').update(preparation_time='12 minutes')
    Meal.objects.filter(meal_type='Dinner').update(preparation_time='15 minutes')
    Meal.objects.filter(meal_type='Snack').update(preparation_time='5 minutes')

def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories=400)

def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories=700)

def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


def show_hard_dungeons():
    result = []
    hard_dungeons = Dungeon.objects.filter(difficulty=DifficultyChoice.HARD).order_by('-location')
    for dungeon in hard_dungeons:
        result.append(f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!")

    return '\n'.join(result)


def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.filter(difficulty=DifficultyChoice.EASY).update(name='The Erased Thombs')
    Dungeon.objects.filter(difficulty=DifficultyChoice.MEDIUM).update(name='The Coral Labyrinth')
    Dungeon.objects.filter(difficulty=DifficultyChoice.HARD).update(name='The Lost Haunt')

def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty=DifficultyChoice.EASY).update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.filter(difficulty=DifficultyChoice.EASY).update(recommended_level=25)
    Dungeon.objects.filter(difficulty=DifficultyChoice.MEDIUM).update(recommended_level=50)
    Dungeon.objects.filter(difficulty=DifficultyChoice.HARD).update(recommended_level=75)


def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(reward="1000 Gold")
    Dungeon.objects.filter(location__startswith='E').update(reward="New dungeon unlocked")
    Dungeon.objects.filter(location__endswith='s').update(reward="Dragonheart Amulet")


def set_new_locations():
    Dungeon.objects.filter(recommended_level=25).update(location="Enchanted Maze")
    Dungeon.objects.filter(recommended_level=50).update(location="Grimstone Mines")
    Dungeon.objects.filter(recommended_level=75).update(location="Shadowed Abyss")


def show_workouts() -> str:
    workouts = Workout.objects.filter(
        workout_type__in=[WorkoutChoice.Calisthenics, WorkoutChoice.CrossFit]
    ).order_by('id')

    result = []
    for workout in workouts:
        result.append(f"{workout.name} from {workout.workout_type} type has {workout.difficulty} difficulty!")

    return "\n".join(result)


def get_high_difficulty_cardio_workouts() -> QuerySet:
    return Workout.objects.filter(
        workout_type=WorkoutChoice.Cardio,
        difficulty="High"
    ).order_by('instructor')



def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutChoice.Cardio, then=Value("John Smith")),
            When(workout_type=WorkoutChoice.Strength, then=Value("Michael Williams")),
            When(workout_type=WorkoutChoice.Yoga, then=Value("Emily Johnson")),
            When(workout_type=WorkoutChoice.CrossFit, then=Value("Sarah Davis")),
            When(workout_type=WorkoutChoice.Calisthenics, then=Value("Chris Heria"))
        )
    )


def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor="John Smith", then=Value("15 minutes")),
            When(instructor="Sarah Davis", then=Value("30 minutes")),
            When(instructor="Chris Heria", then=Value("45 minutes")),
            When(instructor="Michael Williams", then=Value("1 hour")),
            When(instructor="Emily Johnson", then=Value("1 hour and 30 minutes"))
        )
    )


def delete_workouts():
    Workout.objects.exclude(workout_type__in=[WorkoutChoice.Strength, WorkoutChoice.Calisthenics]).delete()


# Run and print your queries

workout1 = Workout.objects.create(
    name="Push-Ups",
    workout_type="Calisthenics",
    duration="10 minutes",
    difficulty="Intermediate",
    calories_burned=200,
    instructor="Bob"
)

workout2 = Workout.objects.create(
    name="Running",
    workout_type="Cardio",
    duration="30 minutes",
    difficulty="High",
    calories_burned=400,
    instructor="Lilly"
)

# Run the functions
print(show_workouts())

high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
for workout in high_difficulty_cardio_workouts:
    print(f"{workout.name} by {workout.instructor}")

set_new_instructors()
for workout in Workout.objects.all():
    print(f"Instructor: {workout.instructor}")

set_new_duration_times()
for workout in Workout.objects.all():
    print(f"Duration: {workout.duration}")


# Create two Workout instances

# def d():
#     Workout.objects.all().delete()
#
# d()