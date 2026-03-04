from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB and ensure unique index on email
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index('email', unique=True)

        # Clear existing data using pymongo
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboards.delete_many({})
        db.workouts.delete_many({})

        # Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Users
        ironman = User.objects.create(email='ironman@marvel.com', name='Iron Man', team='Marvel', is_superhero=True)
        captain = User.objects.create(email='captain@marvel.com', name='Captain America', team='Marvel', is_superhero=True)
        batman = User.objects.create(email='batman@dc.com', name='Batman', team='DC', is_superhero=True)
        superman = User.objects.create(email='superman@dc.com', name='Superman', team='DC', is_superhero=True)

        # Activities
        Activity.objects.create(user=ironman, type='Running', duration=30)
        Activity.objects.create(user=captain, type='Cycling', duration=45)
        Activity.objects.create(user=batman, type='Swimming', duration=60)
        Activity.objects.create(user=superman, type='Flying', duration=120)

        # Leaderboard
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        # Workouts
        Workout.objects.create(name='Super Strength', description='Strength training for superheroes', suggested_for='DC')
        Workout.objects.create(name='Agility Boost', description='Agility training for superheroes', suggested_for='Marvel')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
